# สรุป nai0om/buddhist-method

วันที่สรุป: 2026-05-22

แหล่งข้อมูลหลัก:
- https://github.com/nai0om/buddhist-method
- https://github.com/nai0om/buddhist-method/blob/main/README.md
- https://github.com/nai0om/buddhist-method/blob/main/README.th.md
- https://github.com/nai0om/buddhist-method/blob/main/SKILL.md
- https://github.com/nai0om/buddhist-method/blob/main/references/ariyasacca-debug.md
- https://github.com/nai0om/buddhist-method/blob/main/references/extended-principles.md

## ภาพรวม

`nai0om/buddhist-method` เป็น repository ขนาดเล็กที่ทำ “skill สำหรับ Claude” โดยยืมหลักคิดจากพุทธศาสนามาแปลงเป็นวินัยการทำงานสำหรับ LLM และงาน knowledge work ทั่วไป

แกนหลักของ repo ไม่ใช่การสอนธรรมะเชิงศรัทธา แต่เป็นการใช้ชื่อและกรอบคิดทางพุทธมาเป็น mnemonic/checklist เพื่อกัน failure mode ที่โมเดลและคนทำงานเจอบ่อย เช่น:

- พูดจากความคุ้นเคยแทนการตรวจสอบ
- แก้อาการแทนการหาเหตุ
- ทำงานต่อจาก state เก่าในหัว ทั้งที่ของจริงเปลี่ยนแล้ว
- ฝืน patch งานเดิม ทั้งที่ควรเขียนใหม่
- ซ่อนบั๊กด้วย workaround
- เปลี่ยนคำตอบเพราะแรงกดดัน ไม่ใช่เพราะหลักฐานใหม่

ถ้ามองแบบวิศวกรรม นี่คือ repo สาย “reasoning discipline” มากกว่า “software package”

## Repo นี้มีอะไร

โครงสร้างหลักมีแค่ไม่กี่ส่วน:

- `SKILL.md` เป็นตัว skill หลัก
- `references/ariyasacca-debug.md` เป็นกรอบ debug สำหรับปัญหาที่ยากหรือคลุมเครือ
- `references/extended-principles.md` เป็นหลักเสริมสำหรับสถานการณ์เฉพาะ
- `README.md` และ `README.th.md` อธิบายแนวคิดและวิธีติดตั้ง

จากหน้า GitHub ที่ผมตรวจดู Repo นี้เป็น public, ใช้ license แบบ MIT, มี commit history สั้นมาก และเนื้อหาทั้งหมดค่อนข้างตั้งใจให้ “กระชับ ใช้จริงได้” มากกว่าแตกเป็นระบบใหญ่

## แกนกลางของ Skill

repo นี้เสนอหลัก 6 ข้อเป็น checklist หลัก:

| หลัก | ความหมายเชิงปฏิบัติ | failure mode ที่พยายามกัน |
|---|---|---|
| `Kalāma` / กาลามสูตร | อย่าเชื่อจาก pattern ต้อง verify ก่อน | มั่นใจใน fact ทั้งที่ยังไม่ได้เช็ค |
| `Yoniso Manasikāra` / โยนิโสมนสิการ | มองหาเหตุ ไม่ใช่แค่ปิดอาการ | debug แบบฉาบหน้า |
| `Sati-Sampajañña` / สติ-สัมปชัญญะ | เช็ก state ปัจจุบันก่อนลงมือ | ทำงานจากความจำเก่า |
| `Anatta` / อนัตตา | ไม่ยึดติดกับ draft ของตัวเอง | ฝืน patch ของเดิมทั้งที่ทรงผิด |
| `Pahāna` / ปหานะ | ตัดเหตุ ไม่ใช่ซ่อน symptom | workaround ที่ทำให้บั๊กเงียบ |
| `Upekkhā` / อุเบกขา | นิ่งต่อแรงกดดัน แล้วดู evidence | เปลี่ยนคำตอบเพราะโดนกดดัน |

จุดแข็งของ repo คือไม่ได้เล่าเชิงนามธรรมอย่างเดียว แต่เขียนเป็นรูปแบบ `Trigger -> Action -> Anti-pattern` ทำให้นำไปใช้จริงง่าย

## อธิบายทีละหลักแบบภาษาคนทำงาน

### 1. กาลามสูตร = อย่าพูด fact จากความคุ้นเคย

หลักนี้บอกว่า ถ้ากำลังจะพูดเรื่องเฉพาะเจาะจง เช่น API field, CLI flag, version, ราคา, วันที่, พฤติกรรมของ library หรือ role ของคนใดคนหนึ่ง ต้องถามตัวเองก่อนว่า “รู้จากสิ่งที่เพิ่งตรวจ หรือแค่จำ pattern ได้”

สำหรับงาน AI/agent นี่สำคัญมาก เพราะ failure mode หลักของ LLM คือ “พูดเหมือนจริง” ได้ง่ายกว่าการ “รู้จริง”

### 2. โยนิโสมนสิการ = debug จากต้นเหตุ

