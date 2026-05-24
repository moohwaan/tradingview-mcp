# สรุป QuantDinger

แหล่งข้อมูลหลัก: https://github.com/brokermr810/QuantDinger

วันที่สรุป: 2026-05-09

## ภาพรวม

QuantDinger เป็นแพลตฟอร์ม AI quantitative trading แบบ self-hosted ที่ออกแบบให้รวม workflow ตั้งแต่การวิจัยตลาด การเขียน indicator/strategy ด้วย Python การทำ backtest ไปจนถึงการเชื่อมต่อ live trading ไว้ในระบบเดียว

ตัวโปรเจกต์วางตัวเป็น "Private AI Quant Operating System" สำหรับ trader, quant developer และทีมขนาดเล็กที่ต้องการควบคุม infrastructure, strategy code, exchange keys และข้อมูลการใช้งานเอง แทนการพึ่ง SaaS ภายนอกทั้งหมด

## สิ่งที่ระบบทำได้

- AI market research และ AI-assisted analysis สำหรับช่วยวิเคราะห์สินทรัพย์ ตลาด และโอกาสการเทรด
- Generate indicator หรือ strategy code จาก natural language แล้วให้ผู้ใช้แก้ต่อเป็น Python
- เขียนกลยุทธ์แบบ Python-native ทั้งแนว research และ live runtime
- Run server-side backtest พร้อม metrics, equity curve และ strategy snapshots
- เชื่อมต่อ live trading / quick trade กับตลาด crypto และ broker บางประเภท
- รองรับ notifications เช่น Telegram, email, SMS, Discord และ webhook
- มี multi-user, OAuth, credits, membership และ USDT billing primitives สำหรับ operator ที่อยากทำระบบเชิงพาณิชย์
- มี Agent Gateway และ MCP server ให้ AI clients เช่น Cursor, Claude Code หรือ Codex อ่านตลาด จัดการ strategy และสั่ง backtest ได้ผ่าน token ที่กำหนด scope

## Strategy Development Modes

QuantDinger รองรับการเขียน strategy หลัก ๆ 2 รูปแบบ

### IndicatorStrategy

เหมาะกับงาน research, indicator logic และ visual backtesting โดยใช้ dataframe เป็นหลัก สคริปต์จะสร้างสัญญาณ เช่น `buy` และ `sell` แล้วนำไปแสดงบน chart หรือใช้ backtest ต่อ

### ScriptStrategy

เหมาะกับกลยุทธ์ที่ต้องการ logic แบบ event-driven และใกล้เคียง live execution มากขึ้น เช่น `on_init(ctx)` และ `on_bar(ctx, bar)` พร้อมคำสั่ง explicit เช่น `ctx.buy()`, `ctx.sell()` และ `ctx.close_position()`

## Tech Stack

- Frontend: Vue app แบบ prebuilt เสิร์ฟผ่าน Nginx
- Backend: Flask / Python
- Database: PostgreSQL 16
- Worker / cache: Redis 7
- Deployment: Docker Compose
- Integrations: LLM providers, crypto exchanges, IBKR, MT5, market/news APIs, payment APIs และ notification services

## ตลาดและ Integration ที่ระบุว่ารองรับ

### Crypto

รองรับหลาย exchange เช่น Binance, OKX, Bitget, Bybit, Coinbase, Kraken, KuCoin, Gate.io, Deepcoin และ HTX โดยครอบคลุมทั้ง spot และ derivatives ตามแต่ละ venue

### Traditional Markets

- US stocks: IBKR, Yahoo Finance, Finnhub
- Forex: MT5, OANDA
- Futures: มี workflow / data integration บางส่วน

### Prediction Markets

Polymarket ถูกระบุว่าใช้สำหรับ research และ analysis workflow ไม่ใช่ direct in-platform live execution

## วิธีทดลองใช้งานแบบเร็ว

README ระบุว่าสามารถลองด้วย Docker Compose ได้ดังนี้

```bash
git clone https://github.com/brokermr810/QuantDinger.git
cd QuantDinger
cp backend_api_python/env.example backend_api_python/.env
./scripts/generate-secret-key.sh
docker-compose up -d --build
```

