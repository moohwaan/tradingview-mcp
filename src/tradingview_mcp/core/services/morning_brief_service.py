from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from tradingview_mcp.core.services.news_service import fetch_news_summary
from tradingview_mcp.core.services.yahoo_finance_service import get_price

ICT = ZoneInfo("Asia/Bangkok")

THAI_MONTHS = {
    1: "มกราคม",
    2: "กุมภาพันธ์",
    3: "มีนาคม",
    4: "เมษายน",
    5: "พฤษภาคม",
    6: "มิถุนายน",
    7: "กรกฎาคม",
    8: "สิงหาคม",
    9: "กันยายน",
    10: "ตุลาคม",
    11: "พฤศจิกายน",
    12: "ธันวาคม",
}

FINANCE_SOURCES = {
    "bloomberg.com",
    "cnbc",
    "yahoo finance",
    "kitco",
    "benzinga",
    "fxempire",
    "seeking alpha",
    "investmentnews",
    "anadolu ajansı",
    "reuters",
    "tradingview",
    "goldsilver",
    "litefinance",
}

NEGATIVE_NEWS_KEYWORDS = {
    "mortgage",
    "homebuy",
    "housing",
    "real estate",
    "rollercoaster",
    "athletics",
    "wildfire",
    "board of directors",
    "nicu",
    "mining project",
    "oil and gas resources",
    "gold cards",
}

MARKET_NEWS_KEYWORDS = {
    "gold",
    "bullion",
    "xau",
    "federal reserve",
    "fed",
    "inflation",
    "yield",
    "treasury",
    "rate",
    "rates",
    "payroll",
    "dollar",
    "dxy",
    "oil",
    "brent",
    "wti",
    "hormuz",
    "iran",
    "war",
    "safe haven",
    "geopolitical",
}


@dataclass(frozen=True)
class ThemeRule:
    topic: str
    keywords: tuple[str, ...]
    direction_for_gold: str
    strength: float
    summary_th: str
    driver_th: str
    narrative_th: str
    watchout_th: str
    market_relevance: str


