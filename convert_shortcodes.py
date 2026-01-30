#!/usr/bin/env python3
"""
Convert Hugo shortcodes to Markdown/HTML equivalents in blog .md files.

Changes:
1. {{< img src="..." caption="..." >}} → ![caption](src)
2. {{< hubungi_kami >}} → HTML block with Bootstrap styling
"""

import re
import os
from pathlib import Path

# Path ke blog directory
BLOG_DIR = Path("./src/content/blog")

# HTML replacement untuk {{< hubungi_kami >}}
HUBUNGI_KAMI_HTML = """<div class="d-flex justify-content-center">
<div class="col-lg-6">
  <div class="card row related mb-5 mt-5">
    <div class="card-body">
      <span class="h3">ADA <strong>PERTANYAAN</strong>?</span>
      <img class="img-fluid mt-5" src="/images/sadap-phone.webp" width="660" height="895" alt="Jasa Sadap HP">
      <p>📱 Tersedia Untuk iPhone & Android</p>
      <p>💬 Sadap Aplikasi WhatsApp, Telegram, Line, Instagram, Facebook, Skype, Viber, Snapchat</p>
      <p>📷 Remote kamera dan layar</p>
      <p>📞 Rekam Panggilan telepon & Akses Galeri</p>
      
      <p>🔒 Ketentuan Penggunaan & Privasi Berlaku</p>
      <p>😋 Apabila <strong>ada pertanyaan lebih?</strong> tentang perangkat sadap bisa kontak kami berikut:</p>
      <small>tinggal klik aja</small>
      <a href="/chat-wa/" class="btn btn-primary btn-lg stretched-link">{{ $.Site.Params.nomer}} (WA)</a>
    </div>
  </div>
</div>
</div>"""


def convert_img_shortcode(content):
    """
    Convert <Img src="..." caption="..." /> to ![caption](src)
    Also converts old Hugo {{< img src="..." caption="..." >}} to ![caption](src)
    """
    # Pattern untuk Astro component <Img />
    pattern_astro = r'<Img\s+src="([^"]+)"\s+caption="([^"]+)"\s*\/>'
    
    # Pattern untuk Hugo shortcode {{< img >}}
    pattern_hugo = r'\{\{<\s*img\s+src="([^"]+)"\s+caption="([^"]+)"\s*>\}\}'
    
    def replacement(match):
        src = match.group(1)
        caption = match.group(2)
        return f"![{caption}]({src})"
    
    # Replace both patterns
    content = re.sub(pattern_astro, replacement, content)
    content = re.sub(pattern_hugo, replacement, content)
    return content


def convert_hubungi_kami_shortcode(content):
    """
    Convert <QuestionCard ... /> to HTML block
    Also convert old Hugo {{< hubungi_kami >}} to HTML block
    """
    # Pattern untuk Astro component <QuestionCard />
    pattern_astro = r'<QuestionCard\s+[^>]*\/>'
    
    # Pattern untuk Hugo shortcode {{< hubungi_kami >}}
    pattern_hugo = r'\{\{<\s*hubungi_kami\s*>\}\}'
    
    # Replace both patterns
    content = re.sub(pattern_astro, HUBUNGI_KAMI_HTML, content)
    content = re.sub(pattern_hugo, HUBUNGI_KAMI_HTML, content)
    return content


def process_file(file_path):
    """
    Process single .md file and apply conversions
    """
    try:
        # Debug: print absolute path
        abs_path = file_path.resolve() if hasattr(file_path, 'resolve') else file_path
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Apply conversions
        content = convert_img_shortcode(content)
        content = convert_hubungi_kami_shortcode(content)
        
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
    
    converted_count = 0
    unchanged_count = 0
    error_count = 0
    
    for file_path in sorted(md_files):
        success, message = process_file(file_path)
        
        status = "✓" if success and message == "Converted" else "○"
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
