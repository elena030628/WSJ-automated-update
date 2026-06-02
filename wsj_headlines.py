#!/usr/bin/env python3
"""Fetch and display the latest Wall Street Journal headlines from RSS feeds."""

import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime

FEEDS = {
    "World News":  "https://feeds.a.dj.com/rss/RSSWorldNews.xml",
    "US Business": "https://feeds.a.dj.com/rss/WSJcomUSBusiness.xml",
    "Markets":     "https://feeds.a.dj.com/rss/RSSMarketsMain.xml",
    "Technology":  "https://feeds.a.dj.com/rss/RSSWSJD.xml",
}

MAX_ITEMS = 5


def fetch_feed(url: str) -> ET.Element:
    req = urllib.request.Request(url, headers={"User-Agent": "WSJ-RSS-Reader/1.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        return ET.fromstring(resp.read())


def parse_items(root: ET.Element) -> list[dict]:
    items = []
    for item in root.findall(".//item")[:MAX_ITEMS]:
        title = item.findtext("title", "").strip()
        link  = item.findtext("link", "").strip()
        pub   = item.findtext("pubDate", "").strip()
        items.append({"title": title, "link": link, "pubDate": pub})
    return items


def print_section(section: str, items: list[dict]) -> None:
    print(f"\n{'─' * 60}")
    print(f"  {section}")
    print(f"{'─' * 60}")
    for i, item in enumerate(items, 1):
        print(f"{i}. {item['title']}")
        if item["pubDate"]:
            print(f"   {item['pubDate']}")
        if item["link"]:
            print(f"   {item['link']}")


def main() -> None:
    print(f"WSJ Headlines  —  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    for section, url in FEEDS.items():
        try:
            root  = fetch_feed(url)
            items = parse_items(root)
            print_section(section, items)
        except Exception as exc:
            print(f"\n[{section}] ERROR: {exc}")

    print()


if __name__ == "__main__":
    main()
