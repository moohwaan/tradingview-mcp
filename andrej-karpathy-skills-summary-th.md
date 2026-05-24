# สรุป multica-ai/andrej-karpathy-skills

แหล่งข้อมูลหลัก: https://github.com/multica-ai/andrej-karpathy-skills

วันที่สรุป: 2026-05-22

## ภาพรวม

`multica-ai/andrej-karpathy-skills` เป็น repository ขนาดเล็กที่ตั้งใจทำ "guideline สำหรับ coding agent" มากกว่าจะเป็น library, SDK, framework หรือ application runtime

แกนหลักของ repo คือไฟล์คำสั่งเพียงชุดเดียวที่สรุปแนวคิดจากโพสต์ของ Andrej Karpathy เรื่องข้อผิดพลาดที่ LLM มักทำเวลาเขียนโค้ด เช่น เดาเองเกินไป, ซ่อนความไม่แน่ใจ, overengineer, แก้ไฟล์เกิน scope และทำงานแบบไม่มี success criteria ที่ตรวจสอบได้

repo นี้จึงพยายามแปลงข้อสังเกตเหล่านั้นให้กลายเป็น behavioral rules ที่เอาไปใช้ได้ทันทีในเครื่องมืออย่าง Claude Code และ Cursor

## สถานะของ Repo ณ วันที่สรุป

- Owner: `multica-ai`
- Repository: `andrej-karpathy-skills`
- Default branch: `main`
- Public repository
- สร้างเมื่อ: 2026-01-27
- Push ล่าสุดที่เห็นผ่าน GitHub API: 2026-04-20
- อัปเดต metadata ล่าสุดที่เห็นผ่าน GitHub API: 2026-05-22
- Stars: ประมาณ 144k
- Forks: ประมาณ 14.8k
- Watchers/Subscribers ที่ API แสดง: ประมาณ 783
- License ที่หน้า metadata repo: ยังไม่ระบุในช่อง `license`
- License ที่ระบุในไฟล์ภายใน repo: `MIT`

หมายเหตุ: metadata บางจุดสะท้อนความไม่สอดคล้องเล็กน้อย เช่น GitHub API ไม่โชว์ค่า `license` แต่ใน `README`, `SKILL.md` และ plugin manifest ระบุว่าใช้ MIT

## Repo นี้ทำอะไร

สาระจริงของ repo คือ guideline 4 ข้อ:

1. `Think Before Coding`
2. `Simplicity First`
3. `Surgical Changes`
4. `Goal-Driven Execution`

ทั้ง 4 ข้อถูกกระจายซ้ำในหลายรูปแบบเพื่อให้ใช้กับหลายเครื่องมือ แต่ใจความแทบเหมือนกันทั้งหมด

## หลักการทั้ง 4 ข้อ

### 1. Think Before Coding

แนวคิดคือ agent ไม่ควรเดา requirement เงียบ ๆ แล้วลงมือเลย แต่ควร:

- บอก assumption ออกมาตรง ๆ
- ถ้ามีหลายความหมาย ต้องเสนอหลาย interpretation
- ถ้ามีทางที่ง่ายกว่า ควร push back
- ถ้ายังงง ต้องหยุดและถาม

จุดนี้ตั้งใจแก้พฤติกรรม LLM ที่ "มั่นใจผิด" และวิ่งต่อทั้งที่โจทย์ยังไม่ชัด

### 2. Simplicity First

เน้นเขียน "โค้ดน้อยที่สุดที่แก้ปัญหาวันนี้ได้" ไม่เติม flexibility, abstraction, configurability หรือ error handling ที่ไม่มี requirement รองรับ

หลักคิดสำคัญคือ:

- อย่าเพิ่ม feature ที่ไม่ได้ขอ
- อย่าสร้าง abstraction สำหรับ use case เดียว
- อย่าเตรียมระบบเผื่ออนาคตโดยไม่มีสัญญาณว่าต้องใช้จริง
- ถ้า 200 บรรทัดย่อเหลือ 50 ได้ ควรย่อ

นี่คือแกนต้าน overengineering โดยตรง

### 3. Surgical Changes

เวลาแก้ codebase เดิม ให้แตะเฉพาะส่วนที่เกี่ยวกับคำขอ:

