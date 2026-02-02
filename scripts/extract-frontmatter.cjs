const fs = require('fs');
const path = require('path');

// Simple YAML front matter parser without external deps
function parseFrontmatter(content) {
  // Remove BOM if present
  if (content.charCodeAt(0) === 0xFEFF) {
    content = content.slice(1);
  }
  
  // Normalize line endings to \n
  content = content.replace(/\r\n/g, '\n');
  
  // Match content between --- markers
  const match = content.match(/^---\n([\s\S]*?)\n---/);
  if (!match) {
    return null;
  }
  
  const fm = {};
  const lines = match[1].split('\n');
  
  let i = 0;
  while (i < lines.length) {
    const line = lines[i];
    
    // Skip empty lines
    if (!line.trim()) {
      i++;
      continue;
    }
    
    // Skip comments
    if (line.trim().startsWith('#')) {
      i++;
      continue;
    }
    
    // Check if line is a key: value pair (not indented)
    if (!line.startsWith(' ') && !line.startsWith('\t') && line.includes(':')) {
      const colonIdx = line.indexOf(':');
      const key = line.substring(0, colonIdx).trim();
      let value = line.substring(colonIdx + 1).trim();
      
      // Skip array/object markers on same line
      if (value === '' || value === '[]' || value === '{}' || value.startsWith('-') || value.startsWith('[')) {
        // Multi-line structure
        if (value === '' || value.startsWith('-')) {
          i++;
          // Skip until we hit next key or end
          while (i < lines.length && (lines[i].startsWith(' ') || lines[i].startsWith('\t') || !lines[i].trim())) {
            i++;
          }
          i--; // Back up one because loop will increment
        }
      } else {
        // Single line or start of multi-line value
        // Check if next lines are indented continuation
        let j = i + 1;
        while (j < lines.length && (lines[j].startsWith('  ') || lines[j].startsWith('\t'))) {
          value += ' ' + lines[j].trim();
          j++;
        }
        
        if (j > i + 1) {
          i = j - 1; // Skip the lines we just consumed
        }
        
        // Remove quotes
        value = value.replace(/^["']|["']$/g, '');
        fm[key] = value;
      }
    }
    
    i++;
  }
  
  return fm;
}

function walk(dir) {
  let results = [];
  const list = fs.readdirSync(dir, { withFileTypes: true });
  for (const dirent of list) {
    const full = path.join(dir, dirent.name);
    if (dirent.isDirectory()) {
      results = results.concat(walk(full));
    } else if (dirent.name.endsWith('.mdx')) {
      results.push(full);
    }
  }
  return results;
}

function escapeCsv(value) {
  if (!value) return '';
  const str = String(value);
  if (str.includes(',') || str.includes('"') || str.includes('\n')) {
    return `"${str.replace(/"/g, '""')}"`;
  }
  return str;
}

const blogDir = path.join(__dirname, '../src/content/blog');
const files = walk(blogDir).sort();

console.log(`Found ${files.length} MDX files`);

const rows = [['Filename', 'Title', 'Description']];
let successCount = 0;

for (const file of files) {
  const content = fs.readFileSync(file, 'utf8');
  const fm = parseFrontmatter(content);
  
  if (fm) {
    const filename = path.basename(file, '.mdx');
    rows.push([
      filename,
      escapeCsv(fm.title || ''),
      escapeCsv(fm.description || '')
    ]);
    successCount++;
  }
}

const csv = rows.map(r => r.join(',')).join('\n');
const outputPath = path.join(__dirname, '../blog-frontmatter.csv');
fs.writeFileSync(outputPath, csv, 'utf8');

console.log(`✓ CSV file created: blog-frontmatter.csv`);
console.log(`✓ Total files processed: ${files.length}`);
console.log(`✓ Total entries exported: ${successCount}`);