THEME_RULES: tuple[ThemeRule, ...] = (
    ThemeRule(
        topic="Federal Reserve and rates",
        keywords=("fed", "federal reserve", "rate", "rates", "yield", "treasury", "inflation", "cpi", "payroll"),
        direction_for_gold="bearish_for_gold",
        strength=0.9,
        summary_th="ตลาดยังให้น้ำหนักกับทิศทางดอกเบี้ยและบอนด์ยีลด์ของสหรัฐฯ",
        driver_th="ความกังวลเรื่องดอกเบี้ยสูงและบอนด์ยีลด์",
        narrative_th="แรงกดดันจากแนวโน้มดอกเบี้ยสูงนานขึ้นมักเป็นปัจจัยลบต่อทองคำ เพราะเพิ่มต้นทุนค่าเสียโอกาสของสินทรัพย์ที่ไม่มีดอกผล",
        watchout_th="จับตาข้อมูลเศรษฐกิจสหรัฐฯ และการเปลี่ยนแปลงของบอนด์ยีลด์",
        market_relevance="Macro policy pressure on non-yielding assets",
    ),
    ThemeRule(
        topic="US dollar strength",
        keywords=("dollar", "dxy", "greenback", "usd"),
        direction_for_gold="bearish_for_gold",
        strength=0.8,
        summary_th="การแข็งค่าของดอลลาร์ยังเป็นแรงกดดันต่อทองคำ",
        driver_th="การเคลื่อนไหวของดอลลาร์สหรัฐ",
        narrative_th="เมื่อดอลลาร์แข็งค่า ราคาทองคำมักเผชิญแรงกดดันเชิงเปรียบเทียบสำหรับผู้ถือสกุลเงินอื่น",
        watchout_th="จับตาการเคลื่อนไหวของดอลลาร์ หากแข็งค่าต่ออาจจำกัด upside ของทอง",
        market_relevance="Dollar strength can cap precious-metals upside",
    ),
    ThemeRule(
        topic="Geopolitical risk",
        keywords=("iran", "israel", "war", "attack", "missile", "hormuz", "strait", "geopolitical", "conflict"),
        direction_for_gold="bullish_for_gold",
        strength=0.85,
        summary_th="ความเสี่ยงภูมิรัฐศาสตร์ยังหนุนแรงซื้อเชิง safe haven",
        driver_th="ความตึงเครียดทางภูมิรัฐศาสตร์",
        narrative_th="ประเด็นความตึงเครียดทางภูมิรัฐศาสตร์มักช่วยหนุนความต้องการถือทองคำในฐานะสินทรัพย์ปลอดภัย",
        watchout_th="จับตาความคืบหน้าความขัดแย้งและเส้นทางขนส่งพลังงานสำคัญ",
        market_relevance="Safe-haven demand can support gold during geopolitical stress",
    ),
    ThemeRule(
        topic="Energy market disruption",
        keywords=("oil", "brent", "wti", "lng", "energy", "shipping", "supply"),
        direction_for_gold="bullish_for_gold",
        strength=0.7,
        summary_th="ความเสี่ยงด้านพลังงานอาจเพิ่มแรงกังวลเงินเฟ้อและหนุน safe haven",
        driver_th="ความผันผวนของตลาดพลังงานและอุปทาน",
        narrative_th="หากพลังงานผันผวนจากความเสี่ยงด้านอุปทาน ตลาดอาจกลับมากังวลเงินเฟ้อควบคู่กับความต้องการป้องกันความเสี่ยง",
        watchout_th="จับตาราคาน้ำมันและความต่อเนื่องของ supply disruption",
        market_relevance="Energy stress can feed inflation and risk aversion at the same time",
    ),
    ThemeRule(
        topic="Growth slowdown risk",
        keywords=("recession", "slowdown", "weak demand", "contraction", "manufacturing slump"),
        direction_for_gold="bullish_for_gold",
        strength=0.65,
        summary_th="สัญญาณชะลอตัวเศรษฐกิจยังช่วยพยุงแรงซื้อป้องกันความเสี่ยง",
        driver_th="ความเสี่ยงเศรษฐกิจชะลอตัว",
        narrative_th="หากภาพรวมเศรษฐกิจอ่อนลง ความต้องการลดความเสี่ยงมักกลับมาสนับสนุนทองคำบางส่วน",
        watchout_th="จับตาว่าตลาดมองเศรษฐกิจชะลอเป็น risk-off จริงหรือไม่",
        market_relevance="Growth fear can support defensive positioning",
    ),
)

ASSET_CONFIG = {
    "XAUUSD": {
        "news_category": "macro",
        "primary_reference": {
            "symbol": "GC=F",
            "label": "COMEX gold futures proxy",
        },
        "drivers": [
            {"key": "silver", "symbol": "SI=F", "label": "COMEX silver futures proxy"},
            {"key": "us_dollar_index", "symbol": "DX-Y.NYB", "label": "US Dollar Index proxy"},
            {"key": "wti_crude", "symbol": "CL=F", "label": "WTI crude futures"},
            {"key": "us_10y_yield", "symbol": "^TNX", "label": "US 10Y Treasury yield index"},
            {"key": "vix", "symbol": "^VIX", "label": "CBOE Volatility Index"},
        ],
        "news_queries": (None,),
    }
}


