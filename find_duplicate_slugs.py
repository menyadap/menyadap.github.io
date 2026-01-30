#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script untuk mencari duplicate slugs dalam frontmatter
"""

import os
import re
from pathlib import Path
from collections import defaultdict
import yaml

def extract_frontmatter(content):
    """Extract frontmatter dari markdown file"""
    if not content.startswith('---'):
        return None
    
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if match:
        try:
            return yaml.safe_load(match.group(1))
        except:
            return None
    return None

def get_slug_from_file(filepath):
    """Get slug dari filename atau frontmatter"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Cek frontmatter untuk slug field
    fm = extract_frontmatter(content)
    if fm and 'slug' in fm:
        return fm['slug']
    
    # Default ke filename tanpa .md
    return filepath.stem

def main():
    blog_dir = Path('src/content/blog')
    
    slugs = defaultdict(list)
    
    for md_file in sorted(blog_dir.glob('*.md')):
        try:
            slug = get_slug_from_file(md_file)
            slugs[slug].append(md_file.name)
        except Exception as e:
            print(f"Error reading {md_file.name}: {e}")
    
    print("Checking for duplicate slugs in all collections...\n")
    
    duplicates = {k: v for k, v in slugs.items() if len(v) > 1}
    
    if duplicates:
        print(f"Found {len(duplicates)} duplicate slugs:\n")
        for slug, files in sorted(duplicates.items()):
            print(f"Slug: {slug}")
            for f in files:
                print(f"  - {f}")
            print()
    else:
        print("No duplicate slugs found!")

if __name__ == '__main__':
    main()
