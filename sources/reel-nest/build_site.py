"""Build the Reel Nest privacy policy and terms of use pages.

Sources: content/*.txt (current texts, same as the app's assets/legal files) and
content/archive/*.txt (previous versions). Writes products/reel-nest/privacy/,
products/reel-nest/terms/ and products/reel-nest/sitemap.xml in this repository.
products/reel-nest/index.html (the product page) and products/reel-nest/policy.css
are maintained by hand and left untouched.

Run from anywhere: python -X utf8 sources/reel-nest/build_site.py
"""
from __future__ import annotations

import argparse
import difflib
import html
import re
import shutil
from datetime import date, timedelta
from pathlib import Path


SOURCE = Path(__file__).resolve().parent
CONTENT = SOURCE / "content"
OUT = SOURCE.parents[1] / "products" / "reel-nest"

LANGUAGES = {
    "ko": {"name": "한국어", "html_lang": "ko"},
    "en": {"name": "English", "html_lang": "en"},
    "ja": {"name": "日本語", "html_lang": "ja"},
    "zh": {"name": "中文", "html_lang": "zh-CN"},
    "es": {"name": "Español", "html_lang": "es"},
    "pt": {"name": "Português", "html_lang": "pt-BR"},
}

# Each document is published under its own path prefix below /products/reel-nest/.
# Korean is served at the prefix itself, other languages below it. The earlier
# addresses (fellowsurvivor.com/reel-nest/... and github.io/reel-nest/..., used by
# app versions before 1.3.0) are forwarded here permanently by the _redirects rules
# in scripts/cloudflare-build.sh.
DOCUMENTS = {
    "privacy": {"source": "privacy_policy", "prefix": "privacy/"},
    "terms": {"source": "terms_of_use", "prefix": "terms/"},
}

DESCRIPTIONS = {
    "privacy": {
        "ko": "Reel Nest 개인정보처리방침",
        "en": "Reel Nest Privacy Policy",
        "ja": "Reel Nest プライバシーポリシー",
        "zh": "Reel Nest 隐私政策",
        "es": "Política de privacidad de Reel Nest",
        "pt": "Política de Privacidade do Reel Nest",
    },
    "terms": {
        "ko": "Reel Nest 이용약관",
        "en": "Reel Nest Terms of Use",
        "ja": "Reel Nest 利用規約",
        "zh": "Reel Nest 使用条款",
        "es": "Términos de Uso de Reel Nest",
        "pt": "Termos de Uso do Reel Nest",
    },
}

