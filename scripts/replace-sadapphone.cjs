const fs = require('fs');
const path = require('path');

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

const blogDir = path.join(__dirname, '../src/content/blog');
const files = walk(blogDir);

let totalReplacements = 0;
const changedFiles = [];

for (const file of files) {
  let content = fs.readFileSync(file, 'utf8');
  const originalContent = content;
  
  // Replace all variations of sadapphone with menyadap.github.io
  const replacements = [
    { from: /sadapphone\.com/gi, to: 'menyadap.github.io' },
    { from: /sadapphone/gi, to: 'menyadap.github.io' },
    { from: /www\.menyadap\.github\.io/gi, to: 'menyadap.github.io' }, // Normalize www prefix
  ];
  
  for (const replacement of replacements) {
    content = content.replace(replacement.from, replacement.to);
  }
  
  if (content !== originalContent) {
    const count = (originalContent.match(/sadapphone/gi) || []).length;
    fs.writeFileSync(file, content, 'utf8');
    changedFiles.push({
      file: path.relative(process.cwd(), file),
      replacements: count
    });
    totalReplacements += count;
  }
}

console.log(`✓ Total files with replacements: ${changedFiles.length}`);
console.log(`✓ Total replacements made: ${totalReplacements}`);
console.log('\nFiles changed:');
changedFiles.forEach(f => {
  console.log(`  - ${f.file} (${f.replacements} replacements)`);
});
