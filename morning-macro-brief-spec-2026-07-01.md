# Morning Macro Brief Spec

## วัตถุประสงค์

เอกสารนี้ใช้กำหนดรูปแบบและแนวทางสร้าง `morning macro brief` รายวันสำหรับสินทรัพย์อย่าง `XAUUSD` โดยเน้นให้ผลลัพธ์:

- อ่านง่ายสำหรับมนุษย์
- ใช้ข้อมูลล่าสุดจริงในช่วงเช้า
- ลดความเสี่ยงจากการสรุปข่าวผิดทิศหรืออ้างอิงข้อมูลเก่า
- ต่อเชื่อมกับ service เดิมใน repo นี้ได้

เอกสารนี้โฟกัสตามข้อควรระวังหลัก 3 เรื่อง:

1. ข่าวอย่างเดียวไม่พอ
2. ต้องกัน hallucination เชิงเหตุผล
3. ต้องคุม freshness

## ลักษณะของ output เป้าหมาย

ตัวอย่างรายงานที่ต้องการไม่ใช่แค่ feed ข่าว แต่เป็นการรวม 4 ชั้นเข้าด้วยกัน:

- `headline summary` สรุป 2-4 ประเด็นหลักของเช้า
- `market snapshot` ตัวเลขตลาดสำคัญ ณ เวลาสรุป
- `cause-and-effect narrative` อธิบายว่าข่าวไหนกำลังกดดันหรือหนุนราคา
- `risk framing` สรุปสิ่งที่ต้องจับตาต่อในวันนั้น

## ขอบเขต v1

### In Scope

- สรุปเช้าสำหรับ 1 สินทรัพย์หลักต่อหนึ่งรัน เช่น `XAUUSD`
- รองรับ narrative ภาษาไทย
- ใช้ข่าวมหภาค + ข่าวสินทรัพย์ + market snapshot
- ระบุเวลา `as_of` ชัดเจน
- แสดงสถานะความเชื่อมั่นของการสรุป

### Out of Scope

- การ execute order อัตโนมัติ
- การทำนายราคาด้วยโมเดลแยก
- intraday refresh loop ทั้งวัน
- portfolio optimization

## ของเดิมใน repo ที่ควร reuse

- [morning-analysis-workflow-spec.md](/Volumes/MoohCreator/Codex/AITrading/morning-analysis-workflow-spec.md)
- [src/tradingview_mcp/core/services/news_service.py](/Volumes/MoohCreator/Codex/AITrading/src/tradingview_mcp/core/services/news_service.py)
- [src/tradingview_mcp/server.py](/Volumes/MoohCreator/Codex/AITrading/src/tradingview_mcp/server.py)

building blocks ที่ใช้ต่อได้:

- `financial_news`
- `market_sentiment`
- future reuse ของ `market_brief` และ `risk_rules`

หมายเหตุ: สำหรับ brief แบบนี้ ของเดิมยังขาด `macro data layer` และ `fact consistency layer`

## แหล่งข้อมูลที่ต้องมี

brief ที่เชื่อถือได้ต้องใช้ข้อมูลอย่างน้อย 3 กลุ่ม

### 1. News Layer

ใช้สำหรับหาเหตุการณ์และ theme หลัก

- ข่าวมหภาค
- ข่าวภูมิรัฐศาสตร์
- ข่าวนโยบายการเงิน
- ข่าวพลังงาน
- ข่าวเฉพาะทองคำ/ดอลลาร์

### 2. Market Snapshot Layer

ใช้เป็น anchor ว่าตลาดกำลังตอบสนองอย่างไรจริง

- `gold spot` หรือ futures proxy ที่ระบุชัดว่าใช้อะไร
- `silver`
- `DXY`
- `WTI` หรือ `Brent`
- `US 2Y` และ `US 10Y yield` ถ้าหาได้
- optional: `VIX`

### 3. Calendar / Event Layer

ใช้ระบุความเสี่ยงล่วงหน้าในวันนั้น