LABELS = {
    "ko": {"privacy": "개인정보 보호", "terms": "이용약관", "privacy_link": "개인정보처리방침", "language": "언어", "toc": "목차", "top": "맨 위로", "updated": "시행일", "skip": "본문으로 건너뛰기"},
    "en": {"privacy": "Privacy", "terms": "Terms", "privacy_link": "Privacy Policy", "language": "Language", "toc": "Contents", "top": "Back to top", "updated": "Effective date", "skip": "Skip to content"},
    "ja": {"privacy": "プライバシー", "terms": "利用規約", "privacy_link": "プライバシーポリシー", "language": "言語", "toc": "目次", "top": "ページ上部へ", "updated": "施行日", "skip": "本文へ移動"},
    "zh": {"privacy": "隐私", "terms": "使用条款", "privacy_link": "隐私政策", "language": "语言", "toc": "目录", "top": "返回顶部", "updated": "生效日期", "skip": "跳到正文"},
    "es": {"privacy": "Privacidad", "terms": "Términos", "privacy_link": "Política de privacidad", "language": "Idioma", "toc": "Contenido", "top": "Volver arriba", "updated": "Fecha de vigencia", "skip": "Saltar al contenido"},
    "pt": {"privacy": "Privacidade", "terms": "Termos", "privacy_link": "Política de Privacidade", "language": "Idioma", "toc": "Conteúdo", "top": "Voltar ao topo", "updated": "Data de vigência", "skip": "Ir para o conteúdo"},
}
TERMS_LINK = {"ko": "이용약관", "en": "Terms of Use", "ja": "利用規約", "zh": "使用条款", "es": "Términos de uso", "pt": "Termos de Uso"}
# Previous versions stay published (the privacy policy promises that the pre-change
# text can be viewed on the same site). Put a replaced text in content/archive/ as
# <source>_<lang>_<YYYY-MM-DD of its effective date>.txt before overwriting content/.
ARCHIVE_LABELS = {
    "ko": {"previous": "이전 버전", "notice": "이 문서는 이전 버전입니다.", "current": "현재 버전 보기"},
    "en": {"previous": "Previous versions", "notice": "This is a previous version of this document.", "current": "View the current version"},
    "ja": {"previous": "以前の版", "notice": "この文書は以前の版です。", "current": "現行版を見る"},
    "zh": {"previous": "历史版本", "notice": "本文件为历史版本。", "current": "查看当前版本"},
    "es": {"previous": "Versiones anteriores", "notice": "Esta es una versión anterior de este documento.", "current": "Ver la versión vigente"},
    "pt": {"previous": "Versões anteriores", "notice": "Esta é uma versão anterior deste documento.", "current": "Ver a versão vigente"},
}
ARCHIVE = CONTENT / "archive"
ARCHIVE_NAME_RE = re.compile(r"^(?P<source>[a-z_]+)_(?P<lang>[a-z]{2})_(?P<date>\d{4}-\d{2}-\d{2})\.txt$")
# A revised text announced before its effective date goes in content/upcoming/ (same naming,
# date = its future effective date) while content/<source>_<lang>.txt keeps the text in force.
# On the effective date, archive the text in force and move the upcoming one into content/.
UPCOMING = CONTENT / "upcoming"
# Reason for each revision, shown on its revision page: content/revisions/<source>_<lang>_<date>.txt
REVISIONS = CONTENT / "revisions"
# Revision pages (<prefix>revision/<date>/: reason, before/after comparison, full revised text)
# for revisions effective on or after these dates. Terms of use Article 3(2), from the
# 2026-11-14 revision, promises the reason, the full text and the comparison on the web page.
REVISION_PAGES_SINCE = {"terms": "2026-11-14"}
REVISION_LABELS = {
    "ko": {"in_force_until": "이 문서는 {end}까지 적용되는 현행 버전입니다. {date}부터 개정 버전이 시행됩니다.",
           "see_revision": "개정 버전과 변경 전후 비교 보기", "pending": "이 문서는 {date}부터 시행될 예정인 개정 버전입니다. 그 전까지는 현행 버전이 적용됩니다.",
           "in_force_from": "이 개정 버전은 {date}부터 시행되었습니다.", "revisions": "개정 안내", "page_title": "{title} 개정 안내",
           "reason": "변경 사유", "changes": "변경 전후 비교", "changes_intro": "{before} 시행 버전과 비교해 바뀐 문단만 보여 줍니다.",
           "section": "조항", "before": "변경 전 ({date} 시행)", "after": "변경 후 ({date} 시행)", "none": "(없음)",
           "full_text": "개정 버전 전문", "header": "머리말"},
    "en": {"in_force_until": "This is the version in force until {end}. A revised version takes effect on {date}.",
           "see_revision": "View the revised version and the comparison", "pending": "This revised version takes effect on {date}. Until then, the current version applies.",
           "in_force_from": "This revised version took effect on {date}.", "revisions": "Revisions", "page_title": "{title}: revision",
           "reason": "Reason for the change", "changes": "Comparison of changes", "changes_intro": "Only the paragraphs that differ from the version effective {before} are shown.",
           "section": "Section", "before": "Before (effective {date})", "after": "After (effective {date})", "none": "(none)",
           "full_text": "Full text of the revised version", "header": "Heading"},
    "ja": {"in_force_until": "この文書は{end}まで適用される現行版です。{date}から改定版が施行されます。",
           "see_revision": "改定版と変更前後の比較を見る", "pending": "この文書は{date}から施行予定の改定版です。それまでは現行版が適用されます。",
           "in_force_from": "この改定版は{date}から施行されました。", "revisions": "改定のお知らせ", "page_title": "{title} 改定のお知らせ",
           "reason": "変更の理由", "changes": "変更前後の比較", "changes_intro": "{before}施行版と比べて変更された段落のみを表示します。",
           "section": "条項", "before": "変更前（{date}施行）", "after": "変更後（{date}施行）", "none": "（なし）",
           "full_text": "改定版の全文", "header": "冒頭"},
    "zh": {"in_force_until": "本文件为适用至{end}的现行版本。修订版本将于{date}起生效。",
           "see_revision": "查看修订版本及修改前后对照", "pending": "本文件为将于{date}起生效的修订版本。在此之前适用现行版本。",
           "in_force_from": "本修订版本已于{date}起生效。", "revisions": "修订说明", "page_title": "{title} 修订说明",
           "reason": "修改理由", "changes": "修改前后对照", "changes_intro": "仅显示与{before}生效版本相比有修改的段落。",
           "section": "条款", "before": "修改前（{date}生效）", "after": "修改后（{date}生效）", "none": "（无）",
           "full_text": "修订版本全文", "header": "开头"},
    "es": {"in_force_until": "Esta es la versión vigente hasta el {end}. Una versión revisada entra en vigor el {date}.",
           "see_revision": "Ver la versión revisada y la comparación", "pending": "Esta versión revisada entra en vigor el {date}. Hasta entonces se aplica la versión vigente.",
           "in_force_from": "Esta versión revisada entró en vigor el {date}.", "revisions": "Revisiones", "page_title": "{title}: revisión",
           "reason": "Motivo del cambio", "changes": "Comparación de cambios", "changes_intro": "Solo se muestran los párrafos que difieren de la versión vigente desde el {before}.",
           "section": "Sección", "before": "Antes (vigente desde el {date})", "after": "Después (vigente desde el {date})", "none": "(ninguno)",
           "full_text": "Texto completo de la versión revisada", "header": "Encabezado"},
    "pt": {"in_force_until": "Esta é a versão em vigor até {end}. Uma versão revisada entra em vigor em {date}.",
           "see_revision": "Ver a versão revisada e a comparação", "pending": "Esta versão revisada entra em vigor em {date}. Até lá, aplica-se a versão em vigor.",
           "in_force_from": "Esta versão revisada entrou em vigor em {date}.", "revisions": "Revisões", "page_title": "{title}: revisão",
           "reason": "Motivo da alteração", "changes": "Comparação das alterações", "changes_intro": "Apenas os parágrafos que diferem da versão em vigor desde {before} são mostrados.",
           "section": "Seção", "before": "Antes (em vigor desde {date})", "after": "Depois (em vigor desde {date})", "none": "(nenhum)",
           "full_text": "Texto completo da versão revisada", "header": "Cabeçalho"},
}
EN_MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
ES_MONTHS = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
PT_MONTHS = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
KO_DATE_RE = re.compile(r"(\d{4})년\s*(\d{1,2})월\s*(\d{1,2})일")

