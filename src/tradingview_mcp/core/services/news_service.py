"""
Financial News Service via RSS feeds.

Uses feedparser (already installed as part of agent-reach dependencies).
No API keys required. Pulls from free, public RSS feeds.

Sources:
  crypto: CoinDesk, Cointelegraph
  stocks: Reuters Business News
  all:    Combined
"""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Optional
from math import ceil

# Allow workspace-local vendor installs for optional dependencies.
VENDOR_DIR = Path(__file__).resolve().parents[4] / ".vendor"
if VENDOR_DIR.exists():
    sys.path.insert(0, str(VENDOR_DIR))

# feedparser is bundled with agent-reach (installed globally)
try:
    import feedparser
    _FEEDPARSER_AVAILABLE = True
except ImportError:
    _FEEDPARSER_AVAILABLE = False

# ─── Feed Catalog ─────────────────────────────────────────────────────────────

RSS_FEEDS: dict[str, list[dict]] = {
    "crypto": [
        {"url": "https://www.coindesk.com/arc/outboundfeeds/rss/", "name": "CoinDesk"},
        {"url": "https://cointelegraph.com/rss", "name": "CoinTelegraph"},
    ],
    "macro": [
        {"url": "https://news.google.com/rss/search?q=gold+when:1d&hl=en-US&gl=US&ceid=US:en", "name": "Google News Gold"},
        {"url": "https://news.google.com/rss/search?q=%22Federal+Reserve%22+OR+inflation+OR+Treasury+yield+when:1d&hl=en-US&gl=US&ceid=US:en", "name": "Google News Fed"},
        {"url": "https://news.google.com/rss/search?q=%22US+dollar%22+OR+DXY+when:1d&hl=en-US&gl=US&ceid=US:en", "name": "Google News Dollar"},
        {"url": "https://news.google.com/rss/search?q=oil+OR+Brent+OR+WTI+OR+Hormuz+when:1d&hl=en-US&gl=US&ceid=US:en", "name": "Google News Energy"},
    ],
    "stocks": [
        {"url": "https://feeds.reuters.com/reuters/businessNews", "name": "Reuters Business"},
        {"url": "https://feeds.reuters.com/reuters/companyNews", "name": "Reuters Company"},
    ],
    "all": [
        {"url": "https://feeds.reuters.com/reuters/businessNews", "name": "Reuters Business"},
        {"url": "https://news.google.com/rss/search?q=markets+when:1d&hl=en-US&gl=US&ceid=US:en", "name": "Google News Markets"},
        {"url": "https://www.coindesk.com/arc/outboundfeeds/rss/", "name": "CoinDesk"},
        {"url": "https://cointelegraph.com/rss", "name": "CoinTelegraph"},
    ],
}

_TIMEOUT = 8


# ─── Public API ───────────────────────────────────────────────────────────────

def fetch_news(
    symbol: Optional[str] = None,
    category: str = "stocks",
    limit: int = 10,
) -> list[dict]:
    """
    Fetch financial news from RSS feeds.

    Args:
        symbol:   Optional ticker filter. If provided, only returns headlines
                  that mention the symbol (case-insensitive). e.g. "AAPL", "BTC"
        category: Feed group — "crypto" | "stocks" | "all"
        limit:    Maximum number of items to return

    Returns:
        List of news items with title, url, published, summary, source.
    """
    if not _FEEDPARSER_AVAILABLE:
        return [{
            "error": "feedparser not installed. Run: pip install feedparser",
            "install": "pip install feedparser"
        }]

    feeds = RSS_FEEDS.get(category, RSS_FEEDS["stocks"])
    results: list[dict] = []
    seen_keys: set[str] = set()
    per_feed_limit = max(1, ceil(limit / max(len(feeds), 1)))

    for feed_info in feeds:
        try:
            feed = feedparser.parse(feed_info["url"])
            source_name = feed.feed.get("title", feed_info["name"])
            collected_from_feed = 0

            for entry in feed.entries:
                if len(results) >= limit or collected_from_feed >= per_feed_limit:
                    break

                title = entry.get("title", "")
                summary = entry.get("summary", "") or entry.get("description", "")

                # Symbol filter
                if symbol:
                    combined = f"{title} {summary}".upper()
                    if symbol.upper() not in combined:
                        continue

                dedupe_key = f"{title}|{entry.get('link', '')}".strip().lower()
                if dedupe_key in seen_keys:
                    continue
                seen_keys.add(dedupe_key)

                results.append({
                    "title": title,
                    "url": entry.get("link", ""),
                    "published": entry.get("published", ""),
                    "published_at": _entry_published_at(entry),
                    "summary": _clean_html(summary)[:300],
                    "source": source_name,
                })
                collected_from_feed += 1

        except Exception:
            continue

    return results[:limit]


def fetch_news_summary(
    symbol: Optional[str] = None,
    category: str = "stocks",
    limit: int = 10,
) -> dict:
    """
    Fetch news and return structured dict for MCP tool output.
    """
    items = fetch_news(symbol, category, limit)
    return {
        "symbol": symbol,
        "category": category,
        "count": len(items),
        "feedparser_available": _FEEDPARSER_AVAILABLE,
        "items": items,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# ─── Utils ────────────────────────────────────────────────────────────────────

def _clean_html(text: str) -> str:
    """Strip basic HTML tags from text."""
    import re
    text = re.sub(r"<[^>]+>", "", text)
    for entity, char in (("&amp;", "&"), ("&lt;", "<"), ("&gt;", ">"), ("&nbsp;", " ")):
        text = text.replace(entity, char)
    return text.strip()


def _entry_published_at(entry: dict) -> str | None:
    """Normalize a feed entry published timestamp to ISO-8601 UTC when possible."""
    parsed = entry.get("published_parsed") or entry.get("updated_parsed")
    if parsed:
        try:
            return datetime(*parsed[:6], tzinfo=timezone.utc).isoformat()
        except Exception:
            pass

    published = entry.get("published") or entry.get("updated")
    if not published:
        return None
    try:
        dt = parsedate_to_datetime(published)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc).isoformat()
    except Exception:
        return None
