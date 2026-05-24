# สรุป QuantAgent

วันที่บันทึก: 2026-05-13

แหล่งข้อมูลหลัก:
- https://github.com/Y-Research-SBU/QuantAgent
- https://github.com/Y-Research-SBU/QuantAgent/blob/main/README.md
- https://arxiv.org/abs/2509.09995

## ภาพรวม

QuantAgent คือโปรเจกต์วิจัย/ตัวอย่างระบบเทรดที่ใช้ multi-agent LLM ร่วมกับ technical analysis เพื่อวิเคราะห์ตลาดระยะสั้นหรือ high-frequency trading โดยรับข้อมูลราคา OHLC/K-line แล้วให้ agent หลายตัวช่วยกันตีความ indicator, pattern และ trend ก่อนส่งต่อให้ decision agent ตัดสินใจเป็น `LONG` หรือ `SHORT`

- Repo: `Y-Research-SBU/QuantAgent`
- แนวคิดหลัก: price-driven multi-agent LLMs for high-frequency trading
- Tech หลัก: Python, Flask, LangChain, LangGraph, TA-Lib, yfinance, matplotlib, mplfinance
- License: MIT

## Agent Architecture

จากโครงสร้างใน repo ระบบไหลงานหลักผ่าน LangGraph ในลำดับนี้:

`Indicator Agent -> Pattern Agent -> Trend Agent -> Decision Maker`

- Indicator Agent: คำนวณ indicator เช่น RSI, MACD, ROC, Stochastic และ Williams %R แล้วให้ LLM สรุปความหมายของสัญญาณ
- Pattern Agent: สร้าง candlestick chart เป็นภาพ แล้วใช้ vision-capable LLM วิเคราะห์ chart pattern เช่น double bottom, wedge, triangle และ flag
- Trend Agent: สร้างกราฟพร้อม trendlines และ support/resistance เพื่อให้ LLM วิเคราะห์ทิศทางระยะสั้น
- Decision Maker: รวมผลจากทุก agent แล้วสรุปคำสั่ง `LONG` หรือ `SHORT` พร้อมเหตุผล, horizon และ risk/reward ratio

จุดที่น่าสังเกตคือ paper อธิบายภาพรวมของ specialized agents ไว้กว้างกว่า implementation ใน GitHub เล็กน้อย ดังนั้นตัว repo อาจยังไม่ตรงกับ paper แบบครบทุกองค์ประกอบ

## การใช้งานโดยรวม

แนวทางใช้งานตามเอกสารคือ:

- ใช้ Python 3.11
- ติดตั้ง dependencies ผ่าน `pip install -r requirements.txt`
- ตั้ง API key ของผู้ให้บริการ LLM เช่น `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `DASHSCOPE_API_KEY`, `MINIMAX_API_KEY`
- รันเว็บด้วย `python web_interface.py`

ตัวเว็บจะเปิดที่ `http://127.0.0.1:5000` และใช้ข้อมูลตลาดจาก Yahoo Finance โดยรองรับสินทรัพย์หลายประเภท เช่น BTC, S&P 500, Nasdaq, QQQ, Gold Futures และ VIX รวมถึงหลาย timeframe ตั้งแต่ระดับนาทีไปจนถึงวัน/สัปดาห์

## จุดเด่น

- โครงสร้าง multi-agent ชัดเจน เหมาะสำหรับศึกษา workflow ของ LangGraph + LLM ในงานวิเคราะห์ตลาด
- มีทั้ง web UI และโค้ดที่นำไปเรียกใช้แบบ programmatic ได้
- รองรับ LLM หลาย provider
- ใช้ทั้งตัวเลข indicator และการมองภาพกราฟ ทำให้แนวคิดค่อนข้างใกล้กับวิธีคิดของ discretionary trader
- ใช้ MIT license ซึ่งเปิดทางให้ต่อยอดได้ง่ายกว่าหลายโปรเจกต์สาย trading research

## ข้อควรระวัง

- ยังดูเป็น research/demo มากกว่าระบบ production trading
- ระบบตัดสินใจบังคับออก `LONG` หรือ `SHORT` ทำให้ไม่มีโหมด `HOLD` หรือ `NO TRADE`
- ต้องพึ่ง vision-capable LLM สำหรับการอ่าน pattern/trend จากภาพกราฟ
- dependency บางตัวอย่าง TA-Lib อาจติดตั้งยุ่งในบางเครื่อง
- ใช้ Yahoo Finance เป็น data source หลัก ซึ่งอาจไม่เหมาะกับงาน execution จริงที่ต้องการความเสถียรและ latency ต่ำ
- ยังไม่เห็นส่วน backtesting, position sizing, slippage model, transaction cost model และ risk engine ที่แข็งแรงพอสำหรับใช้งานเงินจริงทันที

## มุมมองสรุป

QuantAgent เหมาะมากถ้าต้องการศึกษาแนวคิดว่า LLM สามารถช่วยอ่าน indicator, candlestick pattern และ trend context เพื่อสรุป trading bias ได้อย่างไร โดยเฉพาะในฐานะ reference architecture สำหรับงานวิจัยหรือการทำ prototype

แต่ถ้าจะนำไปใช้กับการเทรดจริง ควรเพิ่มอย่างน้อยส่วนของ backtest, walk-forward validation, execution/risk rules, position sizing, logging และตัวเลือก `HOLD` ก่อน เพื่อไม่ให้ระบบถูกบังคับเปิดสถานะทุกครั้งแม้สัญญาณยังไม่ชัด
