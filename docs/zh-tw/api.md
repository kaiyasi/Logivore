# API 文件（Logivore）

語言：繁體中文 | [English](../api.md) | [简体中文](../zh-cn/api.md)

本文件說明 Logivore 的核心模組、初始化流程、指令註冊、i18n、日誌、Docker 與 SSL 整合，以及錯誤處理模式。

## 架構概覽
```
Logivore/
├─ main.py                # 啟動與初始化
├─ utils/                 # 日誌、i18n、Embed、指令工具
├─ cogs/                  # 功能模組（系統監控/警報/Docker/設定/管理/重啟/恢復/SSL）
└─ languages/             # 多語字串
```

## 啟動與初始化
入口 `python main.py`：
1) 載入 .env → 2) 初始化日誌 → 3) 列印系統資訊 → 4) 建立 `Logivore()` → 5) 載入 Cogs 與同步 Slash 指令

## 設定管理（ConfigManager）
- 檔案 `config.json`；缺失/毀損時回寫預設
- 以 `.get/.set` 在執行期讀寫供 Cogs 使用

## 模組（Cogs）
- `setup(bot)` 註冊；`cog_unload()` 清理
- 可用 `tasks.loop` 建立背景任務

## i18n（國際化）
- `utils/i18n.py` + `languages/*.json`
- `i18n.t(key, lang)` 或設定 `i18n.default_language`

## 指令系統（Slash）
- `discord.app_commands` 宣告；於 `setup_hook()` 全域同步 `tree.sync()`
- 描述與輸出支援多語

## 動態/本地化指令工具
- `utils/localized_commands.py`、`utils/command_registry.py` 提供依語言動態產生描述與群組的能力

## 日誌（utils/logging_config.py）
- `setup_bot_logging("logs/logivore.log")`：彩色主控台 + 檔案輸出
- 名稱空間：`logivore`、`logivore.cogs`、`logivore.discord` 等

## 系統監控
- `/monitor`：嵌入式面板（CPU/記憶體/磁碟/網路）
- `/ports`：主機端口（合併 v4/v6），按鈕分頁；超長改附件
- `/top`、`/smart`：進程/磁碟健康

## 警報
- `alerts[]`（`config.json`）或指令維護；支援 CPU/記憶體/磁碟/進程，並可指定頻道

## Docker 整合
- `/docker status|logs|start|stop|restart|stats`
- 建議 Compose 啟用 `network_mode: host`、`pid: host`，唯讀掛載 `/var/run/docker.sock`

## SSL/NPM 整合
- `/ssl list|check|renew|auto-renew`；透過 `docker exec` + openssl 解析憑證

## 錯誤處理
- Slash 同步/API 呼叫失敗：記錄並降級
- 400 長度限制：分頁或附件回退
- Owner/權限不足：清楚回應所需權限

