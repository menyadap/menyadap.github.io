import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const blog = defineCollection({
  // Nama berkas tanpa ekstensi dipakai sebagai slug URL, sama seperti route di
  // src/pages/blog/[...slug].astro. Tanpa `generateId` ini, `entry.id` masih
  // membawa ".md"/".mdx" sehingga link yang dibangun dari `post.id` jadi 404.
  loader: glob({
    pattern: '**/*.{md,mdx}',
    base: './src/content/blog',
    generateId: ({ entry }) => entry.replace(/\.(md|mdx)$/, ''),
  }),
  // `image()` membuat Astro meng-import berkas gambar dari path relatif di
  // frontmatter, sehingga thumbnail dapat diproses lewat pipeline astro:assets.
  schema: ({ image }) =>
    z.object({
      title: z.string(),
      description: z.string().optional(),
      date: z.coerce.date(),
      excerpt: z.string().optional(),
      categories: z.array(z.string()).default([]),
      tags: z.array(z.string()).default([]),
      author: z.string().default('Anonymous'),
      image: z.string().optional(),
      thumbnail: image().optional(),
    }),
});

// Halaman statis (about-me, jasa-sadap, ketentuan-layanan, privacy-police).
// Dirender oleh src/pages/[page].astro dan src/pages/about.astro.
const pages = defineCollection({
  type: 'content',
  schema: ({ image }) =>
    z
      .object({
        title: z.string(),
        description: z.string().optional(),
        date: z.coerce.date().optional(),
        lastmod: z.coerce.date().optional(),
        thumbnail: image().optional(),
        toc: z.boolean().optional(),
        draft: z.boolean().optional(),
        outputs: z.array(z.string()).optional(),
      })
      .passthrough(),
});

export const collections = { blog, pages };