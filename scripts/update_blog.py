#!/usr/bin/env python3
"""
scripts/update_blog.py

Fetches the latest blog posts from the RSS/Atom feed at BLOG_RSS_URL
and updates the <!-- BLOG_START --> ... <!-- BLOG_END --> block in README.md.

Usage:
    python scripts/update_blog.py

Environment variables:
    BLOG_RSS_URL  - Full URL to RSS/Atom feed (optional, falls back to default)
"""

from __future__ import annotations

import os
import re
import textwrap
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

README_PATH = Path(__file__).parent.parent / "README.md"
BLOG_RSS_URL = os.environ.get("BLOG_RSS_URL", "https://mihirdixit.dev/blog/rss.xml")
MAX_POSTS = 5

BLOCK_START = "<!-- BLOG_START -->"
BLOCK_END = "<!-- BLOG_END -->"


def fetch_feed(url: str) -> list[dict]:
    """Download and parse RSS feed, return list of post dicts."""
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            raw = response.read()
    except Exception as exc:  # noqa: BLE001
        print(f"[update_blog] WARNING: could not fetch feed ({exc}). Skipping update.")
        return []

    root = ET.fromstring(raw)

    # Handle both RSS 2.0 and Atom feeds
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    posts: list[dict] = []

    if root.tag == "rss":
        for item in root.findall(".//item")[:MAX_POSTS]:
            title = (item.findtext("title") or "").strip()
            link = (item.findtext("link") or "").strip()
            pub_date = (item.findtext("pubDate") or "").strip()
            posts.append({"title": title, "link": link, "date": pub_date})
    else:
        # Atom
        for entry in root.findall("atom:entry", ns)[:MAX_POSTS]:
            title_el = entry.find("atom:title", ns)
            link_el = entry.find("atom:link", ns)
            updated_el = entry.find("atom:updated", ns)
            title = (title_el.text or "").strip() if title_el is not None else ""
            link = link_el.get("href", "") if link_el is not None else ""
            date = (updated_el.text or "").strip() if updated_el is not None else ""
            posts.append({"title": title, "link": link, "date": date})

    return posts


def build_blog_block(posts: list[dict]) -> str:
    """Render the markdown table for the blog posts section."""
    if not posts:
        return textwrap.dedent("""\
            <!-- BLOG_START -->
            > _No posts yet. First post in progress._
            <!-- BLOG_END -->""")

    lines = [
        "<!-- BLOG_START -->",
        "| Post | Date |",
        "|------|------|",
    ]
    for post in posts:
        lines.append(f"| [{post['title']}]({post['link']}) | {post['date']} |")

    updated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines.append("")
    lines.append(f"<sub>Last updated: {updated_at}</sub>")
    lines.append("<!-- BLOG_END -->")
    return "\n".join(lines)


def update_readme(readme_path: Path, new_block: str) -> bool:
    """Replace the BLOG block in README.md. Returns True if content changed."""
    content = readme_path.read_text(encoding="utf-8")
    pattern = re.compile(
        rf"{re.escape(BLOCK_START)}.*?{re.escape(BLOCK_END)}",
        re.DOTALL,
    )
    if not pattern.search(content):
        print("[update_blog] ERROR: BLOG_START/BLOG_END markers not found in README.md")
        return False

    new_content = pattern.sub(new_block, content)
    if new_content == content:
        print("[update_blog] No changes detected.")
        return False

    readme_path.write_text(new_content, encoding="utf-8")
    print(f"[update_blog] README.md updated with {len(new_block.splitlines())} lines.")
    return True


def main() -> None:
    posts = fetch_feed(BLOG_RSS_URL)
    blog_block = build_blog_block(posts)
    update_readme(README_PATH, blog_block)


if __name__ == "__main__":
    main()
