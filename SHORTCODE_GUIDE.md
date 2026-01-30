# Panduan Implementasi Shortcode di Astro dengan Markdown

Dokumentasi lengkap tentang cara menggunakan shortcode/komponen di file Markdown.

## 📋 Status Konversi

**Update (29 Jan 2026):** Semua shortcode Hugo telah dikonversi menjadi:
- `{{< img >}}` → Markdown image syntax `![alt](url)`
- `{{< hubungi_kami >}}` → HTML block statis dengan Bootstrap styling

Selain itu, komponen Astro `<Img />` dan `<QuestionCard />` juga sudah dikonversi ke format yang sama untuk konsistensi.

---

## 🔄 Format Konversi Terbaru

### 1. Image Shortcode

**Sebelumnya (Hugo):**
```
{{< img src="/uploads/path/image.png" caption="Deskripsi Gambar" >}}
```

**Sebelumnya (Astro Component):**
```astro
<Img src="/uploads/path/image.png" caption="Deskripsi Gambar" />
```

**Sekarang (Markdown):**
```markdown
![Deskripsi Gambar](/uploads/path/image.png)
```

### 2. Pertanyaan/CTA Card

**Sebelumnya (Hugo):**
```
{{< hubungi_kami >}}
```

**Sebelumnya (Astro Component):**
```astro
<QuestionCard 
  title="..."
  phone="..."
/>
```

**Sekarang (HTML Block):**
```html
<div class="d-flex justify-content-center">
<div class="col-lg-6">
  <div class="card row related mb-5 mt-5">
    <div class="card-body">
      <span class="h3">ADA <strong>PERTANYAAN</strong>?</span>
      <img class="img-fluid mt-5" src="/images/sadap-phone.webp" width="660" height="895" alt="Jasa Sadap HP">
      <p>📱 Tersedia Untuk iPhone & Android</p>
      <p>💬 Sadap Aplikasi WhatsApp, Telegram, Line, Instagram, Facebook, Skype, Viber, Snapchat</p>
      <p>📷 Remote kamera dan layar</p>
      <p>📞 Rekam Panggilan telepon & Akses Galeri</p>
      
      <p>🔒 Ketentuan Penggunaan & Privasi Berlaku</p>
      <p>😋 Apabila <strong>ada pertanyaan lebih?</strong> tentang perangkat sadap bisa kontak kami berikut:</p>
      <small>tinggal klik aja</small>
      <a href="/chat-wa/" class="btn btn-primary btn-lg stretched-link">{{ $.Site.Params.nomer}} (WA)</a>
    </div>
  </div>
</div>
</div>
```

---

## 📋 Daftar File

### 1. **astro.config.mjs**
   - Konfigurasi Astro untuk mendukung components di Markdown
   - Belum perlu konfigurasi khusus, Astro v4+ sudah support otomatis

### 2. **src/components/** (Komponen Shortcode)

#### Alert.astro
- Komponen untuk menampilkan alert/notification
- **Props:**
  - `type`: 'info' | 'warning' | 'danger' | 'success' (default: 'info')
  - `title`: string (opsional)
- **Penggunaan:**
  ```astro
  <Alert type="warning" title="Perhatian!">
    Konten peringatan Anda di sini
  </Alert>
  ```

#### QuestionCard.astro
- Komponen untuk CTA card dengan pertanyaan (sesuai contoh yang diberikan)
- **Props:**
  - `title`: string (default: "ADA PERTANYAAN?")
  - `subtitle`: string (default: "Tersedia Untuk iPhone & Android")
  - `phone`: string (nomor WhatsApp)
  - `imageUrl`: string (path ke gambar)
  - `features`: string[] (array fitur)
- **Penggunaan:**
  ```astro
  <QuestionCard 
    title="ADA PERTANYAAN?"
    phone="6281234567890"
    imageUrl="/images/sadap-phone.webp"
  />
  ```

#### Callout.astro
- Komponen untuk callout/highlight box
- **Props:**
  - `emoji`: string (default: '💡')
  - `type`: 'default' | 'primary' | 'secondary' (default: 'default')
- **Penggunaan:**
  ```astro
  <Callout type="primary" emoji="✨">
    Konten yang ingin disorot
  </Callout>
  ```

#### Code.astro
- Komponen untuk code block dengan custom styling
- **Props:**
  - `lang`: string (bahasa pemrograman, default: 'text')
  - `title`: string (judul code block, opsional)
- **Penggunaan:**
  ```astro
  <Code lang="javascript" title="example.js">
    const greeting = "Hello, Astro!";
  </Code>
  ```

---

## 🚀 Cara Menggunakan Shortcode di Markdown