- ไม่ drive-by refactor
- ไม่แก้ format/comment/adjacent code โดยไม่จำเป็น
- ต้อง match style เดิมของ repo
- ลบเฉพาะของเสียที่ "เกิดจากการแก้ครั้งนี้" ไม่ใช่ dead code เก่าที่มีอยู่ก่อน

หลักนี้ช่วยลด diff ที่ฟุ้งและลดความเสี่ยงทำของที่ไม่ได้ตั้งใจพัง

### 4. Goal-Driven Execution

แทนที่จะรับคำสั่งแบบคลุมเครือ เช่น "fix bug" หรือ "add validation" ให้แปลงเป็นเป้าหมายที่พิสูจน์ได้ เช่น:

- เขียน test ให้ fail ก่อน
- แก้ให้ test ผ่าน
- เช็ก regression

repo นี้มองว่า LLM จะเก่งมากเมื่อมี success criteria ชัดและวนลูป verify ได้เอง

## โครงสร้าง Repository

โครงสร้างจริงเล็กและตรงมาก:

```text
.claude-plugin/
  marketplace.json
  plugin.json
.cursor/rules/
  karpathy-guidelines.mdc
skills/karpathy-guidelines/
  SKILL.md
CLAUDE.md
CURSOR.md
EXAMPLES.md
README.md
README.zh.md
```

ความหมายของแต่ละส่วน:

- `CLAUDE.md`: เวอร์ชัน instruction file สำหรับใส่ระดับโปรเจกต์
- `.cursor/rules/karpathy-guidelines.mdc`: เวอร์ชัน Cursor rule ที่ตั้ง `alwaysApply: true`
- `skills/karpathy-guidelines/SKILL.md`: เวอร์ชัน skill package
- `.claude-plugin/`: manifest สำหรับติดตั้งเป็น Claude Code plugin
- `EXAMPLES.md`: ตัวอย่าง anti-pattern และตัวอย่างที่ควรทำ
- `CURSOR.md`: วิธีใช้ repo นี้กับ Cursor

สรุปคือไม่ได้มี logic/runtime ซับซ้อนเลย แต่เป็น "content repackaging" ของ guideline เดียวกันสำหรับหลาย environment

## วิธีใช้งานตามที่ README ระบุ

README ระบุ 2 ทางหลักสำหรับ Claude Code:

### 1. ติดตั้งเป็น plugin

```text
/plugin marketplace add forrestchang/andrej-karpathy-skills
/plugin install andrej-karpathy-skills@karpathy-skills
```

### 2. ใช้เป็น `CLAUDE.md`

ดาวน์โหลดหรือ append ไฟล์ `CLAUDE.md` เข้าโปรเจกต์

สำหรับ Cursor ให้ใช้ไฟล์:

```text
.cursor/rules/karpathy-guidelines.mdc
```

และใน repo นี้ตั้ง `alwaysApply: true` ไว้แล้ว

## จุดที่น่าสนใจ

### 1. มันไม่ใช่ "skills repo" แบบมีหลาย skill

แม้ชื่อ repo จะลงท้ายด้วย `skills` แต่ของจริงมี skill หลักแค่ตัวเดียว คือ `karpathy-guidelines`

ดังนั้นอย่าคาดหวังชุดคำสั่งหลายโดเมนแบบ `google/skills` หรือ skill library ขนาดใหญ่ นี่คือ guideline แพ็กเดียวที่เน้นคุณภาพการเขียนโค้ดของ agent

### 2. คุณค่าหลักอยู่ที่ format และ framing

สิ่งที่ repo นี้ขายไม่ใช่ความซับซ้อนทางเทคนิค แต่คือการเอา pain point ที่คนใช้ agent เจอบ่อยมาก มาแปลงเป็น instruction ที่สั้น ชัด และ deploy ได้หลายรูปแบบ

จุดแข็งจึงอยู่ที่:

- เข้าใจง่าย
- นำไป merge กับ instruction เดิมได้ง่าย
- ใช้ได้ทั้งแบบ project-local และ personal reusable skill
- เหมาะกับทีมที่อยากลดพฤติกรรม "ทำเกิน scope" ของ agent

