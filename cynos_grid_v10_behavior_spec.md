# Cynos Grid V10.3.3 AntiReverse (Behavior-Reconstructed) - Functional Specification

## 1. ขอบเขตเอกสาร
เอกสารนี้เป็นสเปกสำหรับสร้าง EA MT5 (`.mq5`) ใหม่ โดยอ้างอิงจากพฤติกรรมที่สังเกตได้จาก:
- ไฟล์ไบนารี `Cynos Grid_V10.3.3_AntiReverse - FreeTest.ex5` (ไม่สามารถอ่าน source ได้โดยตรง)
- ภาพกราฟและภาพประวัติการเทรดที่ให้มา

เอกสารนี้ไม่ใช่ source เดิมของ `.ex5` แต่เป็น `behavior-compatible spec` เพื่อให้พัฒนาเวอร์ชันใช้งานได้ใกล้เคียง.

## 2. วัตถุประสงค์ระบบ
- เทรดทองคำ (`XAUUSD`) แบบกึ่งอัตโนมัติเต็มรูปแบบด้วยแนวคิด Grid + Trend/Structure Filter
- เปิดไม้ย่อยหลายไม้ในโซนราคา (mini orders) และบริหารปิดเป็นชุดด้วย TP หลายระดับ
- มีโหมด Anti-Reverse เพื่อลดการกลับฝั่งเร็วเกินไปเมื่อแนวโน้มหลักยังไม่เปลี่ยนจริง

## 3. สมมติฐานหลักจากพฤติกรรมที่พบ
- ระบบใช้การประเมินฝั่งหลัก (`BUY`/`SELL`) จากหลาย timeframe (M1, M5, M15, M30, H1)
- ใช้ oscillator อย่างน้อย RSI และ Stochastic เพื่อยืนยันโมเมนตัม
- ใช้โซนโครงสร้างราคา เช่น Equal High/Low, Sweep, CHoCH, Zone Buy/Sell
- มีการทยอยเปิดไม้เพิ่มเป็น Grid เมื่อราคาเคลื่อนสวนภายในขอบเขตที่กำหนด
- มี TP หลายชั้น (TP1..TP5) และ SL ระดับ basket

## 4. สถาปัตยกรรมระบบ (โมดูล)
1. `Market Context Module`
- อ่านข้อมูลราคา, spread, volatility (เช่น ATR), session
- คำนวณ trend score ราย timeframe

2. `Structure Signal Module`
- ตรวจจับ swing high/low
- ตรวจจับ sweep, CHoCH, EQH/EQL แบบเชิงกฎ
- สร้างโซน supply/demand ที่ใช้งานจริง

3. `Bias Engine`
- รวมสัญญาณ trend + momentum + structure
- คืนค่า bias: `BUY`, `SELL`, `NEUTRAL`
- คืนค่า confidence 0..100

4. `Grid Execution Module`
- เริ่มคำสั่งชุดแรก (seed order)
- วางไม้เพิ่มตามระยะ grid
- จำกัดจำนวนไม้สูงสุดต่อฝั่งและต่อ basket

5. `Basket Risk Module`
- กำหนด TP ladder และ basket SL
- ปิดทั้งชุดเมื่อถึงเงื่อนไขกำไร/ขาดทุน/timeout
- ทำ anti-meltdown (หยุดเปิดเพิ่มเมื่อเสี่ยงเกิน threshold)

6. `Trade Guard Module`
- spread/slippage guard
- news/session guard (เปิดเป็น option)
- anti-reverse cooldown

## 5. พารามิเตอร์อินพุต (แนะนำ)
## 5.1 General
- `InpMagicNumber` (long): หมายเลข magic
- `InpSymbol` (string): สัญลักษณ์ (default `XAUUSD`)
- `InpEnableBuy` (bool)
- `InpEnableSell` (bool)
- `InpMaxSpreadPoints` (int)
- `InpTradeSessionFilter` (bool)

## 5.2 Trend & Signal
- `InpTrendTF1` = `PERIOD_M5`
- `InpTrendTF2` = `PERIOD_M15`
- `InpTrendTF3` = `PERIOD_H1`
- `InpRSIPeriod` (int, default 14)
- `InpRSIBuyMin` / `InpRSISellMax`
- `InpStochK`, `InpStochD`, `InpStochSlowing`
- `InpMinBiasScore` (double, 0..100)

## 5.3 Zone/Structure
- `InpSwingLookback` (int)
- `InpEqualTolerancePoints` (int)
- `InpSweepLookbackBars` (int)
- `InpZoneATRMultiplier` (double)

