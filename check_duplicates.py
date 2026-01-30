#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script untuk menemukan duplicate blog IDs di Astro
"""

import os
from pathlib import Path
from collections import defaultdict

def get_slug_from_filename(filename):
    """
    Extract slug dari filename dengan menghilangkan suffix angka
    """
    name = Path(filename).stem
    # Hilangkan suffix -XX di akhir
    parts = name.rsplit('-', 1)
    if len(parts) == 2 and parts[1].isdigit():
        return parts[0]
    return name

def main():
    blog_dir = Path('src/content/blog')
    
    # Group files by slug
    slugs = defaultdict(list)
    
    for md_file in sorted(blog_dir.glob('*.md')):
        slug = get_slug_from_filename(md_file.name)
        slugs[slug].append(md_file.name)
    
    # Cari duplikat
    print("Checking for duplicate slugs...\n")
    
    duplicates = {k: v for k, v in slugs.items() if len(v) > 1}
    
    if duplicates:
        print(f"Found {len(duplicates)} potential duplicate slugs:\n")
        for slug, files in sorted(duplicates.items()):
            print(f"Slug: {slug}")
            for f in files:
                filepath = blog_dir / f
                print(f"  - {f}")
            print()
    else:
        print("No duplicate slugs found!")

if __name__ == '__main__':
    main()
