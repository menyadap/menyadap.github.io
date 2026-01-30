#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script untuk mengganti link WhatsApp template {{ $.Site.Params.nomer}} 
dengan nomor WhatsApp yang sebenarnya (wa.me/628128398998288)
di semua file .md di folder src/content/blog/
"""

import os
import re
from pathlib import Path

def replace_whatsapp_link(content):
    """
    Mengganti link WhatsApp template dengan nomor sebenarnya
    """
    # Pattern untuk mengganti {{ $.Site.Params.nomer}} dengan wa.me/628128398998288
    pattern = r'({{ \$\.Site\.Params\.nomer}})'
    replacement = r'wa.me/628128398998288'
    
    new_content = re.sub(pattern, replacement, content)
    return new_content, content != new_content

def process_file(filepath):
    """
    Memproses satu file markdown
    """
    try:
        # Baca file
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Ganti link WhatsApp
        new_content, changed = replace_whatsapp_link(content)
        
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
    
    stats = {'replaced': 0, 'unchanged': 0, 'errors': 0}
    
    for filepath in md_files:
        result = process_file(filepath)
        filename = filepath.name
        
        if result == 'OK':
            print(f"[OK] {filename} - WhatsApp link replaced")
            stats['replaced'] += 1
        elif result == '--':
            print(f"[--] {filename} - No template found")
            stats['unchanged'] += 1
        else:
            print(f"[ERROR] {filename} - Error processing file")
            stats['errors'] += 1
    
    # Summary
    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  Replaced: {stats['replaced']} files")
    print(f"  Unchanged: {stats['unchanged']} files")
    print(f"  Errors: {stats['errors']} files")
    print(f"  Total: {len(md_files)} files")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
