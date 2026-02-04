#!/usr/bin/env python3
"""Convert TOML frontmatter (+++ ... +++) to YAML frontmatter (--- ... ---)

This script makes a backup copy of each modified file with extension `.bak`.
It handles simple TOML key = value and array lines common in Hugo frontmatter.
"""
import os
import re
import sys
from pathlib import Path


def parse_toml_block(toml_text: str):
    data = {}
    # split into lines and handle simple key = value or key = [..]
    for raw in toml_text.splitlines():
        line = raw.strip()
        if not line or line.startswith('#'):
            continue
        # skip tables and arrays of tables
        if line.startswith('[') and line.endswith(']'):
            # not handling nested tables — skip
            continue
        m = re.match(r"^([A-Za-z0-9_\-]+)\s*=\s*(.*)$", line)
        if not m:
            continue
        key, val = m.group(1), m.group(2).strip()
        # remove trailing comment
        val = re.sub(r"\s+#.*$", "", val).strip()
        # String
        if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
            data[key] = val[1:-1]
            continue
        # Array
        if val.startswith('[') and val.endswith(']'):
            inner = val[1:-1].strip()
            if not inner:
                data[key] = []
            else:
                # split by comma but naive (assume no nested commas)
                items = [i.strip() for i in inner.split(',')]
                parsed = []
                for it in items:
                    if (it.startswith('"') and it.endswith('"')) or (it.startswith("'") and it.endswith("'")):
                        parsed.append(it[1:-1])
                    else:
                        # try boolean/number
                        if it.lower() in ('true','false'):
                            parsed.append(it.lower() == 'true')
                        else:
                            try:
                                if '.' in it:
                                    parsed.append(float(it))
                                else:
                                    parsed.append(int(it))
                            except Exception:
                                parsed.append(it)
                data[key] = parsed
            continue
        # Boolean
        if val.lower() in ('true', 'false'):
            data[key] = val.lower() == 'true'
            continue
        # Number
        try:
            if '.' in val:
                data[key] = float(val)
            else:
                data[key] = int(val)
            continue
        except Exception:
            pass
        # fallback: unquoted string
        data[key] = val
    return data


def to_yaml_frontmatter(data: dict) -> str:
    lines = ['---']
    for k, v in data.items():
        if isinstance(v, list):
            # use block list for readability
            lines.append(f"{k}:")
            for item in v:
                # quote strings that contain colon or leading/trailing spaces
                if isinstance(item, str):
                    safe = item.replace('"', '\\"')
                    lines.append(f"  - \"{safe}\"")
                else:
                    lines.append(f"  - {item}")
        else:
            if isinstance(v, str):
                safe = v.replace('"', '\\"')
                lines.append(f"{k}: \"{safe}\"")
            elif isinstance(v, bool):
                lines.append(f"{k}: {str(v).lower()}")
            else:
                lines.append(f"{k}: {v}")
    lines.append('---')
    return '\n'.join(lines) + '\n'


def convert_file(path: Path) -> bool:
    text = path.read_text(encoding='utf-8')
    parts = text.split('\n')
    # find start index where a line contains only +++ (allow leading whitespace)
    start_idx = None
    for i in range(0, min(20, len(parts))):
        if parts[i].strip() == '+++':
            start_idx = i
            break
    if start_idx is None:
        return False
    # find end index of frontmatter (next line that is exactly +++)
    end_idx = None
    for i in range(start_idx + 1, len(parts)):
        if parts[i].strip() == '+++':
            end_idx = i
            break
    if end_idx is None:
        return False
    toml_block = '\n'.join(parts[1:end_idx])
    try:
        data = parse_toml_block(toml_block)
    except Exception as e:
        print(f"Failed to parse TOML block in {path}: {e}")
        return False
    yaml_block = to_yaml_frontmatter(data)
    rest = '\n'.join(parts[end_idx+1:])
    # backup
    bak = path.with_suffix(path.suffix + '.bak')
    if not bak.exists():
        path.rename(bak)
        bak.write_text(bak.read_text(encoding='utf-8'), encoding='utf-8')
        # after rename, restore original content from bak variable
        original = bak.read_text(encoding='utf-8')
        # write new file
        path.write_text(yaml_block + rest, encoding='utf-8')
    else:
        # if bak already exists, avoid overwriting
        path.write_text(yaml_block + rest, encoding='utf-8')
    return True


def main(root: str):
    root_path = Path(root)
    if not root_path.exists():
        print(f"Path not found: {root}")
        return
    converted = []
    for p in root_path.rglob('*.md'):
        try:
            if convert_file(p):
                converted.append(str(p))
        except Exception as e:
            print(f"Error processing {p}: {e}")
    print(f"Converted {len(converted)} files")
    for c in converted[:200]:
        print(c)


if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else 'content'
    main(target)
