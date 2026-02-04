#!/usr/bin/env python3
"""Replace sadapphone.com -> menyadap.github.io in src/content/blog MD/MDX files.
Prints files changed.
"""
from pathlib import Path


def main():
    root = Path('src/content/blog')
    if not root.exists():
        print('Path not found:', root)
        return 1
    old = 'sadapphone.com'
    new = 'menyadap.github.io'
    changed = []
    for p in root.rglob('*'):
        if p.suffix.lower() not in ('.md', '.mdx'):
            continue
        if p.name.endswith('.bak'):
            continue
        try:
            txt = p.read_text(encoding='utf-8')
        except Exception:
            continue
        if old in txt:
            newtxt = txt.replace(old, new)
            p.write_text(newtxt, encoding='utf-8')
            changed.append(str(p))
    print(f'Updated {len(changed)} files')
    for c in changed:
        print(c)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
