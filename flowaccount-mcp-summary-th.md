# สรุป FlowAccountMCP

แหล่งข้อมูลหลัก: https://github.com/todsawat/FlowAccountMCP

วันที่สรุป: 2026-05-13

## ภาพรวม

FlowAccountMCP เป็น MCP server สำหรับเชื่อม AI assistant เช่น Claude เข้ากับ FlowAccount ซึ่งเป็นแพลตฟอร์มบัญชีออนไลน์ของไทย จุดประสงค์หลักคือให้ผู้ใช้จัดการข้อมูลบัญชีผ่าน natural language ได้ เช่น สร้าง/ดู/แก้ไขเอกสารขาย เอกสารซื้อ รายชื่อลูกค้า/ผู้ขาย สินค้า/บริการ การรับชำระเงิน และแนบไฟล์เอกสาร

โปรเจกต์เขียนด้วย TypeScript บน Node.js และใช้ `@modelcontextprotocol/sdk` เป็นแกน MCP server โดยสื่อสารผ่าน stdio transport เพื่อให้ต่อกับ Claude Desktop หรือ MCP client อื่นได้

## สิ่งที่ระบบทำได้

### เอกสารบัญชี

รองรับเอกสารหลัก 7 ประเภท:

- ใบเสนอราคา: list, get, create, update, delete, change status
- ใบกำกับภาษี: list, get, create, update, delete, record payment
- ใบเสร็จรับเงิน: list, get, create, update, delete, record payment
- ใบวางบิล: list, get, create, update, delete, record payment
- บิลเงินสด: list, get, create, update, delete, record payment
- ใบสั่งซื้อ: list, get, create, update, delete
- ค่าใช้จ่าย: list, get, create, update, delete, record payment

### ข้อมูลพื้นฐาน

- Contacts: สร้าง/ค้นหา/ดู/แก้ไข/ลบ ลูกค้าหรือผู้ขาย
- Products: สร้าง/ค้นหา/ดู/แก้ไข/ลบ สินค้าหรือบริการ
- Business info: ดูข้อมูลบริษัท
- Bank accounts: ดูบัญชีธนาคารที่ตั้งค่าไว้

### Payment และ Attachment

- มี `record_payment` เป็นเครื่องมือกลางสำหรับบันทึกการรับ/จ่ายเงินกับเอกสารหลายชนิด
- รองรับการอัปโหลดไฟล์แนบ เช่น PDF, รูปภาพ, Office docs, ZIP/RAR ไปยังเอกสาร

## Tech Stack

- Runtime: Node.js 18+
- Language: TypeScript / ESM
- MCP SDK: `@modelcontextprotocol/sdk`
- HTTP client: `axios`
- Validation: `zod`
- Authentication automation: `playwright`
- File upload: `form-data`
- Build/dev scripts:
  - `npm run build` สำหรับ compile TypeScript
  - `npm run dev` สำหรับรันด้วย `tsx`
  - `npm start` สำหรับรันไฟล์ compiled ใน `dist`
  - `npm run health-check` สำหรับ health check ตาม script ที่ repo ระบุ

## โครงสร้างระบบ

โครงสร้างหลักที่ README ระบุ:

- `src/index.ts`: entry point สำหรับ MCP stdio transport
- `src/server.ts`: สร้าง MCP server และ register tools ทั้งหมด
- `src/api/endpoints.ts`: กำหนด API endpoints ของ FlowAccount
- `src/api/http-client.ts`: HTTP client สำหรับ JSON request และ multipart file upload
- `src/auth/token-manager.ts`: จัดการ token lifecycle
- `src/auth/token-store.ts`: เก็บ token ลงไฟล์
- `src/auth/browser-auth.ts`: login ผ่าน Playwright browser
- `src/tools/`: กลุ่ม tool สำหรับ contacts, products, expenses, payments, attachments, business info และเอกสารแต่ละประเภท

จาก `src/server.ts` ตัว server จะ initialize auth ก่อน จากนั้นสร้าง `FlowAccountHttpClient` แล้ว register tools ตาม domain เช่น contacts, products, expenses, payments, documents และ attachments

## การเชื่อมต่อ FlowAccount API

ไฟล์ `src/api/endpoints.ts` ระบุว่า endpoints ถูกค้นพบจาก network interception บน `advance.flowaccount.com` และกระจายอยู่หลาย host:

- `https://api-core-canary.flowaccount.com/api`: ใช้กับเอกสารส่วนใหญ่ เช่น quotations, expenses, contacts, banks, tax invoices, receipts, billing notes, purchase orders
- `https://business-api.flowaccount.com`: ใช้กับ cash invoices
- `https://profile.flowaccount.com`: ใช้กับข้อมูล profile/company

