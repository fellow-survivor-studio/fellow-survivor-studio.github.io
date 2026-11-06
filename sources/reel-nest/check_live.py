"""Check the live Reel Nest policy pages and the forwarding of their earlier addresses.

  python -X utf8 sources/reel-nest/check_live.py            # new pages + earlier addresses
  python -X utf8 sources/reel-nest/check_live.py --new-only # new pages only

New pages (every page this repository builds, current and previous versions): HTTP 200 at the
same URL, HTML, canonical link = its own URL. Earlier addresses, on both
https://fellowsurvivor.com/reel-nest/... and https://fellow-survivor-studio.github.io/reel-nest/...
(app versions before 1.3.0 link to the github.io ones): must end on the new URL with HTTP 200.
Exit code 0 when everything passes. Standard library only; reads the network, changes nothing.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import re
import sys
import urllib.error
import urllib.request

from build_site import BASE_URL
from validate_site import expected_pages

UA = {"User-Agent": "fellowsurvivor-reel-nest-check/1"}
OLD_HOSTS = ("https://fellowsurvivor.com", "https://fellow-survivor-studio.github.io")


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


def get(url, follow=True):
    opener = urllib.request.build_opener() if follow else urllib.request.build_opener(NoRedirect)
    try:
        with opener.open(urllib.request.Request(url, headers=UA), timeout=30) as r:
            return r.status, r.geturl(), r.headers.get_content_type(), r.read()
    except urllib.error.HTTPError as e:
        return e.code, url, e.headers.get_content_type(), b""
    except Exception as e:  # network problem
        return None, url, None, str(e).encode()


def old_path(path):
    """Earlier address of a page below products/reel-nest/ (privacy/ was the /reel-nest/ root)."""
    return "/reel-nest/" + (path[len("privacy/"):] if path.startswith("privacy/") else path)


def check_new(path):
    url = BASE_URL + path
    status, final, ctype, body = get(url, follow=False)
    canonical = re.findall(r'<link rel="canonical" href="([^"]+)"', body.decode("utf-8", "replace"))
    ok = status == 200 and ctype == "text/html" and canonical == [url]
    return ok, f"{url} status={status} canonical={'own' if canonical == [url] else canonical}"


def check_file(path):
    url = BASE_URL + path
    status = get(url, follow=False)[0]
    return status == 200, f"{url} status={status}"


def check_old(old_url, new_url):
    status, final, _, _ = get(old_url)
    ok = status == 200 and final == new_url
    return ok, f"{old_url} -> {status} {'(new URL)' if final == new_url else final}"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--new-only", action="store_true", help="skip the earlier addresses")
    args = ap.parse_args()
    expected = expected_pages()
    pages = sorted(expected)
    jobs = [(check_new, (path,)) for path in [""] + pages]  # "" = the product page
    jobs += [(check_file, (name,)) for name in ("sitemap.xml", "policy.css")]
    new_count = len(jobs)
    if not args.new_only:
        extra = {"/reel-nest": "privacy/", "/reel-nest/terms": "terms/", "/reel-nest/home/": "",
                 "/reel-nest/sitemap.xml": "sitemap.xml"}
        # Revision pages are new; only current and previous versions had /reel-nest/ addresses.
        legacy = [p for p in pages if expected[p][2] != "revision"]
        targets = [(old_path(p), p) for p in legacy] + list(extra.items())
        jobs += [(check_old, (host + old, BASE_URL + new)) for host in OLD_HOSTS for old, new in targets]
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(lambda job: job[0](*job[1]), jobs))
    failures = 0
    for ok, line in results:
        failures += not ok
        print(("ok   " if ok else "FAIL ") + line)
    print(f"new addresses: {new_count}, earlier addresses: {len(jobs) - new_count}, failures: {failures}")
    print("RESULT:", "PASS" if not failures else "FAIL")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
