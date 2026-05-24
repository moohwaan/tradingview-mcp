# สรุป mattpocock/skills

แหล่งข้อมูลหลัก: https://github.com/mattpocock/skills

วันที่สรุป: 2026-05-22

## ภาพรวม

`mattpocock/skills` เป็น repository ที่รวม "agent skills" สำหรับงานวิศวกรรมซอฟต์แวร์จริง มากกว่าจะเป็น library, SDK หรือ application runtime

แกนหลักของ repo คือชุดไฟล์ `SKILL.md` ที่ออกแบบให้ coding agent อย่าง Claude Code, Codex หรือ agent อื่น ๆ ทำงานได้มีวินัยขึ้น โดยเฉพาะในเรื่อง:

- ลดความคลาดเคลื่อนระหว่างสิ่งที่ผู้ใช้คิดกับสิ่งที่ agent ลงมือทำ
- ทำให้ agent เข้าใจภาษาของ domain และ architecture ของ repo มากขึ้น
- บังคับให้มี feedback loop เช่น TDD, debugging loop, issue flow และ handoff
- ลดปัญหา codebase กลายเป็น "ball of mud" จากการให้ agent เขียนโค้ดเร็วเกินโดยไม่มีโครง

repo นี้วางตำแหน่งตัวเองชัดมากว่าเป็น "skills for real engineers" ไม่ใช่แนว vibe coding หรือ prompt สั้น ๆ ที่เน้นให้ AI ทำเร็วอย่างเดียว

## Repo นี้คืออะไร

สิ่งสำคัญที่ควรเข้าใจก่อนคือ repo นี้ไม่ได้ให้ความสามารถใหม่กับ runtime โดยตรง แต่มันให้ "behavioral layer" หรือ "workflow layer" แก่ agent

พูดง่าย ๆ คือ มันไม่ได้ทำให้ agent เขียน TypeScript, React, backend หรือ infra ได้เองแบบเวทมนตร์ แต่พยายามทำให้ agent:

- ถามคำถามก่อนเริ่มทำ
- ใช้คำศัพท์สอดคล้องกับ domain
- ทำงานทีละก้าวพร้อม feedback
- แปลงแผนเป็น issue/PRD ได้เป็นระบบ
- สรุป handoff ให้ session ถัดไปทำงานต่อได้

ดังนั้น value จริงของ repo นี้อยู่ที่ "วิธีคิดและวิธีทำงาน" มากกว่าตัวโค้ด

## แนวคิดหลักของ Repo

จาก README ผู้เขียนอธิบายว่า skill เหล่านี้ถูกสร้างขึ้นเพื่อแก้ failure mode ที่พบบ่อยเวลาใช้ coding agent

### 1. Agent ไม่เข้าใจสิ่งที่เราต้องการจริง

Matt Pocock มองว่าปัญหาแรกคือ misalignment ระหว่างคนกับ agent

ทางแก้ของเขาคือใช้ skill แนว grilling เช่น:

- `grill-me`
- `grill-with-docs`

สองตัวนี้มีหน้าที่ไล่ถามจน requirement ชัดขึ้น ไม่ปล่อยให้ agent เดาเงียบ ๆ แล้วลงมือทำทันที

### 2. Agent พูดเยอะ แต่ยังไม่เข้าใจ domain

README เน้นเรื่อง shared language หรือ ubiquitous language มาก โดยใช้ `CONTEXT.md` เป็นตัวเก็บคำศัพท์ domain และความหมายที่ตกลงร่วมกันในโปรเจกต์

แนวคิดนี้สำคัญมาก เพราะถ้า agent เข้าใจภาษาของระบบ เช่น คำเฉพาะใน business domain, module name, workflow state และ architectural decision มันจะ:

- พูดกระชับขึ้น
- ตั้งชื่อไฟล์/ฟังก์ชันได้ตรงบริบท
- อ่าน codebase ได้ง่ายขึ้น
- ใช้ token น้อยลงเพราะไม่ต้องอธิบายซ้ำยาว ๆ

### 3. Agent เขียนโค้ดได้ แต่ผลลัพธ์ไม่มั่นคง

repo นี้พยายามย้ำว่า "feedback loop คือความเร็วที่แท้จริง"

แทนที่จะปล่อยให้ agent เขียนยาว ๆ แล้วหวังว่าจะถูก ผู้เขียนเสนอให้ใช้:

- `tdd` สำหรับวงจร red-green-refactor
- `diagnose` สำหรับดีบักแบบมีขั้นตอน

จุดนี้สะท้อน mindset วิศวกรรมชัดมาก: ถ้าไม่มี test, ไม่มี reproduction, ไม่มี instrumentation งานของ agent จะกลายเป็นเดา

### 4. Agent ทำให้ codebase เสื่อมสภาพเร็ว

ผู้เขียนมองว่าการเร่งการเขียนโค้ดด้วย AI ทำให้ entropy ของระบบเพิ่มเร็วขึ้น

ทางแก้คือไม่มอง AI แค่เป็น code generator แต่ต้องมี skill ที่ช่วยดู architecture เช่น:

- `zoom-out`
- `improve-codebase-architecture`
- `to-prd`

จุดนี้เป็นมุมที่ดีมาก เพราะหลาย repo agent ชอบแก้เฉพาะจุด แต่ไม่ค่อยมีเครื่องมือคอยถามว่า "ระบบกำลังเละขึ้นหรือเปล่า"

## วิธีติดตั้งและเริ่มใช้งาน

README แนะนำ quickstart แบบสั้นมาก:

```bash
npx skills@latest add mattpocock/skills
```

หลังจากนั้นควรเลือกติดตั้ง `/setup-matt-pocock-skills` แล้วรันใน agent เพื่อกำหนด config ระดับ repo เช่น:

- ใช้ issue tracker อะไร
- ใช้ label อะไรสำหรับ triage
- จะเก็บ domain docs ไว้ตรงไหน

จุดนี้สำคัญมาก เพราะ repo นี้ไม่ได้เป็นแค่ collection ของ skill เดี่ยว ๆ แต่บาง skill ต้องมี "บริบทของ repo" ก่อนจึงจะทำงานได้ดี

## Skill สำคัญใน Repo

จาก README ปัจจุบัน repo แบ่ง skill หลักออกเป็น 3 กลุ่ม: Engineering, Productivity และ Misc

### Engineering

- `diagnose`  
  วงจรดีบักแบบมีระเบียบ: reproduce -> minimise -> hypothesise -> instrument -> fix -> regression-test

- `grill-with-docs`  
  ใช้ถามเจาะ requirement พร้อมอ้างอิง `CONTEXT.md` และ ADR เพื่อให้การคุยอยู่บนภาษาเดียวกัน

- `triage`  
  จัดการ issue ตาม state machine ของ triage roles

- `improve-codebase-architecture`  
  ช่วยหาโอกาส refactor หรือ deepening opportunities ใน codebase โดยอิงจาก domain language และ ADR

- `setup-matt-pocock-skills`  
  ตั้งค่า repo ให้ skill อื่นรู้ว่า issue tracker อยู่ที่ไหน, label ใช้อะไร, และ domain docs วางตรงไหน

- `tdd`  
  บังคับแนวทำงาน red-green-refactor ทีละ vertical slice

- `to-issues`  
  แตกแผน, spec หรือ PRD ให้เป็น issue ย่อยที่หยิบไปทำต่อได้

- `to-prd`  
  เปลี่ยน context ของบทสนทนาปัจจุบันให้เป็น PRD และส่งเข้า issue tracker

- `zoom-out`  
  บอกให้ agent อธิบายโค้ดจากมุมมองระดับระบบ ไม่จมกับไฟล์เฉพาะหน้า

- `prototype`  
  ทำ prototype แบบ throwaway เพื่อสำรวจ design ก่อน commit กับ implementation จริง

### Productivity

- `caveman`  
  โหมดสื่อสารแบบกระชับมาก เพื่อลด token และตัดคำฟุ่มเฟือย

- `grill-me`  
  สัมภาษณ์/ซักถามแผนหรือไอเดียอย่างเข้มข้นจน decision tree ชัด

- `handoff`  
  ย่อบริบทสนทนาเพื่อส่งต่องานให้ agent session ถัดไป

- `write-a-skill`  
  ช่วยสร้าง skill ใหม่ให้มีโครงสร้างที่ดี แยก `SKILL.md`, reference files และ utility scripts ตามความจำเป็น

### Misc

- `git-guardrails-claude-code`
- `migrate-to-shoehorn`
- `scaffold-exercises`
- `setup-pre-commit`

กลุ่มนี้เป็น utility skill ที่ไม่ใช่แกนของ methodology แต่หยิบใช้เฉพาะงานได้