จุดนี้สำคัญ เพราะ repo ไม่ได้ดูเหมือนใช้ public SDK อย่างเป็นทางการแบบตรง ๆ แต่ผูกกับ API endpoint ที่ค้นพบจากหน้าเว็บ FlowAccount ดังนั้นความเสถียรอาจขึ้นกับการเปลี่ยนแปลงภายในของ FlowAccount เอง

## Authentication

การ login ใช้ Playwright เปิด browser ไปที่ `https://advance.flowaccount.com/` ให้ผู้ใช้ login และเลือกบริษัท จากนั้นระบบจะจับ Bearer token, cookies และ company ID แล้วบันทึกไว้

ค่าเริ่มต้นของ token storage คือ:

```text
~/.flowaccount-mcp/tokens.json
```

พฤติกรรมสำคัญ:

- ถ้า token ยังไม่หมดอายุ จะ reuse token เดิม
- ถ้า token หมดอายุแต่ยังมี session cookies จะลอง silent refresh ก่อน
- ถ้า silent refresh ไม่สำเร็จ จะเปิด browser ให้ login ใหม่
- มี buffer 2 นาทีในการเช็ก token expiry
- มีการกัน concurrent refresh ด้วย shared promise เพื่อลดการ login/refresh ซ้อนกัน

## การติดตั้งและใช้งาน

เงื่อนไขพื้นฐาน:

- Node.js 18+
- มีบัญชี FlowAccount แบบ paid subscription ตาม README

ขั้นตอนติดตั้งจาก README:

```bash
git clone <repo-url>
cd FlowAccountMCP
npm install
npm run build
```

ตัวอย่างการตั้งค่า Claude Desktop:

```json
{
  "mcpServers": {
    "flowaccount": {
      "command": "node",
      "args": ["/path/to/FlowAccountMCP/dist/index.js"]
    }
  }
}
```

repo มี `.mcp.json` สำหรับ local MCP config:

```json
{
  "mcpServers": {
    "flowaccount": {
      "command": "node",
      "args": ["dist/index.js"],
      "env": {
        "FLOWACCOUNT_CULTURE": "th"
      }
    }
  }
}
```

## Configuration

Environment variables ที่ README ระบุ:

- `FLOWACCOUNT_CULTURE`: ค่าเริ่มต้น `th`, เลือกภาษา/locale เช่น `th`, `en`
- `FLOWACCOUNT_HEADLESS`: ค่าเริ่มต้น `false`, ใช้กำหนดว่า auth browser จะรันแบบ headless หรือไม่
- `FLOWACCOUNT_BROWSER_TIMEOUT`: ค่าเริ่มต้น `120000` ms
- `FLOWACCOUNT_TOKEN_PATH`: ค่าเริ่มต้น `~/.flowaccount-mcp/tokens.json`

## Manifest และ MCPB

repo มี `manifest.json` สำหรับ package/manifest ของ MCP server โดยระบุ:

- `manifest_version`: `0.2`
- ชื่อ server: `flowaccount`
- version: `1.0.0`
- author: Tod Sawatt
- license ใน manifest: `MIT`
- server type: `node`
- entry point: `dist/index.js`
- user config สำหรับ `culture` และ `headless`

หมายเหตุ: จาก file listing ในหน้า repo ไม่เห็นไฟล์ `LICENSE` แยกใน root แต่ `manifest.json` ระบุ license เป็น MIT

## จุดแข็ง

- ครอบคลุม workflow บัญชีพื้นฐานจำนวนมาก ทั้งขาย ซื้อ ค่าใช้จ่าย contacts products payment และ attachments
- เหมาะกับผู้ใช้ FlowAccount ในไทย เพราะมีชื่อเอกสาร/บริบทภาษาไทยชัดเจน
- Auth flow ออกแบบมาให้ผู้ใช้ login ผ่าน browser แทนการกรอก credential ลง config โดยตรง
- มี token refresh และ fallback re-authentication ลดภาระ login ซ้ำ
- โครงสร้าง repo แยก domain tools ค่อนข้างชัด ทำให้ดูแล/ต่อยอดแต่ละกลุ่มเครื่องมือได้ง่าย
- เหมาะกับ AI assistant workflow เช่น “สร้างใบเสนอราคา”, “ค้นหาลูกค้า”, “บันทึกรับชำระเงิน”, “แนบไฟล์เอกสาร”

## จุดที่ควรระวัง