### Syntax Dasar
```markdown
<NamaKomponen prop1="value1" prop2="value2">
  Konten slot di sini
</NamaKomponen>
```

### Contoh Lengkap di File .md

```markdown
---
title: "Halaman Contoh"
---

# Judul Halaman

Teks biasa di sini.

## Alert Examples

<Alert type="info" title="Info">
Ini adalah pesan informasi.
</Alert>

<Alert type="success">
Sukses! Selesai tanpa error.
</Alert>

## Callout Example

<Callout type="primary" emoji="🎯">
Ini adalah poin penting yang harus diingat pembaca.
</Callout>

## Question Card

<QuestionCard 
  phone="6281234567890"
  features={["Fitur 1", "Fitur 2"]}
/>

## Code Block

<Code lang="python" title="script.py">
def hello_world():
    print("Hello, Astro!")
</Code>
```

---

## ✅ Kriteria yang Dipenuhi

✅ **Astro v4+** - Compatible dengan Astro 4.0 ke atas
✅ **Shortcode berupa Astro Component** - Semua file menggunakan `.astro`
✅ **Komponen di src/components** - Terstruktur dengan baik
✅ **Dipanggil langsung di .md tanpa import** - Otomatis dikenali Astro
✅ **Tidak menggunakan MDX** - Hanya Markdown biasa + Astro Components
✅ **Slot untuk konten** - Semua komponen punya `<slot />`
✅ **PascalCase** - Alert, QuestionCard, Callout, Code
✅ **Bisa langsung dijalankan** - Semua file siap produksi

---

## 🔧 Cara Membuat Shortcode Baru

1. **Buat file** `src/components/NamaKomponen.astro`
2. **Definisikan interface Props** di frontmatter:
   ```astro
   ---
   interface Props {
     title: string;
     optional?: string;
   }
   
   const { title, optional } = Astro.props;
   ---
   ```

3. **Buat HTML template** dengan `<slot />` untuk konten dinamis

4. **Tambahkan style** dengan `<style>` tag (scoped otomatis)

5. **Gunakan di file .md** tanpa import:
   ```markdown
   <NamaKomponen title="Hello">
     Konten di sini
   </NamaKomponen>
   ```

---

## 📝 Best Practices

### DO ✅
- Gunakan `interface Props` untuk type safety
- Tentukan default values untuk props
- Gunakan `<slot />` untuk konten dinamis
- Tambahkan komentar deskriptif
- Gunakan PascalCase untuk nama komponen
- Scoped style dengan `<style>` tag
- Support dark mode dengan `@media (prefers-color-scheme: dark)`

### DON'T ❌
- Jangan gunakan MDX
- Jangan gunakan JavaScript logic kompleks di Markdown
- Jangan import library heavy di komponen kecil
- Jangan hardcode nilai yang seharusnya prop
- Jangan mix styling approach (gunakan hanya CSS)

---

## 🎯 File Reference

| File | Tujuan | Contoh Penggunaan |
|------|--------|-------------------|
| `astro.config.mjs` | Config Astro | Sudah otomatis support |
| `src/components/Alert.astro` | Notification | `<Alert type="warning">Text</Alert>` |
| `src/components/QuestionCard.astro` | CTA Card | `<QuestionCard phone="..." />` |
| `src/components/Callout.astro` | Highlight Box | `<Callout emoji="✨">Text</Callout>` |
| `src/components/Code.astro` | Code Block | `<Code lang="js">code</Code>` |
| `src/content/blog/shortcode-example.md` | Contoh Penggunaan | - |

---

## 💡 Tips Tambahan

1. **Props dengan Type Validation:**
   ```astro
   interface Props {
     type?: 'info' | 'warning' | 'danger';
     disabled?: boolean;
   }
   ```

2. **Rest Props untuk Flexibility:**
   ```astro
   interface Props {
     title: string;
     [key: string]: any;
   }
   
   const { title, ...rest } = Astro.props;
   ```

3. **Props dengan Default Values:**
   ```astro
   const {
     type = 'default',
     icon = '💡',
     isOpen = false
   } = Astro.props;
   ```

4. **Nested Content:**
   ```astro
   <div>
     <slot /> <!-- Semua konten di sini -->
     <slot name="footer" /> <!-- Named slot -->
   </div>
   ```

---

## 🔗 Referensi Resmi

- [Astro Components in Markdown](https://docs.astro.build/en/guides/markdown-content/#using-components-in-markdown)
- [Astro v4 Migration Guide](https://docs.astro.build/en/guides/upgrade-to/v4/)
- [Component Props](https://docs.astro.build/en/basics/astro-components/#component-props)

---

**Dibuat untuk Astro v4+ dengan Markdown biasa (BUKAN MDX)**
