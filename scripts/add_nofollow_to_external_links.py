#!/usr/bin/env python3
"""Convert external markdown links to HTML with rel="nofollow noreferrer" target="_blank".
Converts [text](url) to <a href="url" rel="nofollow noreferrer" target="_blank">text</a> for external URLs.
Internal links (starting with / or #) are left unchanged.
"""
from pathlib import Path
import re
import sys


def is_external_url(url: str) -> bool:
    """Check if URL is external (not relative path or anchor)."""
    url = url.strip()
    if url.startswith('/') or url.startswith('#') or url.startswith('mailto:'):
        return False
    if url.startswith('http://') or url.startswith('https://'):
        return True
    return False


def convert_external_links(text: str) -> str:
    """Convert [text](url) to <a> tags for external URLs."""
    def replace_link(match):
        link_text = match.group(1)
        url = match.group(2)
        if is_external_url(url):
            # Convert to HTML with attributes
            return f'<a href="{url}" rel="nofollow noreferrer" target="_blank">{link_text}</a>'
        else:
            # Keep as is for internal links
            return match.group(0)
    # Match [text](url) but not already HTML <a> tags
    pattern = r'\[([^\]]+)\]\(([^\)]+)\)'
    return re.sub(pattern, replace_link, text)


def process_file(path: Path) -> bool:
    """Process file and return True if changed."""
    try:
        txt = path.read_text(encoding='utf-8')
    except Exception:
        return False
    newtxt = convert_external_links(txt)
    if newtxt != txt:
        path.write_text(newtxt, encoding='utf-8')
        return True
    return False


def main():
    root = Path('src/content/blog')
    if not root.exists():
        print('Path not found:', root)
        return 1
    changed = []
    for p in root.rglob('*'):
        if p.suffix.lower() not in ('.md', '.mdx'):
            continue
        if p.name.endswith('.bak'):
            continue
        if process_file(p):
            changed.append(str(p))
    print(f'Updated {len(changed)} files')
    for c in changed:
        print(c)
    return 0


if __name__ == '__main__':
    sys.exit(main())
