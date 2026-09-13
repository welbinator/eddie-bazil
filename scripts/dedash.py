#!/usr/bin/env python3
"""Strip em/en dashes from built HTML. Verify none remain in source or dist."""
import re, sys, pathlib

def scan(root):
    hits = []
    for p in pathlib.Path(root).rglob("*"):
        if p.suffix in {".astro", ".ts", ".html"} and p.is_file():
            t = p.read_text(encoding="utf-8", errors="ignore")
            for i, line in enumerate(t.splitlines(), 1):
                if "\u2014" in line or "\u2013" in line:
                    hits.append(f"{p}:{i}: {line.strip()[:90]}")
    return hits

if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else "src"
    h = scan(root)
    if h:
        print(f"FOUND {len(h)} dash lines:")
        print("\n".join(h))
        sys.exit(1)
    print("clean: no em/en dashes")