BASE_URL = "https://fellowsurvivor.com/products/reel-nest/"
# Hand-authored pages (not generated from content/*.txt) that should still appear in
# the sitemap: the product page products/reel-nest/index.html.
EXTRA_SITEMAP_PATHS = [""]
URL_RE = re.compile(r"^https://[^\s]+$")
# Privacy policy: numbered sections ("1. ...") with lettered subsections ("A." / "가.")
PRIVACY_SECTION_RE = re.compile(r"^(\d+)\.\s+(.+)$")
PRIVACY_SUBSECTION_RE = re.compile(r"^(?:[AB]|[가나다라마바사아자차카타파하])\.\s*(.+)$")
# Terms of use: article headings in every language ("제5조의2 (…)", "Article 5-2 (…)", "第5条の2（…）", …)
TERMS_SECTION_RE = re.compile(
    r"^(?:제\d+조(?:의\d+)?\s*\(.+\)|Article \d+(?:-\d+)? \(.+\)|第\d+条(?:[の之]\d+)?[（(].+[)）]"
    r"|Artículo \d+(?:-\d+)? \(.+\)|Artigo \d+(?:-\d+)? \(.+\)|부칙|Addendum|附則|附则|Disposición adicional|Disposição final"
    r"|사업자 정보|Business Information|事業者情報|经营者信息|Información de la empresa|Informações da empresa)$"
)
BULLETS = ("- ", "・")


