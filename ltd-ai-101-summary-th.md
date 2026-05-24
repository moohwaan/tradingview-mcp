# สรุป LTD AI 101

แหล่งข้อมูลหลัก: https://github.com/longtundiary/ltd-ai-101

วันที่สรุป: 2026-05-13

## ภาพรวม

`ltd-ai-101` คือคอร์สภาษาไทยสำหรับคนเริ่มใช้ Claude Code จากศูนย์ โดยวางตัวเป็นคอร์สแบบ interactive ที่ให้ผู้เรียนเปิด repo นี้ใน Claude Code แล้วพิมพ์ `Start Lesson 1`, `Start Lesson 2`, ... เพื่อให้ Claude ทำหน้าที่เป็นผู้สอนทีละขั้น

แกนหลักของคอร์สคือการสร้างเครื่องมือเดียวที่ค่อย ๆ พัฒนาขึ้นตลอด 5 บท ได้แก่ `/brief TICKER` สำหรับสรุปหุ้น 1 ตัวเป็นไฟล์ Markdown ในโฟลเดอร์ `briefs/` โดยเริ่มจาก slash command แบบง่าย แล้วค่อยเพิ่ม skill, source จริง, sub-agent และหน้า showcase ที่ deploy ได้

จากข้อมูล repo ณ วันที่อ่าน โปรเจกต์เพิ่งสร้างเมื่อ 2026-05-09 และยังมีสถานะใน README ว่า `in-progress` แต่ไฟล์ lesson ทั้ง 5 บทมีอยู่ใน repo แล้ว

## เป้าหมายของคอร์ส

คอร์สนี้แก้ปัญหาคนที่ติดตั้ง Claude Code แล้ว แต่ยังไม่รู้ว่าจะเริ่มใช้งานจริงอย่างไร โดยเฉพาะคนที่ไม่ถนัด terminal หรือไม่ใช่นักพัฒนา

แนวทางของคอร์สไม่ใช่ให้นั่งอ่าน documentation เฉย ๆ แต่ให้ Claude Code เป็นผู้สอนในหน้าต่างหนึ่ง และให้ผู้เรียนสร้าง project จริงในอีกหน้าต่างหนึ่ง ระหว่างทางมี checkpoint ให้หยุดยืนยันผลลัพธ์ก่อนขยับต่อ

ผลลัพธ์ปลายทางคือผู้เรียนจะเข้าใจ 4 building blocks สำคัญของ Claude Code:

- `CLAUDE.md`: ไฟล์กำหนดบริบท วิธีทำงาน และเสียงของโปรเจกต์
- Slash command: คำสั่งลัด เช่น `/brief AAPL`
- Skill: SOP หรือทักษะที่ Claude เรียกใช้ซ้ำได้
- Sub-agent: การแตกงาน research ออกเป็น agent เฉพาะทางหลายตัว

## โครงสร้าง repo

ไฟล์หลักที่สำคัญ:

- `README.md`: หน้าแนะนำคอร์สสำหรับผู้เรียน
- `CLAUDE.md`: instructor frame สำหรับให้ Claude รับบทเป็นผู้สอน
- `DISCLAIMER.md`: คำเตือนว่าเป็นเนื้อหาเพื่อการศึกษา ไม่ใช่คำแนะนำลงทุน
- `LICENSE`: เงื่อนไขการใช้แบบ All Rights Reserved ใช้ส่วนตัวเพื่อการศึกษาได้ แต่ห้ามขาย/ใช้เชิงพาณิชย์/เผยแพร่ต่อในนามอื่น
- `lesson-modules/1-foundations/CLAUDE.md`: Lesson 1
- `lesson-modules/2-skill-and-voice/CLAUDE.md`: Lesson 2
- `lesson-modules/3-earning-and-cost/CLAUDE.md`: Lesson 3
- `lesson-modules/4-subagents/CLAUDE.md`: Lesson 4
- `lesson-modules/5-deploy-and-recap/CLAUDE.md`: Lesson 5
- `Welcome.pdf` และ `welcome-source/`: เอกสาร/asset สำหรับหน้า welcome

## สรุปแต่ละบทเรียน

### Lesson 1: Foundations

เป้าหมายคือให้ผู้เรียนเข้าใจความต่างของ Chat, Cowork และ Code, รู้จักจุดสำคัญบนหน้าจอ Claude Code เช่น working directory, model picker และ mode picker จากนั้นสร้างโฟลเดอร์ `my-first-project` เป็นหน้าต่างที่ 2

สิ่งที่สร้างในบทนี้:

- `CLAUDE.md` ตัวแรกใน project ใหม่
- `.claude/commands/brief.md`
- Slash command `/brief TICKER`
- ไฟล์ผลลัพธ์ใน `briefs/<TICKER>.md`

จุดสำคัญคือ `/brief` เวอร์ชันแรกยังเป็น prompt ตรง ๆ มากกว่า workflow ที่แข็งแรง จึงอาจมีปัญหาเรื่อง hallucination หรือ output ไม่ครบ แต่ใช้เป็น skeleton สำหรับบทถัดไป

