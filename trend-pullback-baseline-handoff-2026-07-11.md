# Trend Pullback Baseline Handoff - 2026-07-11

## Decision

ให้ใช้ **Trend Pullback + Price Action** เป็นระบบหลักสำหรับการทดสอบและใช้งานรอบถัดไป เพราะมีกติกาน้อยกว่า SMC Reversal และทำซ้ำได้ง่ายกว่า

ไฟล์ implementation หลักคือ [trend_pullback_price_action_strategy_v2_1.pine](/Volumes/MoohCreator/Codex/AITrading/trend_pullback_price_action_strategy_v2_1.pine)

ให้เปลี่ยนบทบาทของ SMC Reversal เป็น **A+ reversal setup** สำหรับศึกษาและใช้เฉพาะเมื่อ liquidity event, structure shift และ retest ชัดเจน ไม่ใช่ baseline ที่ต้องเจอทุกวัน

## Core Rules

1. กำหนดแนวโน้มจากกรอบ `H1`: EMA 20 อยู่เหนือ EMA 50 สำหรับ Long หรืออยู่ใต้สำหรับ Short
2. ใช้กรอบ execution `M5` หรือ `M15` รอราคาย่อเข้าโซน EMA
3. เข้าเฉพาะเมื่อมี engulfing ยืนยันทิศเดียวกับแนวโน้ม และโครงสร้าง swing ยังไม่เสีย
4. วาง Stop Loss หลัง swing ล่าสุด พร้อม ATR buffer
5. ใช้ Take Profit คงที่ `2R` และเสี่ยงต่อไม้เท่าเดิมทุกครั้ง

## First Test Configuration

ล็อกการทดสอบรอบแรกให้มีตัวแปรน้อยที่สุด:

| Setting | Baseline |
| --- | --- |
| Instrument | `XAUUSD` |
| Execution timeframe | `M5` หรือ `M15` เลือกเพียงหนึ่งกรอบก่อน |
| Bias timeframe | `H1` |
| Trend filter | EMA 20 / EMA 50 |
| Entry confirmation | Strong engulfing |
| Stop | ล่าสุด swing high/low + ATR buffer |
| Target | Fixed `2R` |
| Position risk | คงที่และต่ำตามแผนบริหารเงิน |
| Costs | ตั้ง spread และ slippage ให้ใกล้โบรกเกอร์จริง |

session filter ใช้ได้เมื่อยืนยัน timezone ของสัญลักษณ์ใน TradingView แล้วเท่านั้น เพื่อไม่ให้ช่วงเวลาที่ทดสอบคลาดเคลื่อน

## Test Discipline

- ทดสอบตลาดและ timeframe เดียวก่อน ไม่ผสมหลายตลาดในผลชุดแรก
- อย่าปรับค่า EMA, buffer, confirmation หรือ target พร้อมกันหลายตัว
- แยกผล Long/Short, session และ market condition
- ใช้ `expectancy`, `profit factor`, `max drawdown`, จำนวนไม้ และผลเป็น R-multiple เป็นตัวตัดสิน ไม่ใช้ win rate อย่างเดียว
- ยืนยันผลด้วย out-of-sample หรือ forward test ก่อนเพิ่มความเสี่ยง

## System Roles After This Decision

| System | Role |
| --- | --- |
| Trend Pullback v2.1 | Primary baseline for testing and execution |
| SMC Reversal | A+ discretionary reversal setup and research system |
| Morning Analysis + Prefilter | Context and watchlist gate before searching for setups |
| CDC + SMC Workflow | Experimental comparison only |
| Trend Short Continuation | Bearish-only specialist, not a primary system |

## Next Work

1. เลือก execution timeframe ระหว่าง `M5` และ `M15`
2. สร้าง backtest protocol และ journal template สำหรับ Trend Pullback baseline
3. รันผลชุด baseline โดยไม่ optimize เพิ่ม
4. เมื่อได้จำนวนตัวอย่างเพียงพอ ค่อยทดสอบ session filter และ break-even ทีละตัว
5. เปรียบเทียบกับ SMC Reversal โดยใช้ช่วงข้อมูล, ต้นทุน และ risk model เดียวกัน

## Validation Boundary

การเลือก Trend Pullback เป็น baseline สรุปจากความเรียบง่ายและความสามารถในการทำซ้ำ ไม่ได้หมายความว่าระบบทำกำไรได้แน่นอน

ผล backtest ไม่ทดแทน forward test และต้นทุนจริง, slippage, leverage และวินัยการส่งคำสั่งสามารถทำให้ผลใช้งานจริงต่างจากผลทดสอบได้
