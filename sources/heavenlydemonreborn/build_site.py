"""Build the dependency-free Korean policy site. Source: content/site.py.

Writes the published pages to <repository root>/heavenlydemonreborn/.
"""
from pathlib import Path
from html import escape
from urllib.parse import quote
import argparse
import runpy

SOURCE = Path(__file__).resolve().parent
ROOT = SOURCE.parents[1] / "heavenlydemonreborn"
BASE = "https://fellowsurvivor.com/heavenlydemonreborn/"


def build(out):
    site = runpy.run_path(str(SOURCE / "content/site.py"))["SITE"]
    pages, company = site["pages"], site["company"]
    out.mkdir(parents=True, exist_ok=True)
    for page in pages:
        prefix = "../" if page["slug"] else "./"
        href = lambda slug: prefix + (slug + "/" if slug else "")
        nav = "".join(f'<a href="{href(p["slug"])}"' + (' aria-current="page"' if p == page else '') + f'>{escape(p["nav"])}</a>' for p in pages)
        toc = "".join(f'<li><a href="#section-{i}">{escape(s["title"])}</a></li>' for i, s in enumerate(page["sections"], 1))
        sections = "".join(f'<section aria-labelledby="section-{i}"><h2 id="section-{i}">{escape(s["title"])}</h2>{s["body"]}</section>' for i, s in enumerate(page["sections"], 1))
        replacements = {"{{ROOT}}": prefix, "{{EMAIL}}": company["email"], "{{DELETE_MAIL}}": "mailto:" + company["email"] + "?subject=" + quote("[환생천마] 계정 및 개인정보 삭제 요청") + "&amp;body=" + quote("환생천마 계정 및 관련 개인정보 삭제를 요청합니다.\n\n게임 UID(확인 가능한 경우):\n연결한 Google 계정 이메일:\n삭제 요청 범위: 게임 계정 및 관련 개인정보\n\n비밀번호, 인증번호, 신분증, 카드번호는 보내지 않습니다."), "{{SUPPORT_MAIL}}": "mailto:" + company["email"] + "?subject=" + quote("[환생천마] 고객지원 문의")}
        for key, value in replacements.items():
            sections = sections.replace(key, value)
        business = f'<strong>{escape(company["name"])}</strong> · 대표 {escape(company["representative"])}<br>사업자등록번호 {escape(company["registration"])} · 통신판매업 신고: 발급 대기 중<br>{escape(company["address"])}<br><a href="tel:+821025301902">010-2530-1902</a> · <a href="mailto:{company["email"]}">{company["email"]}</a>'
        url = BASE + (page["slug"] + "/" if page["slug"] else "")
        html = f'''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light"><title>{escape(page["title"])} | 환생천마</title>
<meta name="description" content="{escape(page['description'], quote=True)}"><meta name="theme-color" content="#231c28">
<link rel="canonical" href="{url}"><meta property="og:type" content="website"><meta property="og:locale" content="ko_KR"><meta property="og:title" content="환생천마 · {escape(page['title'], quote=True)}"><meta property="og:description" content="{escape(page['description'], quote=True)}"><meta property="og:url" content="{url}">
<link rel="icon" href="{prefix}favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="{prefix}styles.css"></head>
<body id="top"><a class="skip-link" href="#main">본문으로 건너뛰기</a>
<header class="site-header"><a class="brand" href="{prefix}" aria-label="환생천마 정책 및 고객지원 홈"><span class="brand-mark" aria-hidden="true">天</span><span><strong>환생천마</strong><small>정책 및 고객지원</small></span></a><span class="header-label">FELLOW SURVIVOR STUDIO</span></header>
<nav class="site-nav" aria-label="문서 메뉴">{nav}</nav>
<div class="page-shell"><aside class="toc" aria-label="문서 목차"><span>이 페이지에서</span><ol>{toc}</ol><a class="toc-help" href="{href('support')}">도움이 필요하신가요? →</a></aside>
<main id="main" class="policy-card"><div class="document-heading"><p class="eyebrow">HEAVENLY DEMON REBORN · 한국 서비스</p><h1>{escape(page['title'])}</h1><p class="document-summary">{escape(page['description'])}</p><p class="effective"><span>게시일</span> <time datetime="{site['published']}">2026년 10월 15일</time><span>문서 버전</span> 1.0</p></div>
<div class="release-notice"><strong>출시 준비 안내</strong><p>게임은 출시 준비 중이며 15세 이용가를 목표로 합니다. 실제 이용등급과 서비스 개시일은 확정 후 안내합니다. 게임 관련 문서는 서비스 개시 전에 최종 운영 내용에 맞춰 갱신하며, 이 웹사이트의 문의·개인정보 요청 안내는 지금 이용할 수 있습니다.</p></div>
<details class="mobile-toc"><summary>문서 목차 열기</summary><ol>{toc}</ol></details>
<div class="document-body">{sections}</div><a class="back-to-top" href="#top">맨 위로 ↑</a></main></div>
<footer class="site-footer"><div>{business}</div><p><a href="{href('privacy')}">개인정보처리방침</a> · <a href="{href('terms')}">이용약관</a> · <a href="{href('delete-account')}">계정 삭제 요청</a> · <a href="{href('notices')}">공지 및 변경 이력</a></p><p>© 2026 Fellow Survivor Studio. 환생천마.</p></footer></body></html>'''
        target = out / page["slug"] / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(html + "\n", encoding="utf-8", newline="\n")
    (out / ".nojekyll").write_text("", encoding="utf-8", newline="\n")
    (out / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n", encoding="utf-8", newline="\n")
    urls = "".join(f'<url><loc>{BASE}{p["slug"] + "/" if p["slug"] else ""}</loc><lastmod>{site["published"]}</lastmod></url>' for p in pages)
    (out / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n', encoding="utf-8", newline="\n")
    (out / "404.html").write_text(f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>페이지를 찾을 수 없습니다 | 환생천마</title><link rel="stylesheet" href="{BASE}styles.css"></head><body><main class="not-found"><p class="eyebrow">404</p><h1>페이지를 찾을 수 없습니다.</h1><p>주소가 변경되었거나 존재하지 않는 페이지입니다.</p><a class="button" href="{BASE}">정책 및 고객지원 홈으로</a></main></body></html>\n', encoding="utf-8", newline="\n")
    print(f"Built {len(pages)} pages plus 404, sitemap and robots.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT)
    build(parser.parse_args().output.resolve())
