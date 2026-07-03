# Playbook Index and Usage Guide

เอกสารนี้สรุปว่าใน workspace `AITrading` มี playbook / workflow docs อะไรอยู่บ้าง, แต่ละชิ้นมีหน้าที่อะไร, และควรหยิบใช้งานตอนไหน

## สรุปสั้นที่สุด

ถ้าถามว่า "เอกสารไหนใช้หน้าเทรดได้เลย" ให้เริ่มจาก 4 ไฟล์นี้:

1. [trade-playbook-2026.md](/Volumes/MoohCreator/Codex/AITrading/trade-playbook-2026.md)
2. [smc-reversal-trading-rules-and-entry-checklist-th.md](/Volumes/MoohCreator/Codex/AITrading/smc-reversal-trading-rules-and-entry-checklist-th.md)
3. [smc-reversal-entry-techniques-th.md](/Volumes/MoohCreator/Codex/AITrading/smc-reversal-entry-techniques-th.md)
4. [smc-reversal-tradingview-cheatsheet-th.md](/Volumes/MoohCreator/Codex/AITrading/smc-reversal-tradingview-cheatsheet-th.md)

ถ้าถามว่า "เอกสารไหนใช้ตอนออกแบบระบบ / backtest / automation" ให้ดู 3 ไฟล์นี้:

1. [smc-reversal-pine-backtest-spec.md](/Volumes/MoohCreator/Codex/AITrading/smc-reversal-pine-backtest-spec.md)
2. [morning-analysis-workflow-spec.md](/Volumes/MoohCreator/Codex/AITrading/morning-analysis-workflow-spec.md)
3. [morning-macro-brief-spec-2026-07-01.md](/Volumes/MoohCreator/Codex/AITrading/morning-macro-brief-spec-2026-07-01.md)

## 1. Playbook กลุ่มหน้าเทรด

### [trade-playbook-2026.md](/Volumes/MoohCreator/Codex/AITrading/trade-playbook-2026.md)

**แนวคิดหลัก**

- ท่าเทรดจากไฟล์ `ระบบเทรดใหม่ 2026.sbv`
- ใช้กับ `Gold` และ `NASDAQ`
- เน้น `M1-M5`
- แกนคิดคือ `Liquidity fail -> MSS -> เข้าโซน`

**จุดเด่น**

- แยกคุณภาพ setup เป็น `5 ดาว / 4 ดาว / 3 ดาว`
- ชัดเรื่องเงื่อนไขเข้า, โซนเข้า, จุดวาง `SL`, และกรอบ `RR 4R-8R`
- เหมาะกับการเปิดกราฟแล้วตัดสินใจทีละไม้

**เหมาะใช้เมื่อ**

- ต้องการ trade playbook ที่เป็น "ท่าเทรด" ตรง ๆ
- ต้องการตัดสินใจเร็วบนกราฟสั้น
- ต้องการ framework สำหรับคัดคุณภาพ setup

### [smc-reversal-trading-rules-and-entry-checklist-th.md](/Volumes/MoohCreator/Codex/AITrading/smc-reversal-trading-rules-and-entry-checklist-th.md)

**แนวคิดหลัก**

- เป็นกติกาเชิงปฏิบัติของระบบ `SMC Reversal`
- ใช้ `ZigZag + Fibonacci + Structure shift + confirmation candle`

**จุดเด่น**

- ครบทั้ง rules, entry checklist, post-trade review, money management
- เหมาะเป็นคู่มือหลักก่อนเข้าเทรด
- ลดการตัดสินใจตามอารมณ์ได้ดี

**เหมาะใช้เมื่อ**

- ต้องการกฎที่รัดกุมกว่า cheat sheet
- ต้องการ checklist ก่อนกดออเดอร์
- ต้องการใช้เป็น baseline rulebook ของระบบ SMC Reversal

### [smc-reversal-entry-techniques-th.md](/Volumes/MoohCreator/Codex/AITrading/smc-reversal-entry-techniques-th.md)

**แนวคิดหลัก**

- สรุปภาพรวม SMC ในมุมวิธีคิด
- ครอบคลุม `3M`: Mindset, Method, Money Management

**จุดเด่น**

- อธิบายเชิงสอนมากกว่าเชิง rule enforcement
- มี step-by-step execution
- มีแนวคิดแบ่งไม้และการบริหารทุน

**เหมาะใช้เมื่อ**

- ต้องการอ่านเพื่อเข้าใจระบบให้ลึกขึ้น
- ใช้ onboarding หรือทบทวนหลักคิด
- ใช้ก่อนแปลงเป็นกติกาเข้ม ๆ

