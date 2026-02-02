const fs = require('fs');
const path = require('path');

function walk(dir) {
  let results = [];
  const list = fs.readdirSync(dir, { withFileTypes: true });
  list.forEach((dirent) => {
    const full = path.join(dir, dirent.name);
    if (dirent.isDirectory()) {
      results = results.concat(walk(full));
    } else {
      results.push(full);
    }
  });
  return results;
}

function shouldProcess(file) {
  const exts = ['.md', '.mdx', '.astro'];
  return exts.includes(path.extname(file).toLowerCase());
}

function isAssetSegment(seg) {
  return /\.[a-z0-9]{1,6}$/i.test(seg);
}

function addTrailingToPath(p) {
  if (!p) return p;
  if (p.endsWith('/')) return p;
  const last = p.split('/').pop();
  if (!last) return p; // ends with slash handled above
  if (isAssetSegment(last)) return p; // skip assets
  return p + '/';
}

const root = path.resolve(process.cwd(), 'src');
const allFiles = walk(root).filter(shouldProcess);
const changed = [];

allFiles.forEach((file) => {
  let src = fs.readFileSync(file, 'utf8');
  let out = src;

  // Replace HTML href="/path[...](#hash|?q=)" occurrences
  out = out.replace(/href="(\/[^"#?\s]+)([^"\s]*)"/g, (m, p, rest) => {
    const newPath = addTrailingToPath(p);
    if (newPath === p) return m;
    return `href="${newPath}${rest || ''}"`;
  });

  // Replace markdown links: ](/path[#anchor|?q])
  out = out.replace(/\]\((\/[^)\s]*?)([#?][^)]*)?\)/g, (m, p, rest) => {
    const newPath = addTrailingToPath(p);
    if (newPath === p) return m;
    return `](${newPath}${rest || ''})`;
  });

  if (out !== src) {
    fs.writeFileSync(file, out, 'utf8');
    changed.push(path.relative(process.cwd(), file));
  }
});

console.log('Files changed:', changed.length);
changed.forEach((f) => console.log(f));
