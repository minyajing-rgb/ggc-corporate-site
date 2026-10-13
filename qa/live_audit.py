#!/usr/bin/env python3
"""Read-only audit of the published GGC site."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse, urldefrag
from urllib.request import Request, urlopen
from urllib.error import HTTPError
import json
import ssl
import xml.etree.ElementTree as ET

BASE = "https://ggcgames.com"
HEADERS = {"User-Agent": "GGC-Release-QA/1.0"}

def get(url):
    for attempt in range(3):
        try:
            with urlopen(Request(url, headers=HEADERS), timeout=20, context=ssl.create_default_context()) as r:
                result = r.status, r.geturl(), r.headers, r.read()
        except HTTPError as e:
            result = e.code, e.geturl(), e.headers, e.read()
        if result[0] not in (502, 503, 504) or attempt == 2:
            return result

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.assets = []
        self.canonical = []
        self.alternates = []
        self.h1 = 0
        self.images_without_alt = 0
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        if tag == "img":
            if "alt" not in a:
                self.images_without_alt += 1
            if a.get("src"):
                self.assets.append(a["src"])
        if tag == "script" and a.get("src"):
            self.assets.append(a["src"])
        if tag == "link" and a.get("href"):
            if a.get("rel") == "canonical":
                self.canonical.append(a["href"])
            elif a.get("rel") == "alternate" and a.get("hreflang"):
                self.alternates.append((a["hreflang"], a["href"]))
            elif a.get("rel") == "stylesheet":
                self.assets.append(a["href"])
        if tag == "h1":
            self.h1 += 1

def main():
    failures = []
    status, final, _, xml = get(BASE + "/sitemap.xml")
    if status != 200:
        failures.append(f"sitemap status {status}")
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = [e.text for e in ET.fromstring(xml).findall("s:url/s:loc", ns)]
    if len(urls) != 94 or len(set(urls)) != 94:
        failures.append(f"sitemap count/uniqueness {len(urls)}/{len(set(urls))}, expected 94")
    if any(not u.startswith(BASE + "/") for u in urls):
        failures.append("sitemap contains an off-domain URL")
    page_urls = urls + [BASE + "/zh/privacy.html", BASE + "/en/privacy.html"]
    parsed = {}
    with ThreadPoolExecutor(max_workers=8) as pool:
        futs = {pool.submit(get, url): url for url in page_urls}
        for fut in as_completed(futs):
            url = futs[fut]
            status, final, headers, data = fut.result()
            if status != 200 or final != url:
                failures.append(f"page {url}: {status}, final {final}")
            if "text/html" not in headers.get("Content-Type", ""):
                failures.append(f"page {url}: wrong content type")
            page = Page()
            page.feed(data.decode("utf-8"))
            parsed[url] = page
            if page.canonical != [url]:
                failures.append(f"page {url}: canonical {page.canonical}")
            if page.h1 != 1:
                failures.append(f"page {url}: {page.h1} h1 elements")
            if page.images_without_alt:
                failures.append(f"page {url}: {page.images_without_alt} images without alt")
            if b"../review.html" in data or b"readiness-manifest.json" in data:
                failures.append(f"page {url}: review artifact reference")
    linked = set()
    assets = set()
    for url, page in parsed.items():
        for ref in page.links:
            target = urldefrag(urljoin(url, ref))[0]
            p = urlparse(target)
            if p.netloc in ("ggcgames.com", "www.ggcgames.com"):
                linked.add(target)
        for ref in page.assets:
            target = urljoin(url, ref)
            if urlparse(target).netloc == "ggcgames.com":
                assets.add(target)
    to_check = linked | assets | {BASE + "/robots.txt"}
    with ThreadPoolExecutor(max_workers=8) as pool:
        futs = {pool.submit(get, url): url for url in to_check}
        for fut in as_completed(futs):
            url = futs[fut]
            status, final, _, _ = fut.result()
            if status != 200:
                failures.append(f"resource {url}: {status}, final {final}")
    redirects = {}
    for url in ("http://ggcgames.com/", "http://www.ggcgames.com/", "https://www.ggcgames.com/", BASE + "/"):
        status, final, _, body = get(url)
        redirects[url] = [status, final]
        if status != 200 or final != BASE + "/":
            failures.append(f"redirect {url}: {status}, final {final}")
        if b'url=zh/index.html' not in body or b'href="review.html"' in body:
            failures.append(f"root fallback {url}: missing language redirect or contains review link")
    unknown = BASE + "/release-audit-nonexistent-page-20261013"
    status, _, _, body = get(unknown)
    if status != 404 or b"GGC" not in body:
        failures.append(f"404 behavior: status {status}, branded {b'GGC' in body}")
    report = {"sitemap_urls":len(urls),"pages_checked":len(page_urls),"internal_links_checked":len(linked),"assets_checked":len(assets),"redirects":redirects,"unknown_path_status":status,"failures":sorted(failures)}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(bool(failures))

if __name__ == "__main__":
    main()
