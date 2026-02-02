const fs = require('fs');
const path = require('path');

function walk(dir, fileList = []) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      walk(full, fileList);
    } else if (entry.isFile()) {
      if (full.endsWith('.md') || full.endsWith('.mdx') || full.endsWith('.astro')) {
        fileList.push(full);
      }
    }
  }
  return fileList;
}

function processFile(file) {
  let text = fs.readFileSync(file, 'utf8');
  let original = text;

  text = text.replace(/\(\/blog\/([^\)"'\s]+)\)/g, (m, p1) => {
    if (p1.endsWith('/')) return m;
    return `(/blog/${p1}/)`;
  });

  text = text.replace(/\(\/blog\/([^\)"'\s]+)(\s+"[^"]*")\)/g, (m, p1, p2) => {
    if (p1.endsWith('/')) return m;
    return `(/blog/${p1}/${p2})`;
  });

  text = text.replace(/href=(\"|\')(\/blog\/[^\"'\s>]+)(\"|\')/g, (m, q, p1) => {
    if (p1.endsWith('/')) return m;
    return `href=${q}${p1}/${q}`;
  });

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

const startDirs = ['src/content/blog', 'src/components', 'src/pages'];
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