## สิ่งที่น่าสนใจมากในเชิงออกแบบ

### 1. มันไม่พยายาม "ครอบทั้งกระบวนการ"

README ระบุชัดว่าผู้เขียนไม่ชอบแนวทางที่พยายาม own process ทั้งหมดแบบ rigid framework

เขาเลยออกแบบ skill ให้:

- เล็ก
- ดัดแปลงง่าย
- เอาไปประกอบกันได้
- ใช้ได้กับหลาย model

นี่เป็นข้อดีมากสำหรับคนที่ไม่อยากผูก workflow ทั้งชีวิตกับระบบเดียว

### 2. ใช้ `CONTEXT.md` เป็นอาวุธหลัก

repo นี้ไม่ใช่แค่รวม prompt แต่พยายามสร้าง shared domain memory ให้ agent ผ่าน `CONTEXT.md` และ `docs/adr/`

ความคิดนี้ดีมาก เพราะมันแก้ pain point จริงของงาน AI coding คือ "agent อ่าน code ได้ แต่ยังไม่เข้าใจภาษาของทีม"

### 3. มี concept ของ per-repo setup

skill อย่าง `setup-matt-pocock-skills` แสดงให้เห็นว่า Matt ไม่ได้มอง skill เป็น prompt ลอย ๆ

เขามองว่าถ้าจะใช้ skill ให้ได้ผล ต้องมี config ของ repo เช่น:

- issue tracker
- label mapping
- single-context หรือ multi-context
- ตำแหน่ง domain docs

นี่คือการขยับจาก prompt engineering ไปสู่ repository-aware workflow

### 4. ฝัง software engineering philosophy ลงใน skill

repo นี้แอบ encode ปรัชญาวิศวกรรมหลายสายไว้ เช่น:

- Domain-Driven Design
- TDD
- ADR-driven decision memory
- feedback loop first
- architecture as ongoing care

ดังนั้นมันไม่ใช่แค่ชุดคำสั่งสำหรับ AI แต่มันคือ "วิธีสอน AI ให้ทำงานคล้าย senior engineer มากขึ้น"

## ข้อดี

- แนวคิดชัด และมีปรัชญารองรับ ไม่ใช่ prompt random
- เน้นปัญหาจริงของ coding agent เช่น misalignment, verbosity, lack of feedback, architecture decay
- composable ดี สามารถเลือกใช้เฉพาะ skill ที่เหมาะกับ workflow ของตัวเองได้
- มีทั้งระดับ discovery, planning, implementation, debugging และ handoff
- ใช้โครง `CONTEXT.md` + ADR + issue tracker config ซึ่งมีประโยชน์มากใน repo ที่จริงจัง
- เหมาะกับทีมที่อยากทำให้ agent ทำงานสม่ำเสมอขึ้น ไม่ใช่เก่งเป็นครั้ง ๆ

## ข้อจำกัดและข้อควรระวัง

- มันไม่ใช่ระบบอัตโนมัติเต็มรูปแบบ ผลลัพธ์ขึ้นกับว่า agent ปฏิบัติตาม skill ได้ดีแค่ไหน
- ไม่ได้ให้ domain knowledge เฉพาะทาง เช่น cloud, data engineering, trading, security product detail หรือ framework-specific best practices มากนัก
- บาง skill ต้องพึ่งวินัยในการใช้งานจริง ถ้าทีมไม่รัน `setup-matt-pocock-skills` หรือไม่อัปเดต `CONTEXT.md` ก็อาจได้ประโยชน์ไม่เต็ม
- มันช่วยให้ process ดีขึ้น แต่ไม่ได้การันตีว่า implementation จะถูกต้อง ถ้าไม่มี tests/tools/observability จริง
- ถ้าใช้แบบทื่อ ๆ อาจกลายเป็น overhead สำหรับงานเล็กมากที่ไม่จำเป็นต้องมีพิธีการเยอะ

## เหมาะกับใคร

- คนที่ใช้ Claude Code, Codex หรือ coding agent อื่นแล้วรู้สึกว่า agent "ทำได้ แต่ยังไม่น่าไว้ใจ"
- ทีมที่อยากให้ AI ทำงานใน repo อย่างมีภาษาและกติกากลาง
- คนที่อยากยกระดับจาก prompt เดี่ยว ๆ ไปสู่ workflow ระดับ repo
- คนที่ต้องทำงานยาวหลาย session แล้วต้องการ handoff, issue flow และ context memory ที่ดี
- คนที่สนใจสร้าง skill ของตัวเองและอยากดู reference ที่มี philosophy ค่อนข้างชัด