## 5.4 Grid
- `InpBaseLot` (double)
- `InpLotMultiplier` (double)  (เช่น 1.0 สำหรับคงที่ หรือ >1 สำหรับเพิ่ม lot)
- `InpGridStepPoints` (int)
- `InpGridStepATRFactor` (double)  (dynamic grid)
- `InpMaxOrdersPerSide` (int)
- `InpMaxBasketOrders` (int)
- `InpMinSecBetweenAdds` (int)

## 5.5 TP/SL
- `InpUseTPLadder` (bool)
- `InpTP1_Points` ... `InpTP5_Points` (int)
- `InpTP1_ClosePct` ... `InpTP5_ClosePct` (double, รวมกัน = 100)
- `InpBasketSL_Points` (int)
- `InpBasketSL_ATRFactor` (double)
- `InpBreakEvenAfterTP1` (bool)

## 5.6 Anti-Reverse & Safety
- `InpAntiReverseEnabled` (bool)
- `InpReverseConfirmBars` (int)
- `InpReverseMinScoreDelta` (double)
- `InpCooldownAfterStopMin` (int)
- `InpMaxDailyLoss` (double, account currency)
- `InpMaxDailyDrawdownPct` (double)
- `InpEmergencyCloseDDPct` (double)

## 6. นิยามสัญญาณหลัก
## 6.1 Trend Score (ต่อ TF)
ให้คะแนนฝั่ง BUY/SELL ต่อ TF จาก:
- ตำแหน่งราคาต่อ EMA fast/slow
- slope ของ EMA
- RSI zone
- Stochastic cross direction

จากนั้น normalize เป็นช่วง `-100..+100`
- >0 = bullish
- <0 = bearish

## 6.2 Multi-TF Bias
คำนวณ:
- `BiasScore = w1*M5 + w2*M15 + w3*H1 + w4*Structure + w5*Momentum`

เกณฑ์:
- `BiasScore >= +InpMinBiasScore` => `BUY`
- `BiasScore <= -InpMinBiasScore` => `SELL`
- อื่นๆ => `NEUTRAL`

## 6.3 Structure Events
- `Sweep High`: ราคาแทง high ล่าสุดแล้วปิดกลับลงในช่วง n bars
- `Sweep Low`: ราคาแทง low ล่าสุดแล้วปิดกลับขึ้น
- `CHoCH Up/Down`: โครงสร้างทำ higher-high/lower-low หลังชุดก่อนหน้า
- `EQH/EQL`: high/low ใกล้เคียงกันภายใน tolerance

## 7. กติกาเข้าออเดอร์
## 7.1 Seed Entry
เปิด seed order เมื่อ:
1. bias เป็นฝั่งที่อนุญาต (buy/sell enabled)
2. confidence ผ่าน threshold
3. spread <= max spread
4. ไม่มี basket ฝั่งเดียวกันที่ active เกิน limit
5. ไม่อยู่ใน cooldown ของ anti-reverse

## 7.2 Add-on Grid Entry
เพิ่มไม้เมื่อ:
1. มี basket active ฝั่งนั้นอยู่แล้ว
2. ราคาเคลื่อนสวนจากราคาเฉลี่ยเกิน `grid_step_dynamic`
3. เวลาห่างจากไม้ก่อนหน้า >= `InpMinSecBetweenAdds`
4. ยังไม่เกิน `InpMaxOrdersPerSide` และ `InpMaxBasketOrders`
5. guard ด้านความเสี่ยงยังผ่าน

โดย:
- `grid_step_dynamic = max(InpGridStepPoints, ATR*InpGridStepATRFactor converted to points)`

## 8. กติกาปิดออเดอร์
## 8.1 TP Ladder (Basket-aware)
- นิยามราคาเฉลี่ยถ่วงน้ำหนัก `VWAP_basket`
- ตั้งเป้าหมาย TP1..TP5 จาก `VWAP_basket` ตามฝั่ง
- เมื่อแตะ TP แต่ละชั้น ให้ปิดบางส่วนตามเปอร์เซ็นต์

## 8.2 Basket SL
ปิดทั้งชุดเมื่อ:
- floating loss ถึง `InpBasketSL_Points` จาก `VWAP_basket`
- หรือเงื่อนไข DD ฉุกเฉินถึง `InpEmergencyCloseDDPct`

## 8.3 Time/Condition Exit
- ปิดเมื่อ bias สวนทางรุนแรงต่อเนื่องเกิน `InpReverseConfirmBars`
- ปิดเมื่อหมดช่วง session ที่อนุญาต (ถ้าเปิด filter)

## 9. Anti-Reverse Logic
วัตถุประสงค์: ป้องกัน flip BUY<->SELL ถี่ในช่วงแกว่ง

กฎ:
1. เมื่อมี basket active ฝั่งหนึ่ง ห้ามเปิดฝั่งตรงข้ามจนกว่าจะ:
- basket เดิมถูกปิดครบ และ
- bias ฝั่งใหม่ยืนยันต่อเนื่อง >= `InpReverseConfirmBars` และ
- ส่วนต่างคะแนนเกิน `InpReverseMinScoreDelta`