### 3. `EXAMPLES.md` มีประโยชน์มากกว่าที่คิด

ถ้าอ่านแค่ 4 principles จะเข้าใจในเชิงแนวคิด แต่ `EXAMPLES.md` คือส่วนที่ทำให้ guideline นี้ "ใช้เป็น" เพราะยกเทียบระหว่าง:

- สิ่งที่ LLM มักทำผิด
- สิ่งที่ควรตอบ/ควรทำแทน

เช่น:

- คำขอคลุมเครืออย่าง "make search faster" ต้องแตกเป็นหลาย interpretation
- งานง่ายอย่าง discount function ไม่ควรสร้าง strategy pattern ทั้งชุด
- bug fix เล็ก ๆ ไม่ควรแอบ reformat หรือเพิ่ม validation อื่น
- งานอย่าง "fix auth" ต้องแปลงเป็น testable plan

สำหรับคนที่ทำ agent prompt engineering หรือ system instruction อยู่แล้ว ไฟล์นี้มีค่ามาก เพราะช่วยทำให้หลักคิดไม่ลอย

## จุดแข็ง

- แนวคิดคมและชัดมาก ใช้ภาษาง่าย ไม่ฟุ้ง
- ขนาดเล็ก จึงเอาไปใช้ต่อหรือ remix ได้เร็ว
- ครอบคลุมเครื่องมือหลายแบบใน repo เดียว ทั้ง Claude Code plugin, `CLAUDE.md`, Cursor rules และ skill
- เน้นแก้ pain point จริงของ coding agent ได้แก่ assumption ผิด, overengineering, diff ฟุ้ง, และ lack of verification
- `EXAMPLES.md` ทำหน้าที่เป็น training examples แบบไม่ต้องมี runtime
- เหมาะเป็น baseline instruction สำหรับทีมที่เริ่มใช้ AI coding agent ในงานจริง

## จุดที่ควรระวัง

- repo นี้ไม่ใช่เทคนิคพิเศษหรือระบบอัตโนมัติ มันคือ instruction layer ดังนั้นผลลัพธ์ขึ้นกับว่าตัว agent ปฏิบัติตามได้ดีแค่ไหน
- guideline นี้ bias ไปทาง "ระวังมากกว่าความเร็ว" ซึ่งดีสำหรับงานไม่ trivial แต่บางทีมอาจรู้สึกช้าถ้าใช้กับงานเล็กมาก
- ไม่มี domain knowledge เฉพาะด้าน เช่น cloud, trading, backend framework, database หรือ infra มันช่วยเรื่องพฤติกรรม ไม่ได้ช่วยเรื่องเนื้อหาวิชา
- ชื่อ owner และคำสั่งติดตั้งบางจุดยังอ้าง `forrestchang` ขณะที่ repo ปัจจุบันอยู่ใต้ `multica-ai`; มีแนวโน้มว่าเป็นร่องรอยจากที่มาหรือการย้ายแพ็กเกจ จึงควรเช็กอีกครั้งก่อนใช้คำสั่งติดตั้งจริง
- การสรุปนี้อ้างอิงจากไฟล์เอกสารและ metadata บน GitHub ไม่ได้ติดตั้ง plugin หรือทดสอบกับ Claude/Cursor จริงในเครื่องนี้

## เหมาะกับใคร

- คนที่ใช้ AI coding agent แล้วเจอปัญหา agent "มั่นใจผิดแต่ไปต่อ"
- ทีมที่อยากลด overengineering และ noisy diffs
- คนที่อยากมี baseline instruction file แบบสั้นและเอาไป merge ต่อได้
- ผู้ที่ออกแบบ internal skill / prompt / coding policy ให้ agent ในทีม
- คนที่ใช้ Claude Code หรือ Cursor และต้องการ rule ที่นำไปใช้ได้ทันที

## ไม่เหมาะกับใคร

- คนที่มองหา framework, SDK หรือระบบ skill orchestration ขนาดใหญ่
- ทีมที่คาดหวังความสามารถเฉพาะโดเมน เช่น trading execution, broker integration, cloud deployment หรือ data pipeline จาก repo นี้โดยตรง
- คนที่ต้องการ "วิธีทำงานทั้งหมด" มากกว่า "หลักพฤติกรรมการทำงาน"