### [smc-reversal-tradingview-cheatsheet-th.md](/Volumes/MoohCreator/Codex/AITrading/smc-reversal-tradingview-cheatsheet-th.md)

**แนวคิดหลัก**

- เวอร์ชันย่อสำหรับใช้หน้า TradingView

**จุดเด่น**

- สั้น
- เช็กเร็ว
- เหมาะเปิดข้างกราฟ

**เหมาะใช้เมื่อ**

- ต้องการ quick reference
- ไม่อยากเปิดเอกสารยาว
- ใช้เป็น pre-trade short checklist

## 2. เอกสารกลุ่มออกแบบระบบ / backtest

### [smc-reversal-pine-backtest-spec.md](/Volumes/MoohCreator/Codex/AITrading/smc-reversal-pine-backtest-spec.md)

**หน้าที่**

- แปลงระบบ SMC Reversal ให้กลายเป็น logic ที่คำนวณและ backtest ได้

**จุดเด่น**

- แยก structure, confirmation, entry, stop, target, filters, metrics
- เหมาะมากสำหรับการเขียน Pine Strategy
- ช่วยกันปัญหา "คิดว่าใช่" แต่พิสูจน์ด้วยข้อมูลไม่ได้

**เหมาะใช้เมื่อ**

- จะเขียน Pine
- จะทำ backtest
- จะตรวจว่า edge จริงอยู่ตรงไหน

### [morning-analysis-workflow-spec.md](/Volumes/MoohCreator/Codex/AITrading/morning-analysis-workflow-spec.md)

**หน้าที่**

- ออกแบบ workflow เช้าก่อนเริ่มเทรด

**จุดเด่น**

- ตอบ 4 คำถามสำคัญ: market regime, qualified symbols, watchlist, risk constraints
- เชื่อมกับ service ใน repo เช่น scoring, prefilter, setup generation
- เหมาะกับการทำ workflow เชิงระบบมากกว่าการอ่านกราฟทีละตัวแบบ manual ล้วน

**เหมาะใช้เมื่อ**

- จะเริ่มวันเทรดอย่างเป็นระบบ
- จะคัดหุ้น/สินทรัพย์ก่อนทำแผน
- จะสร้าง automation หรือ orchestration layer

### [morning-macro-brief-spec-2026-07-01.md](/Volumes/MoohCreator/Codex/AITrading/morning-macro-brief-spec-2026-07-01.md)

**หน้าที่**

- สเปกสำหรับ brief ข่าวและ macro ตอนเช้า โดยเฉพาะบริบท `XAUUSD`

**จุดเด่น**

- มี guardrails เรื่อง freshness, hallucination, snapshot cross-check
- ชัดทั้ง source layers, pipeline, output contract, verification checklist
- เป็นเอกสารฝั่ง "สรุปภาพตลาด" มากกว่ากติกาเข้าเทรดตรง ๆ

**เหมาะใช้เมื่อ**

- ต้องการ morning brief ภาษาไทย
- ต้องการดูภาพข่าว + market snapshot ก่อนเทรด
- จะพัฒนาระบบสรุป macro ก่อนตลาดเปิด

## 3. เทียบกันแบบเร็ว

| ไฟล์ | ประเภท | ใช้ตอน | ความยาว/ความละเอียด | เหมาะกับ |
| --- | --- | --- | --- | --- |
| `trade-playbook-2026.md` | ท่าเทรด | ตอนหา entry หน้า chart | กลาง | discretionary intraday setup |
| `smc-reversal-trading-rules-and-entry-checklist-th.md` | rulebook + checklist | ก่อนกดเข้า | ค่อนข้างละเอียด | คนที่ต้องการวินัยและกติกาชัด |
| `smc-reversal-entry-techniques-th.md` | คู่มืออธิบายระบบ | ตอนศึกษา/ทบทวน | ละเอียดเชิงสอน | onboarding และทำความเข้าใจ |
| `smc-reversal-tradingview-cheatsheet-th.md` | cheat sheet | ใช้งานหน้า TradingView | สั้น | quick reference |
| `smc-reversal-pine-backtest-spec.md` | backtest spec | ตอนแปลงเป็น Pine / test | ละเอียดเชิงเทคนิค | system design |
| `morning-analysis-workflow-spec.md` | workflow spec | ก่อนเริ่มวัน | ละเอียดเชิง process | pre-market orchestration |
| `morning-macro-brief-spec-2026-07-01.md` | macro brief spec | ก่อนเริ่มวัน | ละเอียดเชิง pipeline | macro/news summary |

