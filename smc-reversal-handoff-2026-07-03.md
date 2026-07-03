# SMC Reversal Handoff - 2026-07-03

## Goal

สรุปและจัดระบบแนวคิด SMC Reversal ให้พร้อมใช้งาน 3 ระดับ:

- เอกสารสรุปแนวคิดหลัก
- กติกาใช้งานจริงพร้อม checklist
- เอกสารต่อยอดสำหรับ TradingView และ Pine/backtest

## Current Baseline

ตอนนี้มีไฟล์หลักครบ 4 ชุดแล้ว:

1. [smc-reversal-entry-techniques-th.md](/Volumes/MoohCreator/Codex/AITrading/smc-reversal-entry-techniques-th.md)
   สรุปแนวคิดต้นฉบับเรื่อง SMC reversal, ZigZag, Fibonacci และ money management
2. [smc-reversal-trading-rules-and-entry-checklist-th.md](/Volumes/MoohCreator/Codex/AITrading/smc-reversal-trading-rules-and-entry-checklist-th.md)
   เวอร์ชันใช้งานจริง มี trading rules, entry checklist, post-trade review และกรอบ risk management
3. [smc-reversal-tradingview-cheatsheet-th.md](/Volumes/MoohCreator/Codex/AITrading/smc-reversal-tradingview-cheatsheet-th.md)
   เวอร์ชันสั้นสำหรับเปิดดูหน้า TradingView
4. [smc-reversal-pine-backtest-spec.md](/Volumes/MoohCreator/Codex/AITrading/smc-reversal-pine-backtest-spec.md)
   สเปกสำหรับแปลงเป็น Pine Script Strategy หรือระบบ backtest

## What Was Improved

- แยกเนื้อหาออกจากกันชัดเจนระหว่าง “แนวคิด”, “กติกาใช้งาน”, “cheat sheet”, และ “spec”
- ปรับประเด็น money management ให้ระวังความเสี่ยงมากขึ้น และไม่ตีความ All-In แบบเสี่ยงทั้งพอร์ต
- วางโครงสำหรับ backtest โดยแยก swing detection, BOS, retest depth, confirmation, entry, exit, และ metrics

## Recommended Next Order

### Phase 1

ใช้ [smc-reversal-tradingview-cheatsheet-th.md](/Volumes/MoohCreator/Codex/AITrading/smc-reversal-tradingview-cheatsheet-th.md) จริงระหว่างดูกราฟ เพื่อเช็กว่า flow การตัดสินใจอ่านง่ายพอหรือยัง

### Phase 2

รีวิว [smc-reversal-trading-rules-and-entry-checklist-th.md](/Volumes/MoohCreator/Codex/AITrading/smc-reversal-trading-rules-and-entry-checklist-th.md) แล้วตัดสินใจให้ชัด 3 เรื่อง:

- จะนิยาม ChoCh แบบไหน
- จะใช้ confirmation อะไรเป็นหลัก: engulfing, pin bar หรือทั้งคู่
- จะใช้ target ตาม retest depth หรือ fixed RR เป็น baseline

### Phase 3

แปลง [smc-reversal-pine-backtest-spec.md](/Volumes/MoohCreator/Codex/AITrading/smc-reversal-pine-backtest-spec.md) เป็น Pine Script v1 โดยเริ่มจาก:

- pivot swing logic
- BOS detection
- single-entry model
- stop + target แบบง่ายก่อน

### Phase 4

รัน backtest แล้วแยกผลตาม:

- shallow / mid / deep retest
- long / short
- timeframe ที่ใช้จริง

## Open Decisions

- จะใช้ ZigZag เป็นแค่ visual aid หรือจะมี logic อ้างอิงทางอ้อมมากน้อยแค่ไหน
- จะให้ระบบรองรับ scale out ตั้งแต่ v1 หรือเก็บไว้ v2
- จะกรองด้วย trend filter ตั้งแต่แรกหรือทดสอบแบบ raw price structure ก่อน

## Quick Resume Checklist

- เปิดไฟล์ rules และ cheatsheet เทียบกันก่อน
- ยืนยันนิยาม ChoCh และ confirmation logic
- เลือก baseline target model
- เริ่มเขียน Pine v1 จาก backtest spec
- วัดผลขั้นต่ำ: win rate, profit factor, max drawdown, expectancy

## Suggested First Build

ถ้าจะทำต่อทันที ให้เริ่มที่ Pine v1 แบบง่ายที่สุด:

- ใช้ pivot high/low แทน ZigZag
- ใช้ BOS จากแท่งปิด
- ใช้ engulfing เป็น confirmation เดียวก่อน
- ใช้ fixed RR 1:2 เป็น baseline
- ค่อยเพิ่ม retest depth logic เป็น Phase 2
