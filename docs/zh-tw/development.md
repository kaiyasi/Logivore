# 開發指南（Logivore）

語言：繁體中文 | [English](../development.md) | [简体中文](../zh-cn/development.md)

本指南協助開發者快速理解專案結構、設置開發環境、遵守程式風格、撰寫/測試 Cogs、維護 i18n 與日誌、提交 PR 與發版流程。

## 目錄
- 專案結構
- 開發環境設置
- 執行與除錯
- 程式風格與規範
- Cogs 開發實務
- 指令與互動（Slash/Buttons）
- i18n 與字串管理
- 日誌與診斷
- 測試與驗證
- Docker 開發流程
- 版本控管與提交規範
- 發版與變更日誌

---

## 專案結構
```
Logivore/
├─ main.py                    # 啟動/初始化/載入 Cogs/同步指令
├─ cogs/                      # 主要功能模組
├─ utils/                     # 工具模組（i18n/Embed/日誌/指令工具）
├─ languages/                 # 多語 JSON
├─ deploy/                    # 部署（systemd/docker）
└─ docs/                      # 文件
```

---

## 開發環境設置
```bash
git clone https://github.com/kaiyasi/Logivore.git
cd Logivore
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # 設定 DISCORD_TOKEN/OWNER_ID
python main.py
```

---

## 執行與除錯
- `.env` 設 `LOG_LEVEL=DEBUG` 觀察詳細輸出
- `python main.py 2>&1 | tee logs/startup.log` 保存啟動日誌
- 指令同步需數十秒；未出現可重啟再試

---

## 程式風格與規範
- Python 3.8+；型別註記以 3.8 相容
- 命名：snake_case（函式/變數）、PascalCase（類別）
- 例外處理：記錄→友善訊息→不中斷主流程
- 嵌入輸出遵守 1024 限制（分頁或附件）

---

## Cogs 開發實務
- `cogs/my_feature.py`；於 `async def setup(bot)` 註冊
- 背景任務用 `tasks.loop`；於 `cog_unload()` 取消
- Slash 指令使用 `discord.app_commands`

---

## 指令與互動
- 指令於 `setup_hook()` 載入後由 `tree.sync()` 同步
- 大量輸出使用按鈕分頁與附件回退
- 提供用法/權限提示的錯誤處理

---

## i18n 與字串管理
- 新增語言：複製 `languages/en.json` → 翻譯→ `.env DEFAULT_LANGUAGE`
- 使用 `i18n.t(key, lang)`，避免移除既有鍵

---

## 日誌與診斷
- `utils/logging_config.py`：彩色主控台 + 檔案
- 命名空間：`logivore.*`（如 `logivore.cogs`）

---

## 測試與驗證
- 建議以 pytest 撰寫對 utils/邏輯的測試
- 手動驗證：/monitor、/ports、/docker status、/ssl list

---

## Docker 開發流程
- 使用 `deploy/docker/docker-compose.yml`
- 預設開啟 host/pid 模式與唯讀 docker.sock

---

## 版本控管與提交規範
- Commit：`feat/fix/docs/refactor`
- PR：描述動機/範圍/測試/相容性
- 變更日誌：摘要功能與修正

---

## 發版與變更日誌
- 標籤：`vX.Y.Z`
- 發版說明：新增/修正/破壞相容性/升級注意事項

