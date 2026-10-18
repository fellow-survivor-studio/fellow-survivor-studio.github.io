"""Read-only GitHub Pages checks. Python 3.10+, standard library only."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote, urljoin, urlsplit
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / "scripts/pages-manifest.json").read_text(encoding="utf-8"))
BASE = CONFIG["base_url"]


class Document(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids, self.refs, self.canonicals = set(), [], []
        self.refresh = False
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if tag == "a" and attrs.get("name"):
            self.ids.add(attrs["name"])
        for name in ("href", "src", "poster"):
            if attrs.get(name):
                self.refs.append(attrs[name])
        if attrs.get("srcset"):
            self.refs.extend(item.strip().split()[0] for item in attrs["srcset"].split(","))
        if tag == "link" and attrs.get("rel") == "canonical":
            self.canonicals.append(attrs.get("href"))
        if tag == "meta" and attrs.get("http-equiv", "").lower() == "refresh":
            self.refresh = True


def digest(data):
    return hashlib.sha256(data).hexdigest()


def deployment_bytes(name):
    data = (ROOT / name).read_bytes()
    # Git core.autocrlf=true checks out CRLF on Windows, but commits LF.
    if Path(name).suffix in (".html", ".css", ".svg", ".txt"):
        data = data.replace(b"\r\n", b"\n")
    return data


def page_file(path):
    return path.lstrip("/") + ("index.html" if path.endswith("/") else "")


def live_paths():
    paths = list(CONFIG["other_live_paths"])
    for prefix in ("/reel-nest/", "/reel-nest/terms/"):
        paths.extend(prefix + lang for lang in CONFIG["locales"])
    paths.extend(f"/reel-nest/archive/{date}/{lang}"
                 for date in CONFIG["privacy_archives"] for lang in CONFIG["locales"])
    paths.extend("/heavenlydemonreborn/" + path for path in CONFIG["game_paths"])
    return sorted(set(paths))


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT).decode("utf-8")


def fetch(path):
    url = urljoin(BASE, path)
    result = {"path": path, "url": url}
    try:
        with urlopen(Request(url, headers={"User-Agent": "FellowSurvivor-Pages-Preflight/1"}), timeout=20) as response:
            body = response.read()
            result.update(status=response.status, final_url=response.url,
                          content_type=response.headers.get_content_type(), sha256=digest(body))
        issues = []
        if result["status"] != 200 or result["final_url"] != url:
            issues.append("Expected HTTP 200 at the original URL, without redirect")
        if path.endswith("/"):
            text = body.decode("utf-8")
            doc = Document(text)
            title = re.search(r"<title>(.*?)</title>", text, re.S | re.I)
            result["title"] = title.group(1).strip() if title else ""
            if result["content_type"] != "text/html" or not result["title"] or doc.refresh:
                issues.append("Invalid HTML page or automatic redirect")
        if path.endswith("sitemap.xml"):
            root = ET.fromstring(body)
            result["sitemap_paths"] = [urlsplit(node.text).path for node in root.iter()
                                       if node.tag.endswith("}loc") and node.text]
        expected = CONFIG["protected_sha256"].get(path.lstrip("/"))
        if expected and result["sha256"] != expected:
            issues.append("Protected file bytes changed")
        if path == "/app-ads.txt" and result["content_type"] != "text/plain":
            issues.append("app-ads.txt must be served as text/plain")
        result["errors"] = issues
    except Exception as exc:
        result["errors"] = [str(exc)]
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--online", action="store_true", help="Check the existing 40 public URLs")
    parser.add_argument("--require-index", action="store_true", help="Require every deployment file staged or committed")
    parser.add_argument("--after-deploy", action="store_true", help="Also compare all live deployment files to local bytes")
    parser.add_argument("--compare", type=Path, help="Compare preserved live content to an earlier JSON report")
    parser.add_argument("--report", type=Path, help="Write a JSON report (use .preview/ to avoid publishing it)")
    args = parser.parse_args()
    if args.compare and not (args.online or args.after_deploy):
        parser.error("--compare requires --online or --after-deploy")
    errors, notes = [], []
    files = set(CONFIG["files"])
    live = set(live_paths())
    documents = {}
    for name in sorted(files):
        path = ROOT / name
        if not path.is_file() or path.is_symlink():
            errors.append(f"Missing file or symlink: {name}")
        elif name.endswith(".html"):
            documents[name] = Document(path.read_text(encoding="utf-8"))
        if path.is_file() and name in CONFIG["protected_sha256"]:
            if digest(deployment_bytes(name)) != CONFIG["protected_sha256"][name]:
                errors.append(f"Protected file changed: {name}")
    for prefix in CONFIG["reserved_prefixes"]:
        if (ROOT / prefix).exists() or (ROOT / (prefix + ".html")).exists():
            errors.append(f"Project-site path collision: /{prefix}/")
    for name in ("CNAME", "robots.txt", "404.html", "_config.yml"):
        if (ROOT / name).exists():
            errors.append(f"New routing/crawling configuration needs review: {name}")
    ref_count = 0
    for name in sorted(files):
        if not (ROOT / name).is_file():
            continue
        text = (ROOT / name).read_text(encoding="utf-8") if name.endswith((".html", ".css", ".svg")) else ""
        refs = documents[name].refs if name in documents else []
        refs = list(refs) + re.findall(r"url\(\s*['\"]?([^'\")]+)['\"]?\s*\)", text)
        for ref in refs:
            if ref.startswith(("mailto:", "tel:", "data:")):
                continue
            target = urlsplit(urljoin(BASE + name, ref))
            if target.netloc != urlsplit(BASE).netloc:
                continue
            ref_count += 1
            if any(target.path.startswith("/" + prefix + "/") for prefix in CONFIG["reserved_prefixes"]):
                if target.path not in live:
                    errors.append(f"Unregistered project-site link: {name} -> {ref}")
                continue
            dest = page_file(unquote(target.path))
            if dest not in files:
                errors.append(f"Link/asset absent from deployment list: {name} -> {ref}")
            elif target.fragment and dest in documents and unquote(target.fragment) not in documents[dest].ids:
                errors.append(f"Missing anchor: {name} -> {ref}")
    for route in CONFIG["pages"]:
        name = page_file(route)
        doc = documents.get(name)
        if doc is None:
            continue
        if doc.canonicals != [urljoin(BASE, route)] or doc.refresh:
            errors.append(f"Wrong canonical or automatic redirect: {route}")
    home = documents.get("index.html")
    if home and not set(CONFIG["home_fragments"]).issubset(home.ids):
        errors.append("A published homepage anchor was removed")
    detail = documents.get("products/reel-nest/index.html")
    if detail:
        for route in CONFIG["policy_links"]:
            if urljoin(BASE, route) not in detail.refs:
                errors.append(f"Missing Reel Nest policy link: {route}")
    for name in ("products/index.html", "products/reel-nest/index.html"):
        if name in documents and CONFIG["play_url"] not in documents[name].refs:
            errors.append(f"Missing Google Play download link: {name}")

    # Two bounded, serial Git reads; never fan out Git commands per file.
    indexed = set(filter(None, git("ls-files", "--cached", "-z").split("\0")))
    allowed = files | set(CONFIG["maintenance_files"])
    unknown = sorted(indexed - allowed)
    if unknown:
        errors.append("Unexpected indexed files (would be published): " + ", ".join(unknown))
    unstaged = set(filter(None, git("diff", "--name-only", "-z", "--", *sorted(allowed)).split("\0")))
    pending = sorted((allowed - indexed) | unstaged)
    if pending:
        message = f"{len(pending)} files need explicit staging before deployment"
        (errors if args.require_index else notes).append(message)

    results = []
    if args.online or args.after_deploy:
        targets = live | ({"/" + name for name in files} | set(CONFIG["pages"]) if args.after_deploy else set())
        with ThreadPoolExecutor(max_workers=4) as pool:
            results = list(pool.map(fetch, sorted(targets)))
        for row in results:
            errors.extend(f"{row['path']}: {issue}" for issue in row["errors"])
            for route in row.get("sitemap_paths", []):
                if route not in live:
                    errors.append(f"New sitemap route needs registration: {route}")
            if args.after_deploy:
                name = page_file(row["path"])
                if name in files and (ROOT / name).is_file() and row.get("sha256") != digest(deployment_bytes(name)):
                    errors.append(f"Live bytes differ from prepared file: {row['path']}")
        if args.compare:
            baseline = json.loads(args.compare.read_text(encoding="utf-8"))
            if baseline.get("status") != "PASS" or not baseline.get("live_results"):
                errors.append("Comparison baseline must be a successful online report")
            previous = {row["path"]: row for row in baseline["live_results"]}
            for row in results:
                if row["path"] in live - {"/"}:
                    before = previous.get(row["path"])
                    if not before or before.get("sha256") != row.get("sha256"):
                        errors.append(f"Preserved live content changed since baseline: {row['path']}")
    report = {
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "mode": "after-deploy" if args.after_deploy else "pre-deploy",
        "status": "PASS" if not errors else "FAIL",
        "deployment_file_count": len(files), "local_reference_count": ref_count,
        "live_url_count": len(results), "pending_index_files": pending,
        "errors": errors, "notes": notes, "live_results": results,
    }
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{report['status']}: {len(files)} deployment files, {ref_count} local references, {len(results)} live URLs")
    for line in notes:
        print("NOTE: " + line)
    for line in errors:
        print("ERROR: " + line)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
