# Morning Analysis Workflow Spec

## Purpose

Define a daily morning analysis workflow for this repository that:

- summarizes overall market context,
- scans a chosen trading universe,
- filters symbols before trade-plan generation,
- produces trade plans only for qualified candidates, and
- returns a concise report the trader can use before market open.

This spec is intentionally designed around the existing service-layer building blocks in this repo. It avoids new abstractions unless implementation requires them.

## Goal

Every morning the workflow should answer four questions:

1. What is today's market regime?
2. Which symbols are qualified for active planning?
3. Which symbols belong on the watchlist but are not ready yet?
4. What are today's execution and risk constraints?

## Existing Building Blocks

The workflow should reuse the current functions and tools:

- `get_market_snapshot()` from `yahoo_finance_service.py`
- `analyze_sentiment()` / MCP tool `market_sentiment`
- `fetch_news_summary()` / MCP tool `financial_news`
- `run_multi_timeframe_analysis()` / MCP tool `get_multi_timeframe_analysis`
- `compute_stock_score()` in `indicators.py`
- `compute_trade_prefilter()` in `indicators.py`
- `compute_trade_setup()` in `indicators.py`
- `compute_trade_quality()` in `indicators.py`
- exchange-specific screening flows already present in `screener_service.py` and `egx_service.py`

## Scope

### In Scope

- A reusable morning analysis service flow
- Output for `market_brief`, `qualified_trades`, `watchlist`, and `risk_rules`
- Support for one selected universe per run
- Reuse of current score, prefilter, setup, and quality logic

### Out of Scope

- Auto execution
- Broker integration
- Intraday re-planning loop
- Portfolio optimization across many open positions
- New scoring framework separate from the current one

## Assumptions

- The user chooses one primary universe per run, such as `EGX`, `NASDAQ`, `NYSE`, `BINANCE`, or a custom watchlist.
- The workflow is used before trading decisions, not as a live execution engine.
- Morning analysis should be conservative: trade plans are generated only for symbols that pass the prefilter.
- The implementation should match current repo style: routing in `server.py`, business logic in `core/services/*`.

## Proposed Workflow

### Step 1. Gather Market Context

Collect top-down context before scanning symbols.

Inputs:

- `market_snapshot`
- `market_sentiment` for a small set of anchor symbols if relevant
- `financial_news`

Expected output:

- `regime`: `bullish`, `selective_bullish`, `mixed`, `risk_off`, or `no_trade`
- `risk_level`: `low`, `medium`, or `high`
- `summary`: short human-readable brief
- `drivers`: key risk-on or risk-off observations

Suggested interpretation rules:

- Strong upside in major indices with contained volatility -> `bullish`
- Mixed index action or conflicting sentiment/news -> `mixed` or `selective_bullish`
- High volatility, sharp market weakness, or strong negative news cluster -> `risk_off`
- Severe instability or missing trusted context -> `no_trade`

This layer should stay simple. It is a gate and summary, not a second full scoring model.

### Step 2. Define Universe

The run should operate on exactly one declared universe.

Example inputs:

- `exchange="EGX"` with stock screener flow
- `exchange="NASDAQ"` with stock screener flow
- `exchange="BINANCE"` with crypto screener flow
- `symbols=[...]` for a manual watchlist mode

Output:

- `universe_type`
- `exchange`
- `timeframe`
- `symbols_considered` or scan count

### Step 3. Generate Candidate Set

Run the existing screener flow for the chosen universe.

Goal:

- produce a limited candidate pool worth evaluating further,
- not a final trade list.

Implementation note:

- Use whichever existing screener path is already most natural for that universe.
- Do not generate full trade setups at this stage.

Suggested result size:

- keep the candidate pool compact, for example top 10 to 30 symbols depending on universe size.

### Step 4. Score Candidates

For each candidate, calculate `compute_stock_score()`.

This score already captures:

- trend and momentum,
- confirmation,
- risk-adjusted technical quality,
- TradingView recommendation proxy, and
- liquidity gates.

Required per-symbol output:

- `stock_score`
- `grade`
- `trend_state`
- `score_breakdown`
- `signals`
- `penalties`
- `liquidity`

### Step 5. Apply Pre-Trade Filter

For each scored candidate, run `compute_trade_prefilter()`.

This is the main transition between "interesting symbol" and "plan-worthy symbol".

The prefilter currently checks:

- score threshold,
- price vs `EMA200`,
- volume participation,
- trend strength via `ADX`,
- acceptable `ATR%`,
- liquidity pass/fail.

Expected classifications:

- `qualified`
- `watchlist`
- `rejected`

Important rule:

- Only `qualified` symbols may continue to trade-plan generation.
- `watchlist` symbols remain visible in the report but do not get a full plan.
- `rejected` symbols should usually be omitted from the final trader-facing report, except optionally in diagnostics.

### Step 6. Build Trade Plans For Qualified Symbols Only

For each `qualified` symbol:

- run `compute_trade_setup()`
- run `compute_trade_quality()`

Expected output:

- setup type
- breakout entry
- pullback entry
- stop loss
- stop distance percent
- target 1
- target 2
- risk/reward
- support/resistance levels
- `trade_quality_score`
- `trade_quality`
- notes

Additional qualification hint:

- Prefer symbols with `trade_quality_score >= 65`
- Prefer `R:R to target 2 >= 2.0`

These thresholds already align with current EGX execution rules.

### Step 7. Confirm Multi-Timeframe Alignment

For the final shortlist, run multi-timeframe confirmation.

Use the existing Weekly -> Daily -> 4H -> 1H -> 15m structure:

- Weekly sets bias
- Daily defines the swing setup
- 4H refines zone
- 1H and 15m help timing

Expected output:

- alignment status
- confidence
- divergent timeframes
- recommended entry timeframe

Suggested use:

- attach this only to final candidates,
- do not spend this cost on all rejected names.

### Step 8. Apply Daily Risk Rules

The report should conclude with trader-facing risk rules.

Minimum fields:

- `max_positions`
- `max_risk_per_trade`
- `max_total_daily_risk`
- `no_trade_conditions`

Suggested default policy for v1:

- keep this static and configurable later,
- do not build portfolio optimization yet.

Example `no_trade_conditions`:

- market regime is `risk_off` or `no_trade`
- higher timeframes conflict materially
- liquidity fails
- `trade_quality_score` below threshold
- risk/reward too weak

## Proposed Output Contract

```json
{
  "run_type": "morning_analysis",
  "timestamp": "ISO-8601 or real-time label",
  "market_brief": {
    "regime": "selective_bullish",
    "risk_level": "medium",
    "summary": "Short narrative summary",
    "drivers": ["..."]
  },
  "universe": {
    "exchange": "EGX",
    "timeframe": "1D",
    "candidate_count": 18
  },
  "qualified_trades": [
    {
      "symbol": "EGX:COMI",
      "stock_score": 78,
      "grade": "Strong",
      "trend_state": "Uptrend",
      "trade_prefilter": {"status": "qualified"},
      "trade_setup": {},
      "trade_quality_score": 72,
      "trade_quality": "Good",
      "multi_timeframe_alignment": {}
    }
  ],
  "watchlist": [
    {
      "symbol": "EGX:HRHO",
      "stock_score": 64,
      "grade": "Watchlist",
      "trade_prefilter": {
        "status": "watchlist",
        "failed_checks": ["volume_participation"]
      }
    }
  ],
  "risk_rules": {
    "max_positions": 3,
    "max_risk_per_trade": "1R",
    "max_total_daily_risk": "3R",
    "no_trade_conditions": [
      "market regime = risk_off",
      "trade quality below threshold"
    ]
  }
}
```

## Suggested Service Design

### Option A: New orchestration service

Create a new service such as:

- `src/tradingview_mcp/core/services/morning_analysis_service.py`

Responsibilities:

- orchestrate the full flow,
- call existing services,
- keep decision logic lightweight,
- return one normalized output object.

This is the preferred path because it preserves the current separation between routing and business logic.

### Option B: Add a thin wrapper to an existing service

Possible but less clean if it mixes market-brief orchestration into an exchange-specific service.

Recommendation:

- prefer Option A.

## Suggested MCP Tool

After service implementation, expose a single MCP tool, for example:

- `morning_trade_plan(exchange: str = "EGX", timeframe: str = "1D", limit: int = 10) -> dict`

Possible future extension:

- optional `symbols` input for watchlist-only mode

Keep v1 simple:

- either `exchange` mode or explicit symbol-list mode,
- not both with complex precedence rules.

## Success Criteria

The first implementation should be considered successful if it can:

1. produce one coherent morning report from a chosen universe,
2. reuse existing score/prefilter/setup/quality functions without duplicating them,
3. avoid generating trade plans for non-qualified symbols,
4. clearly separate `qualified_trades` from `watchlist`, and
5. return output that is readable by both humans and downstream tools.

## Verification Plan

When implementation starts, verify with checks like:

1. Run one universe flow and confirm the report contains `market_brief`, `qualified_trades`, `watchlist`, and `risk_rules`.
2. Confirm symbols that fail prefilter never receive `trade_setup`.
3. Confirm at least one synthetic or representative case each for:
   - `qualified`
   - `watchlist`
   - `rejected`
4. Confirm multi-timeframe confirmation is only applied to the final shortlist.
5. Confirm routing stays thin and business logic lives in services.

## Open Questions Before Implementation

- Which universe should be the default for v1: `EGX`, `NASDAQ`, or `BINANCE`?
- Should `market_brief` use a fixed set of anchor instruments per exchange, or a global macro snapshot for all runs?
- Should watchlist-only mode be part of v1 or deferred?
- Should the report include rejected-symbol diagnostics, or keep the output trader-clean by default?

## Recommendation

Implement v1 as:

- one new orchestration service,
- one MCP tool,
- one exchange at a time per run,
- conservative gating with current thresholds,
- trader-facing output optimized for pre-market decision support.