def output_path(doc: str, lang: str, archived: str | None = None, revision: str | None = None) -> str:
    """Path of a page relative to products/reel-nest/, e.g. 'privacy/', 'privacy/en/', 'terms/',
    'terms/ja/', 'privacy/archive/2026-09-11/en/' for a previous version and
    'terms/revision/2026-11-14/' for the revision page of the version effective that day."""
    prefix = DOCUMENTS[doc]["prefix"]
    if archived:
        prefix = f"{prefix}archive/{archived}/"
    elif revision:
        prefix = f"{prefix}revision/{revision}/"
    return prefix if lang == "ko" else f"{prefix}{lang}/"


def dated_texts(folder: Path, doc: str) -> dict[str, dict[str, Path]]:
    """{date: {lang: path}} of <source>_<lang>_<date>.txt files in a folder, newest first."""
    versions: dict[str, dict[str, Path]] = {}
    if folder.exists():
        for path in folder.iterdir():
            match = ARCHIVE_NAME_RE.match(path.name)
            if match and match["source"] == DOCUMENTS[doc]["source"] and match["lang"] in LANGUAGES:
                versions.setdefault(match["date"], {})[match["lang"]] = path
    return dict(sorted(versions.items(), reverse=True))


def archived_versions(doc: str) -> dict[str, dict[str, Path]]:
    """{date: {lang: path}} of the previous versions of a document, newest first."""
    return dated_texts(ARCHIVE, doc)


def upcoming_version(doc: str) -> tuple[str, dict[str, Path]] | None:
    """(date, {lang: path}) of the announced revision not yet in force, if any (at most one)."""
    upcoming = dated_texts(UPCOMING, doc)
    if len(upcoming) > 1:
        raise ValueError(f"More than one upcoming {doc} version: {sorted(upcoming)}")
    return next(iter(upcoming.items()), None)


def current_date(doc: str) -> str:
    """Effective date (YYYY-MM-DD) of the text in force, read from its Korean effective-date line."""
    text = (CONTENT / f"{DOCUMENTS[doc]['source']}_ko.txt").read_text(encoding="utf-8")
    effective = next(line for line in text.splitlines()[1:] if line.strip())
    match = KO_DATE_RE.search(effective)
    if not match:
        raise ValueError(f"No date in the effective-date line of the Korean {doc} text: {effective!r}")
    return f"{int(match[1]):04d}-{int(match[2]):02d}-{int(match[3]):02d}"


def localized_date(lang: str, iso: str) -> str:
    d = date.fromisoformat(iso)
    if lang == "ko":
        return f"{d.year}년 {d.month}월 {d.day}일"
    if lang in ("ja", "zh"):
        return f"{d.year}年{d.month}月{d.day}日"
    if lang == "es":
        return f"{d.day} de {ES_MONTHS[d.month - 1]} de {d.year}"
    if lang == "pt":
        return f"{d.day} de {PT_MONTHS[d.month - 1]} de {d.year}"
    return f"{EN_MONTHS[d.month - 1]} {d.day}, {d.year}"


def version_chain(doc: str) -> list[tuple[str, str, dict[str, Path]]]:
    """Every version of a document, oldest first: (date, 'archive' | 'current' | 'upcoming', {lang: path})."""
    source = DOCUMENTS[doc]["source"]
    chain = [(d, "archive", langs) for d, langs in sorted(archived_versions(doc).items())]
    chain.append((current_date(doc), "current", {lang: CONTENT / f"{source}_{lang}.txt" for lang in LANGUAGES}))
    upcoming = upcoming_version(doc)
    if upcoming:
        chain.append((upcoming[0], "upcoming", upcoming[1]))
    dates = [d for d, _, _ in chain]
    if dates != sorted(set(dates)):
        raise ValueError(f"{doc} versions are not in date order or repeat a date: {dates}")
    return chain


