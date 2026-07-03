# SMC Reversal Pine / Backtest Specification

เอกสารนี้ใช้เป็นสเปกสำหรับแปลงระบบ SMC Reversal เป็น Pine Script Strategy หรือระบบ backtest ที่วัดผลได้อย่างเป็นกติกา

## 1. วัตถุประสงค์

- แปลง checklist เชิงแนวคิดให้เป็นเงื่อนไขที่คำนวณได้
- แยกระหว่าง logic สำหรับหา setup, logic สำหรับเข้า, และ logic สำหรับออก
- ใช้ทดสอบว่ากฎเรื่อง BOS, retest depth และ target levels มี edge จริงหรือไม่

## 2. ขอบเขตเวอร์ชันแรก

- รองรับ Long และ Short
- ใช้แท่งปิดในการยืนยันสัญญาณ
- ใช้ pivot-based swing detection แทน ZigZag โดยตรงเพื่อลด repaint
- ใช้ Fibonacci ratios เป็น derived levels จาก swing ล่าสุด
- ใช้ single-position model ก่อนใน v1

## 3. Inputs ที่ควรมี

### 3.1 Structure

- `pivotLeft` (int)
- `pivotRight` (int)
- `minSwingAtr` (float): ความต่างขั้นต่ำของ swing เทียบ ATR
- `useCloseBreakOnly` (bool): ใช้ close break เท่านั้น

### 3.2 Retest & Zone

- `fibShallowLow` = `0.382`
- `fibShallowHigh` = `0.5`
- `fibMid` = `0.618`
- `fibDeep` = `0.78`
- `zoneBufferAtr` (float): buffer รอบระดับ Fib

### 3.3 Confirmation

- `confirmMode` (string): `engulfing`, `pinbar`, `either`
- `minBodyAtr` (float)
- `requireCloseInSignalDirection` (bool)

### 3.4 Risk

- `atrLen` (int)
- `slAtrBuffer` (float)
- `riskRewardPrimary` (float)
- `riskPct` (float)
- `useTargetByRetestDepth` (bool)

### 3.5 Filters

- `useTrendFilter` (bool)
- `biasTf` (timeframe)
- `emaFastLen` (int)
- `emaSlowLen` (int)
- `useSessionFilter` (bool)
- `sessionInput` (session)

## 4. นิยามสัญญาณหลัก

### 4.1 Swing Detection

ใช้ pivot highs / pivot lows:

- `swingHigh = ta.pivothigh(high, pivotLeft, pivotRight)`
- `swingLow = ta.pivotlow(low, pivotLeft, pivotRight)`

เก็บ swing ล่าสุดที่ valid และกรอง swing ที่เล็กเกินไปด้วย ATR

### 4.2 Break of Structure

#### Bullish BOS

- ราคาปิดเหนือ swing high ล่าสุด
- หาก `useCloseBreakOnly = true` ไม่ใช้เพียงไส้เทียนแทงทะลุ

#### Bearish BOS

- ราคาปิดต่ำกว่า swing low ล่าสุด

### 4.3 Change of Character

ให้ ChoCh เป็นเหตุการณ์ที่ฝั่งตรงข้ามทำลาย swing สำคัญตัวล่าสุดหลังจากตลาดสร้างลำดับ trend เดิมมาแล้วอย่างน้อย 1 ชุด

ในเวอร์ชันแรกสามารถใช้ BOS เป็น trigger หลัก และเก็บ ChoCh เป็น label/diagnostic ก่อน

## 5. การกางโครงสร้าง Fibonacci

### 5.1 Bullish Reversal Setup

- ระบุ swing low ต้นทาง
- ระบุ swing high ที่ถูกทะลุ
- หลังเกิด break ให้คำนวณช่วงราคา `range = brokenHigh - originLow`
- สร้างโซน retest จาก range นี้

### 5.2 Bearish Reversal Setup

- ระบุ swing high ต้นทาง
- ระบุ swing low ที่ถูกทะลุ
- หลังเกิด break ให้คำนวณช่วงราคา `range = originHigh - brokenLow`
- สร้างโซน retest จาก range นี้

## 6. การจัดประเภท Retest Depth

### 6.1 Shallow Retest

- ราคาย่อเข้าโซน `0.382 - 0.5`

### 6.2 Mid Retest

- ราคาย่อใกล้ `0.618`

### 6.3 Deep Retest

- ราคาย่อใกล้ `0.78`

ให้ใช้ `zoneBufferAtr` เป็น tolerance เช่น `ATR * 0.10` ถึง `ATR * 0.25`

## 7. Confirmation Logic

### 7.1 Bullish Confirmation

