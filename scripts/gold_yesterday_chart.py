from __future__ import annotations

import json
import sys
import urllib.request
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from tradingview_mcp.core.services.proxy_manager import build_opener_with_proxy

SYMBOL = "GC=F"
INTERVAL = "1h"
RANGE = "5d"
USER_AGENT = "tradingview-mcp/yesterday-gold-chart"
BASE_URL = "https://query1.finance.yahoo.com/v8/finance/chart"
OUTPUT_DIR = Path(__file__).resolve().parents[1] / "outputs"
LOCAL_TZ = ZoneInfo("Asia/Bangkok")


def fetch_ohlcv(symbol: str, interval: str, period: str) -> list[dict]:
    url = f"{BASE_URL}/{symbol}?interval={interval}&range={period}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})

    data = None
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception:
        opener = build_opener_with_proxy(USER_AGENT)
        with opener.open(url, timeout=18) as resp:
            data = json.loads(resp.read().decode("utf-8"))

    result = data["chart"]["result"][0]
    timestamps = result["timestamp"]
    quote = result["indicators"]["quote"][0]

    candles = []
    for i, ts in enumerate(timestamps):
        open_ = quote["open"][i]
        high = quote["high"][i]
        low = quote["low"][i]
        close = quote["close"][i]
        volume = quote["volume"][i]
        if None in (open_, high, low, close):
            continue
        candles.append(
            {
                "timestamp": ts,
                "datetime_utc": datetime.fromtimestamp(ts, tz=timezone.utc),
                "open": round(open_, 4),
                "high": round(high, 4),
                "low": round(low, 4),
                "close": round(close, 4),
                "volume": volume or 0,
            }
        )
    return candles


def select_yesterday(candles: list[dict]) -> tuple[str, list[dict]]:
    by_day: dict[str, list[dict]] = defaultdict(list)
    for candle in candles:
        local_dt = candle["datetime_utc"].astimezone(LOCAL_TZ)
        candle["datetime_local"] = local_dt
        key = local_dt.date().isoformat()
        by_day[key].append(candle)

    yesterday_key = (datetime.now(LOCAL_TZ).date()).fromordinal(datetime.now(LOCAL_TZ).date().toordinal() - 1).isoformat()
    if yesterday_key not in by_day:
        ordered_days = sorted(by_day)
        raise RuntimeError(
            f"No candles found for yesterday in Asia/Bangkok ({yesterday_key}). Available days: {ordered_days}"
        )

    return yesterday_key, by_day[yesterday_key]


def build_svg(day_key: str, candles: list[dict]) -> str:
    width = 1000
    height = 520
    margin_left = 70
    margin_right = 30
    margin_top = 30
    margin_bottom = 80
    plot_width = width - margin_left - margin_right
    plot_height = height - margin_top - margin_bottom

    lows = [c["low"] for c in candles]
    highs = [c["high"] for c in candles]
    min_price = min(lows)
    max_price = max(highs)
    price_span = max(max_price - min_price, 1)
    pad = price_span * 0.08
    y_min = min_price - pad
    y_max = max_price + pad

    def y_for(price: float) -> float:
        ratio = (price - y_min) / (y_max - y_min)
        return margin_top + plot_height - (ratio * plot_height)

    x_step = plot_width / max(len(candles) - 1, 1)
    points = []
    x_labels = []
    for idx, candle in enumerate(candles):
        x = margin_left + idx * x_step
        y = y_for(candle["close"])
        points.append(f"{x:.2f},{y:.2f}")
        x_labels.append((x, candle["datetime_utc"].strftime("%H:%M")))

    y_ticks = []
    for tick in range(6):
        price = y_min + ((y_max - y_min) * tick / 5)
        y = y_for(price)
        y_ticks.append((price, y))

    polyline = " ".join(points)
    start = candles[0]["close"]
    end = candles[-1]["close"]
    stroke = "#0f766e" if end >= start else "#b91c1c"

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#f8fafc"/>',
        '<rect x="18" y="18" width="964" height="484" rx="18" fill="#ffffff" stroke="#cbd5e1"/>',
        f'<text x="{margin_left}" y="58" font-family="Helvetica, Arial, sans-serif" font-size="24" font-weight="700" fill="#0f172a">GC=F Gold Futures - {day_key} (Asia/Bangkok)</text>',
        f'<text x="{margin_left}" y="84" font-family="Helvetica, Arial, sans-serif" font-size="14" fill="#475569">Hourly closes from Yahoo Finance via tradingview-mcp data path</text>',
    ]

    for price, y in y_ticks:
        svg.append(
            f'<line x1="{margin_left}" y1="{y:.2f}" x2="{width - margin_right}" y2="{y:.2f}" stroke="#e2e8f0" />'
        )
        svg.append(
            f'<text x="{margin_left - 10}" y="{y + 5:.2f}" text-anchor="end" font-family="Helvetica, Arial, sans-serif" font-size="12" fill="#64748b">{price:,.1f}</text>'
        )

    svg.append(
        f'<polyline fill="none" stroke="{stroke}" stroke-width="3" points="{polyline}" />'
    )

    for idx, candle in enumerate(candles):
        x = margin_left + idx * x_step
        y = y_for(candle["close"])
        svg.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="3" fill="{stroke}" />')
        if idx % 2 == 0 or idx == len(candles) - 1:
            label = candle["datetime_local"].strftime("%H:%M")
            svg.append(
                f'<text x="{x:.2f}" y="{height - 38}" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="11" fill="#64748b">{label}</text>'
            )

    svg.append(
        f'<line x1="{margin_left}" y1="{margin_top + plot_height}" x2="{width - margin_right}" y2="{margin_top + plot_height}" stroke="#94a3b8" />'
    )
    svg.append("</svg>")
    return "\n".join(svg)