### Lesson 2: Skill + Voice

บทนี้ยกระดับ `/brief` จาก slash command ธรรมดาให้มี SOP ผ่าน skill ชื่อ `company-brief`

สิ่งที่สร้าง/แก้:

- `.claude/skills/company-brief/SKILL.md`
- เพิ่ม section `How I invest` ใน `my-first-project/CLAUDE.md`
- ปรับ output ให้มี 6 sections เช่น company snapshot, fundamentals signal, latest earnings, bull/bear, kill conditions และ questions before owning

จุดเด่นของบทนี้คือเริ่มทำให้ output มีโครงคงที่ และเริ่มใส่ "เสียงนักลงทุน" ของผู้ใช้เอง เพื่อลดความ generic ของบทวิเคราะห์

### Lesson 3: Earnings Transcript + Cost Control

บทนี้แก้จุดอ่อนของ `/brief` ที่อาจแต่งข้อมูล earnings จาก memory โดยให้ผู้เรียนใส่ transcript จริงลงในโฟลเดอร์ source

สิ่งที่สร้าง/แก้:

- `sources/`
- `sources/<TICKER>/q*-call.md`
- ปรับ `company-brief` skill ให้อ่านไฟล์ใน `sources/<TICKER>/` ก่อนเขียนส่วน Latest earnings
- ฝึกใช้ `/context` เพื่อดู token usage
- ฝึกเลือก model ให้เหมาะกับงาน เช่น Sonnet/Opus/Haiku ตามความหนักของงาน

บทนี้เป็นจุดเปลี่ยนสำคัญ เพราะเปลี่ยน `/brief` จากการให้ Claude ตอบจากความจำ ไปเป็นการให้ Claude อ่าน source ที่ผู้ใช้ควบคุมและตรวจสอบได้

### Lesson 4: Sub-agents

บทนี้แตกงาน research ออกเป็น agent 3 ตัว เพื่อให้แต่ละ agent ถือบริบทของตัวเองและทำงานเฉพาะด้าน

ตัวอย่าง agent ที่บทนี้ให้สร้าง:

- Fundamentals agent: อ่าน 10-K หรือข้อมูลพื้นฐานบริษัท
- Earnings agent: อ่าน transcript จาก Lesson 3
- News/Sentiment agent: ใช้ web search หรือข่าวล่าสุด

สิ่งที่สร้าง/แก้:

- `.claude/agents/<agent-name>.md` จำนวน 3 ตัว
- ปรับ `company-brief` skill ให้เรียก agent by name แทนการ inline research ทั้งก้อน
- เพิ่ม source 10-K เช่น `sources/<TICKER>/10-k-*.md`

บทนี้มี caveat ชัดเจนว่า sub-agent dispatch อาจขึ้นกับ version ของ Claude Code และ syntax ของ tool ในเครื่องผู้เรียน หาก parallel dispatch ไม่ทำงาน อย่างน้อยยังได้ structure ที่สะอาดขึ้นกว่าการให้ skill ตัวเดียวแบกทุกอย่าง

### Lesson 5: Deploy + ClaudyOS Recap

บทสุดท้ายสร้างหน้า showcase สำหรับอ่าน brief ที่ generate แล้ว และ deploy ขึ้น Vercel

สิ่งที่สร้าง/ทำ:

- `showcase/index.html`
- หน้าเว็บที่ list ไฟล์ใน `briefs/`
- Preview ในเครื่องก่อน deploy
- Deploy ไป Vercel เพื่อได้ URL แบบ `*.vercel.app`
- สรุปภาพรวมว่า artifact ที่สร้างมาตลอดคอร์สประกอบเป็น layered system อย่างไร

บทนี้ยังชวนให้เอา pattern เดียวกันไปใช้กับงานอื่น เช่น watchlist scout, earnings recap หรือ vendor/partnership/hiring brief

## วิธีใช้งานตาม repo

ขั้นตอนเริ่มต้นตาม README คือ:

1. เปิดโฟลเดอร์ `ltd-ai-101` ใน Claude Code
2. ตรวจว่าเห็น `README.md`, `CLAUDE.md` และ `lesson-modules/`
3. พิมพ์ `Start Lesson 1`
4. ทำตามบทสนทนาที่ Claude สอนทีละ checkpoint
5. จบบทแล้วค่อยพิมพ์ `Start Lesson 2`, `Start Lesson 3`, ต่อไปตามลำดับ

คอร์สใช้ two-window pattern:

- Window 1: เปิด repo `ltd-ai-101` ทำหน้าที่เป็นผู้สอน
- Window 2: เปิด project ของผู้เรียน เช่น `my-first-project` สำหรับสร้างไฟล์จริง

## จุดแข็ง