2. หลัง stop-out:
- เข้า `cooldown` ตาม `InpCooldownAfterStopMin`
- ห้ามเปิดฝั่งใหม่จน cooldown ครบ

## 10. การคำนวณขนาด lot
โหมดที่รองรับ:
- `Fixed`: ทุกไม้ = `InpBaseLot`
- `Progressive`: `lot_n = InpBaseLot * pow(InpLotMultiplier, n-1)`
- `Capped`: จำกัด lot สูงสุดด้วย `InpMaxLotPerOrder` (เพิ่มพารามิเตอร์เสริม)

คำแนะนำ default สำหรับบัญชีเล็ก:
- ใช้ `Fixed` หรือ multiplier ต่ำ (`<=1.2`)

## 11. State Machine ของ EA
สถานะหลัก:
- `IDLE`: ไม่มี basket
- `SEED_OPENED`: เปิดไม้แรกแล้ว
- `GRID_BUILDING`: มีการเพิ่มไม้
- `TP_SCALING`: กำลังทยอยปิดกำไร
- `COOLDOWN`: พักหลัง reverse/stop
- `LOCKDOWN`: หยุดเทรดเมื่อชน daily risk

Transition สำคัญ:
- `IDLE -> SEED_OPENED`: ได้สัญญาณเข้า
- `SEED_OPENED -> GRID_BUILDING`: ราคาไปทาง adverse แล้วถึง step
- `GRID_BUILDING -> TP_SCALING`: ราคาเด้งกลับถึง TP ladder
- `ANY -> LOCKDOWN`: ชน max daily loss/DD

## 12. Risk Controls (ต้องมี)
- จำกัดจำนวน basket พร้อมกัน (`max 1 ต่อ symbol` แนะนำสำหรับ v1)
- จำกัดจำนวน order รวมต่อวัน
- daily loss stop
- daily drawdown stop
- spread guard ก่อนส่งคำสั่งทุกครั้ง
- slippage guard และ retry แบบจำกัดจำนวนครั้ง

## 13. Logging & Telemetry
ต้อง log อย่างน้อย:
- bias score ต่อ tick/bar สำคัญ
- เหตุผลเข้า/ไม่เข้าออเดอร์
- เหตุผลเพิ่มไม้
- เหตุผลปิด (TP layer / basket SL / reverse / DD guard)
- basket metrics: order count, avg price, floating PnL, margin level

รูปแบบแนะนำ:
- เขียนทั้ง `Experts log` และ CSV audit ต่อวัน

## 14. โครงสร้างข้อมูลภายใน (แนะนำ)
- `struct BasketState`
- `struct SignalSnapshot`
- `struct RiskSnapshot`
- map ด้วย key: `symbol + side`

field สำคัญใน `BasketState`:
- `side`, `open_time`, `order_count`, `total_lot`, `vwap`
- `tp_stage_done[5]`
- `last_add_time`
- `max_adverse_excursion`

## 15. Acceptance Criteria (MVP)
ระบบผ่านเมื่อ:
1. เปิด/เพิ่ม/ปิดออเดอร์ตามกติกาได้ครบทุกกรณีหลัก
2. TP ladder ทำงานถูกต้องกับ basket หลายไม้
3. Anti-reverse กันการ flip ถี่ได้จริงในการทดสอบ sideway
4. daily risk lock ทำงานและหยุดเทรดจริง
5. backtest 6-12 เดือนบน XAUUSD ไม่มี error ร้ายแรงใน journal

## 16. Test Plan
1. Unit-like checks (ผ่านฟังก์ชัน utility)
- pip/point conversion
- VWAP basket calc
- TP ladder allocation

2. Strategy Tester scenarios
- trend day ขึ้นแรง
- trend day ลงแรง
- sideway สลับเร็ว
- spike ช่วงข่าว

3. Stress tests
- spread สูงผิดปกติ
- slippage สูง
- reconnect/disconnection

## 17. ข้อจำกัดที่ต้องรับรู้
- ไม่สามารถยืนยันว่า logic ตรง 100% กับ EA เดิมใน `.ex5`
- ชื่อ label บนกราฟอาจมาจาก indicator ภายในที่แยกโมดูล
- ค่าพารามิเตอร์จริงของต้นฉบับยังไม่ทราบ ต้อง tune จาก statement เพิ่ม

## 18. แผนต่อเนื่อง (ถัดจากเอกสารนี้)
1. สร้างโครง EA `.mq5` ตาม state machine ในสเปกนี้
2. ใส่ input ทั้งชุด + logging
3. ทำ backtest baseline
4. ปรับค่า grid/risk ตามผลจริงและ tolerance drawdown ที่ต้องการ