- ตัวเลขเศรษฐกิจสำคัญ
- ถ้อยแถลงจาก Fed
- เส้นตายทางการเมืองหรือภูมิรัฐศาสตร์

## โครงสร้าง pipeline ที่แนะนำ

### Step 1. Collect

ดึงข้อมูลดิบทั้งหมดในช่วงเวลาเดียวกัน

- ข่าวล่าสุด 10-20 ชิ้น
- ข่าวเฉพาะ asset focus
- market snapshot ของสินทรัพย์หลัก
- optional economic calendar

output:

- `raw_news_items`
- `market_snapshot_raw`
- `calendar_events`

### Step 2. Normalize

ทำข้อมูลให้พร้อมใช้

- แปลง timestamp ให้เป็น timezone เดียว
- ตัดข่าวซ้ำ
- clean html/summary
- tag หมวดข่าว เช่น `geopolitics`, `fed`, `inflation`, `energy`, `usd`

output:

- `normalized_news_items`
- `snapshot_normalized`

### Step 3. Cluster Themes

รวมหลายข่าวที่พูดเรื่องเดียวกันให้เป็น theme เดียว

ตัวอย่าง:

- `US-Iran peace talks`
- `Hormuz shipping risk`
- `Fed higher-for-longer`

output:

- `themes[]`
  - `topic`
  - `importance`
  - `evidence`
  - `market_relevance`

### Step 4. Map Market Impact

ตีความผลกระทบของแต่ละ theme ต่อสินทรัพย์เป้าหมาย

ตัวอย่างสำหรับทอง:

- geopolitical escalation -> `bullish_for_gold`
- stronger USD -> `bearish_for_gold`
- higher rate expectations -> `bearish_for_gold`
- growth scare / safe-haven demand -> `bullish_for_gold`

ผลลัพธ์ต้องไม่เป็นแค่ label แต่ต้องมีเหตุผลประกอบ

output:

- `impact_assessment[]`
  - `topic`
  - `direction`
  - `strength`
  - `reason`

### Step 5. Cross-Check Against Market Snapshot

เช็กว่าการตีความจากข่าวสอดคล้องกับ price action จริงหรือไม่

ตัวอย่าง:

- ข่าวเสี่ยงภูมิรัฐศาสตร์รุนแรง แต่ทองไม่ขึ้นและ DXY แข็งแรงมาก -> narrative ควรเป็น `mixed`
- ข่าว dovish แต่ bond yields พุ่ง -> ห้ามสรุป bullish ตรงๆ โดยไม่เตือนความขัดแย้ง

output:

- `consistency_status`: `confirmed` | `mixed` | `conflicted`
- `consistency_notes[]`

### Step 6. Compose Thai Brief

จัดรูปแบบให้อ่านเหมือนบันทึกเช้า ไม่ใช่ dump ข้อมูล

โครงสร้างแนะนำ:

1. วันที่
2. `📌 หัวข้อประเด็นสำคัญ`
3. bullet 2-4 ข้อ
4. narrative block 2-3 ย่อหน้า
5. `⚠️ สิ่งที่ต้องระวังวันนี้`
6. `as_of` และสถานะความมั่นใจ

## ข้อกำหนดเพื่อแก้ความเสี่ยงตามข้อ 6

## 6.1 ข่าวอย่างเดียวไม่พอ

### ปัญหา

ถ้าใช้เฉพาะ RSS หรือ headline ระบบอาจเล่าเรื่องได้ดีแต่ผิดจากสภาวะตลาดจริง เพราะไม่มี anchor price

### Requirement

- brief ทุกฉบับต้องมี `market_snapshot` แนบมาด้วย
- ตัวเลขทุกชุดต้องบอกว่ามาจากสินทรัพย์ใดจริง เช่น `spot gold` หรือ `GC=F proxy`
- ถ้าหา snapshot ไม่ได้ ต้องลดระดับ output เป็น `news-only brief`
- ห้ามเขียนประโยคยืนยันเชิงตลาด เช่น "ทองคำปรับขึ้นเพราะ..." หากไม่มีข้อมูลราคาในรันนั้น