def build_morning_macro_brief(asset: str = "XAUUSD", lang: str = "th", news_limit: int = 12) -> dict:
    """Build a morning macro brief with freshness and consistency checks."""
    asset_key = (asset or "XAUUSD").strip().upper()
    config = ASSET_CONFIG.get(asset_key, ASSET_CONFIG["XAUUSD"])
    as_of = datetime.now(timezone.utc)

    news_payload, news_errors = _collect_news(config["news_category"], config["news_queries"], news_limit)
    market_snapshot, snapshot_errors = _collect_snapshot(config, as_of)

    normalized_news = _normalize_news(news_payload, as_of)
    themes = _cluster_themes(normalized_news)
    consistency = _assess_consistency(themes, market_snapshot)
    freshness = _compute_freshness(normalized_news, market_snapshot, as_of)
    confidence_level = _compute_confidence(freshness, consistency, themes, snapshot_errors, news_errors)
    data_status = _compute_data_status(freshness, market_snapshot, normalized_news)
    report_mode = _compute_report_mode(market_snapshot, normalized_news)
    summary_bullets = _build_summary_bullets(themes, market_snapshot, consistency, data_status)
    narrative = _build_narrative(themes, market_snapshot, consistency, data_status)
    watchouts = _build_watchouts(themes, freshness, data_status)
    formatted_brief = _render_brief(asset_key, as_of, summary_bullets, narrative, watchouts, confidence_level, data_status)

    return {
        "run_type": "morning_macro_brief",
        "asset_focus": asset_key,
        "language": lang,
        "as_of": as_of.isoformat(),
        "data_status": data_status,
        "report_mode": report_mode,
        "confidence_level": confidence_level,
        "freshness": freshness,
        "market_snapshot": market_snapshot,
        "themes": themes,
        "consistency_status": consistency["status"],
        "consistency_notes": consistency["notes"],
        "summary_bullets_th": summary_bullets,
        "narrative_th": narrative,
        "watchouts_th": watchouts,
        "news_items": normalized_news,
        "errors": news_errors + snapshot_errors,
        "formatted_brief_th": formatted_brief,
    }


