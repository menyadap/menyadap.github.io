#!/usr/bin/env python3
import os
import re
from datetime import datetime

# New date to use (February 2, 2026)
NEW_DATE = "2026-02-02T12:00:00Z"

# Bajak files
BAJAK_FILES = [
    '10-aplikasi-social-spy-sadap-wa-014c687.mdx',
    '10-sadap-hp-tersembunyi-suami-selingkuh-13a3b.mdx',
    '12-aplikasi-sadap-wa-gratis-tanpa-ketahuan-5117c.mdx',
    '9-sadap-hp-pacar-tanpa-ketahuan-bdb42.mdx',
    'cara-hack-akun-facebook-lupa-password.mdx',
    'cara-hack-akun-instagram-lupa-password-1dc.mdx',
    'sadap-android-gratis-tanpa-rooting-d04c.mdx',
    'sadap-hp-gratis-istri-selingkuh-29f9f.mdx',
    'sadap-iphone-android-tanpa-pinjam.mdx',
    'sadap-iphone-ipad-dengan-itunes-977c1.mdx'
]

# Penyadap files - get all files with "- penyadap" in categories
BLOG_DIR = 'src/content/blog'
PENYADAP_FILES = []

for filename in os.listdir(BLOG_DIR):
    if filename.endswith('.mdx'):
        filepath = os.path.join(BLOG_DIR, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            if '- penyadap' in content:
                PENYADAP_FILES.append(filename)

def update_date_in_file(filepath, new_date):
    """Update the date field in frontmatter"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace date field in frontmatter
    # Match pattern: date: YYYY-MM-DDTHH:MM:SS.sssZ or date: YYYY-MM-DDTHH:MM:SSZ
    updated_content = re.sub(
        r'date: \d{4}-\d{2}-\d{2}T[\d:\.]+Z',
        f'date: {new_date}',
        content,
        count=1
    )
    
    if updated_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        return True
    return False

# Update bajak files
print(f"Updating {len(BAJAK_FILES)} bajak files...")
updated_count = 0
for filename in BAJAK_FILES:
    filepath = os.path.join(BLOG_DIR, filename)
    if os.path.exists(filepath):
        if update_date_in_file(filepath, NEW_DATE):
            print(f"  ✓ {filename}")
            updated_count += 1
    else:
        print(f"  ✗ {filename} (not found)")
print(f"Bajak files updated: {updated_count}/{len(BAJAK_FILES)}\n")

# Update penyadap files
print(f"Updating {len(PENYADAP_FILES)} penyadap files...")
updated_count = 0
for filename in PENYADAP_FILES:
    filepath = os.path.join(BLOG_DIR, filename)
    if os.path.exists(filepath):
        if update_date_in_file(filepath, NEW_DATE):
            updated_count += 1
print(f"Penyadap files updated: {updated_count}/{len(PENYADAP_FILES)}\n")

print(f"Total files processed: {len(BAJAK_FILES) + len(PENYADAP_FILES)}")
print(f"Total updated: {updated_count + len(BAJAK_FILES)}")
