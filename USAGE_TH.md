# คู่มือการใช้งาน `tradingview-mcp`

เอกสารนี้สรุปการใช้งานโปรเจกต์ `tradingview-mcp` จากโค้ดและเอกสารใน repo สำหรับคนที่ต้องการติดตั้ง รัน และนำไปใช้กับ MCP client เช่น Claude Desktop หรือเชื่อมต่อกับ OpenClaw

## โปรเจกต์นี้คืออะไร

`tradingview-mcp` คือ MCP server สำหรับงานวิเคราะห์การลงทุนและตลาด โดยรวมความสามารถหลักไว้ในตัวเดียว เช่น:

- สแกนหุ้นและคริปโตตาม exchange หรือ market
- วิเคราะห์ทางเทคนิค เช่น RSI, MACD, Bollinger Bands
- ดูราคาปัจจุบันผ่าน Yahoo Finance
- วิเคราะห์ sentiment จาก Reddit และข่าวการเงินจาก RSS
- ทำ backtest ได้ 6 กลยุทธ์
- ทำ walk-forward backtest เพื่อตรวจความเสี่ยงเรื่อง overfitting
- ใช้งานได้ทั้งตลาด crypto, US stocks, BIST, EGX, Malaysia, Hong Kong และตลาดอื่นบางส่วนที่มีใน coin list

จุดสำคัญคือโปรเจกต์นี้ไม่ใช่แอป UI โดยตรง แต่เป็น server/tool layer ที่ให้ LLM หรือ agent เรียกใช้งานต่อ

## ความสามารถหลัก

### Market screening

- `top_gainers`
- `top_losers`
- `bollinger_scan`
- `rating_filter`
- `volume_breakout_scanner`
- `smart_volume_scanner`

### Technical analysis

- `coin_analysis`
- `multi_timeframe_analysis`
- `consecutive_candles_scan`
- `advanced_candle_pattern`
- `volume_confirmation_analysis`

### Multi-signal analysis

- `multi_agent_analysis`
- `market_sentiment`
- `financial_news`
- `combined_analysis`

### Backtesting

- `backtest_strategy`
- `compare_strategies`
- `walk_forward_backtest_strategy`

รองรับ 6 กลยุทธ์:

- `rsi`
- `bollinger`
- `macd`
- `ema_cross`
- `supertrend`
- `donchian`

### Market data via Yahoo Finance

- `yahoo_price`
- `market_snapshot`
- `get_prices_bulk`

## โครงสร้างสำคัญใน repo

- `src/tradingview_mcp/server.py` เป็น MCP entry point และประกาศ tool หลักทั้งหมด
- `src/tradingview_mcp/core/services/` เก็บ business logic หลัก
- `src/tradingview_mcp/core/services/backtest_service.py` ดูแลการ backtest และ walk-forward
- `src/tradingview_mcp/core/services/yahoo_finance_service.py` ดึงราคาผ่าน Yahoo Finance
- `src/tradingview_mcp/core/utils/validators.py` กำหนด exchange และ timeframe ที่รองรับ
- `openclaw/trading.py` เป็น wrapper script สำหรับเรียกใช้จาก OpenClaw ผ่าน shell

## ความต้องการของระบบ

จาก `pyproject.toml` โปรเจกต์นี้ต้องการ:

- Python `>= 3.10`
- dependency หลัก:
  - `mcp[cli]`
  - `tradingview-screener`
  - `tradingview-ta`
  - `feedparser`

การใช้งานหลายส่วนต้องมีอินเทอร์เน็ต เพราะโปรเจกต์ดึงข้อมูลจาก TradingView, Yahoo Finance, Reddit และ RSS feeds

## วิธีติดตั้ง

### แบบที่ 1: ติดตั้งจาก PyPI

```bash
pip install tradingview-mcp-server
```

### แบบที่ 2: รันจาก source

```bash
git clone https://github.com/atilaahmettaner/tradingview-mcp.git
cd tradingview-mcp
uv sync
uv run tradingview-mcp
```