def _collect_news(category: str, queries: tuple[str | None, ...], limit: int) -> tuple[list[dict], list[str]]:
    items: list[dict] = []
    errors: list[str] = []
    seen_errors: set[str] = set()
    per_query_limit = max(4, limit // max(1, len(queries)))

    for query in queries:
        payload = fetch_news_summary(query, category=category, limit=per_query_limit)
        payload_items = payload.get("items", [])
        if not payload.get("feedparser_available", True):
            _push_unique(errors, seen_errors, "feedparser unavailable")
        if payload_items and isinstance(payload_items[0], dict) and payload_items[0].get("error"):
            _push_unique(errors, seen_errors, payload_items[0]["error"])
            continue
        items.extend(payload_items)

    return items, errors


def _collect_snapshot(config: dict, as_of: datetime) -> tuple[dict, list[str]]:
    errors: list[str] = []
    primary_meta = config["primary_reference"]
    primary = get_price(primary_meta["symbol"])
    if "error" in primary:
        errors.append(f"{primary_meta['symbol']}: {primary['error']}")

    drivers = []
    for driver in config["drivers"]:
        data = get_price(driver["symbol"])
        if "error" in data:
            errors.append(f"{driver['symbol']}: {data['error']}")
            continue
        drivers.append(
            {
                "key": driver["key"],
                "instrument": driver["symbol"],
                "label": driver["label"],
                "price": data.get("price"),
                "change": data.get("change"),
                "change_pct": data.get("change_pct"),
                "currency": data.get("currency"),
                "market_state": data.get("market_state"),
                "snapshot_time": data.get("timestamp") or as_of.isoformat(),
                "source": data.get("source", "Yahoo Finance"),
            }
        )

    snapshot = {
        "gold_reference": {
            "instrument": primary_meta["symbol"],
            "label": primary_meta["label"],
            "price": primary.get("price"),
            "change": primary.get("change"),
            "change_pct": primary.get("change_pct"),
            "currency": primary.get("currency"),
            "market_state": primary.get("market_state"),
            "snapshot_time": primary.get("timestamp") or as_of.isoformat(),
            "source": primary.get("source", "Yahoo Finance"),
            "error": primary.get("error"),
        },
        "drivers": drivers,
    }
    return snapshot, errors


def _normalize_news(items: list[dict], as_of: datetime) -> list[dict]:
    deduped: dict[str, dict] = {}
    for item in items:
        title = (item.get("title") or "").strip()
        url = (item.get("url") or "").strip()
        if not title and not url:
            continue
        key = (url or title).lower()
        if key in deduped:
            continue
        published_at = _parse_datetime(item.get("published_at") or item.get("published"))
        normalized = {
            "title": title,
            "url": url,
            "source": item.get("source", ""),
            "published": item.get("published", ""),
            "published_at": published_at.isoformat() if published_at else None,
            "age_hours": round((as_of - published_at).total_seconds() / 3600, 2) if published_at else None,
            "summary": item.get("summary", ""),
            "tags": _classify_tags(title, item.get("summary", "")),
        }
        if not _is_relevant_news(normalized):
            continue
        deduped[key] = normalized

    news_items = list(deduped.values())
    news_items.sort(key=lambda entry: entry.get("published_at") or "", reverse=True)
    return news_items


def _classify_tags(title: str, summary: str) -> list[str]:
    text = f"{title} {summary}".lower()
    tags = set()
    if any(token in text for token in ("fed", "inflation", "yield", "rate", "treasury", "payroll", "cpi")):
        tags.add("fed")
    if any(token in text for token in ("iran", "israel", "war", "missile", "hormuz", "strait", "conflict")):
        tags.add("geopolitics")
    if any(token in text for token in ("oil", "brent", "wti", "lng", "shipping", "supply")):
        tags.add("energy")
    if any(token in text for token in ("dollar", "dxy", "usd", "greenback")):
        tags.add("usd")
    if any(token in text for token in ("gold", "bullion", "precious")):
        tags.add("gold")
    if any(token in text for token in ("xau", "bullion", "safe haven", "haven demand")):
        tags.add("gold_market")
    return sorted(tags)


def _is_relevant_news(item: dict) -> bool:
    source = (item.get("source") or "").lower()
    title = (item.get("title") or "").lower()
    summary = (item.get("summary") or "").lower()
    tags = set(item.get("tags") or [])
    text = f"{title} {summary}"

    if any(keyword in text for keyword in NEGATIVE_NEWS_KEYWORDS):
        return False
    if any(source_key in source for source_key in FINANCE_SOURCES) and any(token in text for token in MARKET_NEWS_KEYWORDS):
        return True
    if tags.intersection({"fed", "geopolitics", "energy", "usd", "gold_market"}):
        return True
    if "gold" in text and any(token in text for token in ("price", "bullion", "xau", "ounces", "safe haven", "interest rate")):
        return True
    return False


def _cluster_themes(news_items: list[dict]) -> list[dict]:
    grouped: dict[str, dict] = {}
    for rule in THEME_RULES:
        matched = []
        for item in news_items:
            haystack = f"{item.get('title', '')} {item.get('summary', '')}".lower()
            if any(keyword in haystack for keyword in rule.keywords):
                matched.append(item)
        if not matched:
            continue
        grouped[rule.topic] = {
            "topic": rule.topic,
            "direction_for_gold": rule.direction_for_gold,
            "importance": round(min(0.99, rule.strength + 0.03 * min(len(matched), 3) + _recency_bonus(matched)), 2),
            "market_relevance": rule.market_relevance,
            "evidence": [],
            "driver_th": rule.driver_th,
            "latest_published_at": matched[0].get("published_at"),
            "matched_item_count": len(matched),
            "summary_th": rule.summary_th,
            "narrative_th": rule.narrative_th,
            "watchout_th": rule.watchout_th,
            "_matched_items": matched,
        }

    themes = list(grouped.values())
    themes.sort(key=lambda item: (item["importance"], item["matched_item_count"]), reverse=True)

    if themes:
        return _finalize_theme_evidence(themes[:4])

    if not news_items:
        return [
            {
                "topic": "No fresh headlines available",
                "direction_for_gold": "mixed",
                "importance": 0.3,
                "market_relevance": "Insufficient news flow for a high-conviction read",
                "evidence": [],
                "latest_published_at": None,
                "matched_item_count": 0,
                "summary_th": "ยังไม่มี headline สดพอสำหรับสรุปธีมหลักด้วยความมั่นใจสูง",
                "narrative_th": "ระบบยังไม่พบข่าวสดเพียงพอ จึงควรให้น้ำหนักกับ price action และ market snapshot มากกว่าการตีความเชิงเหตุการณ์",
                "watchout_th": "ระวังการสรุปเชิงเหตุผลเกินข้อมูลเมื่อ news flow บาง",
            }
        ]

    fallback_titles = [item["title"] for item in news_items[:3]]
    return [
        {
            "topic": "Broader macro headlines",
            "direction_for_gold": "mixed",
            "importance": 0.45,
            "market_relevance": "Generic macro flow without a dominant rule-based cluster",
            "evidence": fallback_titles,
            "latest_published_at": news_items[0].get("published_at"),
            "matched_item_count": min(3, len(news_items)),
            "summary_th": "ภาพรวมข่าวมหภาคยังคละกันและยังไม่มีธีมเดียวที่เด่นชัดมากพอ",
            "narrative_th": "headline ล่าสุดยังสะท้อนสภาวะตลาดแบบผสม ทำให้ควรใช้การยืนยันทิศทางจากราคาและดอลลาร์ร่วมด้วยก่อนสรุป bias ของทองคำ",
            "watchout_th": "หากไม่มีธีมข่าวเด่น ตลาดอาจตอบสนองต่อข้อมูลเศรษฐกิจหรือกระแสเงินระยะสั้นมากขึ้น",
        }
    ]


def _assess_consistency(themes: list[dict], market_snapshot: dict) -> dict:
    directional_score = 0.0
    for theme in themes:
        if theme["direction_for_gold"] == "bullish_for_gold":
            directional_score += theme["importance"]
        elif theme["direction_for_gold"] == "bearish_for_gold":
            directional_score -= theme["importance"]

    gold_reference = market_snapshot.get("gold_reference", {})
    gold_change = gold_reference.get("change_pct")
    driver_map = {item["key"]: item for item in market_snapshot.get("drivers", [])}
    dollar_change = (driver_map.get("us_dollar_index") or {}).get("change_pct")
    yield_change = (driver_map.get("us_10y_yield") or {}).get("change_pct")

    notes = []
    status = "mixed"

    if gold_change is None:
        notes.append("Gold proxy price is unavailable, so news direction cannot be fully confirmed.")
        return {"status": "conflicted", "notes": notes}

    price_supports_bullish = gold_change > 0.15
    price_supports_bearish = gold_change < -0.15
    dollar_supports_bearish = dollar_change is not None and dollar_change > 0.1
    dollar_supports_bullish = dollar_change is not None and dollar_change < -0.1

    if directional_score >= 0.7 and (price_supports_bullish or dollar_supports_bullish):
        status = "confirmed"
        notes.append("Safe-haven or supportive macro themes are aligned with the latest gold proxy / dollar move.")
    elif directional_score <= -0.7 and (price_supports_bearish or dollar_supports_bearish or (yield_change is not None and yield_change > 0.1)):
        status = "confirmed"
        notes.append("Rate / dollar pressure is aligned with the latest gold proxy move.")
    elif abs(directional_score) < 0.5:
        status = "mixed"
        notes.append("Headline flow is mixed, so price confirmation matters more than the narrative.")
    else:
        status = "conflicted"
        notes.append("News direction and current market behavior are not fully aligned.")

    if dollar_change is not None:
        notes.append(f"US dollar proxy move: {dollar_change:+.2f}%")
    if yield_change is not None:
        notes.append(f"US 10Y yield proxy move: {yield_change:+.2f}%")
    return {"status": status, "notes": notes}


def _compute_freshness(news_items: list[dict], market_snapshot: dict, as_of: datetime) -> dict:
    published_times = [_parse_datetime(item.get("published_at")) for item in news_items if item.get("published_at")]
    published_times = [dt for dt in published_times if dt]

    if not published_times:
        news_status = "missing"
    else:
        newest = max(published_times)
        oldest = min(published_times)
        age = as_of - newest
        if age <= timedelta(hours=12):
            news_status = "fresh"
        elif age <= timedelta(hours=24):
            news_status = "stale"
        else:
            news_status = "missing"
    primary_time = _parse_datetime(market_snapshot.get("gold_reference", {}).get("snapshot_time"))
    if primary_time is None:
        snapshot_status = "missing"
    else:
        snapshot_age = as_of - primary_time
        snapshot_status = "fresh" if snapshot_age <= timedelta(minutes=30) else "stale"

    return {
        "news_status": news_status,
        "snapshot_status": snapshot_status,
        "newest_news_at": max(published_times).isoformat() if published_times else None,
        "oldest_news_at": min(published_times).isoformat() if published_times else None,
        "snapshot_time": market_snapshot.get("gold_reference", {}).get("snapshot_time"),
    }


def _compute_confidence(
    freshness: dict,
    consistency: dict,
    themes: list[dict],
    snapshot_errors: list[str],
    news_errors: list[str],
) -> str:
    score = 2
    if freshness["news_status"] == "fresh":
        score += 1
    elif freshness["news_status"] != "stale":
        score -= 1
    if freshness["snapshot_status"] == "fresh":
        score += 1
    elif freshness["snapshot_status"] != "stale":
        score -= 1
    if consistency["status"] == "confirmed":
        score += 1
    elif consistency["status"] == "conflicted":
        score -= 1
    if not themes:
        score -= 1
    if snapshot_errors or news_errors:
        score -= 1

    if score >= 4:
        return "high"
    if score >= 2:
        return "medium"
    return "low"


def _compute_data_status(freshness: dict, market_snapshot: dict, news_items: list[dict]) -> str:
    gold_price = market_snapshot.get("gold_reference", {}).get("price")
    if gold_price is None and not news_items:
        return "partial_data"
    if gold_price is None:
        return "partial_data"
    if freshness["news_status"] == "missing" or freshness["snapshot_status"] == "missing":
        return "partial_data"
    if freshness["news_status"] == "stale" or freshness["snapshot_status"] == "stale":
        return "partial_data"
    return "complete"


def _compute_report_mode(market_snapshot: dict, news_items: list[dict]) -> str:
    gold_price = market_snapshot.get("gold_reference", {}).get("price")
    has_news = bool(news_items)
    if gold_price is not None and has_news:
        return "full"
    if has_news:
        return "news_only"
    if gold_price is not None:
        return "snapshot_only"
    return "empty"


def _build_summary_bullets(themes: list[dict], market_snapshot: dict, consistency: dict, data_status: str) -> list[str]:
    bullets: list[str] = []
    gold_reference = market_snapshot.get("gold_reference", {})
    gold_price = gold_reference.get("price")
    gold_change = gold_reference.get("change_pct")
    if gold_price is not None:
        if gold_change is None:
            bullets.append(f"Gold proxy ผ่าน {gold_reference.get('instrument')} อยู่ที่ {gold_price:,.2f} ดอลลาร์ แต่ยังไม่มีข้อมูลการเปลี่ยนแปลงที่ครบถ้วน")
        else:
            bullets.append(
                f"Gold proxy ผ่าน {gold_reference.get('instrument')} เคลื่อนไหวที่ {gold_price:,.2f} ดอลลาร์ ({gold_change:+.2f}%)"
            )
    else:
        bullets.append("ยังไม่สามารถยืนยันราคา gold proxy ได้ ทำให้ brief ฉบับนี้อยู่ในสถานะ partial data")

    for theme in themes[:3]:
        bullets.append(theme["summary_th"])

    if consistency["status"] == "conflicted":
        bullets.append("ข่าวกับพฤติกรรมตลาดยังไม่ยืนยันกันเต็มที่ จึงควรใช้มุมมองแบบระวัง")
    elif consistency["status"] == "mixed":
        bullets.append("ภาพรวมยังผสมกัน ระหว่างปัจจัยหนุนเชิง safe haven กับแรงกดดันจากดอลลาร์/ดอกเบี้ย")

    if data_status != "complete":
        bullets.append("คุณภาพข้อมูลเช้านี้ยังไม่สมบูรณ์เต็มที่ ควรใช้ร่วมกับการเช็กตลาดสดอีกครั้งก่อนตัดสินใจ")

    return bullets[:4]


def _build_narrative(themes: list[dict], market_snapshot: dict, consistency: dict, data_status: str) -> list[str]:
    paragraphs: list[str] = []
    bearish = [theme for theme in themes if theme["direction_for_gold"] == "bearish_for_gold"]
    bullish = [theme for theme in themes if theme["direction_for_gold"] == "bullish_for_gold"]
    mixed = [theme for theme in themes if theme["direction_for_gold"] == "mixed"]

    if bearish:
        paragraphs.append(
            "ฝั่งแรงกดดันหลักต่อทองคำยังมาจาก"
            f" {_join_driver_labels(bearish[:2])} โดยรวมแล้วตลาดยังระวังผลของดอกเบี้ยและค่าเงินต่อสินทรัพย์ที่ไม่มีดอกผล"
        )
    if bullish:
        paragraphs.append(
            "ขณะเดียวกัน แรงหนุนเชิงป้องกันความเสี่ยงยังมาจาก"
            f" {_join_driver_labels(bullish[:2])} ซึ่งช่วยพยุงแรงซื้อ safe haven ไว้บางส่วน"
        )
    elif mixed and not bearish:
        paragraphs.append("headline ล่าสุดยังสะท้อนสภาวะตลาดแบบผสม ทำให้ควรใช้การยืนยันทิศทางจากราคาและดอลลาร์ร่วมด้วยก่อนสรุป bias ของทองคำ")

    driver_map = {item["key"]: item for item in market_snapshot.get("drivers", [])}
    dollar = driver_map.get("us_dollar_index")
    oil = driver_map.get("wti_crude")
    yield_10y = driver_map.get("us_10y_yield")
    gold_change = market_snapshot.get("gold_reference", {}).get("change_pct")
    parts = []
    if gold_change is not None:
        parts.append(f"gold proxy ล่าสุดเปลี่ยนแปลง {gold_change:+.2f}%")
    if dollar and dollar.get("change_pct") is not None:
        parts.append(f"ดอลลาร์เคลื่อนไหว {dollar['change_pct']:+.2f}%")
    if yield_10y and yield_10y.get("change_pct") is not None:
        parts.append(f"ผลตอบแทนพันธบัตร 10 ปีเปลี่ยนแปลง {yield_10y['change_pct']:+.2f}%")
    if oil and oil.get("change_pct") is not None:
        parts.append(f"น้ำมัน WTI เปลี่ยนแปลง {oil['change_pct']:+.2f}%")

    if parts:
        market_line = " / ".join(parts)
        suffix = {
            "confirmed": "ภาพราคายังสอดคล้องกับ narrative หลักมากกว่า",
            "mixed": "ตลาดยังตอบรับแบบคละกัน จึงยังไม่ควรสรุป bias แรงเกินไป",
            "conflicted": "พฤติกรรมตลาดยังไม่ยืนยันธีมข่าวอย่างชัดเจน",
        }[consistency["status"]]
        paragraphs.append(f"ฝั่ง market snapshot พบว่า {market_line} ซึ่งหมายความว่า{suffix}")

    if data_status != "complete":
        paragraphs.append("brief ฉบับนี้ควรอ่านในเชิงสถานการณ์เบื้องต้น เนื่องจาก freshness หรือความครบถ้วนของข้อมูลยังไม่ถึงระดับ complete")

    return paragraphs[:3]


def _build_watchouts(themes: list[dict], freshness: dict, data_status: str) -> list[str]:
    watchouts = []
    seen = set()
    for theme in themes[:3]:
        text = theme["watchout_th"]
        if text not in seen:
            watchouts.append(text)
            seen.add(text)

    if freshness["news_status"] != "fresh":
        watchouts.append("headline บางส่วนอาจไม่สดพอ จึงควรเช็กข่าวล่าสุดซ้ำก่อนใช้งานจริง")
    if freshness["snapshot_status"] != "fresh":
        watchouts.append("market snapshot ล่าสุดอาจเก่าเกิน threshold สำหรับ morning brief แบบ intraday")
    if data_status != "complete":
        watchouts.append("หากจะใช้เพื่อวาง bias เชิงเทรด ควรยืนยันราคาตลาดสดอีกครั้งก่อน")
    return watchouts[:4]


def _finalize_theme_evidence(themes: list[dict]) -> list[dict]:
    used_titles: set[str] = set()
    finalized: list[dict] = []

    for theme in themes:
        evidence: list[str] = []
        for item in theme.get("_matched_items", []):
            title = item.get("title", "")
            normalized_title = title.strip().lower()
            if not title or normalized_title in used_titles:
                continue
            evidence.append(title)
            used_titles.add(normalized_title)
            if len(evidence) >= 3:
                break

        if not evidence:
            for item in theme.get("_matched_items", []):
                title = item.get("title", "")
                if title:
                    evidence.append(title)
                    break

        cleaned = {k: v for k, v in theme.items() if not k.startswith("_")}
        cleaned["evidence"] = evidence
        finalized.append(cleaned)

    return finalized


def _join_driver_labels(themes: list[dict]) -> str:
    labels = [theme.get("driver_th", theme.get("summary_th", "")) for theme in themes if theme.get("driver_th") or theme.get("summary_th")]
    if not labels:
        return "หลายปัจจัยพร้อมกัน"
    if len(labels) == 1:
        return labels[0]
    if len(labels) == 2:
        return f"{labels[0]} และ {labels[1]}"
    return ", ".join(labels[:-1]) + f" และ {labels[-1]}"


def _recency_bonus(items: list[dict]) -> float:
    published_at = _parse_datetime(items[0].get("published_at")) if items else None
    if published_at is None:
        return 0.0
    age_hours = (datetime.now(timezone.utc) - published_at).total_seconds() / 3600
    if age_hours <= 6:
        return 0.03
    if age_hours <= 12:
        return 0.02
    return 0.0


def _render_brief(
    asset: str,
    as_of: datetime,
    summary_bullets: list[str],
    narrative: list[str],
    watchouts: list[str],
    confidence_level: str,
    data_status: str,
) -> str:
    local = as_of.astimezone(ICT)
    lines = [format_buddhist_date(local), "📌 หัวข้อประเด็นสำคัญ :"]
    for bullet in summary_bullets:
        lines.append(f"▪️{bullet}")
    lines.append("_____________________________")
    lines.append(f"🤝 ปัจจัยหลักที่กำลังชี้นำ{_asset_label_th(asset)}")
    lines.extend(narrative)
    lines.append("___")
    lines.append("⚠️ สิ่งที่ต้องระวังวันนี้")
    lines.extend(watchouts)
    lines.append("")
    lines.append(
        f"as of {local.strftime('%H:%M')} ICT | confidence: {confidence_level} | data_status: {data_status}"
    )
    return "\n".join(lines)


def format_buddhist_date(dt: datetime) -> str:
    return f"{dt.day} {THAI_MONTHS[dt.month]} {dt.year + 543}"


def _asset_label_th(asset: str) -> str:
    labels = {
        "XAUUSD": "ราคาทองคำ",
    }
    return labels.get(asset, asset)


def _parse_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)
    except Exception:
        return None


def _push_unique(target: list[str], seen: set[str], value: str) -> None:
    if value not in seen:
        target.append(value)
        seen.add(value)
