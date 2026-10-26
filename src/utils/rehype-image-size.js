import fs from 'node:fs';
import path from 'node:path';

/**
 * Membaca dimensi (lebar x tinggi) dari berkas gambar raster.
 * Mendukung JPEG, PNG, GIF, dan WebP tanpa dependensi eksternal.
 * Mengembalikan null bila formatnya tidak dikenali.
 */
function readSize(buffer) {
  // PNG — signature 8 byte, dimensi ada di chunk IHDR
  if (buffer.length > 24 && buffer.readUInt32BE(0) === 0x89504e47) {
    return { width: buffer.readUInt32BE(16), height: buffer.readUInt32BE(20) };
  }

  // GIF — "GIF87a" / "GIF89a"
  if (buffer.length > 10 && buffer.toString('ascii', 0, 3) === 'GIF') {
    return { width: buffer.readUInt16LE(6), height: buffer.readUInt16LE(8) };
  }

  // WebP — container RIFF
  if (
    buffer.length > 30 &&
    buffer.toString('ascii', 0, 4) === 'RIFF' &&
    buffer.toString('ascii', 8, 12) === 'WEBP'
  ) {
    const chunk = buffer.toString('ascii', 12, 16);

    if (chunk === 'VP8 ') {
      // WebP lossy
      return {
        width: buffer.readUInt16LE(26) & 0x3fff,
        height: buffer.readUInt16LE(28) & 0x3fff,
      };
    }
    if (chunk === 'VP8L') {
      // WebP lossless
      const bits = buffer.readUInt32LE(21);
      return {
        width: (bits & 0x3fff) + 1,
        height: ((bits >> 14) & 0x3fff) + 1,
      };
    }
    if (chunk === 'VP8X') {
      // WebP extended
      return {
        width: (buffer[24] | (buffer[25] << 8) | (buffer[26] << 16)) + 1,
        height: (buffer[27] | (buffer[28] << 8) | (buffer[29] << 16)) + 1,
      };
    }
    return null;
  }

  // JPEG — telusuri marker sampai menemukan SOF
  if (buffer.length > 4 && buffer[0] === 0xff && buffer[1] === 0xd8) {
    let offset = 2;
    while (offset + 9 < buffer.length) {
      if (buffer[offset] !== 0xff) {
        offset++;
        continue;
      }

      const marker = buffer[offset + 1];
      const isStartOfFrame =
        marker >= 0xc0 && marker <= 0xcf && marker !== 0xc4 && marker !== 0xc8 && marker !== 0xcc;

      if (isStartOfFrame) {
        return {
          width: buffer.readUInt16BE(offset + 7),
          height: buffer.readUInt16BE(offset + 5),
        };
      }

      // Marker tanpa payload panjang
      if (marker === 0xd8 || marker === 0x01 || (marker >= 0xd0 && marker <= 0xd7)) {
        offset += 2;
        continue;
      }

      offset += 2 + buffer.readUInt16BE(offset + 2);
    }
  }

  return null;
}

// Menelusuri node hast secara rekursif untuk mencari elemen <img>.
function walk(node, callback) {
  if (!node || typeof node !== 'object') return;

  if (node.type === 'element' && node.tagName === 'img') {
    callback(node);
  }

  if (Array.isArray(node.children)) {
    node.children.forEach((child) => walk(child, callback));
  }
}

/**
 * Plugin rehype: menyisipkan atribut `width` dan `height` pada gambar di dalam
 * konten Markdown berdasarkan dimensi asli berkas di folder `public`.
 *
 * Browser memakai atribut tersebut untuk menghitung aspect-ratio dan menyediakan
 * ruang sebelum gambar selesai dimuat, sehingga Cumulative Layout Shift (CLS)
 * berkurang tanpa perlu menulis dimensi secara manual di berkas konten.
 */
export default function rehypeImageSize(options = {}) {
  const publicDir = options.publicDir || path.resolve(process.cwd(), 'public');

  return (tree) => {
    walk(tree, (node) => {
      const src = node.properties?.src;
      if (typeof src !== 'string' || !src.startsWith('/')) return;

      // Buang query/hash lalu petakan URL publik ke berkas di folder public
      const publicPath = decodeURIComponent(src.split('?')[0].split('#')[0]);
      const filePath = path.join(publicDir, publicPath);

      try {
        const size = readSize(fs.readFileSync(filePath));
        if (!size?.width || !size?.height) return;

        node.properties.width = size.width;
        node.properties.height = size.height;
      } catch {
        // Berkas tidak ditemukan (mis. gambar eksternal) — lewati.
      }
    });
  };
}