### แบบที่ 3: ติดตั้งแบบ editable ด้วย venv

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
python src/tradingview_mcp/server.py
```

## การใช้งานกับ Claude Desktop

ตัวอย่าง config:

```json
{
  "mcpServers": {
    "tradingview": {
      "command": "/Users/YOUR_USERNAME/.local/bin/uvx",
      "args": ["--from", "tradingview-mcp-server", "tradingview-mcp"]
    }
  }
}
```

ถ้ารันจาก source:

```json
{
  "mcpServers": {
    "tradingview-mcp-local": {
      "command": "uv",
      "args": ["run", "python", "src/tradingview_mcp/server.py"],
      "cwd": "/path/to/tradingview-mcp"
    }
  }
}
```

หลังแก้ config แล้วควรปิดและเปิด Claude Desktop ใหม่

## การใช้งานกับ OpenClaw

repo นี้มีโฟลเดอร์ `openclaw/` สำหรับเชื่อมต่อกับ OpenClaw โดยตรง

flow หลักคือ:

```text
Telegram/WhatsApp/Discord -> OpenClaw agent -> openclaw/trading.py -> tradingview-mcp services
```

wrapper script หลักคือ:

```bash
python3 ~/.openclaw/tools/trading.py <command> [args]
```

คำสั่งที่รองรับใน wrapper:

- `price <symbol>`
- `snapshot`
- `backtest <symbol> <strategy> <period> [interval]`
- `compare <symbol> [period]`
- `walkforward <symbol> [strategy] [period]`
- `sentiment <symbol>`

ตัวอย่าง:

```bash
python3 ~/.openclaw/tools/trading.py price AAPL
python3 ~/.openclaw/tools/trading.py snapshot
python3 ~/.openclaw/tools/trading.py backtest BTC-USD supertrend 1y 1h
python3 ~/.openclaw/tools/trading.py compare AAPL 2y
python3 ~/.openclaw/tools/trading.py walkforward AAPL rsi 2y
python3 ~/.openclaw/tools/trading.py sentiment BTC
```

## Timeframe, period และตลาดที่รองรับ

### Timeframe ฝั่ง MCP tools

- `5m`
- `15m`
- `1h`
- `4h`
- `1D`
- `1W`
- `1M`

### Period ฝั่ง backtest

- `1mo`
- `3mo`
- `6mo`
- `1y`
- `2y`

### Interval ฝั่ง backtest

- `1d`
- `1h`

### Exchange/market ที่มีใน validator

- Crypto: `KUCOIN`, `BINANCE`, `BYBIT`, `OKX`, `BITGET`, `COINBASE`, `GATEIO`, `HUOBI`, `BITFINEX`
- Stocks/indices: `NASDAQ`, `NYSE`, `BIST`, `EGX`, `BURSA`, `MYX`, `KLSE`, `ACE`, `LEAP`, `HKEX`, `HK`, `HSI`, `ASX`

หมายเหตุ: บางเครื่องมือรองรับ exchange ไม่เท่ากัน ควรดูคำอธิบายใน tool นั้น ๆ เพิ่ม

## ตัวอย่างการถาม LLM หรือ MCP client

### Screening

- “Show me the top 10 gainers on Binance in 15m”
- “Find oversold assets with Bollinger squeeze on KuCoin”
- “Scan NASDAQ stocks with strong volume breakout”

### Technical analysis

- “Analyze BTCUSDT on KUCOIN timeframe 1h”
- “Run multi timeframe analysis for AAPL on NASDAQ”
- “Find bullish consecutive candles on BINANCE”

### Sentiment and news

- “What is the market sentiment for BTC?”
- “Show latest financial news for NVDA”
- “Give me a combined analysis for TSLA on NASDAQ”

### Backtesting

- “Backtest RSI strategy for AAPL over 1 year”
- “Compare all strategies for BTC-USD over 2 years”
- “Run walk-forward backtest for supertrend on NVDA”

## ผลลัพธ์ที่คาดหวังจาก backtest

ตัว backtest service สามารถคืนข้อมูลได้มากกว่าแค่ผลตอบแทน เช่น:

- จำนวน trades
- win rate
- total return
- Sharpe ratio
- Calmar ratio
- max drawdown
- profit factor
- expectancy
- trade log
- equity curve

จุดเด่นคือมี simulation ของ commission และ slippage อยู่ใน logic ด้วย ทำให้ผล realistic กว่า backtest แบบง่าย

## ข้อควรระวังในการใช้งาน

- ข้อมูลส่วนใหญ่พึ่งพาแหล่งข้อมูลออนไลน์ ถ้า network ไม่พร้อมบาง tool จะ error ได้
- ผล backtest เป็น historical simulation ไม่ใช่การรับประกันผลในอนาคต
- symbol ของ Yahoo Finance กับ symbol ของ TradingView อาจต่างกัน เช่น `BTC-USD` เทียบกับ `BTCUSDT`
- ตลาดหุ้นบางแห่งต้องระบุ suffix หรือ exchange ให้ถูกต้อง เช่น `THYAO.IS` ใน Yahoo Finance
- บางคำอธิบายในเอกสารเดิมของ repo ยังมีรายละเอียดเก่าปะปนกันอยู่ ควรยึดพฤติกรรมจาก source code เป็นหลัก

## วิธีเริ่มใช้งานแบบแนะนำ

1. ติดตั้ง `tradingview-mcp-server`
2. เพิ่ม config เข้า Claude Desktop
3. restart Claude Desktop
4. ทดสอบถามเช่น:
   - “show available tradingview tools”
   - “analyze BTCUSDT on KUCOIN 1h”
   - “compare strategies for BTC-USD over 1y”

ถ้าต้องการต่อเข้าระบบแชตหรือบอท:

1. ติดตั้ง OpenClaw
2. คัดลอก `openclaw/SKILL.md` และ `openclaw/trading.py`
3. ตั้งค่า model/provider ใน OpenClaw
4. เรียก wrapper script เพื่อทดสอบก่อนต่อเข้าช่องทางจริง

## สรุป

`tradingview-mcp` เหมาะกับการใช้เป็น backend intelligence layer สำหรับ agent หรือ MCP client ที่ต้องการความสามารถด้านตลาดการเงินแบบครบชุดในตัวเดียว โดยเฉพาะถ้าต้องการรวม:

- real-time market snapshot
- technical analysis
- screening
- sentiment/news
- backtesting

ถ้าจะใช้งานจริง แนะนำให้เริ่มจาก Claude Desktop หรือ MCP client ก่อน แล้วค่อยขยายไป OpenClaw เมื่อ flow พื้นฐานใช้งานได้แล้ว