### Fallback behavior

- ถ้ามีข่าว แต่ไม่มีราคา:
  - รายงานต้องขึ้นสถานะ `partial_data`
  - เปลี่ยนคำอธิบายเป็นเชิง conditional เช่น "มีแนวโน้มหนุนทอง หากตลาดตอบรับเชิง safe haven"

## 6.2 ต้องกัน hallucination เชิงเหตุผล

### ปัญหา

ระบบอาจเชื่อมเหตุและผลเกินจริง เช่น เห็นข่าวตะวันออกกลางแล้วสรุปทันทีว่าทอง bullish ทั้งที่ตลาดจริงอาจให้น้ำหนักกับ USD หรือ yields มากกว่า

### Requirement

- ทุก theme ต้องมี `evidence headlines` อย่างน้อย 1-2 ชิ้น
- ทุก narrative สำคัญต้องโยงกับ `market_snapshot` อย่างน้อย 1 ตัว
- ต้องมีสถานะ `consistency_status`
- ถ้าข่าวกับตลาดขัดกัน ต้องใช้คำว่า `mixed`, `conflicted`, หรือ `market not fully confirming`
- ห้ามสรุป direction เด็ดขาดเมื่อ evidence ไม่พอ

### Guardrails

- ใช้ phrase bank ที่บังคับระดับความมั่นใจ
  - `confirmed`: "ตลาดตอบรับสอดคล้องกับข่าว"
  - `mixed`: "แม้ข่าวจะ..., แต่ราคา/ดอลลาร์/บอนด์ยัง..."
  - `conflicted`: "ข่าวและพฤติกรรมตลาดยังส่งสัญญาณไม่ตรงกัน"
- ต้องมี field `confidence_level`: `high` | `medium` | `low`
- ถ้า theme ไหนไม่มี market confirmation ให้ลด `confidence_level`

## 6.3 ต้องคุม freshness

### ปัญหา

morning brief ที่ใช้ข่าวเก่าหรือราคาเมื่อหลายชั่วโมงก่อน จะดูน่าเชื่อถือแต่ใช้ตัดสินใจผิดเวลาได้

### Requirement

- ทุก output ต้องมี `as_of` แบบ ISO timestamp
- ข่าวทุกชิ้นต้องมี `published_at`
- market snapshot ต้องมี `snapshot_time`
- ต้องกำหนด `freshness window` สำหรับข่าวและราคาแยกกัน

### Suggested freshness policy for v1

- ข่าวหลัก: ไม่เก่าเกิน 12 ชั่วโมง
- ข่าวรองหรือ background: ไม่เก่าเกิน 24 ชั่วโมง
- market snapshot: ไม่เก่าเกิน 30 นาทีจากเวลารัน ถ้าเป็น intraday morning brief
- ถ้าเกิน threshold:
  - ติดธง `stale_news`
  - หรือ `stale_snapshot`
  - ลดระดับความมั่นใจของรายงาน

### Fallback behavior

- ถ้าข่าวสด แต่ snapshot เก่า:
  - รายงานเป็น `partial_data`
  - อธิบายว่า narrative มาจากข่าวล่าสุด แต่ price confirmation ยังไม่สดพอ
- ถ้า snapshot สด แต่ข่าวเก่า:
  - รายงานควรลดการตีความเชิงเหตุการณ์ และเน้นตลาด snapshot มากขึ้น

## Output Contract ที่แนะนำ