def revisions(doc: str) -> dict[str, tuple[str, dict[str, tuple[Path, str, Path]]]]:
    """{date: (state, {lang: (new text, previous version's date, previous text)})} of the versions that
    get a revision page, newest first. state is 'upcoming' or 'in force' (current or archived)."""
    since = REVISION_PAGES_SINCE.get(doc)
    result = {}
    if not since:
        return result
    chain = version_chain(doc)
    for index, (when, kind, langs) in enumerate(chain):
        if when < since or index == 0:
            continue
        pairs = {}
        for lang, path in langs.items():
            before = next(((d, l[lang]) for d, _, l in reversed(chain[:index]) if lang in l), None)
            if before:
                pairs[lang] = (path, before[0], before[1])
        if "ko" not in pairs:
            raise FileNotFoundError(f"Korean text needed for the {doc} revision of {when}")
        result[when] = ("upcoming" if kind == "upcoming" else "in force", pairs)
    return dict(sorted(result.items(), reverse=True))


def comparison_rows(doc: str, lang: str, before: str, after: str) -> list[tuple[str, list[str], list[str]]]:
    """(section heading, paragraphs before, paragraphs after) for every changed run of paragraphs."""
    section_re = TERMS_SECTION_RE if doc == "terms" else PRIVACY_SECTION_RE

    def paragraphs(text: str) -> tuple[list[str], list[str]]:
        lines, headings, heading = [], [], REVISION_LABELS[lang]["header"]
        for line in (line.strip() for line in text.replace("\r\n", "\n").split("\n")):
            if not line:
                continue
            if section_re.match(line):
                heading = line
            lines.append(line)
            headings.append(heading)
        return lines, headings

    old, old_headings = paragraphs(before)
    new, new_headings = paragraphs(after)
    rows = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(a=old, b=new, autojunk=False).get_opcodes():
        if tag == "equal":
            continue
        if tag == "replace" and i2 - i1 == j2 - j1:
            rows.extend((new_headings[j1 + k], [old[i1 + k]], [new[j1 + k]]) for k in range(i2 - i1))
        else:
            heading = new_headings[j1] if j1 < j2 else old_headings[i1]
            rows.append((heading, old[i1:i2], new[j1:j2]))
    return rows


def relative_href(from_path: str, to_path: str) -> str:
    depth = from_path.count("/")
    return "../" * depth + to_path


def render_document(doc: str, text: str) -> tuple[str, str, list[tuple[str, str]], list[str]]:
    lines = [line.strip() for line in text.replace("\r\n", "\n").split("\n")]
    title = lines[0]
    effective = next((line for line in lines[1:] if line), "")
    body: list[str] = []
    toc: list[tuple[str, str]] = []
    in_list = False
    skipped_effective = False

    def close_list() -> None:
        nonlocal in_list
        if in_list:
            body.append("</ul>")
            in_list = False

    for line in lines[1:]:
        if not line:
            close_list()
            continue
        if not skipped_effective and line == effective:
            skipped_effective = True
            continue
        is_section = (TERMS_SECTION_RE if doc == "terms" else PRIVACY_SECTION_RE).match(line)
        if is_section:
            close_list()
            section_id = f"section-{len(toc) + 1}"
            toc.append((section_id, line))
            body.append(f'<h2 id="{section_id}">{html.escape(line)}</h2>')
            continue
        if doc == "privacy" and PRIVACY_SUBSECTION_RE.match(line):
            close_list()
            body.append(f"<h3>{html.escape(line)}</h3>")
            continue
        bullet = next((b for b in BULLETS if line.startswith(b)), None)
        if bullet:
            if not in_list:
                body.append("<ul>")
                in_list = True
            body.append(f"<li>{html.escape(line[len(bullet):].strip())}</li>")
            continue
        close_list()
        if URL_RE.match(line):
            safe_url = html.escape(line, quote=True)
            body.append(f'<p class="external-link"><a href="{safe_url}" rel="noopener noreferrer">{safe_url}</a></p>')
        else:
            body.append(f"<p>{html.escape(line)}</p>")
    close_list()
    return title, effective, toc, body


