#!/usr/bin/env python3
"""promptfill - fill [BRACKET] placeholders in prompt templates.

Standard library only. No network. Reads template files; writes a file only
when --write is given, only into the chosen output folder, and never
overwrites an existing file.

Commands:
  list  PATH                     show templates (file or folder) and their placeholders
  fill  FILE [options]           fill one template
      --set KEY=VALUE            repeatable; KEY is case-insensitive
      --values FILE              text file with KEY=VALUE lines ('#' = comment)
      --write                    save the result (default: preview on screen only)
      --out-dir DIR              where --write saves (default: ./filled)
"""
import argparse
import re
import sys
from pathlib import Path

PLACEHOLDER = re.compile(r"\[([A-Z][A-Z0-9 /,'&\-]*)\]")


def norm(key):
    return " ".join(key.strip().upper().split())


def find_placeholders(text):
    seen = []
    for m in PLACEHOLDER.finditer(text):
        k = norm(m.group(1))
        if k not in seen:
            seen.append(k)
    return seen


def parse_values_file(path):
    vals = {}
    for n, line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            raise SystemExit(f"{path}:{n}: expected KEY=VALUE")
        k, v = line.split("=", 1)
        vals[norm(k)] = v.strip()
    return vals


def fill(text, values):
    def repl(m):
        k = norm(m.group(1))
        return values.get(k, m.group(0))
    return PLACEHOLDER.sub(repl, text)


def cmd_list(args):
    p = Path(args.path)
    files = [p] if p.is_file() else sorted(p.glob("*.txt"))
    if not files:
        raise SystemExit(f"No .txt templates found in {p}")
    for f in files:
        ph = find_placeholders(f.read_text(encoding="utf-8"))
        print(f"{f.name}: {len(ph)} placeholder(s)")
        for k in ph:
            print(f"    [{k}]")


def cmd_fill(args):
    src = Path(args.file)
    if not src.is_file():
        raise SystemExit(f"Template not found: {src}")
    text = src.read_text(encoding="utf-8")
    values = {}
    if args.values:
        values.update(parse_values_file(args.values))
    for item in args.set or []:
        if "=" not in item:
            raise SystemExit(f"--set needs KEY=VALUE, got: {item}")
        k, v = item.split("=", 1)
        values[norm(k)] = v.strip()
    result = fill(text, values)
    missing = find_placeholders(result)
    if not args.write:
        print(result)
        print("\n--- preview only (add --write to save) ---", file=sys.stderr)
    else:
        out_dir = Path(args.out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        dest = out_dir / src.name
        if dest.exists():
            raise SystemExit(f"Refusing to overwrite {dest}")
        dest.write_text(result, encoding="utf-8")
        print(f"Saved {dest}", file=sys.stderr)
    if missing:
        print("Still empty: " + ", ".join(f"[{k}]" for k in missing), file=sys.stderr)
        return 1
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="Fill [BRACKET] placeholders in prompt templates.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("list", help="list templates and placeholders")
    a.add_argument("path")
    b = sub.add_parser("fill", help="fill one template")
    b.add_argument("file")
    b.add_argument("--set", action="append", metavar="KEY=VALUE")
    b.add_argument("--values", metavar="FILE")
    b.add_argument("--write", action="store_true")
    b.add_argument("--out-dir", default="filled")
    args = ap.parse_args(argv)
    if args.cmd == "list":
        cmd_list(args)
        return 0
    return cmd_fill(args)


if __name__ == "__main__":
    sys.exit(main())