## ไม่เหมาะกับใคร

- คนที่มองหา framework สำหรับ build app โดยตรง
- คนที่ต้องการ integration เชิง runtime เช่น API client, database driver หรือ deployment system
- คนที่หวังว่า install แล้ว agent จะเก่งขึ้นทันทีโดยไม่ต้องดูแล `CONTEXT.md`, ADR หรือ workflow ภายในทีม

## มุมมองสำหรับงาน AITrading

ถ้ามองจากบริบทงาน AITrading หรือการสร้าง internal agent workflow ผมว่าจุดที่น่าเอาไปใช้จริงมีหลายข้อ:

- ใช้ `grill-me` หรือ `grill-with-docs` ก่อนลงมือทำ strategy, automation หรือ tool ใหม่
- ใช้ `tdd` กับส่วนที่มี logic ชัด เช่น parser, calculator, signal validation หรือ transformation layer
- ใช้ `diagnose` ตอนเจอ bug ยาก ๆ เช่นข้อมูล feed ไม่ตรง, symbol mapping เพี้ยน, หรือ state machine ทำงานผิด
- ใช้ `handoff` เวลาทำงานหลายรอบและอยากให้ agent ตัวถัดไปต่อบริบทได้แม่น
- ใช้แนวคิด `CONTEXT.md` เพื่อเก็บคำศัพท์สำคัญของระบบ เช่น strategy, signal, execution state, risk event, broker action

ถ้าจะหยิบไปใช้จริง ผมมองว่าไม่จำเป็นต้องใช้ทุก skill ทั้ง repo แต่ควรเลือกเฉพาะชุดที่ตรง pain point ของทีม เช่น:

- discovery/planning: `grill-me`, `grill-with-docs`
- implementation quality: `tdd`, `diagnose`
- architecture hygiene: `zoom-out`, `improve-codebase-architecture`
- continuity: `handoff`

## ข้อสรุป

`mattpocock/skills` เป็น repo ที่มีคุณค่าสูงมากถ้ามองมันเป็น "ชุดแนวปฏิบัติสำหรับทำให้ coding agent ทำงานแบบวิศวกรซอฟต์แวร์ที่มีวินัย" ไม่ใช่มองว่าเป็นเครื่องมือวิเศษที่ติดตั้งแล้วจบ

จุดเด่นที่สุดคือมันพยายามแก้ปัญหาหลักของ AI coding โดยตรง:

- เข้าใจ requirement ไม่พอ
- ไม่เข้าใจภาษาของระบบ
- ไม่มี feedback loop
- ทำให้ codebase เละเร็ว

ถ้าคุณใช้ agent ทำงานจริงจังกับ repo เดิมนาน ๆ repo นี้ควรค่าแก่การศึกษาและหยิบบางแนวคิดไปปรับใช้มากกว่า "คัดลอกทั้งหมดมาใช้ทั้งดุ้น"

สรุปแบบตรงไปตรงมา: นี่ไม่ใช่ repo ที่ทำให้ AI ฉลาดขึ้นในเชิงเนื้อหาวิชา แต่มันช่วยให้ AI "ทำงานอย่างมีทรงและมีระบบมากขึ้น" ซึ่งในหลายกรณีมีค่ามากพอ ๆ กับความรู้เฉพาะทางเลย

## แหล่งอ้างอิง

- GitHub repository: https://github.com/mattpocock/skills
- README: https://github.com/mattpocock/skills/blob/main/README.md
- CONTEXT.md: https://github.com/mattpocock/skills/blob/main/CONTEXT.md
- setup-matt-pocock-skills: https://github.com/mattpocock/skills/blob/main/skills/engineering/setup-matt-pocock-skills/SKILL.md
- diagnose: https://github.com/mattpocock/skills/blob/main/skills/engineering/diagnose/SKILL.md
- improve-codebase-architecture: https://github.com/mattpocock/skills/blob/main/skills/engineering/improve-codebase-architecture/SKILL.md
- handoff: https://github.com/mattpocock/skills/blob/main/skills/productivity/handoff/SKILL.md
- write-a-skill: https://github.com/mattpocock/skills/blob/main/skills/productivity/write-a-skill/SKILL.md
