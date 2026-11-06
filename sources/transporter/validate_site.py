"""Check public links, metadata, language pairs, leftover draft text, and generated-source consistency."""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.parse import urlsplit, unquote, parse_qs
import runpy
import xml.etree.ElementTree as ET

from build_site import ROOT, SOURCE, BASE, build

DRAFT_MARKERS = ("(초안)", "(Draft)", "게시 전 채울 것", "To fill in before publishing", "YYYY", "{{", "}}", "@철수")


class Document(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path, self.tags, self.links, self.ids = path, [], [], []
        self.feed(path.read_text(encoding="utf-8"))

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append((tag, attrs))
        if "id" in attrs:
            self.ids.append(attrs["id"])
        for name in ("href", "src"):
            if name in attrs:
                self.links.append(attrs[name])


def check():
    site = runpy.run_path(str(SOURCE / "content/site.py"))["SITE"]
    company = site["company"]
    pages = [(conf, p) for conf in site["langs"].values() for p in conf["pages"]]
    docs = {ROOT / conf["path"] / p["slug"] / "index.html": (conf, Document(ROOT / conf["path"] / p["slug"] / "index.html")) for conf, p in pages}
    not_found = ROOT / "404.html"
    checked_links = 0
    for path, (conf, doc) in list(docs.items()) + [(not_found, ({"html_lang": "ko"}, Document(not_found)))]:
        text = path.read_text(encoding="utf-8")
        for marker in DRAFT_MARKERS:
            assert marker not in text, f"Draft text {marker!r} left in {path}"
        assert len(doc.ids) == len(set(doc.ids)), f"Duplicate id: {path}"
        counts = Counter(tag for tag, _ in doc.tags)
        assert counts["h1"] == counts["title"] == 1, f"Heading/title: {path}"
        assert not counts["script"] and not counts["form"] and not counts["iframe"], f"Unexpected script, form or frame: {path}"
        assert any(tag == "html" and a.get("lang") == conf["html_lang"] for tag, a in doc.tags), f"Language: {path}"
        assert any(tag == "meta" and a.get("name") == "viewport" for tag, a in doc.tags)
        if path != not_found:
            rel = path.parent.relative_to(ROOT).as_posix()
            expected = BASE + ("" if rel == "." else rel + "/")
            assert any(tag == "link" and a.get("rel") == "canonical" and a.get("href") == expected for tag, a in doc.tags), f"Canonical: {path}"
            alternates = {a.get("hreflang"): a.get("href") for tag, a in doc.tags if tag == "link" and a.get("rel") == "alternate"}
            assert set(alternates) == {"ko", "en", "x-default"}, f"hreflang: {path}"
            assert company["registration"] in text and company["email"] in text, f"Operator details: {path}"
        for href in doc.links:
            parsed = urlsplit(href)
            if parsed.scheme == "mailto":
                assert parsed.path == company["email"], f"Unexpected mail address: {path}: {href}"
                continue
            if parsed.scheme or parsed.netloc:
                if not href.startswith(BASE):
                    assert parsed.scheme == "https", f"Insecure link: {href}"
                    continue
                target = ROOT / unquote(href[len(BASE):].split("#")[0].split("?")[0])
            else:
                target = path.parent / unquote(parsed.path) if parsed.path else path
            target = target.resolve()
            assert target.is_relative_to(ROOT), f"Link escapes site: {path}: {href}"
            if target.is_dir():
                target /= "index.html"
            assert target.is_file(), f"Missing link target: {path}: {href}"
            if parsed.fragment:
                assert target in docs and unquote(parsed.fragment) in docs[target][1].ids, f"Missing fragment: {href}"
            checked_links += 1
    support = docs[ROOT / "support/index.html"][1]
    action = next(link for link in support.links if link.startswith("mailto:") and "subject=" in link)
    assert parse_qs(urlsplit(action).query)["subject"] == ["[Transporter] 문의"]
    for conf, p in pages:
        if p["markdown"]:
            text = (ROOT / conf["path"] / p["slug"] / "index.html").read_text(encoding="utf-8")
            assert text.count("<h2 ") >= 8, f"Document looks truncated: {conf['path']}{p['slug']}"
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = ET.parse(ROOT / "sitemap.xml").findall("s:url/s:loc", ns)
    assert {node.text for node in urls} == {BASE + conf["path"] + (p["slug"] + "/" if p["slug"] else "") for conf, p in pages}
    with TemporaryDirectory(prefix="transporter-site-check-") as folder:
        generated = Path(folder)
        build(generated)
        for result in generated.rglob("*"):
            if result.is_file():
                existing = ROOT / result.relative_to(generated)
                assert existing.read_bytes() == result.read_bytes(), f"Rebuild required: {existing}"
    print(f"PASS: {len(docs) + 1} HTML documents, {checked_links} local links, hreflang, sitemap, support email, deterministic build.")


if __name__ == "__main__":
    check()
