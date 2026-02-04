#!/usr/bin/env python3
"""Move markdown files with YAML frontmatter `draft: false` into content/publish.

Creates `content/publish` if missing. Skips files ending with `.bak`.
Backs up moved files by leaving originals removed (use git to track changes).
"""
from pathlib import Path
import shutil
import re
import sys


def has_yaml_frontmatter_and_draft_false(path: Path) -> bool:
    try:
        text = path.read_text(encoding='utf-8')
    except Exception:
        return False
    # find YAML frontmatter delimiters
    if not text.lstrip().startswith('---'):
        return False
    parts = text.split('\n')
    # find first '---'
    start = None
    for i in range(0, min(40, len(parts))):
        if parts[i].strip() == '---':
            start = i
            break
    if start is None:
        return False
    end = None
    for i in range(start+1, min(start+200, len(parts))):
        if parts[i].strip() == '---':
            end = i
            break
    if end is None:
        return False
    fm_lines = parts[start+1:end]
    # search for draft: false (allow spaces, quotes, boolean, case-insensitive)
    for line in fm_lines:
        m = re.match(r"^\s*draft\s*:\s*(.*)$", line, flags=re.IGNORECASE)
        if m:
            val = m.group(1).strip().strip('"\'')
            if val.lower() in ('false', 'no', '0'):
                return True
            else:
                return False
    return False


def main():
    root = Path('content')
    if not root.exists():
        print('content/ not found, aborting')
        return 1
    dest = root / 'publish'
    dest.mkdir(parents=True, exist_ok=True)

    moved = []
    for p in root.rglob('*.md'):
        if p.suffixes and p.name.endswith('.bak'):
            continue
        # skip files under content/publish already
        if dest in p.parents:
            continue
        # skip .bak files
        if p.name.endswith('.bak'):
            continue
        if has_yaml_frontmatter_and_draft_false(p):
            # move file to dest; if name collision, append suffix
            target = dest / p.name
            if target.exists():
                # avoid overwrite
                i = 1
                while True:
                    candidate = dest / f"{p.stem}-{i}{p.suffix}"
                    if not candidate.exists():
                        target = candidate
                        break
                    i += 1
            shutil.move(str(p), str(target))
            moved.append((str(p), str(target)))

    print(f"Moved {len(moved)} files to {dest}")
    for src, dst in moved:
        print(f"{src} -> {dst}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
