# menyadap.github.io

Situs statis berbasis [Astro](https://astro.build) berisi panduan keamanan digital dan monitoring perangkat untuk pasar Indonesia.

- Situs: https://menyadap.github.io
- Konten: Markdown & MDX di `src/content/`
- Output: statis (`astro build`) → dipublikasikan ke GitHub Pages

## Teknologi

- **Framework:** Astro 5 + `@astrojs/mdx`, `@astrojs/sitemap`, `@astrojs/rss`
- **Bahasa:** TypeScript
- **Styling:** CSS scoped + custom properties (design token) di `src/styles/global.css`
- **Font:** self-hosted via `@fontsource` (Oswald, Roboto Condensed, Work Sans, JetBrains Mono)
- **Manajer paket:** pnpm

## Perintah

Semua perintah dijalankan dari root proyek.

| Perintah | Fungsi |
|----------|--------|
| `pnpm install` | Memasang dependensi |
| `pnpm run dev` | Menjalankan server pengembangan di `localhost:4321` |
| `pnpm run build` | Build produksi ke `./dist/` |
| `pnpm run preview` | Pratinjau hasil build secara lokal |
| `pnpm run check` | Pemeriksaan tipe TypeScript |
| `pnpm run lint` | Menjalankan ESLint |
| `pnpm run format` | Memformat kode dengan Prettier |

## Struktur Proyek

```
src/
├── components/          # Komponen UI Astro (Header, Sidebar, Layout, SEO, dll.)
├── content/
│   ├── blog/            # Artikel (.md / .mdx) — nama file = slug URL
│   └── pages/           # Halaman statis (about, ketentuan layanan, privasi, dll.)
├── layouts/             # Layout MDX
├── pages/               # Rute Astro
│   ├── index.astro      # Beranda
│   ├── about.astro      # Tentang
│   ├── blog.astro       # Daftar artikel
│   ├── blog/[...slug].astro  # Halaman artikel
│   ├── [page].astro     # Halaman statis dari src/content/pages
│   ├── categories.astro # Daftar kategori
│   ├── sadap-wa.astro   # Landing page WhatsApp Web
│   ├── rss.xml.js       # Feed RSS
│   └── search.json.js   # Endpoint data pencarian
├── styles/global.css    # Token warna, tipografi, dan gaya global
├── utils/               # Utilitas (reading-time, table-of-contents)
└── config.ts            # Konfigurasi situs (judul, penulis, sosial, URL)
public/                  # Aset statis (favicon, robots.txt, gambar, uploads)
```

## Menambah Artikel

Buat berkas `.md` atau `.mdx` di `src/content/blog/`. Nama berkas dipakai sebagai slug URL.

```markdown
---
title: "Judul Artikel"
description: "Ringkasan singkat untuk meta description dan kartu artikel."
date: "2026-01-15"
categories: ["Aplikasi Sadap"]
tags: ["android", "monitoring"]
draft: false
---

Isi artikel...
```

| Field | Tipe | Wajib | Keterangan |
|-------|------|-------|------------|
| `title` | string | Ya | Judul artikel |
| `description` | string | Tidak | Ringkasan untuk SEO dan kartu artikel |
| `date` | string | Ya | Tanggal terbit (`YYYY-MM-DD`) |
| `categories` | array | Tidak | Kategori artikel |
| `tags` | array | Tidak | Tag untuk artikel terkait |
| `image` | string | Tidak | Path gambar unggulan |
| `draft` | boolean | Tidak | `true` untuk menyembunyikan dari daftar |

## Konfigurasi

Semua pengaturan situs terpusat di `src/config.ts` (judul, deskripsi, penulis, tautan sosial, `siteUrl`, bahasa).

## Deploy

Deployment otomatis ke GitHub Pages melalui `.github/workflows/deploy.yml` setiap kali ada push ke branch `master`.
Sitemap dihasilkan otomatis oleh `@astrojs/sitemap` sebagai `/sitemap-index.xml`.

## Lisensi

MIT — lihat berkas [LICENSE](LICENSE).
