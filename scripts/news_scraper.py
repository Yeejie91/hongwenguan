#!/usr/bin/env python3
"""Daily education news scraper.

Reads RSS sources from sources.py, fetches each feed, dedupes by link/title,
filters out anything older than MAX_AGE_DAYS, groups by region, and writes a
static HTML page to ../news.html.
"""
from __future__ import annotations

import html
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import feedparser

from sources import REGION_GROUPS, SOURCES

MAX_ITEMS_PER_SOURCE = 6
MAX_AGE_DAYS = 7
MAX_ITEMS_PER_GROUP = 60

# Browser-like UA: many feeds (BBC, Google News) reject the default feedparser UA.
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "news.html"


def parse_entry_dt(entry) -> datetime | None:
    for key in ("published_parsed", "updated_parsed"):
        v = entry.get(key)
        if v:
            try:
                return datetime(*v[:6], tzinfo=timezone.utc)
            except (TypeError, ValueError):
                continue
    return None


def clean_text(text: str, max_chars: int = 200) -> str:
    if not text:
        return ""
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"&nbsp;", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > max_chars:
        text = text[: max_chars - 1].rstrip() + "…"
    return text


def fetch_source(source: dict) -> list[dict]:
    feed = feedparser.parse(source["url"], agent=USER_AGENT)
    status = getattr(feed, "status", None)
    entries = feed.entries
    print(f"  - {source['name']}: status={status} entries={len(entries)}", flush=True)
    if status and status >= 400:
        return []
    items: list[dict] = []
    for entry in entries[: MAX_ITEMS_PER_SOURCE * 3]:
        title = (entry.get("title") or "").strip()
        link = (entry.get("link") or "").strip()
        if not title or not link:
            continue
        items.append({
            "title": title,
            "link": link,
            "published": parse_entry_dt(entry),
            "summary": clean_text(entry.get("summary") or ""),
            "source_name": source["name"],
            "source_region": source["region"],
            "source_lang": source["lang"],
        })
    return items[:MAX_ITEMS_PER_SOURCE]


def fetch_all() -> list[dict]:
    out: list[dict] = []
    for source in SOURCES:
        try:
            out.extend(fetch_source(source))
        except Exception as exc:
            print(f"    ! {source['name']}: {exc}", flush=True)
    return out


def filter_and_dedupe(items: list[dict]) -> list[dict]:
    now = datetime.now(timezone.utc)
    seen_links: set[str] = set()
    seen_titles: set[str] = set()
    out: list[dict] = []
    for item in items:
        u = urlparse(item["link"])
        link_key = (u.netloc + u.path).lower()
        title_key = re.sub(r"\s+", "", item["title"])[:40]
        if link_key in seen_links or title_key in seen_titles:
            continue
        if item["published"]:
            age_days = (now - item["published"]).total_seconds() / 86400
            if age_days > MAX_AGE_DAYS:
                continue
        seen_links.add(link_key)
        seen_titles.add(title_key)
        out.append(item)
    return out


def group_by_region(items: list[dict]) -> dict[str, list[dict]]:
    groups: dict[str, list[dict]] = {k: [] for k in REGION_GROUPS}
    for item in items:
        for label, regions in REGION_GROUPS.items():
            if item["source_region"] in regions:
                groups[label].append(item)
                break
    for v in groups.values():
        v.sort(
            key=lambda x: x["published"] or datetime.min.replace(tzinfo=timezone.utc),
            reverse=True,
        )
    return groups


# ---------- HTML rendering ----------

CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
:root {
  --red: #C8102E; --red-d: #A00E25; --red-lt: #FEE2E2;
  --cream: #FFFBF5; --sand: #F5F0E8; --warm: #FFF7ED;
  --brown: #78350F; --dark: #1C1917; --mid: #57534E;
  --light: #A8A29E; --border: #E8E0D5;
}
html { font-size: 17px; scroll-behavior: smooth; }
body {
  font-family: 'Nunito','Noto Sans SC',-apple-system,BlinkMacSystemFont,sans-serif;
  background: var(--cream); color: var(--dark); line-height: 1.7;
}
header { padding: 56px 6vw 32px; background: white; border-bottom: 1.5px solid var(--border); }
header .wrap { max-width: 1100px; margin: 0 auto; }
.eyebrow {
  display: inline-block; background: var(--red-lt); color: var(--red);
  padding: 5px 14px; border-radius: 4px; font-size: 12px;
  font-weight: 800; letter-spacing: 1px; text-transform: uppercase;
}
h1 {
  font-family: 'Noto Sans SC', sans-serif;
  font-size: clamp(28px, 4vw, 42px); font-weight: 900;
  margin: 14px 0 8px;
}
.meta { font-size: 14px; color: var(--mid); }
.meta a { color: var(--red); text-decoration: none; font-weight: 700; }
.toc { margin-top: 22px; display: flex; flex-wrap: wrap; gap: 8px; }
.toc a {
  display: inline-block; padding: 7px 14px;
  background: var(--sand); border: 1px solid var(--border);
  border-radius: 999px; text-decoration: none; color: var(--brown);
  font-size: 13px; font-weight: 700;
  font-family: 'Noto Sans SC', sans-serif;
  transition: all .15s;
}
.toc a:hover { background: var(--red-lt); border-color: var(--red); color: var(--red); }

