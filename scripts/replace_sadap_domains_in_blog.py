#!/usr/bin/env python3
"""Replace sadapphone.com and sadaphone.com with menyadap.github.io in src/content/blog files.
Preserves surrounding markdown/asterisk formatting.
"""
from pathlib import Path
import re
import sys


def replace_in_file(path: Path) -> bool:
    txt = path.read_text(encoding='utf-8')
    pattern = re.compile(r"sadapphone\.com|sadaphone\.com", flags=re.IGNORECASE)
    if not pattern.search(txt):
        return False
    newtxt = pattern.sub('menyadap.github.io', txt)
    path.write_text(newtxt, encoding='utf-8')
    return True


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
        try:
            if replace_in_file(p):
                changed.append(str(p))
        except Exception as e:
            print('Error', p, e)
    print(f'Updated {len(changed)} files')
    for c in changed:
        print(c)
    return 0


if __name__ == '__main__':
    sys.exit(main())
