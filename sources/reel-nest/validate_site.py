"""Check the generated Reel Nest policy pages: every text has its page, metadata and links are
right, the sitemap lists the current pages, and the committed pages equal a fresh build.

Run from anywhere: python -X utf8 sources/reel-nest/validate_site.py
"""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET

from build_site import (ARCHIVE_LABELS, BASE_URL, CONTENT, DATED_DOCS, DOCUMENTS, EXTRA_SITEMAP_PATHS, LANGUAGES,
                        OUT, archived_versions, build, output_path, period_text, periods, revisions)


class Document(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.tags, self.links, self.ids = [], [], []
        self.feed(path.read_text(encoding="utf-8"))

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append((tag, attrs))
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag in ("a", "link") and "href" in attrs:
            self.links.append(attrs["href"])


def expected_pages():
    """{path below products/reel-nest/: (doc, lang, kind, date)} with kind 'current' (date None),
    'archive' (previous version effective `date`) or 'revision' (revision page of `date`)."""
    pages = {}
    for doc, info in DOCUMENTS.items():
        for lang in LANGUAGES:
            assert (CONTENT / f"{info['source']}_{lang}.txt").is_file(), f"Missing text: {info['source']}_{lang}.txt"
            pages[output_path(doc, lang)] = (doc, lang, "current", None)
        for date, langs in archived_versions(doc).items():
            assert "ko" in langs, f"Previous version {date} of {doc} has no Korean text"
            for lang in langs:
                pages[output_path(doc, lang, date)] = (doc, lang, "archive", date)
        for date, pairs in revisions(doc).items():
            for lang in pairs:
                pages[output_path(doc, lang, revision=date)] = (doc, lang, "revision", date)
    return pages


def check():
    pages = expected_pages()
    generated = {p.parent.relative_to(OUT).as_posix() + "/"
                 for info in DOCUMENTS.values() for p in (OUT / info["prefix"]).rglob("index.html")}
    assert generated == set(pages), f"Pages differ from the texts: extra {sorted(generated - set(pages))}, missing {sorted(set(pages) - generated)}"
    docs = {path: Document(OUT / path / "index.html") for path in pages}
    checked_links = 0
    for path, (doc_name, lang, kind, when) in pages.items():
        doc, file = docs[path], OUT / path / "index.html"
        counts = Counter(tag for tag, _ in doc.tags)
        assert counts["h1"] == counts["title"] == 1, f"Heading/title: {file}"
        assert not (counts["script"] or counts["form"] or counts["iframe"]), f"Unexpected script, form or frame: {file}"
        assert len(doc.ids) == len(set(doc.ids)), f"Duplicate id: {file}"
        html_lang = next(a.get("lang") for tag, a in doc.tags if tag == "html")
        assert html_lang == LANGUAGES[lang]["html_lang"], f"Page language: {file}"
        canonical = [a.get("href") for tag, a in doc.tags if tag == "link" and a.get("rel") == "canonical"]
        assert canonical == [BASE_URL + path], f"Canonical: {file} -> {canonical}"
        robots = next(a.get("content") for tag, a in doc.tags if tag == "meta" and a.get("name") == "robots")
        assert robots == ("index, follow" if kind == "current" else "noindex, follow"), f"Robots: {file}"
        classes = {a.get("class") for _, a in doc.tags}
        if kind == "revision":
            assert {"reason", "changes", "full-text"} <= set(doc.ids) and "changes" in classes, f"Revision page parts: {file}"
            assert counts["tr"] >= 2, f"Empty comparison table: {file}"
        if doc_name in DATED_DOCS:
            # Dated documents carry each version's period of application and no wording that turns
            # wrong on a date ("current", "previous version").
            text = file.read_text(encoding="utf-8")
            start = when if kind != "current" else max(periods(doc_name))
            assert period_text(lang, start, periods(doc_name)[start]) in text, f"Period of application missing: {file}"
            assert "archive-notice" not in classes and ARCHIVE_LABELS[lang]["notice"] not in text, \
                f"Dated document labelled as previous version: {file}"
        for href in doc.links:
            parsed = urlsplit(href)
            if parsed.scheme == "data":
                continue
            if parsed.scheme or parsed.netloc:
                assert parsed.scheme == "https", f"Insecure link: {file}: {href}"
                if not href.startswith(BASE_URL):
                    continue  # external link written in the policy text
                target = OUT / unquote(parsed.path[len(urlsplit(BASE_URL).path):])
            else:
                target = (file.parent / unquote(parsed.path)) if parsed.path else file
            target = target.resolve()
            assert target.is_relative_to(OUT.resolve()), f"Link leaves products/reel-nest/: {file}: {href}"
            if target.is_dir():
                target /= "index.html"
            assert target.is_file(), f"Missing link target: {file}: {href}"
            if parsed.fragment:
                rel = target.parent.relative_to(OUT.resolve()).as_posix() + "/"
                assert rel in docs and unquote(parsed.fragment) in docs[rel].ids, f"Missing anchor: {file}: {href}"
            checked_links += 1
    assert (OUT / "policy.css").is_file() and (OUT / "index.html").is_file()
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    listed = [node.text for node in ET.parse(OUT / "sitemap.xml").findall("s:url/s:loc", ns)]
    current = [path for path, (_, _, kind, _) in pages.items() if kind == "current"]
    assert sorted(listed) == sorted(BASE_URL + p for p in EXTRA_SITEMAP_PATHS + current), "Sitemap differs from the current pages"
    with TemporaryDirectory(prefix="reel-nest-site-check-") as folder:
        fresh = Path(folder)
        build(fresh)
        for result in fresh.rglob("*"):
            if result.is_file():
                existing = OUT / result.relative_to(fresh)
                assert existing.is_file() and existing.read_bytes() == result.read_bytes(), f"Rebuild required: {existing}"
    kinds = Counter(kind for _, _, kind, _ in pages.values())
    print(f"PASS: {kinds['current']} current pages, {kinds['archive']} previous-version pages, "
          f"{kinds['revision']} revision pages, {checked_links} links, sitemap, rebuild matches.")


if __name__ == "__main__":
    check()