- เหมาะกับ beginner จริง เพราะบทเรียนออกแบบให้หยุดรอผู้เรียน ไม่เร่งข้าม checkpoint
- ใช้ artifact เดียวต่อเนื่องทั้งคอร์ส ทำให้เห็นพัฒนาการจาก prompt ง่าย ๆ ไปเป็น workflow ที่เป็นระบบ
- เนื้อหาเป็นภาษาไทยและใช้บริบทนักลงทุน/คนทำคอนเทนต์ไทย ทำให้จับต้องง่ายกว่าคู่มือ generic
- สอนแนวคิด Claude Code ที่ใช้ทำงานจริง เช่น `CLAUDE.md`, slash command, skill, sub-agent, source discipline และ deploy
- มีการย้ำเรื่อง hallucination, source traceability และ cost/token discipline ตั้งแต่ต้น
- ไม่บังคับให้ผู้เรียนเขียน code เองตั้งแต่แรก แต่ให้เรียนผ่านการสั่ง Claude สร้างและตรวจไฟล์จริง

## จุดที่ควรระวัง

- Repo ระบุสถานะ `in-progress` จึงควรมองเป็นคอร์สที่ยังอาจเปลี่ยนแปลงได้
- เนื้อหาออกแบบมาสำหรับ Claude Code โดยตรง ถ้าใช้ editor/agent ตัวอื่น อาจต้องปรับคำสั่งและ workflow
- Lesson 4 พึ่งพาความสามารถ sub-agent ของ Claude Code ซึ่งอาจต่างกันตาม version หรือ UI ของผู้เรียน
- ตัวอย่าง `/brief` เกี่ยวกับหุ้น แต่ repo ย้ำว่าเป็นเพื่อการศึกษา ไม่ใช่คำแนะนำลงทุน
- License เป็น All Rights Reserved ใช้ได้เพื่อการศึกษาส่วนตัวเท่านั้น ไม่ควรนำไปทำคอร์ส/บริการ/สินค้าต่อโดยไม่ขออนุญาต
- การสรุปนี้อ้างอิงจาก README, CLAUDE.md, lesson files, DISCLAIMER และ LICENSE เท่านั้น ยังไม่ได้ clone/run คอร์สจริงใน Claude Code

## เหมาะกับใคร

- คนที่เพิ่งติดตั้ง Claude Code และยังไม่รู้ว่าจะเริ่มใช้งานจริงอย่างไร
- นักลงทุนหรือ creator ที่อยากสร้างเครื่องมือ research ส่วนตัวโดยไม่ต้องเริ่มจากการเขียน code เต็มรูปแบบ
- คนที่อยากเข้าใจ workflow ของ Claude Code ผ่านตัวอย่างที่เป็นงานจริง ไม่ใช่ demo เล็ก ๆ แบบ todo app
- คนที่ต้องการเรียนวิธีคุม AI ให้ทำงานกับไฟล์, source, SOP และ agent หลายตัวอย่างเป็นระบบ

## ไม่เหมาะกับใคร

- คนที่ต้องการ trading bot สำเร็จรูป หรือระบบให้สัญญาณซื้อขายอัตโนมัติ
- คนที่ต้องการ framework production-ready สำหรับ financial research ทันที
- คนที่อยากอ่านเอกสารสั้น ๆ แล้วจบ เพราะคอร์สนี้ตั้งใจให้ทำตามใน Claude Code แบบ interactive
- คนที่ต้องการนำเนื้อหาไปใช้เชิงพาณิชย์ เพราะ license จำกัดการใช้งานไว้เพื่อการศึกษาส่วนตัว

## มุมมองสรุป

`ltd-ai-101` เป็นคอร์ส Claude Code ภาษาไทยที่น่าสนใจมากในแง่ "สอนให้ใช้ agentic coding tool ผ่านการสร้างระบบงานจริง" ไม่ใช่แค่สอนคำสั่งแยก ๆ จุดเด่นคือการค่อย ๆ ทำให้ผู้เรียนเห็นว่า prompt ธรรมดาสามารถพัฒนาเป็น slash command, skill, source-aware workflow, sub-agent system และ public showcase ได้อย่างไร

สำหรับบริบทในโฟลเดอร์ AITrading repo นี้ควรมองเป็น learning resource สำหรับสร้าง research workflow ส่วนตัว มากกว่าจะเป็น quantitative trading framework หรือ trading system โดยตรง ถ้าจะเอาแนวคิดไปใช้กับงานลงทุนจริง ควรเพิ่ม source verification, financial data pipeline, risk model และ human review ก่อนเสมอ

## แหล่งอ้างอิง

- GitHub repository: https://github.com/longtundiary/ltd-ai-101
- README: https://github.com/longtundiary/ltd-ai-101/blob/main/README.md
- Instructor frame: https://github.com/longtundiary/ltd-ai-101/blob/main/CLAUDE.md
- Lesson modules: https://github.com/longtundiary/ltd-ai-101/tree/main/lesson-modules
- Disclaimer: https://github.com/longtundiary/ltd-ai-101/blob/main/DISCLAIMER.md
- License: https://github.com/longtundiary/ltd-ai-101/blob/main/LICENSE
