"""Build the dependency-free Transporter policy site (Korean and English).

Sources: content/site.py (settings, home and support pages) and content/*.md (privacy policy, terms).
Writes the published pages to <repository root>/products/transporter/ (Korean) and .../en/ (English).
"""
from pathlib import Path
from html import escape
from urllib.parse import quote
import argparse
import re
import runpy

SOURCE = Path(__file__).resolve().parent
ROOT = SOURCE.parents[1] / "products" / "transporter"
BASE = "https://fellowsurvivor.com/products/transporter/"

LINK = re.compile(r"\[([^\]]+)\]\((https://[^)\s]+)\)|([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})")
LIST_ITEM = re.compile(r"(- |\d+\. )")
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


def long_date(iso, lang):
    year, month, day = (int(part) for part in iso.split("-"))
    return f"{year}년 {month}월 {day}일" if lang == "ko" else f"{MONTHS[month - 1]} {day}, {year}"


def inline(text):
    """Markdown inline text -> HTML: unescape, links [text](https://...) and bare email addresses."""
    text = re.sub(r"\\([\\\[\]*_`#>~|.-])", r"\1", text)
    out, last = [], 0
    for match in LINK.finditer(text):
        out.append(escape(text[last:match.start()], quote=False))
        if match.group(1):
            out.append(f'<a href="{escape(match.group(2))}">{escape(match.group(1), quote=False)}</a>')
        else:
            out.append(f'<a href="mailto:{match.group(3)}">{match.group(3)}</a>')
        last = match.end()
    out.append(escape(text[last:], quote=False))
    return "".join(out)


def cells(row):
    return [cell.strip() for cell in re.split(r"(?<!\\)\|", row.strip()[1:-1])]


def table(rows):
    head = "".join(f'<th scope="col">{inline(cell)}</th>' for cell in cells(rows[0]))
    body = "".join("<tr>" + "".join(f"<td>{inline(cell)}</td>" for cell in cells(row)) + "</tr>" for row in rows[2:])
    return f'<div class="table-wrap"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


def blocks(lines):
    """The Markdown subset the document export uses: ### headings, paragraphs, - and 1. lists, pipe tables."""
    html, i = [], 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
        elif line.startswith("### "):
            html.append(f"<h3>{inline(line[4:].strip())}</h3>")
            i += 1
        elif line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append(lines[i])
                i += 1
            html.append(table(rows))
        elif LIST_ITEM.match(line):
            tag = "ol" if line[0].isdigit() else "ul"
            items = []
            while i < len(lines) and LIST_ITEM.match(lines[i]):
                items.append(LIST_ITEM.sub("", lines[i], count=1))
                i += 1
            html.append(f"<{tag}>" + "".join(f"<li>{inline(item)}</li>" for item in items) + f"</{tag}>")
        else:
            paragraph = []
            while i < len(lines) and lines[i].strip() and not re.match(r"(#|\|)", lines[i]) and not LIST_ITEM.match(lines[i]):
                paragraph.append(lines[i].strip())
                i += 1
            html.append(f"<p>{inline(' '.join(paragraph))}</p>")
    return "".join(html)


def markdown_sections(text, intro):
    """Split on '## ' headings. Text before the first heading becomes a section titled `intro`."""
    sections, title, lines = [], intro, []
    for line in text.splitlines():
        if line.startswith("## "):
            if any(part.strip() for part in lines):
                sections.append({"title": title, "body": blocks(lines)})
            title, lines = line[3:].strip(), []
        else:
            lines.append(line)
    sections.append({"title": title, "body": blocks(lines)})
    return sections


def business(company, lang):
    email = f'<a href="mailto:{company["email"]}">{company["email"]}</a>'
    if lang == "ko":
        return (f'<strong>{escape(company["name"])}</strong> · 대표 {escape(company["representative"])}<br>'
                f'사업자등록번호 {escape(company["registration"])}<br>{escape(company["address"])}<br>{email}')
    return (f'<strong>{escape(company["name_en"])}</strong> ({escape(company["name"])}) · Representative {escape(company["representative"])}<br>'
            f'Business registration number {escape(company["registration"])} (Republic of Korea)<br>{escape(company["address_en"])}<br>{email}')


