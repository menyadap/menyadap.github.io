#!/usr/bin/env python3
"""
Hapus semua {{< rekomendasi-blog >}} shortcode dari file .md di folder blog.
"""

import re
from pathlib import Path

# Path ke blog directory
BLOG_DIR = Path("./src/content/blog")

def remove_rekomendasi_shortcode(content):
    """
    Hapus {{< rekomendasi-blog >}} dan bersihkan whitespace berlebihan.
    """
    # Pattern untuk {{< rekomendasi-blog >}}
    pattern = r'\{\{<\s*rekomendasi-blog\s*>\}\}'
    
    # Hapus shortcode
    content = re.sub(pattern, '', content)
    
    # Bersihkan multiple blank lines (lebih dari 2 newline berturut-turut)
    content = re.sub(r'\n\n\n+', '\n\n', content)
    
    return content


def process_file(file_path):
    """
    Process single .md file dan hapus shortcode
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Apply removal
        content = remove_rekomendasi_shortcode(content)
        
        # Write back if changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, "Removed"
        return True, "No shortcode found"
    
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
    print(f"Removing {{< rekomendasi-blog >}} shortcode...\n")
    print(f"{'='*70}\n")
    
    removed_count = 0
    unchanged_count = 0
    error_count = 0
    
    for file_path in sorted(md_files):
        success, message = process_file(file_path)
        
        status = "[OK]" if success and message == "Removed" else "[--]"
        print(f"{status} {file_path.name:<50} - {message}")
        
        if success:
            if message == "Removed":
                removed_count += 1
            else:
                unchanged_count += 1
        else:
            error_count += 1
    
    print(f"\n{'='*70}")
    print(f"Summary:")
    print(f"  Removed:  {removed_count} files")
    print(f"  Unchanged: {unchanged_count} files")
    print(f"  Errors:    {error_count} files")
    print(f"  Total:     {len(md_files)} files")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()
