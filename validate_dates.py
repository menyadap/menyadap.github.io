#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script untuk memvalidasi frontmatter date field di semua blog files
"""

import os
import re
from pathlib import Path
from datetime import datetime

def check_date_format(date_str):
    """
    Validate if date string is valid ISO 8601 format
    """
    # Check common invalid formats
    if date_str.strip() == '':
        return False, "Empty date"
    
    # Try to parse as ISO 8601
    formats = [
        '%Y-%m-%d',
        '%Y-%m-%dT%H:%M:%S.%fZ',
        '%Y-%m-%dT%H:%M:%S%z',
        '%Y-%m-%dT%H:%M:%S.%f%z',
    ]
    
    for fmt in formats:
        try:
            datetime.strptime(date_str.replace('Z', '+0000').replace('+09:00', '').replace('+00:00', ''), fmt.replace('%z', ''))
            return True, "Valid"
        except ValueError:
            continue
    
    return False, f"Invalid format: {date_str}"

def extract_frontmatter(content):
    """
    Extract frontmatter from markdown file
    """
    if not content.startswith('---'):
        return None
    
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if match:
        return match.group(1)
    return None

def check_file(filepath):
    """
    Check date field in a file
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        frontmatter = extract_frontmatter(content)
        if not frontmatter:
            return 'NO_FRONTMATTER', None
        
        # Extract date field
        date_match = re.search(r'^date:\s*(.+?)$', frontmatter, re.MULTILINE)
        if not date_match:
            return 'NO_DATE', None
        
        date_str = date_match.group(1).strip()
        is_valid, msg = check_date_format(date_str)
        
        if is_valid:
            return 'OK', date_str
        else:
            return 'INVALID', date_str
    
    except Exception as e:
        return 'ERROR', str(e)

def main():
    blog_dir = Path('src/content/blog')
    
    md_files = sorted(blog_dir.glob('*.md'))
    
    print(f"Checking {len(md_files)} files...\n")
    
    invalid_files = []
    
    for filepath in md_files:
        status, date_val = check_file(filepath)
        filename = filepath.name
        
        if status == 'INVALID':
            print(f"[INVALID] {filename}: {date_val}")
            invalid_files.append((filename, date_val))
        elif status == 'NO_DATE':
            print(f"[NO_DATE] {filename}")
        elif status == 'NO_FRONTMATTER':
            print(f"[NO_FM] {filename}")
        elif status == 'ERROR':
            print(f"[ERROR] {filename}: {date_val}")
        # OK files are not printed
    
    print(f"\n{'='*60}")
    print(f"Total files checked: {len(md_files)}")
    print(f"Invalid date formats: {len(invalid_files)}")
    
    if invalid_files:
        print(f"\nFiles with invalid dates:")
        for filename, date_val in invalid_files:
            print(f"  {filename}: {date_val}")

if __name__ == '__main__':
    main()