หลักนี้เน้นว่าเวลาเห็น error หรือ output แปลก อย่าเพิ่งรีบแปะ `try/catch`, default value หรือ config tweak เพื่อให้ symptom หาย แต่ให้ตั้งสมมติฐานสาเหตุหลายทางก่อน แล้วเลือกตรวจจาก cause space

ถ้าเอาไปใช้กับงานโค้ด นี่คือ anti-hack mindset ที่ค่อนข้างดีมาก

### 3. สติ-สัมปชัญญะ = อย่าทำงานต่อจาก state ในหัว

เหมาะกับงานหลายขั้นตอน เช่น edit file, run command, เปลี่ยน config, อ่านผล test, แล้วค่อยกลับไปแก้อีกรอบ หลักนี้เตือนให้ re-read ของจริงก่อนเสมอ เพราะ mental model ที่ถูกเมื่อ 5 นาทีที่แล้วอาจไม่จริงแล้ว

หลักนี้เข้าท่ามากสำหรับ agent workflow เพราะหลายความพังเกิดจาก “จำว่าไฟล์เป็นแบบนี้” มากกว่าจะ “เปิดดูตอนนี้จริงๆ”

### 4. อนัตตา = กล้าทิ้ง draft ตัวเอง

ถ้ามีข้อมูลใหม่หรือ feedback ใหม่จนทำให้ approach เดิมดูผิดรูป หลักนี้บอกว่าอย่าฝืน patch ให้รอดหน้า แต่ให้ถามว่า “ถ้ายังไม่ได้เขียนของเดิมเลย ตอนนี้เราจะเลือกทรงแบบนี้ไหม”

ถ้าคำตอบคือไม่ ควร rewrite

ในมุม engineering นี่คือ anti sunk-cost principle ที่ดีมาก

### 5. ปหานะ = fix ให้หาย ไม่ใช่ทำให้เงียบ

หลักนี้ต่อจากโยนิโสมนสิการ คือเมื่อเจอสาเหตุแล้ว ให้แก้ที่สาเหตุจริง ไม่ใช่ทำ workaround ที่ซ่อนปัญหาไว้

repo อธิบายชัดว่า ถ้าแก้ต้นเหตุไม่ได้จริงๆ อย่างน้อยต้องเปิดเผยว่าเป็น limitation หรือ TODO ไม่ใช่พรางให้คนอ่านทีหลังคิดว่าปัญหาหายแล้ว

### 6. อุเบกขา = นิ่งเมื่อโดนกดดัน

หลักนี้ผมว่าดีมากสำหรับ agent/human collaboration เพราะจับพฤติกรรมที่เจอบ่อยมาก คือ พอ user ทักแรงหรือ tool fail หลายรอบ ระบบเริ่ม “มั่วเพราะกดดัน” หรือกลับคำตอบทั้งที่หลักฐานยังไม่เปลี่ยน

ใจความคือ ก่อนเปลี่ยนทิศ ให้ถามว่า evidence เปลี่ยนจริงไหม หรือแค่ pressure เพิ่มขึ้น

## Reference เสริมที่น่าสนใจ

repo นี้มีไฟล์อ้างอิงเสริม 2 ตัวที่ทำให้กรอบคิดลึกขึ้น:

### 1. Four Noble Truths as a Debugging Frame

ไฟล์ `ariyasacca-debug.md` เอาอริยสัจ 4 มาจัดเป็น flow debug:

- `Dukkha` = ระบุปัญหาให้ชัด
- `Samudaya` = หาเหตุ
- `Nirodha` = ยืนยันว่าปัญหาจบจริง
- `Magga` = สร้างทางป้องกัน/พัฒนาไม่ให้กลับมาอีก

ส่วนนี้ดีตรงที่ไม่หยุดแค่ “แก้ได้แล้ว” แต่บังคับให้คิดเรื่อง regression test, class ของ bug, และ habit change ต่อ

### 2. Extended Principles

ไฟล์ `extended-principles.md` เพิ่มหลักย่อยสำหรับสถานการณ์เฉพาะ เช่น:

- `Apāyakosalla` = รู้ว่า retry แล้วคุณภาพกำลังแย่ลง
- `Appamāda` = รักษาวินัยตอนงานยาว ไม่ให้มาตรฐานตกตอนท้าย
- `Sappurisadhamma` บางส่วน = รู้ตน รู้กาล รู้ผู้รับสาร
- `Atthatraya` = ชั่งประโยชน์ระยะสั้นกับระยะยาว
- `Majjhimā Paṭipadā` = หาทางสายกลางระหว่าง hardcode กับ over-engineering

อันนี้ทำให้ repo ไม่ได้หยุดแค่เรื่อง anti-hallucination แต่ขยายไปถึง decision quality และ execution quality ด้วย

## วิธีใช้งานตาม repo

แนวทางใช้งานหลักคือ clone ไปไว้ใน skill directory ของ Claude แล้วเพิ่ม pointer ใน `CLAUDE.md` เพื่อให้ Claude consult skill นี้เมื่อต้องทำงานที่เกี่ยวกับ:

- factual claims
- debugging
- user pushback
- long multi-step tasks

