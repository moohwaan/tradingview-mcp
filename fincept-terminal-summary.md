# สรุป Fincept Terminal

วันที่บันทึก: 2026-05-09

แหล่งข้อมูลหลัก:
- https://github.com/Fincept-Corporation/FinceptTerminal
- https://github.com/Fincept-Corporation/FinceptTerminal/blob/main/docs/GETTING_STARTED.md
- https://github.com/Fincept-Corporation/FinceptTerminal/blob/main/docs/COMMERCIAL_LICENSE.md
- https://github.com/Fincept-Corporation/FinceptTerminal/releases
- https://sourceforge.net/projects/fincept-terminal.mirror/files/v4.0.2/

## ภาพรวม

Fincept Terminal คือโปรเจกต์โอเพนซอร์สที่พยายามทำ financial intelligence terminal คล้าย Bloomberg/Refinitiv แต่เปิดให้ใช้ฟรีในเชิง non-commercial/academic โดยเน้น desktop native, market data, analytics, AI agents และ workflow automation

- Repo: Fincept-Corporation/FinceptTerminal
- เป้าหมาย: เครื่องมือวิเคราะห์การเงิน/ตลาดทุนแบบครบวงจร สำหรับ equity research, portfolio, derivatives, fixed income, crypto, news, macro/economic data
- Tech หลัก: C++20 + Qt6 สำหรับ desktop UI และ embedded Python สำหรับ analytics/data fetchers
- แอปเวอร์ชัน 4 ถูกอธิบายว่าเป็น native desktop app ไม่ใช่ Electron/web app
- README ล่าสุดระบุ installer สำหรับ Windows, Linux, macOS Apple Silicon และระบุ latest release เป็น v4.0.2

## ฟีเจอร์ที่โปรเจกต์เคลม

- Multi-asset analytics: DCF, portfolio optimization, VaR, Sharpe, derivatives pricing
- AI agents: นักลงทุน/เทรดเดอร์/เศรษฐกิจ/ภูมิรัฐศาสตร์ และรองรับ LLM หลายค่าย เช่น OpenAI, Anthropic, Gemini, Groq, DeepSeek, OpenRouter, Ollama
- Data connectors 100+ แหล่ง เช่น Yahoo Finance, FRED, IMF, World Bank, DBnomics, Polygon, Kraken
- Real-time trading/paper trading และ broker integrations หลายเจ้า
- QuantLib suite, global intelligence, maritime/geopolitical/satellite data
- Node editor สำหรับ workflow automation และ MCP tool integration
- AI Quant Lab สำหรับ ML, factor discovery, high-frequency trading และ reinforcement learning trading

## โครงสร้างโปรเจกต์

จากเอกสาร onboarding:

- `fincept-qt/` คือแอปหลัก
- `src/app/` entry point, MainWindow, screen routing
- `src/core/` config, event bus, logging, result handling, session
- `src/ui/` reusable widgets, theme, charts, tables, navigation
- `src/network/` HTTP/WebSocket
- `src/storage/` SQLite/cache
- `src/auth/` JWT/guest mode
- `src/python/` bridge ไป Python runtime
- `src/trading/` trading engine/brokers
- `src/services/` market data/news
- `src/screens/` หน้าจอต่าง ๆ เช่น dashboard, markets, crypto trading, news, watchlist
- `scripts/` Python analytics, agents, data fetchers

## การติดตั้งและพัฒนา

ทางง่ายสุดคือโหลด installer จาก GitHub Releases

ถ้าจะ build เอง ต้องใช้เวอร์ชันค่อนข้างเฉพาะ:

- CMake 3.27.7
- Ninja 1.11.1
- Qt 6.8.3
- Python 3.11.9
- Compiler ที่รองรับ C++20 เช่น MSVC 19.38, GCC 12.3, Apple Clang 15.0

มี `setup.sh` สำหรับ Linux/macOS แต่ใน GitHub issues มีคนรายงานปัญหาเกี่ยวกับ setup/macOS launch และ crash บางส่วน จึงควรเผื่อเวลาทดลองหากจะใช้งานจริง

## License ที่ควรระวัง

Repo ระบุเป็น dual license: AGPL-3.0 + commercial license แต่เงื่อนไข commercial เขียนค่อนข้างเข้ม

- ใช้ส่วนตัว, เรียนรู้, academic research, contribution กลับ repo ได้ภายใต้ AGPL
- การใช้ในธุรกิจ/internal company/startup/hedge fund/bank/fintech/consulting/SaaS/white-label ต้องมี commercial license
- README ย้ำว่าการ fork หรือเปลี่ยน API/data source เองไม่ได้ทำให้หลุดจากข้อกำหนด commercial license

หากจะใช้ในบริษัทหรือใช้ต่อยอดเชิงพาณิชย์ ควรตรวจสอบ commercial license โดยละเอียดก่อน

## สัญญาณความพร้อมใช้งาน

- โปรเจกต์ active พอสมควร มี releases และ commits จำนวนมาก
- มี installer หลายแพลตฟอร์ม และ SourceForge mirror มีไฟล์ v4.0.2 วันที่ 2026-04-24
- แต่ยังมี bug reports สำคัญ เช่น crash บน macOS, Windows crypto section crash, เพิ่ม broker แล้ว crash
- จำนวนฟีเจอร์ที่เคลมกว้างมาก จึงควรทดสอบเฉพาะ workflow ที่จะใช้จริงก่อนเชื่อว่า production-ready

## มุมมองสรุป

ถ้าใช้เพื่อเรียนรู้ ทดลอง หรือทำ research ส่วนตัว Fincept Terminal เป็นโปรเจกต์ที่น่าสนใจ เพราะ scope ครบและ architecture ดูตั้งใจทำจริง

แต่ถ้าจะใช้ในบริษัท หรือนำไปต่อยอดเชิงพาณิชย์ ต้องระวัง license ก่อนเป็นอันดับแรก และควร proof-of-concept เรื่อง stability, data quality, broker integration และ security ก่อนนำไปผูกกับเงินจริงหรือบัญชีเทรดจริง

