import rss from '@astrojs/rss';
import { config } from '../config';

export async function GET(context) {
  // Support both .md and .mdx files
  const mdPosts = import.meta.glob('../content/blog/*.md', { eager: true });
  const mdxPosts = import.meta.glob('../content/blog/*.mdx', { eager: true });
  const allPosts = { ...mdPosts, ...mdxPosts };

  const items = Object.entries(allPosts).map(([path, post]) => {
    const slug = path.split('/').pop().replace(/\.(md|mdx)$/, '');
    const categories = post.frontmatter.categories || [];
    const author = post.frontmatter.author || config.author?.name || config.title;
    
    return {
      title: post.frontmatter.title,
      pubDate: post.frontmatter.date,
      description: post.frontmatter.excerpt || post.frontmatter.description,
      content: post.frontmatter.excerpt || post.frontmatter.description,
      link: `/blog/${slug}/`,
      author: author,
      categories: categories.length > 0 ? categories : undefined,
    };
  });
  
  return rss({
    title: config.title,
    description: config.description,
    site: context.site,
    items: items.sort((a, b) => new Date(b.pubDate) - new Date(a.pubDate)),
    customData: `<language>id</language><copyright>© ${new Date().getFullYear()} ${config.title}</copyright>`,
  });
}