main { max-width: 1100px; margin: 0 auto; padding: 32px 6vw 80px; }
section { margin-top: 48px; }
section h2 {
  font-family: 'Noto Sans SC', sans-serif;
  font-size: clamp(22px, 3vw, 30px); font-weight: 900;
  margin-bottom: 18px; padding-bottom: 10px;
  border-bottom: 2px solid var(--red);
  display: flex; align-items: baseline; gap: 12px;
}
section h2 .count {
  font-size: 14px; color: var(--mid);
  font-weight: 600; font-family: 'Nunito', sans-serif;
}
.grid {
  display: grid; gap: 18px;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
}
article {
  background: white; border: 1px solid var(--border);
  border-radius: 14px; padding: 20px 22px;
  transition: transform .15s, box-shadow .15s, border-color .15s;
  display: flex; flex-direction: column;
}
article:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(0,0,0,.08);
  border-color: var(--red);
}
article .src {
  font-size: 12px; font-weight: 800; color: var(--red);
  font-family: 'Noto Sans SC', sans-serif;
  letter-spacing: .3px; margin-bottom: 8px;
}
article h3 {
  font-family: 'Noto Sans SC', sans-serif;
  font-size: 17px; font-weight: 800; line-height: 1.45;
  margin-bottom: 10px;
}
article h3 a { color: var(--dark); text-decoration: none; }
article h3 a:hover { color: var(--red); }
article .summary {
  font-size: 14px; color: var(--mid); line-height: 1.65;
  font-family: 'Noto Sans SC', sans-serif;
}
article .when {
  font-size: 12px; color: var(--light);
  margin-top: auto; padding-top: 12px; font-weight: 600;
}
footer {
  text-align: center; padding: 40px 6vw 56px;
  color: var(--light); font-size: 13px;
  border-top: 1px solid var(--border); background: white;
}
.empty { color: var(--mid); font-style: italic; padding: 18px 0; }
@media (max-width: 640px) {
  .grid { grid-template-columns: 1fr; }
  header { padding: 36px 6vw 24px; }
}
""".strip()


def slugify(s: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower() or "section"


def render_card(item: dict) -> str:
    when = item["published"].strftime("%Y-%m-%d %H:%M UTC") if item["published"] else ""
    summary_html = (
        f'<p class="summary">{html.escape(item["summary"])}</p>'
        if item["summary"]
        else ""
    )
    return (
        '<article>'
        f'<div class="src">{html.escape(item["source_name"])} · {html.escape(item["source_region"])}</div>'
        f'<h3><a href="{html.escape(item["link"])}" target="_blank" rel="noopener noreferrer">'
        f'{html.escape(item["title"])}</a></h3>'
        f'{summary_html}'
        f'<div class="when">{html.escape(when)}</div>'
        '</article>'
    )


def render(groups: dict[str, list[dict]]) -> str:
    now = datetime.now(timezone.utc)
    total = sum(len(v) for v in groups.values())
    toc = "\n".join(
        f'<a href="#{slugify(label)}">{html.escape(label)} · {len(items)}</a>'
        for label, items in groups.items()
    )
    section_parts: list[str] = []
    for label, items in groups.items():
        if items:
            cards = "\n".join(render_card(it) for it in items)
            body = f'<div class="grid">{cards}</div>'
        else:
            body = '<p class="empty">本类暂无新闻</p>'
        section_parts.append(
            f'<section id="{slugify(label)}">'
            f'<h2>{html.escape(label)} <span class="count">{len(items)} 条</span></h2>'
            f'{body}'
            '</section>'
        )
    sections_html = "\n".join(section_parts)
    updated = now.strftime("%Y-%m-%d %H:%M UTC")
    return (
        '<!DOCTYPE html>\n'
        '<html lang="zh">\n'
        '<head>\n'
        '<meta charset="UTF-8" />\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1.0" />\n'
        '<title>每日教育资讯 · 弘文馆</title>\n'
        '<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;600;700;800;900&family=Nunito:wght@400;600;700;800;900&display=swap" rel="stylesheet" />\n'
        f'<style>{CSS}</style>\n'
        '</head>\n'
        '<body>\n'
        '<header><div class="wrap">'
        '<span class="eyebrow">每日教育资讯 · Daily Education News</span>'
        '<h1>亚洲与全球教育动态</h1>'
        f'<p class="meta">共 {total} 条 · 更新于 {html.escape(updated)} · '
        '<a href="index.html">← 回首页</a></p>'
        f'<nav class="toc">{toc}</nav>'
        '</div></header>\n'
        f'<main>{sections_html}</main>\n'
        '<footer>自动抓取自公开 RSS 与 Google News RSS · 每日由 GitHub Actions 更新</footer>\n'
        '</body>\n'
        '</html>\n'
    )


def main() -> int:
    print("Fetching feeds...", flush=True)
    raw = fetch_all()
    print(f"  raw items: {len(raw)}", flush=True)
    items = filter_and_dedupe(raw)
    print(f"  after filter/dedupe: {len(items)}", flush=True)
    groups = group_by_region(items)
    for k in groups:
        groups[k] = groups[k][:MAX_ITEMS_PER_GROUP]
    OUTPUT.write_text(render(groups), encoding="utf-8")
    print(f"Wrote {OUTPUT}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