def build_markdown(day_key: str, candles: list[dict], svg_path: Path) -> str:
    open_ = candles[0]["open"]
    high = max(c["high"] for c in candles)
    low = min(c["low"] for c in candles)
    close = candles[-1]["close"]
    change = close - open_
    change_pct = (change / open_) * 100 if open_ else 0
    range_points = high - low
    midpoint = (high + low) / 2
    close_vs_mid = close - midpoint

    tone = "bullish intraday" if change > 0 else "bearish intraday" if change < 0 else "flat intraday"
    close_bias = "closed in the upper half of the day's range" if close >= midpoint else "closed in the lower half of the day's range"

    return "\n".join(
        [
            f"# Gold Analysis for {day_key}",
            "",
            f"Symbol: `{SYMBOL}`",
            f"Interval: `{INTERVAL}`",
            f"Data timezone used in this report: `Asia/Bangkok`",
            "",
            f"![GC=F chart]({svg_path.resolve()})",
            "",
            "## Summary",
            "",
            f"- Open: `{open_:,.1f}`",
            f"- High: `{high:,.1f}`",
            f"- Low: `{low:,.1f}`",
            f"- Close: `{close:,.1f}`",
            f"- Net change: `{change:+,.1f}` ({change_pct:+.2f}%)",
            f"- Intraday range: `{range_points:,.1f}` points",
            "",
            "## Quick Read",
            "",
            f"- The session was `{tone}`.",
            f"- Price `{close_bias}`.",
            f"- Close vs midpoint: `{close_vs_mid:+,.1f}` points.",
            f"- Bars captured: `{len(candles)}` hourly candles.",
            "",
            "## Notes",
            "",
            "- This uses Yahoo Finance hourly candles for `GC=F`.",
            "- `GC=F` is COMEX gold futures, not spot `XAUUSD`.",
            "- The script treats 'yesterday' using `Asia/Bangkok` calendar dates.",
            "",
        ]
    )


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    candles = fetch_ohlcv(SYMBOL, INTERVAL, RANGE)
    day_key, yesterday_candles = select_yesterday(candles)

    svg_path = OUTPUT_DIR / f"gold-{day_key}.svg"
    md_path = OUTPUT_DIR / f"gold-{day_key}-analysis.md"

    svg_path.write_text(build_svg(day_key, yesterday_candles), encoding="utf-8")
    md_path.write_text(build_markdown(day_key, yesterday_candles, svg_path), encoding="utf-8")

    print(json.dumps({"date": day_key, "svg": str(svg_path), "markdown": str(md_path)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
