const fs = require('fs');
const path = require('path');

function walk(dir) {
  let results = [];
  const list = fs.readdirSync(dir, { withFileTypes: true });
  list.forEach((dirent) => {
    const full = path.join(dir, dirent.name);
    if (dirent.isDirectory()) {
      results = results.concat(walk(full));
    } else if (dirent.isFile() && dirent.name.endsWith('.mdx')) {
      results.push(full);
    }
  });
  return results;
}

function extractFrontmatter(content) {
  // Find frontmatter block between --- markers
  const frontmatterMatch = content.match(/^---\n([\s\S]*?)\n---\n/);
  if (!frontmatterMatch) {
    return null;
  }
  
  const frontmatterText = frontmatterMatch[1];
  const frontmatter = {};
  
  // Parse YAML-like format manually
  const lines = frontmatterText.split('\n');
  let currentKey = null;
  let currentValue = '';
  let inMultiline = false;
  
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    
    // Skip empty lines at the beginning
    if (!currentKey && !line.trim()) continue;
    
    // Check if line starts a new key (not indented)
    if (line && !line.startsWith(' ') && !line.startsWith('\t') && line.includes(':')) {
      // Save previous key-value if exists
      if (currentKey && currentValue.trim()) {
        frontmatter[currentKey] = currentValue.trim().replace(/^["']|["']$/g, '');
      }
      
      const [key, ...valueParts] = line.split(':');
      currentKey = key.trim();
      currentValue = valueParts.join(':').trim().replace(/^["']|["']$/g, '');
      inMultiline = currentValue.endsWith('|') || currentValue.endsWith('>');
      
      if (inMultiline) {
        currentValue = '';
      }
    } else if (currentKey && (line.startsWith(' ') || line.startsWith('\t') || inMultiline)) {
      // Continuation of previous value
      if (inMultiline) {
        currentValue += (currentValue ? ' ' : '') + line.trim();
      } else {
        currentValue += ' ' + line.trim();
      }
    }
  }
  
  // Save last key-value
  if (currentKey && currentValue.trim()) {
    frontmatter[currentKey] = currentValue.trim().replace(/^["']|["']$/g, '');
  }
  
  return frontmatter;
}

function escapeCsvValue(value) {
  if (!value) return '';
  const str = String(value);
  if (str.includes(',') || str.includes('"') || str.includes('\n')) {
    return `"${str.replace(/"/g, '""')}"`;
  }
  return str;
}

const blogDir = path.resolve(process.cwd(), 'src/content/blog');
const files = walk(blogDir);

const rows = [];
rows.push(['Filename', 'Title', 'Description']);

files.forEach((file) => {
  const content = fs.readFileSync(file, 'utf8');
  const frontmatter = extractFrontmatter(content);
  
  if (frontmatter && (frontmatter.title || frontmatter.description)) {
    const filename = path.basename(file, '.mdx');
    rows.push([
      filename,
      escapeCsvValue(frontmatter.title || ''),
      escapeCsvValue(frontmatter.description || '')
    ]);
  } else if (!frontmatter) {
    console.warn(`⚠ No frontmatter found in: ${path.basename(file)}`);
  }
});

const csv = rows.map((row) => row.join(',')).join('\n');
const outputPath = path.resolve(process.cwd(), 'blog-frontmatter.csv');
fs.writeFileSync(outputPath, csv, 'utf8');

console.log(`✓ CSV generated: ${outputPath}`);
console.log(`✓ Total files processed: ${files.length}`);
console.log(`✓ Total rows in CSV: ${rows.length - 1}`);
