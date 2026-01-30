# Python Scripts untuk Konversi Blog

## 1. convert_shortcodes.py
Mengkonversi shortcode Hugo dan komponen Astro ke format Markdown/HTML.

### Konversi yang dilakukan:
- `{{< img src="..." caption="..." >}}` → `![caption](src)`
- `<Img src="..." caption="..." />` → `![caption](src)`
- `{{< hubungi_kami >}}` → HTML block dengan Bootstrap styling
- `<QuestionCard ... />` → HTML block dengan Bootstrap styling

### Hasil:
- **2 file terkonversi**
- **100 file tidak perlu perubahan**

### Cara menjalankan:
```bash
python convert_shortcodes.py
```

---

## 2. convert_permalinks.py
Mengkonversi permalink dari domain lama (sadapphone.com) ke domain baru (menyadap.github.io/blog).

### Konversi yang dilakukan:
- `https://sadapphone.com/sadap/test-post/` → `/blog/test-post`
- `https://www.sadapphone.com/sadap/test-post/` → `/blog/test-post`
- `sadapphone.com/sadap/test-post/` → `/blog/test-post`
- `/sadap/test-post/` → `/blog/test-post`

### Cleanup otomatis:
- Menghapus double slashes (`/blog//`)
- Menghapus double `/blog/blog/`
- Membersihkan trailing slashes

### Hasil:
- **26 file terkonversi** (semua link internal dan eksternal)
- **76 file tidak perlu perubahan** (tidak ada link ke sadapphone.com atau /sadap/)
- **0 error pada semua 102 file**

### Cara menjalankan:
```bash
python convert_permalinks.py
```

---

## Contoh Konversi Sebelum & Sesudah

### Sebelum (Markdown dengan link lama):
```markdown
[Baca selengkapnya](https://sadapphone.com/sadap/cara-sadap-wa)
```

### Sesudah (Markdown dengan link baru):
```markdown
[Baca selengkapnya](/blog/cara-sadap-wa)
```

---

## File-file yang Dikonversi

### convert_shortcodes.py:
- `9-sadap-hp-pacar-tanpa-ketahuan-bdb42.md`
- `shortcode-example.md`

### convert_permalinks.py:
- `10-aplikasi-social-spy-sadap-wa-014c687.md`
- `10-sadap-hp-tersembunyi-suami-selingkuh-13a3b.md`
- `12-aplikasi-sadap-wa-gratis-tanpa-ketahuan-5117c.md`
- `9-sadap-hp-pacar-tanpa-ketahuan-bdb42.md`
- `aplikasi-sadap-safespy.md`
- `aplikasi-sadap-spyic.md`
- `aplikasi-sadap-spyzie.md`
- `aplikasi-teensafe.md`
- `cara-hack-akun-facebook-lupa-password.md`
- `cara-hack-akun-instagram-lupa-password-1dc.md`
- `flexispy-penyadap-hp-iphone.md`
- `hack-spy-wa-whatsapp-teman-pacar-87.md`
- `highstermobile.md`
- `kidsguard-pro.md`
- `mobile-spy.md`
- `ownspy-penyadap-hp-pasangan.md`
- `penyadap-fonemonitor.md`
- `penyadap-hp-pasangan-selingkuh.md`
- `penyadap-pasangan-selingkuh-xnspy.md`
- `penyadap-thetruthspy.md`
- `perangkat-sadap-trackmyfone.md`
- `sadap-android-gratis-tanpa-rooting-d04c.md`
- `sadap-hp-gratis-istri-selingkuh-29f9f.md`
- `sadap-hp-mspy.md`
- `sadap-iphone-android-tanpa-pinjam.md`
- `sadap-iphone-ipad-dengan-itunes-977c1.md`
- `whatsapp-social-spy-tool-apk-24.md`

---

## Catatan

- Kedua script bersifat **idempotent** (aman untuk dijalankan berkali-kali)
- Jika file tidak perlu perubahan, script tidak akan mengubah timestamp file
- Encoding UTF-8 untuk mendukung karakter Indonesia
- Error handling otomatis untuk file yang tidak dapat dibaca