## 4. ถ้าจะใช้จริง ควรเริ่มจากอะไร

### กรณี 1: อยากมี playbook สำหรับเข้าเทรดทันที

ลำดับแนะนำ:

1. อ่าน [trade-playbook-2026.md](/Volumes/MoohCreator/Codex/AITrading/trade-playbook-2026.md)
2. เปิด [smc-reversal-tradingview-cheatsheet-th.md](/Volumes/MoohCreator/Codex/AITrading/smc-reversal-tradingview-cheatsheet-th.md) ไว้หน้า chart
3. ใช้ [smc-reversal-trading-rules-and-entry-checklist-th.md](/Volumes/MoohCreator/Codex/AITrading/smc-reversal-trading-rules-and-entry-checklist-th.md) เป็นตัวคุมวินัย

### กรณี 2: อยากเข้าใจระบบให้ลึกก่อน

ลำดับแนะนำ:

1. อ่าน [smc-reversal-entry-techniques-th.md](/Volumes/MoohCreator/Codex/AITrading/smc-reversal-entry-techniques-th.md)
2. ต่อด้วย [smc-reversal-trading-rules-and-entry-checklist-th.md](/Volumes/MoohCreator/Codex/AITrading/smc-reversal-trading-rules-and-entry-checklist-th.md)
3. สุดท้ายเก็บ [smc-reversal-tradingview-cheatsheet-th.md](/Volumes/MoohCreator/Codex/AITrading/smc-reversal-tradingview-cheatsheet-th.md) ไว้ใช้จริง

### กรณี 3: อยากพัฒนาเป็นระบบ backtest / Pine

ลำดับแนะนำ:

1. อ่าน [smc-reversal-trading-rules-and-entry-checklist-th.md](/Volumes/MoohCreator/Codex/AITrading/smc-reversal-trading-rules-and-entry-checklist-th.md)
2. แปลงด้วย [smc-reversal-pine-backtest-spec.md](/Volumes/MoohCreator/Codex/AITrading/smc-reversal-pine-backtest-spec.md)
3. เทียบกับไฟล์ Pine ที่มีอยู่ใน repo

### กรณี 4: อยากมี workflow เช้าก่อนเริ่มวัน

ลำดับแนะนำ:

1. อ่าน [morning-macro-brief-spec-2026-07-01.md](/Volumes/MoohCreator/Codex/AITrading/morning-macro-brief-spec-2026-07-01.md)
2. ต่อด้วย [morning-analysis-workflow-spec.md](/Volumes/MoohCreator/Codex/AITrading/morning-analysis-workflow-spec.md)
3. ค่อยดู output ที่มีใน `outputs/`

## 5. ข้อเสนอแนะเชิงโครงสร้าง

ตอนนี้เอกสารใน repo เริ่มมีโครงชัดแล้ว และสามารถมองเป็น 3 ชั้นได้:

1. `Concept layer`
   เช่น `smc-reversal-entry-techniques-th.md`
2. `Execution layer`
   เช่น `trade-playbook-2026.md`, `smc-reversal-trading-rules-and-entry-checklist-th.md`, `smc-reversal-tradingview-cheatsheet-th.md`
3. `System layer`
   เช่น `smc-reversal-pine-backtest-spec.md`, `morning-analysis-workflow-spec.md`, `morning-macro-brief-spec-2026-07-01.md`

ถ้าจะจัด repo ให้หยิบง่ายขึ้นในอนาคต ผมแนะนำให้มองโฟลเดอร์ปลายทางประมาณนี้:

- `playbooks/`
- `workflow-specs/`
- `backtest-specs/`
- `handoffs/`

## 6. ข้อสรุป

ถ้าถามว่า "playbook หลักของ workspace นี้คืออะไร" คำตอบสั้นที่สุดคือ:

- ฝั่งเข้าเทรด: `trade-playbook-2026.md` และชุด `SMC Reversal`
- ฝั่ง workflow เช้า: `morning-analysis-workflow-spec.md` และ `morning-macro-brief-spec-2026-07-01.md`
- ฝั่งแปลงเป็นระบบ: `smc-reversal-pine-backtest-spec.md`

ดังนั้น repo นี้ไม่ได้มีแค่ playbook เดียว แต่เริ่มมี "playbook stack" แล้ว คือมีตั้งแต่ระดับวิธีคิด, กติกาใช้งานจริง, ไปจนถึงสเปกสำหรับทำ automation และ backtest