def page_html(
    doc: str,
    lang: str,
    here: str,
    title: str,
    robots: str,
    page_paths: dict[str, str],
    toc: list[tuple[str, str]],
    eyebrow: str,
    effective_value: str,
    notice: str,
    body: str,
) -> str:
    """The page shell shared by every generated page. page_paths = {lang: path} of this page's languages."""
    meta = LANGUAGES[lang]
    labels = LABELS[lang]
    css_href = relative_href(here, "policy.css")
    canonical = BASE_URL + here
    language_items = []
    for code, path in page_paths.items():
        item = LANGUAGES[code]
        current = ' aria-current="page"' if code == lang else ""
        language_items.append(
            f'<a href="{relative_href(here, path)}" lang="{item["html_lang"]}"{current}>'
            f'{html.escape(item["name"])}</a>'
        )
    language_links = "".join(language_items)
    alternate_links = "\n".join(
        f'<link rel="alternate" hreflang="{LANGUAGES[code]["html_lang"]}" href="{BASE_URL + path}">'
        for code, path in page_paths.items()
    )
    toc_links = "".join(f'<li><a href="#{anchor}">{html.escape(label)}</a></li>' for anchor, label in toc)
    privacy_href = relative_href(here, output_path("privacy", lang))
    terms_href = relative_href(here, output_path("terms", lang))
    return f'''<!doctype html>
<html lang="{meta["html_lang"]}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{html.escape(DESCRIPTIONS[doc][lang], quote=True)}">
  <meta name="theme-color" content="#13263f">
  <meta name="robots" content="{robots}">
  <title>{html.escape(title)}</title>
  <link rel="canonical" href="{canonical}">
  {alternate_links}
  <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='16' fill='%2313263f'/%3E%3Cpath d='M18 18h28v8H27v8h16v8H27v4h19v8H18z' fill='%236dc5ff'/%3E%3C/svg%3E">
  <link rel="stylesheet" href="{css_href}">
</head>
<body>
  <a class="skip-link" href="#policy">{html.escape(labels["skip"])}</a>
  <header class="site-header">
    <a class="brand" href="{relative_href(here, output_path(doc, "ko"))}" aria-label="Reel Nest">
      <span class="brand-mark" aria-hidden="true">R</span>
      <span><strong>Reel Nest</strong><small>{html.escape(labels[doc])}</small></span>
    </a>
    <nav class="languages" aria-label="{html.escape(labels["language"], quote=True)}">{language_links}</nav>
  </header>
  <main class="page-shell">
    <aside class="toc" aria-label="{html.escape(labels["toc"], quote=True)}">
      <span>{html.escape(labels["toc"])}</span>
      <ol>{toc_links}</ol>
    </aside>
    <article id="policy" class="policy-card">
      <div class="document-heading">
        <p class="eyebrow">{html.escape(eyebrow)}</p>
        <h1>{html.escape(title)}</h1>
        <p class="effective"><span>{html.escape(labels["updated"])}</span>{html.escape(effective_value)}</p>
      </div>
      {notice}
      <div class="document-body">{body}</div>
      <a class="back-to-top" href="#">↑ {html.escape(labels["top"])}</a>
    </article>
  </main>
  <footer><a href="{terms_href}">{html.escape(TERMS_LINK[lang])}</a> · <a href="{privacy_href}">{html.escape(labels["privacy_link"])}</a><br>© 2026 Fellow Survivor Studio · Reel Nest</footer>
</body>
</html>
'''


def effective_value_of(effective: str) -> str:
    return re.sub(r"^[^:：]+[:：]\s*", "", effective)


