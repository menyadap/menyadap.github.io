const fs = require('fs');
const path = require('path');
const glob = require('glob');

function processFile(file) {
  let text = fs.readFileSync(file, 'utf8');
  let original = text;

  // 1) Markdown/MDX links: (...)
  text = text.replace(/\(\/blog\/([^\)"'\s]+)\)/g, (m, p1) => {
    if (p1.endsWith('/')) return m; // already has slash
    return `(/blog/${p1}/)`;
  });

  // 2) Markdown links with title: (/blog/slug "title")
  text = text.replace(/\(\/blog\/([^\)"'\s]+)(\s+"[^"]*")\)/g, (m, p1, p2) => {
    if (p1.endsWith('/')) return m;
    return `(/blog/${p1}/${p2})`;
  });

  // 3) HTML href attributes: href="/blog/slug" or href='/blog/slug'
  text = text.replace(/href=(\"|\')(\/blog\/[^\"'\s>]+)(\"|\')/g, (m, q, p1) => {
    if (p1.endsWith('/')) return m;
    return `href=${q}${p1}/${q}`;
  });

  // 4) Plain text occurrences like /blog/slug followed by whitespace or line end in lists
  text = text.replace(/(^|\s)(\/blog\/[^\s\)\]\"]+)(?!\/)(?=$|[\s\)\]\"])/g, (m, lead, p1) => {
    if (p1.endsWith('/')) return m;
    return `${lead}${p1}/`;
  });

  if (text !== original) {
    fs.writeFileSync(file, text, 'utf8');
    return true;
  }
  return false;
}

const patterns = [
  'src/content/blog/**/*.mdx',
  'src/content/blog/**/*.md',
  'src/components/**/*.astro',
  'src/pages/**/*.astro',
  'src/**/*.mdx',
  'src/**/*.md'
];

let filesChanged = [];
for (const pattern of patterns) {
  const files = glob.sync(pattern, { nodir: true });
  for (const file of files) {
    try {
      const changed = processFile(file);
      if (changed) filesChanged.push(file);
    } catch (e) {
      console.error('Error processing', file, e.message);
    }
  }
}

console.log('Files changed:', filesChanged.length);
filesChanged.forEach(f => console.log('-', f));

if (filesChanged.length === 0) process.exit(0);
process.exit(0);