อีกมุมหนึ่ง ต่อให้ไม่ใช้ Claude ก็ยังอ่าน `SKILL.md` กับ `references/` เป็น checklist ส่วนตัวได้

## จุดเด่น

- ไอเดียชัด และมี positioning ชัดมากว่าแก้ failure mode อะไร
- เขียนสั้น แต่ใช้งานได้จริง เพราะทุกหลักมี trigger/action/anti-pattern
- ใช้ศัพท์บาลีเป็น mnemonic ได้ดี ถ้าผู้ใช้โอเคกับ framing นี้
- เอาหลักคิดเชิงพุทธมาแปลเป็น operational discipline ได้ค่อนข้างเนียน
- เหมาะกับทั้ง LLM workflow และ human workflow ไม่ได้จำกัดแค่ Claude
- MIT license ทำให้หยิบไปดัดแปลงหรือเอาไปเป็นต้นแบบได้ง่าย

## ข้อควรระวัง / ข้อจำกัด

- มันเป็น framework เชิงแนวคิด ไม่ใช่เครื่องมือที่ enforce พฤติกรรมจริง ดังนั้นผลลัพธ์ขึ้นกับว่าผู้ใช้หรือ agent เอาไปใช้สม่ำเสมอแค่ไหน
- ถ้าคนอ่านไม่คุ้นกับศัพท์บาลี อาจรู้สึกมี friction ช่วงแรก แม้ repo จะอธิบายว่าตั้งใจเก็บชื่อไว้เป็น mnemonic
- หลักการหลายข้อ “ดูจริง” ได้ยากถ้าไม่มี verification habit หรือ test discipline รองรับ
- repo นี้ไม่ได้มี implementation เชิงระบบ เช่น linter, policy engine หรือ evaluator ที่ตรวจจับได้อัตโนมัติว่า agent ทำตามหลักหรือไม่

## มุมมองสรุป

ถ้ามองตรงๆ `buddhist-method` ไม่ใช่ repo ที่ซับซ้อน แต่มันมี value สูงในฐานะ “operating manual สำหรับการคิดและทำงานให้ดีขึ้น” โดยเฉพาะกับยุค agent/LLM ที่ความเสี่ยงใหญ่ไม่ใช่แค่โค้ดพัง แต่คือการตอบผิดอย่างมั่นใจ, debug แบบปิดอาการ, และเปลี่ยนทิศเพราะแรงกดดัน

จุดที่น่าสนใจที่สุดไม่ใช่การเอาธรรมะมาแปะกับ AI แบบเก๋ๆ แต่คือการเลือกหลักที่ map กับ failure mode ของงานจริงได้ค่อนข้างแม่น:

- กาลามสูตร -> anti-hallucination
- โยนิโสมนสิการ + ปหานะ -> root-cause debugging
- สติ-สัมปชัญญะ -> state awareness
- อนัตตา -> anti sunk-cost rewrite discipline
- อุเบกขา -> steadiness under pushback

ถ้าคุณกำลังมองหา reference สำหรับออกแบบ skill, prompt discipline หรือ review checklist ของ agent ตัวเอง repo นี้น่าอ่านมาก เพราะมันไม่ยาว แต่แนวคิดคม และเอาไปประยุกต์ต่อได้หลายทาง

ถ้าจะวิจารณ์แบบตรงไปตรงมา ข้อจำกัดคือมันยังเป็น “คู่มือแนวคิด” มากกว่า “ระบบที่พิสูจน์ผลได้” ดังนั้นถ้าจะใช้ในทีมจริง อาจต้องต่อยอดด้วย process หรือ tooling เพิ่ม เช่น verification checklist, regression testing policy, review rubric หรือ agent evaluation harness

## เหมาะกับใคร

- คนที่ใช้ Claude Code หรือ coding agent บ่อย และอยากลด hallucination
- คนที่ทำ debugging งานยากๆ แล้วพบว่าตัวเองชอบแก้ปลายเหตุ
- ทีมที่อยากมี shared language สำหรับพูดเรื่องคุณภาพการคิด เช่น “อันนี้ยังไม่ Kalāma” หรือ “ตรงนี้ควร Anatta แล้ว”
- คนที่สนใจเอากรอบคิดทางพุทธมาแปลงเป็น workflow โดยไม่ต้องยึดเชิงศาสนา

## ข้อสรุปสั้นๆ

`nai0om/buddhist-method` คือ repo แนวคิดที่เล็ก แต่คม ใช้หลักพุทธ 6 ข้อมาแปลงเป็น checklist สำหรับการ verify fact, debug ที่ต้นเหตุ, re-check state, กล้าทิ้ง draft ที่ผิด, ไม่ซ่อนบั๊กด้วย workaround, และไม่เสียศูนย์เมื่อโดนกดดัน

ถ้าถามว่า “คุ้มค่าแก่การศึกษาไหม” คำตอบคือคุ้ม โดยเฉพาะถ้าคุณสนใจการออกแบบ agent workflow หรืออยากมี mental model ที่ช่วยกันพลาดซ้ำแบบเดิมๆ ในงาน reasoning-heavy