- เครื่องมือมีสิทธิ์ create/update/delete เอกสารบัญชีจริง จึงควรใช้กับ MCP client ที่มี confirmation flow ก่อน action สำคัญ
- Token และ cookies ถูกเก็บในเครื่องที่ `~/.flowaccount-mcp/tokens.json`; ต้องป้องกันไฟล์นี้เหมือน credential
- ระบบอาศัย endpoint ที่ค้นพบจาก network interception ไม่ใช่ public API contract ที่ยืนยันจาก FlowAccount ใน README จึงอาจพังเมื่อ FlowAccount เปลี่ยน frontend/API ภายใน
- Host บางตัวใช้ชื่อ `api-core-canary.flowaccount.com` ซึ่งฟังดูเป็น environment ที่อาจเปลี่ยนแปลงได้ ควรทดสอบก่อนใช้จริงเสมอ
- การเปิด browser ด้วย Playwright อาจติดข้อจำกัดใน server/headless environment หรือเครื่องที่ไม่มี browser dependencies
- ยังไม่เห็น releases published ในหน้า GitHub ณ วันที่สรุป จึงควรมองเป็นโปรเจกต์ที่ต้องทดสอบเองก่อนใช้งานจริง
- การสรุปนี้อ้างอิงจาก README และไฟล์ source สำคัญบางไฟล์ ไม่ได้ clone, build, login FlowAccount, หรือทดสอบ API จริง

## เหมาะกับใคร

- ผู้ใช้ FlowAccount ที่อยากให้ AI assistant ช่วยจัดการเอกสารบัญชีจากภาษาธรรมชาติ
- ทีมเล็กหรือเจ้าของกิจการที่ใช้ Claude Desktop/MCP workflow อยู่แล้ว
- Developer ที่ต้องการตัวอย่าง MCP server สำหรับระบบ SaaS ไทยที่ต้องใช้ browser-based authentication
- คนที่ต้องการ automate งานเอกสารซ้ำ ๆ เช่น สร้างใบเสนอราคา ค้นหา contact บันทึก payment หรือแนบไฟล์

## ไม่เหมาะกับใคร

- ทีมที่ต้องการ integration production-grade พร้อม SLA โดยไม่ต้องดูแลเอง
- งานที่ต้องการ audit trail, permission boundary, approval workflow และ control ละเอียด แต่ MCP client ยังไม่มีชั้นยืนยันคำสั่ง
- องค์กรที่ห้ามเก็บ session token/cookies ของระบบบัญชีไว้ในเครื่อง local
- ผู้ใช้ที่ไม่มี FlowAccount paid subscription

## ข้อสรุป

FlowAccountMCP เป็นโปรเจกต์ที่มีประโยชน์มากถ้าต้องการเชื่อม FlowAccount เข้ากับ AI assistant ผ่าน MCP โดยเฉพาะงานเอกสารบัญชีที่ทำซ้ำบ่อย จุดเด่นคือ tool coverage กว้างและ auth flow ที่พยายามทำให้ผู้ใช้ login เองผ่าน browser

อย่างไรก็ตาม ควรมองเป็น integration ที่ต้องทดสอบและ harden ก่อนใช้งานจริง เพราะเกี่ยวข้องกับข้อมูลบัญชีและเอกสารทางธุรกิจโดยตรง รวมถึงใช้ endpoint ภายในที่อาจเปลี่ยนได้ หากจะใช้จริงควรเริ่มจาก environment/บริษัททดสอบ จำกัดสิทธิ์เครื่องที่รัน MCP server และตั้ง workflow ให้ confirm ก่อน create/update/delete หรือ record payment ทุกครั้ง

## แหล่งอ้างอิง

- GitHub repository: https://github.com/todsawat/FlowAccountMCP
- README: https://github.com/todsawat/FlowAccountMCP/blob/main/README.md
- `package.json`: https://github.com/todsawat/FlowAccountMCP/blob/main/package.json
- `src/server.ts`: https://github.com/todsawat/FlowAccountMCP/blob/main/src/server.ts
- `src/api/endpoints.ts`: https://github.com/todsawat/FlowAccountMCP/blob/main/src/api/endpoints.ts
- `src/api/http-client.ts`: https://github.com/todsawat/FlowAccountMCP/blob/main/src/api/http-client.ts
- `src/auth/token-manager.ts`: https://github.com/todsawat/FlowAccountMCP/blob/main/src/auth/token-manager.ts
- `src/auth/browser-auth.ts`: https://github.com/todsawat/FlowAccountMCP/blob/main/src/auth/browser-auth.ts
- `manifest.json`: https://github.com/todsawat/FlowAccountMCP/blob/main/manifest.json
