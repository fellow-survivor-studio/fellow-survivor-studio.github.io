"""Check public links, metadata, mail actions, and generated-source consistency."""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.parse import urlsplit, unquote, parse_qs
import runpy
import xml.etree.ElementTree as ET

from build_site import ROOT, SOURCE, BASE, build


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
    pages = runpy.run_path(str(SOURCE / "content/site.py"))["SITE"]["pages"]
    docs = {ROOT / p["slug"] / "index.html": Document(ROOT / p["slug"] / "index.html") for p in pages}
    docs[ROOT / "404.html"] = Document(ROOT / "404.html")
    checked_links = 0
    for path, doc in docs.items():
        text = path.read_text(encoding="utf-8")
        assert "{{" not in text, f"Unresolved placeholder: {path}"
        assert len(doc.ids) == len(set(doc.ids)), f"Duplicate id: {path}"
        counts = Counter(tag for tag, _ in doc.tags)
        assert counts["h1"] == counts["title"] == 1, f"Heading/title: {path}"
        assert not counts["script"] and not counts["form"], f"Unexpected tracking or form: {path}"
        assert any(tag == "html" and a.get("lang") == "ko" for tag, a in doc.tags)
        assert any(tag == "meta" and a.get("name") == "viewport" for tag, a in doc.tags)
        if path.name != "404.html":
            expected = BASE + path.parent.relative_to(ROOT).as_posix().replace(".", "")
            expected = expected.rstrip("/") + "/"
            assert any(tag == "link" and a.get("rel") == "canonical" and a.get("href") == expected for tag, a in doc.tags)
            assert "773-26-02197" in text and "010-2530-1902" in text
        for href in doc.links:
            parsed = urlsplit(href)
            if parsed.scheme in {"mailto", "tel"}:
                continue
            if parsed.scheme or parsed.netloc:
                if not href.startswith(BASE):
                    assert parsed.scheme == "https", f"Insecure link: {href}"
                    continue
                rel = href[len(BASE):].split("#")[0].split("?")[0]
                target = ROOT / unquote(rel)
            else:
                target = path.parent / unquote(parsed.path) if parsed.path else path
            target = target.resolve()
            assert target.is_relative_to(ROOT), f"Link escapes site: {path}: {href}"
            if target.is_dir():
                target /= "index.html"
            assert target.is_file(), f"Missing link target: {path}: {href}"
            if parsed.fragment:
                assert target in docs and unquote(parsed.fragment) in docs[target].ids, f"Missing fragment: {href}"
            checked_links += 1
    delete_doc = docs[ROOT / "delete-account/index.html"]
    action = next(link for link in delete_doc.links if link.startswith("mailto:") and "body=" in link)
    params = parse_qs(urlsplit(action).query)
    assert params["subject"] == ["[환생천마] 계정 및 개인정보 삭제 요청"]
    assert "게임 UID(확인 가능한 경우)" in params["body"][0]
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = ET.parse(ROOT / "sitemap.xml").findall("s:url/s:loc", ns)
    assert {node.text for node in urls} == {BASE + p["slug"] + ("/" if p["slug"] else "") for p in pages}
    with TemporaryDirectory(prefix="cheonma-site-check-") as folder:
        generated = Path(folder)
        build(generated)
        for result in generated.rglob("*"):
            if result.is_file():
                existing = ROOT / result.relative_to(generated)
                assert existing.read_bytes() == result.read_bytes(), f"Rebuild required: {existing}"
    print(f"PASS: {len(docs)} HTML documents, {checked_links} local links, sitemap, deletion email, deterministic build.")


if __name__ == "__main__":
    check()