def build(out):
    site = runpy.run_path(str(SOURCE / "content/site.py"))["SITE"]
    company, langs, published = site["company"], site["langs"], site["published"]
    version = site["versions"][-1][0]
    out.mkdir(parents=True, exist_ok=True)
    count = 0
    for lang, conf in langs.items():
        pages, other = conf["pages"], langs[conf["other"]]
        for page in pages:
            depth = (1 if conf["path"] else 0) + (1 if page["slug"] else 0)
            home = "../" * depth or "./"
            slug_path = page["slug"] + "/" if page["slug"] else ""
            href = lambda slug: home + conf["path"] + (slug + "/" if slug else "")
            nav = "".join(f'<a href="{href(p["slug"])}"' + (' aria-current="page"' if p is page else "") + f'>{escape(p["nav"])}</a>' for p in pages)
            sections = page["sections"]
            if page["markdown"]:
                text = (SOURCE / "content" / page["markdown"]).read_text(encoding="utf-8")
                text = text.replace("{{DATE}}", long_date(published, lang)).replace("{{ISO}}", published)
                sections = markdown_sections(text, page["intro"])
            toc = "".join(f'<li><a href="#section-{i}">{escape(s["title"])}</a></li>' for i, s in enumerate(sections, 1))
            body = "".join(f'<section aria-labelledby="section-{i}"><h2 id="section-{i}">{escape(s["title"])}</h2>{s["body"]}</section>' for i, s in enumerate(sections, 1))
            replacements = {
                "{{BUSINESS}}": f"<p>{business(company, lang)}</p>",
                "{{HOME}}": home,
                "{{EMAIL}}": company["email"],
                "{{SUPPORT_MAIL}}": "mailto:" + company["email"] + "?subject=" + quote(conf["support_subject"]),
            }
            for key, value in replacements.items():
                body = body.replace(key, value)
            url = BASE + conf["path"] + slug_path
            ko_url, en_url = BASE + slug_path, BASE + "en/" + slug_path
            switch_href = home + other["path"] + slug_path
            html = f'''<!doctype html>
<html lang="{conf["html_lang"]}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light"><title>{escape(page["title"])} | Transporter</title>
<meta name="description" content="{escape(page["description"], quote=True)}"><meta name="theme-color" content="#16343b">
<link rel="canonical" href="{url}"><link rel="alternate" hreflang="ko" href="{ko_url}"><link rel="alternate" hreflang="en" href="{en_url}"><link rel="alternate" hreflang="x-default" href="{en_url}">
<meta property="og:type" content="website"><meta property="og:locale" content="{conf["og_locale"]}"><meta property="og:title" content="Transporter · {escape(page["title"], quote=True)}"><meta property="og:description" content="{escape(page["description"], quote=True)}"><meta property="og:url" content="{url}">
<link rel="icon" href="{home}favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="{home}styles.css"></head>
<body id="top"><a class="skip-link" href="#main">{escape(conf["skip"])}</a>
<header class="site-header"><a class="brand" href="{href("")}" aria-label="{escape(conf["home_label"], quote=True)}"><span class="brand-mark" aria-hidden="true">T</span><span><strong>{escape(conf["site_name"])}</strong><small>{escape(conf["brand_sub"])}</small></span></a><a class="lang-switch" href="{switch_href}" hreflang="{conf["switch_lang"]}" lang="{conf["switch_lang"]}">{escape(conf["switch"])}</a></header>
<nav class="site-nav" aria-label="{escape(conf["menu"], quote=True)}">{nav}</nav>
<div class="page-shell"><aside class="toc" aria-label="{escape(conf["toc_label"], quote=True)}"><span>{escape(conf["toc"])}</span><ol>{toc}</ol><a class="toc-help" href="{href("support")}">{escape(conf["help"])}</a></aside>
<main id="main" class="policy-card"><div class="document-heading"><p class="eyebrow">{escape(conf["eyebrow"])}</p><h1>{escape(page["title"])}</h1><p class="document-summary">{escape(page["description"])}</p><p class="effective"><span>{escape(conf["published"])}</span> <time datetime="{published}">{long_date(published, lang)}</time><span>{escape(conf["version"])}</span> {version}</p></div>
<div class="release-notice"><strong>{escape(conf["notice_title"])}</strong><p>{escape(conf["notice"])}</p></div>
<details class="mobile-toc"><summary>{escape(conf["open_toc"])}</summary><ol>{toc}</ol></details>
<div class="document-body">{body}</div><a class="back-to-top" href="#top">{escape(conf["top"])}</a></main></div>
<footer class="site-footer"><div>{business(company, lang)}</div><p><a href="{href("privacy")}">{escape(pages[1]["nav"])}</a> · <a href="{href("terms")}">{escape(pages[2]["nav"])}</a> · <a href="{href("support")}">{escape(pages[3]["nav"])}</a></p><p>© 2026 Fellow Survivor Studio. Transporter.</p></footer></body></html>'''
            target = out / conf["path"] / page["slug"] / "index.html"
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(html + "\n", encoding="utf-8", newline="\n")
            count += 1
    (out / ".nojekyll").write_text("", encoding="utf-8", newline="\n")
    (out / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n", encoding="utf-8", newline="\n")
    urls = "".join(f'<url><loc>{BASE}{conf["path"]}{p["slug"] + "/" if p["slug"] else ""}</loc><lastmod>{published}</lastmod></url>'
                   for conf in langs.values() for p in conf["pages"])
    (out / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n', encoding="utf-8", newline="\n")
    ko, en = langs["ko"], langs["en"]
    (out / "404.html").write_text(
        f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex">'
        f'<title>페이지를 찾을 수 없습니다 | Transporter</title><link rel="stylesheet" href="{BASE}styles.css"></head><body><main class="not-found"><p class="eyebrow">404</p>'
        f'<h1>{ko["not_found_title"]}</h1><p>{ko["not_found_body"]}</p><a class="button" href="{BASE}">{ko["not_found_home"]}</a>'
        f'<p lang="en">{en["not_found_title"]} {en["not_found_body"]} <a href="{BASE}en/">{en["not_found_home"]}</a></p></main></body></html>\n',
        encoding="utf-8", newline="\n")
    print(f"Built {count} pages plus 404, sitemap and robots.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT)
    build(parser.parse_args().output.resolve())
