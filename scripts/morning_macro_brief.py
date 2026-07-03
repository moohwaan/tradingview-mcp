#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tradingview_mcp.core.services.morning_brief_service import build_morning_macro_brief

OUTPUT_DIR = ROOT / "outputs"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate a daily morning macro brief Markdown file from the service layer."
    )
    parser.add_argument("--asset", default="XAUUSD", help="Asset focus, default is XAUUSD")
    parser.add_argument("--lang", default="th", help="Output language, default is th")
    parser.add_argument(
        "--news-limit",
        type=int,
        default=12,
        help="Approximate number of news items to consider, default is 12",
    )
    parser.add_argument(
        "--output-dir",
        default=str(OUTPUT_DIR),
        help="Directory to write the Markdown and JSON artifacts into",
    )
    return parser


def make_slug(asset: str) -> str:
    return "".join(ch.lower() if ch.isalnum() else "-" for ch in asset).strip("-") or "asset"


def render_markdown(result: dict) -> str:
    lines = [
        f"# Morning Macro Brief - {result['asset_focus']}",
        "",
        result["formatted_brief_th"],
        "",
        "## Structured Status",
        "",
        f"- `as_of`: `{result['as_of']}`",
        f"- `data_status`: `{result['data_status']}`",
        f"- `report_mode`: `{result.get('report_mode', 'unknown')}`",
        f"- `confidence_level`: `{result['confidence_level']}`",
        f"- `consistency_status`: `{result['consistency_status']}`",
        "",
    ]

    if result.get("consistency_notes"):
        lines.extend(["## Consistency Notes", ""])
        for note in result["consistency_notes"]:
            lines.append(f"- {note}")
        lines.append("")

    if result.get("themes"):
        lines.extend(["## Themes", ""])
        for theme in result["themes"]:
            lines.append(
                f"- `{theme['topic']}` | direction: `{theme['direction_for_gold']}` | importance: `{theme['importance']}`"
            )
            if theme.get("evidence"):
                for evidence in theme["evidence"]:
                    lines.append(f"  - evidence: {evidence}")
        lines.append("")

    if result.get("errors"):
        lines.extend(["## Errors", ""])
        for error in result["errors"]:
            lines.append(f"- {error}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    result = build_morning_macro_brief(args.asset, args.lang, args.news_limit)
    date_prefix = result["as_of"][:10]
    asset_slug = make_slug(args.asset)
    md_path = output_dir / f"{asset_slug}-morning-brief-{date_prefix}.md"
    json_path = output_dir / f"{asset_slug}-morning-brief-{date_prefix}.json"

    md_path.write_text(render_markdown(result), encoding="utf-8")
    json_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print(
        json.dumps(
            {
                "asset": args.asset,
                "markdown": str(md_path),
                "json": str(json_path),
                "data_status": result["data_status"],
                "report_mode": result.get("report_mode"),
                "confidence_level": result["confidence_level"],
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