```json
{
  "run_type": "morning_macro_brief",
  "asset_focus": "XAUUSD",
  "language": "th",
  "as_of": "2026-07-01T07:00:00+07:00",
  "data_status": "complete",
  "confidence_level": "medium",
  "freshness": {
    "news_status": "fresh",
    "snapshot_status": "fresh"
  },
  "market_snapshot": {
    "gold_reference": {
      "instrument": "XAUUSD spot",
      "price": 4006.73,
      "snapshot_time": "2026-07-01T06:55:00+07:00"
    },
    "silver": 58.46,
    "dxy_change_pct": 0.1
  },
  "themes": [
    {
      "topic": "US-Iran peace talks",
      "direction_for_gold": "mixed",
      "importance": 0.92,
      "evidence": ["headline 1", "headline 2"]
    }
  ],
  "consistency_status": "mixed",
  "consistency_notes": [
    "Geopolitical risk is supportive, but firmer USD is capping upside."
  ],
  "summary_bullets_th": [
    "ราคาทองคำยังทรงตัว ขณะที่ตลาดรอติดตามพัฒนาการเจรจา",
    "ความเสี่ยงด้านพลังงานยังเป็นปัจจัยหนุนเชิง safe haven"
  ],
  "narrative_th": [
    "ย่อหน้า 1",
    "ย่อหน้า 2"
  ],
  "watchouts_th": [
    "จับตาท่าทีเฟดและดอลลาร์",
    "จับตาความคืบหน้าช่องแคบฮอร์มุซ"
  ]
}
```

## รูปแบบข้อความฝั่งผู้ใช้งาน

ตัวอย่างโครงข้อความ:

```md
1 กรกฎาคม 2569
📌 หัวข้อประเด็นสำคัญ :
▪️...
▪️...
▪️...
_____________________________
🤝 ปัจจัยหลักที่กำลังชี้นำราคาทองคำ
...
___
⚠️ สิ่งที่ต้องระวังวันนี้
...

as of 06:55 ICT | confidence: medium | data_status: complete
```

## Service Design ที่แนะนำ

สร้าง service ใหม่:

- `src/tradingview_mcp/core/services/morning_brief_service.py`

หน้าที่:

- orchestrate การดึงข้อมูล
- normalize และ cluster theme
- map impact ต่อสินทรัพย์
- cross-check กับ market snapshot
- compose output JSON และ Markdown/Thai brief

เพิ่ม MCP tool แบบบางใน:

- [src/tradingview_mcp/server.py](/Volumes/MoohCreator/Codex/AITrading/src/tradingview_mcp/server.py)

ตัวอย่างชื่อ:

- `morning_macro_brief(asset: str = "XAUUSD", lang: str = "th") -> dict`

## Verification Checklist

ก่อนถือว่า v1 พร้อมใช้งาน ควรผ่านอย่างน้อย:

1. มี `as_of`, `confidence_level`, `data_status` ทุกครั้ง
2. ถ้าไม่มี market snapshot รายงานต้องไม่ทำตัวเหมือน complete
3. ถ้าข่าวกับตลาดขัดกัน ต้องมี `consistency_status != confirmed`
4. headline สำคัญทุกอันต้อง trace ย้อนกลับได้ถึง source item
5. รายงานภาษาไทยต้องไม่หลุดเป็นการแปล headline ตรงๆ ทั้งฉบับ
6. ต้องแยกได้ระหว่าง `fact`, `interpretation`, และ `watchout`

## แผนทำงานแนะนำ

### Phase 1

- ร่าง output schema
- สร้าง mock service
- รองรับ `financial_news` + static formatter ก่อน

### Phase 2

- เพิ่ม market snapshot layer
- เพิ่ม consistency checks
- เพิ่ม freshness policy enforcement

### Phase 3

- ปรับ narrative quality
- เพิ่ม template เฉพาะ asset เช่น gold, oil, BTC
- เชื่อม notification/report publishing

## Recommendation

แนะนำให้เริ่มจาก `spec-first` และถือว่า brief นี้เป็นคนละงานกับ `morning trade plan`

เหตุผล:

- macro brief เน้น "ตลาดกำลังเล่าเรื่องอะไร"
- trade plan เน้น "ตัวไหนเข้าเงื่อนไขเทรด"

สองส่วนนี้ควรแชร์ source data บางส่วนได้ แต่ไม่ควรถูกรวม logic ตั้งแต่ v1