- Engulfing ขึ้น หรือ
- Pin bar ที่มี rejection ด้านล่าง

### 7.2 Bearish Confirmation

- Engulfing ลง หรือ
- Pin bar ที่มี rejection ด้านบน

### 7.3 Signal Quality

ควรเช็กเพิ่ม:

- body size มากกว่าค่าขั้นต่ำเทียบ ATR
- แท่งปิดไปในทิศทางเดียวกับ signal
- ไม่ใช่ inside bar ที่อ่อนแรงเกินไป

## 8. Entry Rules

### 8.1 Long Entry

เปิด Long เมื่อครบทุกข้อ:

1. มี bullish BOS หรือ bullish reversal trigger
2. ราคา retest เข้าโซน shallow, mid หรือ deep ตามที่กำหนด
3. มี bullish confirmation
4. ผ่าน filter อื่น เช่น trend หรือ session หากเปิดใช้งาน
5. ไม่มีสถานะค้างอยู่ หาก v1 ยังใช้ single-position model

### 8.2 Short Entry

เปิด Short เมื่อครบทุกข้อ:

1. มี bearish BOS หรือ bearish reversal trigger
2. ราคา retest เข้าโซน shallow, mid หรือ deep
3. มี bearish confirmation
4. ผ่าน filter
5. ไม่มีสถานะค้างอยู่

## 9. Stop Loss Rules

### 9.1 Default Stop

- Long: ต่ำกว่า swing low ล่าสุด ลบด้วย `ATR * slAtrBuffer`
- Short: สูงกว่า swing high ล่าสุด บวกด้วย `ATR * slAtrBuffer`

### 9.2 Invalidation Stop

- หากราคาทะลุเกินระดับ `2.618` ของแผน ให้ถือว่า setup invalid

## 10. Target Rules

### 10.1 Dynamic Target by Retest Depth

- Deep retest -> target `1.2`
- Mid retest -> target `1.618`
- Shallow retest -> target `2.0`

### 10.2 Optional Extended Target

- หากต้องการทดสอบ aggressive mode ให้เพิ่ม target `2.618`

### 10.3 Fixed RR Fallback

- หากไม่ใช้ target ตาม retest depth ให้ fallback เป็น fixed RR เช่น `2R`

## 11. Trade Management

### 11.1 Basic Version

- เข้าเต็มไม้ครั้งเดียว
- ออกทั้งหมดที่ stop หรือ target

### 11.2 Extended Version

- scale out บางส่วนที่ `1.2`
- เลื่อน stop เป็น breakeven หลังได้ `1R`
- ปล่อยส่วนที่เหลือไป `1.618` หรือ `2.0`

## 12. Position Sizing

- รองรับ `fixed qty` และ `risk-based`
- หากใช้ risk-based:
  - `riskCash = strategy.equity * riskPct / 100`
  - `qty = riskCash / stopDistance`

## 13. Filters ที่ควรทดสอบแยก

- ไม่มี filter เลย
- ใช้ trend filter จาก EMA ฝั่ง higher timeframe
- ใช้ session filter
- ใช้ confirmation เฉพาะ engulfing
- ใช้ confirmation แบบ engulfing หรือ pin bar

## 14. Metrics ที่ต้องดูจาก backtest

- Net profit
- Profit factor
- Win rate
- Average win / average loss
- Max drawdown
- Expectancy ต่อไม้
- จำนวนสัญญาณต่อเดือน
- ผลลัพธ์แยกตาม retest depth
- ผลลัพธ์แยกตาม long และ short

## 15. Telemetry / Debug Labels

ควร plot หรือ log ค่าเหล่านี้เพื่อ debug:

- swing high / swing low ล่าสุด
- BOS up / BOS down
- retest depth class
- signal confirmation type
- chosen target type
- stop distance

## 16. แผนการพัฒนาเป็นลำดับ

### Phase 1

- สร้าง pivot swing logic
- สร้าง BOS detection
- สร้าง entry + stop + fixed RR

### Phase 2

- เพิ่ม Fib retest classification
- เพิ่ม target by retest depth
- เพิ่ม confirmation modes

### Phase 3

- เพิ่ม scale out
- เพิ่ม session / trend filters
- เพิ่ม dashboard labels และ diagnostics

## 17. ข้อควรระวัง

- ZigZag ใช้เป็น reference ได้ แต่ไม่ควรใช้ตรง ๆ ใน strategy เพราะ repaint
- คำว่า ChoCh ต้องนิยามให้ชัดก่อน encode ไม่เช่นนั้นผลทดสอบจะไม่เสถียร
- target mapping ระหว่าง depth กับ extension ยังเป็นสมมติฐาน ต้องพิสูจน์ด้วย backtest จริง
