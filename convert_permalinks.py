#!/usr/bin/env python3
"""
Convert permalink URLs dari sadapphone.com domain ke menyadap.github.io/blog format.

Changes:
1. https://sadapphone.com/sadap/test-post/ → /blog/test-post
2. https://www.sadapphone.com/sadap/test-post/ → /blog/test-post
3. sadapphone.com/sadap/test-post/ → /blog/test-post
4. /sadap/test-post/ → /blog/test-post
"""

import re
import os
from pathlib import Path

# Path ke blog directory
BLOG_DIR = Path("./src/content/blog")

def convert_permalink_patterns(content):
    """
    Convert various permalink patterns dari old domain ke new format.
    
    Patterns:
    - https://sadapphone.com/sadap/test-post/ → /blog/test-post
    - https://www.sadapphone.com/sadap/test-post/ → /blog/test-post
    - sadapphone.com/sadap/test-post/ → /blog/test-post
    - /sadap/test-post/ → /blog/test-post
    """
    
    # Pattern 1: Full URL dengan https://sadapphone.com
    pattern1 = r'https://(?:www\.)?sadapphone\.com/sadap/([^\s"\')>]+?)/?'
    content = re.sub(pattern1, r'/blog/\1', content)
    
    # Pattern 2: Full URL tanpa https (sadapphone.com/sadap/...)
    pattern2 = r'sadapphone\.com/sadap/([^\s"\')>]+?)/?'
    content = re.sub(pattern2, r'/blog/\1', content)
    
    # Pattern 3: Relative path (/sadap/...)
    # More carefully: hanya replace /sadap/ menjadi /blog/ jika belum ada /blog/
    pattern3 = r'(?<!blog)/sadap/([^\s"\')>]*?)/?(?=["\'\s>)\]])'
    content = re.sub(pattern3, r'/blog/\1', content)
    
    # Clean up double slashes dan double /blog/
    content = re.sub(r'/blog/+blog/', '/blog/', content)  # /blog/blog/ → /blog/
    content = re.sub(r'/blog/+', '/blog/', content)  # /blog// → /blog/
    
    return content


def process_file(file_path):
    """
    Process single .md file and apply permalink conversions
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Apply conversions
        content = convert_permalink_patterns(content)
        
        # Write back if changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, "Converted"
        return True, "No changes"
    
    except Exception as e:
        return False, f"Error: {str(e)}"


def main():
    """
    Main function to process all .md files in blog directory
    """
    if not BLOG_DIR.exists():
        print(f"Error: Blog directory not found at {BLOG_DIR}")
        return
    
    # Find all .md files
    md_files = list(BLOG_DIR.glob("*.md"))
    
    if not md_files:
        print(f"No .md files found in {BLOG_DIR}")
        return
    
    print(f"Found {len(md_files)} markdown files to process\n")
    print(f"Converting permalinks:")
    print(f"  Old: sadapphone.com/sadap/test-post")
    print(f"  New: /blog/test-post")
    print(f"\n{'='*70}\n")
    
    converted_count = 0
    unchanged_count = 0
    error_count = 0
    
    for file_path in sorted(md_files):
        success, message = process_file(file_path)
        
        status = "[OK]" if success and message == "Converted" else "[--]"
        print(f"{status} {file_path.name:<50} - {message}")
        
        if success:
            if message == "Converted":
                converted_count += 1
            else:
                unchanged_count += 1
        else:
            error_count += 1
    
    print(f"\n{'='*70}")
    print(f"Summary:")
    print(f"  Converted: {converted_count} files")
    print(f"  Unchanged: {unchanged_count} files")
    print(f"  Errors:    {error_count} files")
    print(f"  Total:     {len(md_files)} files")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()
