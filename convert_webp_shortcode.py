#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script untuk mengubah Hugo shortcode {{< webp >}} menjadi Markdown image syntax
"""

import os
import re
from pathlib import Path

def convert_webp_shortcode(content):
    """
    Mengubah {{< webp src="..." caption="..." >}} menjadi ![caption](src)
    """
    # Pattern untuk {{< webp src="..." caption="..." >}}
    pattern = r'\{\{<\s*webp\s+src="([^"]+)"\s+caption="([^"]+)"\s*>\}\}'
    
    def replace_shortcode(match):
        src = match.group(1)
        caption = match.group(2)
        return f'![{caption}]({src})'
    
    new_content = re.sub(pattern, replace_shortcode, content)
    return new_content, content != new_content

def process_file(filepath):
    """
    Memproses satu file markdown
    """
    try:
        # Baca file
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Ganti shortcode webp
        new_content, changed = convert_webp_shortcode(content)
        
        # Jika ada perubahan, tulis kembali file
        if changed:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return 'OK'
        else:
            return '--'
    except Exception as e:
        print(f"[ERROR] {filepath}: {str(e)}")
        return 'ERROR'

def main():
    """
    Main function - memproses semua file .md di src/content/blog/
    """
    blog_dir = Path('src/content/blog')
    
    if not blog_dir.exists():
        print(f"Error: Directory {blog_dir} tidak ditemukan")
        return
    
    # Cari semua file .md
    md_files = sorted(blog_dir.glob('*.md'))
    
    if not md_files:
        print(f"Tidak ada file .md ditemukan di {blog_dir}")
        return
    
    print(f"Processing {len(md_files)} file markdown...\n")
    
    stats = {'converted': 0, 'unchanged': 0, 'errors': 0}
    
    for filepath in md_files:
        result = process_file(filepath)
        filename = filepath.name
        
        if result == 'OK':
            print(f"[OK] {filename} - WebP shortcode converted")
            stats['converted'] += 1
        elif result == '--':
            print(f"[--] {filename} - No shortcode found")
            stats['unchanged'] += 1
        else:
            print(f"[ERROR] {filename} - Error processing file")
            stats['errors'] += 1
    
    # Summary
    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  Converted: {stats['converted']} files")
    print(f"  Unchanged: {stats['unchanged']} files")
    print(f"  Errors: {stats['errors']} files")
    print(f"  Total: {len(md_files)} files")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