def render_page(
    doc: str,
    lang: str,
    text: str,
    archived: str | None = None,
    versions: dict[str, dict[str, Path]] | None = None,
    revision_list: dict[str, tuple[str, dict]] | None = None,
) -> str:
    """Render a current page (archived=None, listing `versions` as previous versions and
    `revision_list` as revision pages) or the previous version effective from `archived`
    (versions = the languages it exists in)."""
    labels = LABELS[lang]
    archive_labels = ARCHIVE_LABELS[lang]
    versions = versions or {}
    revision_list = revision_list or {}
    here = output_path(doc, lang, archived)
    title, effective, toc, body = render_document(doc, text)
    page_paths = {code: output_path(doc, code, archived) for code in LANGUAGES
                  if not archived or code in versions.get(archived, {})}
    robots = "noindex, follow" if archived else "index, follow"
    notice = ""
    previous_versions = ""
    if archived:
        notice = (
            f'<p class="archive-notice">{html.escape(archive_labels["notice"])} '
            f'<a href="{relative_href(here, output_path(doc, lang))}">{html.escape(archive_labels["current"])}</a></p>'
        )
    else:
        rev_labels = REVISION_LABELS[lang]
        pending = next((d for d, (state, _) in revision_list.items() if state == "upcoming"), None)
        if pending:
            end = (date.fromisoformat(pending) - timedelta(days=1)).isoformat()
            message = rev_labels["in_force_until"].format(end=localized_date(lang, end), date=localized_date(lang, pending))
            target = lang if lang in revision_list[pending][1] else "ko"
            notice = (
                f'<p class="status-notice">{html.escape(message)} '
                f'<a href="{relative_href(here, output_path(doc, target, revision=pending))}">{html.escape(rev_labels["see_revision"])}</a></p>'
            )
        items = "".join(
            f'<li><a href="{relative_href(here, output_path(doc, lang if lang in langs else "ko", date))}">{date}</a></li>'
            for date, langs in versions.items()
        )
        if items:
            previous_versions = f'<nav class="previous-versions" aria-label="{html.escape(archive_labels["previous"], quote=True)}"><h2>{html.escape(archive_labels["previous"])}</h2><ul>{items}</ul></nav>'
        revision_items = "".join(
            f'<li><a href="{relative_href(here, output_path(doc, lang if lang in pairs else "ko", revision=when))}">{when}</a></li>'
            for when, (_, pairs) in revision_list.items()
        )
        if revision_items:
            previous_versions += f'<nav class="previous-versions revisions" aria-label="{html.escape(rev_labels["revisions"], quote=True)}"><h2>{html.escape(rev_labels["revisions"])}</h2><ul>{revision_items}</ul></nav>'
    return page_html(doc, lang, here, title, robots, page_paths, toc, f"Reel Nest · {labels[doc]}",
                     effective_value_of(effective), notice, "".join(body) + previous_versions)


def render_revision_page(doc: str, lang: str, when: str, state: str, pairs: dict[str, tuple[Path, str, Path]]) -> str:
    """Revision page of the version effective `when`: status, reason, before/after comparison, full text."""
    labels = LABELS[lang]
    rev_labels = REVISION_LABELS[lang]
    new_path, before_date, before_path = pairs[lang]
    new_text = new_path.read_text(encoding="utf-8")
    here = output_path(doc, lang, revision=when)
    title, effective, toc, body = render_document(doc, new_text)
    reason_path = REVISIONS / f"{DOCUMENTS[doc]['source']}_{lang}_{when}.txt"
    if not reason_path.is_file():
        raise FileNotFoundError(f"Reason for the {doc} revision of {when} ({lang}) is missing: {reason_path}")
    reason = "".join(f"<p>{html.escape(line.strip())}</p>"
                     for line in reason_path.read_text(encoding="utf-8").splitlines() if line.strip())
    rows = comparison_rows(doc, lang, before_path.read_text(encoding="utf-8"), new_text)

    def cell(lines: list[str]) -> str:
        return "".join(f"<p>{html.escape(line)}</p>" for line in lines) or f"<p>{html.escape(rev_labels['none'])}</p>"

    before_label = rev_labels["before"].format(date=localized_date(lang, before_date))
    after_label = rev_labels["after"].format(date=localized_date(lang, when))
    table_rows = "".join(
        f'<tr><th scope="row">{html.escape(heading)}</th>'
        f'<td data-label="{html.escape(before_label, quote=True)}">{cell(old)}</td>'
        f'<td data-label="{html.escape(after_label, quote=True)}">{cell(new)}</td></tr>'
        for heading, old, new in rows
    )
    comparison = (
        f'<h2 id="reason">{html.escape(rev_labels["reason"])}</h2>{reason}'
        f'<h2 id="changes">{html.escape(rev_labels["changes"])}</h2>'
        f'<p>{html.escape(rev_labels["changes_intro"].format(before=localized_date(lang, before_date)))}</p>'
        f'<div class="changes-wrap"><table class="changes"><thead><tr><th scope="col">{html.escape(rev_labels["section"])}</th>'
        f'<th scope="col">{html.escape(before_label)}</th><th scope="col">{html.escape(after_label)}</th></tr></thead>'
        f'<tbody>{table_rows}</tbody></table></div>'
        f'<h2 id="full-text">{html.escape(rev_labels["full_text"])}</h2>'
    )
    status = rev_labels["pending" if state == "upcoming" else "in_force_from"].format(date=localized_date(lang, when))
    archive_labels = ARCHIVE_LABELS[lang]
    notice = (
        f'<p class="status-notice">{html.escape(status)} '
        f'<a href="{relative_href(here, output_path(doc, lang))}">{html.escape(archive_labels["current"])}</a></p>'
    )
    toc = [("reason", rev_labels["reason"]), ("changes", rev_labels["changes"]), ("full-text", rev_labels["full_text"])] + toc
    page_title = rev_labels["page_title"].format(title=title)
    page_paths = {code: output_path(doc, code, revision=when) for code in LANGUAGES if code in pairs}
    return page_html(doc, lang, here, page_title, "noindex, follow", page_paths, toc,
                     f"Reel Nest · {labels[doc]} · {rev_labels['revisions']}", effective_value_of(effective),
                     notice, comparison + "".join(body))


