"""Bring the Reel Nest entries of scripts/pages-manifest.json in line with the files on disk.

Run after build_site.py whenever texts are added, archived or moved:
    python -X utf8 sources/reel-nest/sync_manifest.py

Rewrites only the Reel Nest parts and keeps the rest of the file as it is:
- "files": the generated pages under products/reel-nest/privacy/ and terms/
- "maintenance_files": the texts under sources/reel-nest/content/
- "privacy_archives", "terms_archives": the previous-version dates
"""
import json
import re
from pathlib import Path

from build_site import CONTENT, OUT, SOURCE, archived_versions

ROOT = SOURCE.parents[1]
MANIFEST = ROOT / "scripts" / "pages-manifest.json"
ITEM_RE = re.compile(r'"([^"]*)"')


def replace_items(text: str, key: str, generated_prefixes: tuple[str, ...], items: list[str]) -> str:
    """Drop the lines of list `key` that hold generated items and append `items` two per line."""
    start = text.index(f'"{key}": [') + len(f'"{key}": [')
    end = text.index("\n  ]", start)
    kept = []
    for line in text[start:end].split("\n"):
        names = ITEM_RE.findall(line)
        if not names:
            continue
        generated = [n.startswith(generated_prefixes) for n in names]
        if any(generated) and not all(generated):
            raise ValueError(f"Line mixes Reel Nest generated items with others: {line.strip()}")
        if not any(generated):
            kept.append(line.rstrip().rstrip(","))
    rows = [", ".join(json.dumps(x) for x in items[i:i + 2]) for i in range(0, len(items), 2)]
    body = ",\n".join(kept + ["    " + row for row in rows])
    return text[:start] + "\n" + body + text[end:]


def main() -> None:
    text = MANIFEST.read_text(encoding="utf-8")
    pages = sorted(p.relative_to(ROOT).as_posix() for folder in ("privacy", "terms")
                   for p in (OUT / folder).rglob("index.html"))
    texts = sorted(p.relative_to(ROOT).as_posix() for p in CONTENT.rglob("*.txt"))
    text = replace_items(text, "files", ("products/reel-nest/privacy/", "products/reel-nest/terms/"), pages)
    text = replace_items(text, "maintenance_files", ("sources/reel-nest/content/",), texts)
    for doc in ("privacy", "terms"):
        key = f'"{doc}_archives": '
        s = text.index(key) + len(key)
        e = text.index("]", s) + 1
        text = text[:s] + json.dumps(sorted(archived_versions(doc))) + text[e:]
    data = json.loads(text)
    MANIFEST.write_text(text, encoding="utf-8", newline="\n")
    print(f"{MANIFEST.relative_to(ROOT)}: {len(pages)} Reel Nest pages, {len(texts)} Reel Nest texts, "
          f"previous versions privacy {data['privacy_archives']}, terms {data['terms_archives']}")


if __name__ == "__main__":
    main()