## มุมมองสำหรับงาน AITrading / Agent Workflow

repo นี้ไม่ได้เกี่ยวกับ trading โดยตรง แต่เหมาะมากกับงานที่คุณกำลังทำในเชิง agent workflow เพราะหลายปัญหาในโปรเจกต์สาย automation/trading มักไม่ใช่แค่ "เขียนได้ไหม" แต่เป็น "เขียนแล้วไม่พัง ไม่เกิน scope และ verify ได้ไหม"

สิ่งที่น่าหยิบไปใช้มี 4 เรื่อง:

- ใช้ `Think Before Coding` เวลางานเกี่ยวกับ signal, risk rule, broker API หรือ data source ambiguity
- ใช้ `Simplicity First` กัน agent สร้าง abstraction trading engine เกินจำเป็น
- ใช้ `Surgical Changes` เวลาปรับ strategy/file เดิมที่มี logic ละเอียดและเสี่ยง regression
- ใช้ `Goal-Driven Execution` คู่กับ test/backtest/expected output ที่ตรวจซ้ำได้

ถ้าจะเอาไปใช้จริงในงาน AITrading ผมมองว่า value สูงสุดไม่ใช่การติดตั้ง repo นี้ทั้งดุ้น แต่คือการหยิบ 4 หลักนี้ไป merge กับ instruction เฉพาะโดเมนของคุณ เช่น:

- ห้ามเปลี่ยน trading logic เกินคำขอ
- ต้องยืนยัน expected behavior ด้วย backtest หรือ deterministic example
- ถ้า data source/symbol/timeframe ไม่ชัด ต้องถามก่อน
- อย่าเพิ่ม parameter หรือ configurability โดยไม่มีเหตุผลจาก strategy จริง

## ข้อสรุป

`multica-ai/andrej-karpathy-skills` เป็น repo ที่เล็กแต่มีประโยชน์มาก เพราะมันไม่พยายามเป็น framework ใหญ่โต แต่เจาะตรงปัญหาหลักของ coding agent แบบตรงจุด

ถ้ามองแบบตรงไปตรงมา repo นี้ไม่ได้มีความลึกทางเทคนิคสูงในเชิง implementation แต่มีคุณค่าสูงในเชิง "behavioral guardrail" โดยเฉพาะสำหรับทีมที่เริ่มใช้ AI ช่วยเขียนโค้ดแล้วอยากลดงานแก้ซ้ำจาก assumption ผิด, code ที่บวม, และ diff ที่เกิน scope

ถ้าคุณจะหยิบไปใช้กับงานจริง ผมแนะนำให้มองมันเป็น baseline instruction layer แล้วค่อยผสานกับกฎเฉพาะโปรเจกต์หรือเฉพาะโดเมนของคุณเอง

## แหล่งอ้างอิง

- GitHub repository: https://github.com/multica-ai/andrej-karpathy-skills
- Repository metadata API: https://api.github.com/repos/multica-ai/andrej-karpathy-skills
- Repository tree API: https://api.github.com/repos/multica-ai/andrej-karpathy-skills/git/trees/main?recursive=1
- README: https://github.com/multica-ai/andrej-karpathy-skills/blob/main/README.md
- `CLAUDE.md`: https://github.com/multica-ai/andrej-karpathy-skills/blob/main/CLAUDE.md
- `CURSOR.md`: https://github.com/multica-ai/andrej-karpathy-skills/blob/main/CURSOR.md
- `EXAMPLES.md`: https://github.com/multica-ai/andrej-karpathy-skills/blob/main/EXAMPLES.md
- Cursor rule: https://github.com/multica-ai/andrej-karpathy-skills/blob/main/.cursor/rules/karpathy-guidelines.mdc
- Skill file: https://github.com/multica-ai/andrej-karpathy-skills/blob/main/skills/karpathy-guidelines/SKILL.md
- Claude plugin manifest: https://github.com/multica-ai/andrej-karpathy-skills/blob/main/.claude-plugin/plugin.json
- Claude marketplace manifest: https://github.com/multica-ai/andrej-karpathy-skills/blob/main/.claude-plugin/marketplace.json
