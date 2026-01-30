export interface SiteConfig {
  title: string;
  description: string;
  author: {
    name: string;
    bio: string;
    avatar?: string;
  };
  social: {
    github?: string;
    twitter?: string;
    instagram?: string;
    linkedin?: string;
    email?: string;
  };
  siteUrl: string;
}

export const config: SiteConfig = {
  title: "menyadap.github.io",
  description: "Blog panduan keamanan digital dan teknik penyadapan untuk Indonesia",
  author: {
    name: "menyadap.github.io",
    bio: "Panduan lengkap tentang keamanan digital dan monitoring perangkat untuk Indonesia.",
    // avatar: "/images/avatar.jpg" // Uncomment and add your avatar image to public/images/
  },
  social: {
    github: "https://github.com/menyadap",
    twitter: "https://twitter.com/menyadap",
    linkedin: "https://linkedin.com/in/menyadap",
    email: "info@menyadap.github.io"
  },
  siteUrl: "https://menyadap.github.io",
  language: "id",
  country: "ID"
};

// Export constants for SEO component
export const SITE_TITLE = config.title;
export const SITE_DESCRIPTION = config.description;