def build(out: Path) -> tuple[list[str], list[str], list[str]]:
    """Write every generated page and the sitemap under `out` (LF line endings).
    The privacy/ and terms/ folders are rewritten from scratch; other files are kept.
    Returns the current, previous-version and revision page paths."""
    for info in DOCUMENTS.values():
        generated = out / info["prefix"]
        if generated.exists():
            shutil.rmtree(generated)
    out.mkdir(parents=True, exist_ok=True)
    pages: list[str] = []
    archive_pages: list[str] = []
    revision_pages: list[str] = []

    def write_page(path: str, content: str) -> None:
        output_dir = out / path
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / "index.html").write_text(content, encoding="utf-8", newline="\n")

    for doc, info in DOCUMENTS.items():
        versions = archived_versions(doc)
        revision_list = revisions(doc)
        for lang in LANGUAGES:
            source = CONTENT / f"{info['source']}_{lang}.txt"
            if not source.exists():
                raise FileNotFoundError(source)
            path = output_path(doc, lang)
            write_page(path, render_page(doc, lang, source.read_text(encoding="utf-8"), versions=versions,
                                         revision_list=revision_list))
            pages.append(path)
        for when, langs in versions.items():
            if "ko" not in langs:
                raise FileNotFoundError(ARCHIVE / f"{info['source']}_ko_{when}.txt")
            for lang, source in langs.items():
                path = output_path(doc, lang, when)
                write_page(path, render_page(doc, lang, source.read_text(encoding="utf-8"), archived=when, versions=versions))
                archive_pages.append(path)
        for when, (state, pairs) in revision_list.items():
            for lang in pairs:
                path = output_path(doc, lang, revision=when)
                write_page(path, render_revision_page(doc, lang, when, state, pairs))
                revision_pages.append(path)
    # Previous versions and revision pages are noindex and stay out of the sitemap.
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{BASE_URL}{path}</loc></url>\n" for path in EXTRA_SITEMAP_PATHS + pages) + "</urlset>\n"
    (out / "sitemap.xml").write_text(sitemap, encoding="utf-8", newline="\n")
    return pages, archive_pages, revision_pages


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--output", type=Path, default=OUT, help="output folder (default: products/reel-nest/)")
    out = parser.parse_args().output.resolve()
    pages, archive_pages, revision_pages = build(out)
    print(f"Built {len(pages)} current pages, {len(archive_pages)} previous-version pages and "
          f"{len(revision_pages)} revision pages in {out}")


if __name__ == "__main__":
    main()