หลังระบบเริ่มทำงาน ให้เปิด `http://localhost:8888` แล้ว login ด้วยค่าเริ่มต้น

- User: `quantdinger`
- Password: `123456`

ควรเปลี่ยน default admin password ทันที โดยเฉพาะก่อนใช้งานจริงหรือเปิดให้เครื่องอื่นเข้าถึง

## Agent Gateway และ MCP

QuantDinger มี Agent Gateway ที่ `/api/agent/v1` และ MCP server สำหรับให้ AI agent ใช้งานระบบได้ เช่น

- ดึง candle / market data
- จัดการ strategy
- run backtest
- ทำงานแบบ paper trading โดย default

จุดด้านความปลอดภัยที่เอกสารเน้นคือ agent calls ถูก audit log และ trading token เป็น paper-only โดย default หากจะให้ agent route live order ต้องตั้งค่าทั้ง token และ server flag ให้รองรับ live trading

## จุดแข็ง

- รวม research, chart, Python strategy, backtest, execution และ monitoring ไว้ใน workflow เดียว
- เหมาะกับ self-hosted / local-first usage เพราะ credentials และ strategy code อยู่ใน infrastructure ของผู้ใช้
- มี AI integration ที่ฝังใน workflow จริง ไม่ใช่แค่ chatbot แยกต่างหาก
- มี MCP/Agent Gateway ทำให้เข้ากับ AI coding agent และ research agent ได้ดี
- มีส่วน operator/commercialization เช่น users, roles, credits, membership และ billing ซึ่ง trading tools หลายตัวไม่มี

## จุดที่ควรระวัง

- เป็น software สำหรับ trading ที่อาจเชื่อมต่อเงินจริงได้ จึงควรเริ่มจาก paper trading และ backtest ก่อนเสมอ
- ต้องจัดการ `.env`, `SECRET_KEY`, admin password, exchange API keys, firewall, TLS และ reverse proxy อย่างรัดกุม
- ค่าเริ่มต้นของระบบมี admin credential ตัวอย่าง จึงไม่ควรใช้ใน production โดยไม่เปลี่ยน
- Hosted mode ระบุว่า paper-only แต่ self-hosted สามารถเปิด live trading ได้เอง จึงมี operational risk สูง
- Backend อยู่ภายใต้ Apache 2.0 แต่ frontend source มี license แยกแบบ source-available และ commercial use อาจต้องตรวจสอบเงื่อนไขเพิ่มเติม
- การสรุปนี้อ้างอิงจากเอกสาร repo เป็นหลัก ยังไม่ได้ clone/run/test หรือ audit source code อย่างละเอียด

## เหมาะกับใคร

- Trader หรือ quant ที่อยากมีระบบ research/backtest/execution ในเครื่องหรือ server ของตัวเอง
- Python strategy developer ที่ต้องการ UI, chart, backtest และ live workflow พร้อมกัน
- ทีมขนาดเล็กที่ต้องการทำ internal trading platform หรือ private research stack
- Operator ที่อยากต่อยอดเป็น product เพราะมี user, billing และ deployment primitives อยู่แล้ว

## ข้อสรุป

QuantDinger เป็นโปรเจกต์ที่น่าสนใจถ้ามองเป็น self-hosted AI quant workspace ที่เชื่อมจาก idea ไปสู่ backtest และ live operation ได้ในระบบเดียว จุดเด่นคือความครบของ workflow และการเปิดให้ควบคุม infrastructure เอง

อย่างไรก็ตาม หากจะใช้กับเงินจริง ควรมองเป็น platform ที่ต้อง harden, validate, paper test และกำหนด risk controls เองอย่างจริงจัง ไม่ควรมองว่าเป็น bot สำเร็จรูปที่พร้อมทำกำไรทันที

## แหล่งอ้างอิง

- GitHub repository: https://github.com/brokermr810/QuantDinger
- README: https://github.com/brokermr810/QuantDinger/blob/main/README.md
- Environment example: https://github.com/brokermr810/QuantDinger/blob/main/backend_api_python/env.example
- License: https://github.com/brokermr810/QuantDinger/blob/main/LICENSE
- Trademark policy: https://github.com/brokermr810/QuantDinger/blob/main/TRADEMARKS.md
