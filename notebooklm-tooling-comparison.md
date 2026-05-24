# เปรียบเทียบ `teng-lin/notebooklm-py` vs `PleasePrompto/notebooklm-mcp`

อัปเดตข้อมูล: 13 พฤษภาคม 2026

## TL;DR
- ถ้าคุณต้องการ **เชื่อม NotebookLM เข้ากับ agent ผ่าน MCP แบบเร็วๆ** และใช้กับ Codex/Claude/Cursor เป็นหลัก: เลือก `notebooklm-mcp`
- ถ้าคุณต้องการ **เขียน automation/custom workflow ใน Python แบบลึก** (เช่น pipeline, export หลายแบบ, script เฉพาะงาน): เลือก `notebooklm-py`
- ถ้าจะใช้งานจริงระยะยาว: ใช้คู่กันได้ (`notebooklm-mcp` สำหรับ agent runtime + `notebooklm-py` สำหรับงาน batch/script)

## ภาพรวมสถาปัตยกรรม

### `teng-lin/notebooklm-py`
- แนวทาง: Python library + CLI + skill integration
- จุดเด่น: เน้น "programmatic API" และงาน automation แบบเขียนโค้ดได้ละเอียด
- กลุ่มผู้ใช้หลัก: นักพัฒนา Python, ทีมที่มี backend/data pipeline

### `PleasePrompto/notebooklm-mcp`
- แนวทาง: MCP server (TypeScript/Node) สำหรับให้ agent เรียก tool ได้โดยตรง
- จุดเด่น: plug เข้ากับ MCP client ได้เร็ว (`npx notebooklm-mcp@latest`)
- กลุ่มผู้ใช้หลัก: คนที่ใช้ Codex/Claude/Cursor และอยากให้ agent ใช้ NotebookLM ทันที

## ข้อดี / ข้อด้อย

## 1) `notebooklm-py`

### ข้อดี
- รองรับการใช้งานหลายโหมด: library, CLI, agent skill
- README ระบุ feature กว้างมาก เช่น import source, chat/research, generate artifacts, download/export หลาย format
- เหมาะกับงาน "ควบคุมละเอียด" และต่อเข้าระบบ Python เดิมได้ง่าย
- community traction สูง (ดาว/ฟอร์กค่อนข้างมาก)

### ข้อด้อย
- เป็น unofficial และใช้ undocumented APIs (ผู้พัฒนาระบุเองว่ามีโอกาส break ได้)
- onboarding ฝั่ง Python อาจซับซ้อนกว่า MCP ตรงๆ (dependency, auth state, browser/cookies mode)
- ถ้าเป้าหมายมีแค่ "ให้ agent ถามตอบจาก NotebookLM" อาจเกินความจำเป็น

## 2) `notebooklm-mcp`

### ข้อดี
- ติดตั้งเร็วและตรง use case agent มาก (`codex mcp add ...`, `claude mcp add ...`)
- มี MCP-native concept ครบ: tools/resources, tool profiles, health/auth/session, และ HTTP transport
- รองรับสถานการณ์ใช้งานกับหลาย MCP clients ได้ดี
- มี citation/source formatting สำหรับคำตอบจาก notebook เหมาะกับ workflow ถาม-ตอบ

### ข้อด้อย
- ฟีเจอร์ที่เปิดผ่าน tools อาจแคบกว่า library ขนาดใหญ่บางตัว (เน้น Q&A + library/session/admin + audio workflow ที่กำหนดไว้)
- พึ่งพา browser automation/profile state เช่นกัน จึงยังมีความเปราะต่อการเปลี่ยน UI/flow
- เป็น unofficial integration เหมือนกัน

## ความเสี่ยงร่วม (สำคัญ)
- ทั้งสองโครงการ **ไม่ใช่ API ทางการจาก Google NotebookLM**
- มีความเสี่ยงเรื่องความเสถียรเมื่อ endpoint/UI เปลี่ยน
- ควรใช้บัญชีแยกสำหรับ automation, จำกัดสิทธิ์, และเตรียม fallback เมื่อ auth หลุดหรือ flow เปลี่ยน

## เทียบแบบใช้งานจริง
- ต้องการใช้งานกับ agent เร็วที่สุด: `notebooklm-mcp` เด่นกว่า
- ต้องการเขียนระบบ Python ยืดหยุ่นสูง: `notebooklm-py` เด่นกว่า
- ต้องการทั้งสองแบบ: ใช้ MCP สำหรับ interactive agent และใช้ Python สำหรับ batch/offline processing

## คำแนะนำว่า "ควรใช้อันไหนดี"

แนะนำเริ่มจาก `PleasePrompto/notebooklm-mcp` ก่อน ถ้าเป้าหมายหลักของคุณคือ:
- ใช้งานกับ Codex/Claude/Cursor
- อยากเริ่มเร็ว
- เน้นถาม-ตอบจากความรู้ใน NotebookLM ใน workflow MCP

เลือก `teng-lin/notebooklm-py` แทน ถ้าคุณต้องการ:
- เขียนโค้ด Python เชิงลึก
- pipeline สร้าง/แปลง/export ข้อมูลจำนวนมาก
- custom logic ที่ MCP tool-set มาตรฐานยังไม่ครอบคลุม

ข้อเสนอแนะเชิงปฏิบัติ:
1. เริ่ม PoC ด้วย `notebooklm-mcp` เพื่อยืนยัน workflow agent
2. ถ้าต้องการงาน automation ขั้นสูง ค่อยเสริม `notebooklm-py`
3. แยก account/profile สำหรับงานอัตโนมัติ และทำ runbook เรื่อง re-auth/rollback ไว้เสมอ

## แหล่งอ้างอิง
- https://github.com/teng-lin/notebooklm-py
- https://github.com/PleasePrompto/notebooklm-mcp
