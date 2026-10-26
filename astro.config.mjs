// @ts-check
import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import rehypeExternalLinks from 'rehype-external-links';
import rehypeImageSize from './src/utils/rehype-image-size.js';

// https://astro.build/config
export default defineConfig({
  // The site property should be your final deployed URL
  site: process.env.SITE || 'https://menyadap.github.io',
  // Only use base path for GitHub Pages deployments
  // For Netlify/Vercel, leave this undefined (no base path)
  base: process.env.BASE_PATH || undefined,
  // GitHub Pages requires trailing slash for proper routing
  trailingSlash: 'always',
  // Halaman /contact/ dihilangkan, dialihkan ke /about/
  redirects: {
    '/contact': '/about/',
  },
  integrations: [
    mdx({
      jsxImportSource: 'astro',
      optimize: true,
    }),
    sitemap({
      // Don't add trailing slash to sitemap XML files
      changefreq: 'weekly',
      priority: 0.7,
    }),
  ],
  
  // Markdown configuration untuk mendukung Astro Components (shortcode)
  markdown: {
    rehypePlugins: [
      [
        rehypeExternalLinks,
        {
          target: '_blank',
          rel: ['nofollow', 'noreferrer'],
        },
      ],
      // Menyisipkan width/height pada gambar konten agar ruangnya sudah
      // tersedia sebelum gambar dimuat (mencegah Cumulative Layout Shift).
      rehypeImageSize,
    ],
    shikiConfig: {
      theme: 'github-dark',
      wrap: true,
    },
  },
  
  // Vite configuration untuk component resolution
  vite: {
    ssr: {
      external: ['svgo'],
    },
  },
});
