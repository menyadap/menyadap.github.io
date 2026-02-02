const fs = require('fs');
const path = require('path');

function walk(dir, fileList = []) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      walk(full, fileList);
    } else if (entry.isFile()) {
      if (full.endsWith('.md') || full.endsWith('.mdx') || full.endsWith('.astro') || full.endsWith('.html')) {
        fileList.push(full);
      }
    }
  }
  return fileList;
}

const assetExtRegex = /\.(?:png|jpe?g|gif|svg|webp|avif|mp4|mp3|pdf|zip|ico|css|js|json|xml|txt|csv|woff2?|ttf)$/i;

function shouldAddSlash(p) {
  if (!p) return false;
  if (!p.startsWith('/')) return false; // only absolute internal paths
  if (p === '/') return false; // root
  if (p.startsWith('/#')) return false; // anchor on root
  if (p.includes('://')) return false; // external
  if (assetExtRegex.test(p)) return false; // asset file
  if (p.endsWith('/')) return false; // already has slash
  return true;
}

function processFile(file) {
  let text = fs.readFileSync(file, 'utf8');
  const original = text;

  // 1) Markdown/MDX links: [text](/path)
  text = text.replace(/\(\/(?:[^\)"'\s]+)\)/g, (m) => {
    const inner = m.slice(1, -1); // '/path'
    if (shouldAddSlash(inner)) return `(${inner}/)`;
    return m;
  });

  // 2) Markdown links with title: (/path "title")
  text = text.replace(/\(\/(?:[^\)"'\s]+)(\s+"[^"]*")\)/g, (m) => {
    const match = m.match(/\((\/[^\s\"]+)(\s+"[^"]*")\)/);
    if (!match) return m;
    const p = match[1];
    const rest = match[2];
    if (shouldAddSlash(p)) return `(${p}/${rest})`;
    return m;
  });

  // 3) HTML href attributes: href="/path" or href='/path'
  text = text.replace(/href=(\"|\')(\/[^\"'\s>]+)(\"|\')/g, (m, q, p1, q2) => {
    if (shouldAddSlash(p1)) return `href=${q}${p1}/${q2}`;
    return m;
  });

  // 4) Plain occurrences: whitespace or line start followed by /path and then whitespace or punctuation
  text = text.replace(/(^|\s)(\/[^\s\)\]\"',>]+)(?=$|[\s\)\]\"',>])/g, (m, lead, p1) => {
    if (shouldAddSlash(p1)) return `${lead}${p1}/`;
    return m;
  });

  if (text !== original) {
    fs.writeFileSync(file, text, 'utf8');
    return true;
  }
  return false;
}

const startDirs = ['src'];
let changed = [];
for (const dir of startDirs) {
  if (!fs.existsSync(dir)) continue;
  const files = walk(dir);
  for (const f of files) {
    try {
      if (processFile(f)) changed.push(f);
    } catch (e) {
      console.error('err', f, e.message);
    }
  }
}

console.log('Files changed:', changed.length);
changed.forEach(f => console.log('-', f));
process.exit(0);
