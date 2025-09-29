# 指令參考（Logivore）

語言：繁體中文 | [English](../commands.md) | [简体中文](../zh-cn/commands.md)

本指南完整列出 Logivore 的所有斜線指令、用途、參數與範例。

## 目錄
- 系統監控指令
- Docker 管理指令
- 警報管理指令
- SSL 憑證指令
- 設定指令
- 機器人管理指令
- 說明指令
- 指令分類與權限
- 使用建議與錯誤處理

---

## 系統監控指令

### /monitor
顯示即時系統監控面板（CPU、記憶體、磁碟、網路），每 10 秒自動更新。
- 用法：`/monitor`
- 參數：無

### /ports
顯示主機端口佔用概況（Docker 對映 + 系統監聽），支援分頁與附件回退。
- 用法：`/ports`
- 參數：無（結果分頁呈現，完整清單過長時會附加檔案）

### /top
列出高資源使用的進程（CPU/記憶體）。
- 用法：`/top [count]`
- 參數：`count`（選填，預設 10，1–20）

### /smart
顯示磁碟 SMART 健康資訊（Linux，需 smartmontools）。
- 用法：`/smart`

---

## Docker 管理指令

### /docker status（或 /docker ps）
顯示所有容器狀態、映像、端口對映、資源使用等。
- 用法：`/docker status`

### /docker start
啟動指定容器。
- 用法：`/docker start <container_name>`
- 參數：`container_name`（必填）

### /docker stop
停止指定容器。
- 用法：`/docker stop <container_name>`
- 參數：`container_name`（必填）

### /docker restart
重啟指定容器。
- 用法：`/docker restart <container_name>`

### /docker logs
查看指定容器日誌（可指定返回行數）。
- 用法：`/docker logs <container_name> [lines]`
- 參數：`lines`（選填，預設 50）

### /docker stats
顯示容器即時資源使用統計。
- 用法：`/docker stats [container_name]`

---

## 警報管理指令（alerts）

### /alerts list
列出已設定的警報及狀態。
- 用法：`/alerts list`

### /alerts add
新增系統警報（CPU/記憶體/磁碟/進程）。
- 用法：`/alerts add <type> <threshold> [channel]`
- 參數：
  - `type`：cpu、memory、disk、process
  - `threshold`：門檻值（% 或類型所需值）
  - `channel`：通知頻道（選填）
- 範例：
  - `/alerts add cpu 90`
  - `/alerts add memory 85 #alerts`
  - `/alerts add disk 95`

### /alerts remove
移除既有警報。
- 用法：`/alerts remove <alert_id>`

### /alerts test
測試警報通知（可指定類型）。
- 用法：`/alerts test [type]`

---

## SSL 憑證指令（ssl）

### /ssl list
列出憑證清單、到期日、狀態等。
- 用法：`/ssl list`

### /ssl check
查詢特定網域憑證狀態。
- 用法：`/ssl check <domain>`

### /ssl renew
為指定網域續期憑證（需整合 NPM 與正確 DNS）。
- 用法：`/ssl renew <domain>`

### /ssl auto-renew
設定自動續期。
- 用法：`/ssl auto-renew <enable|disable> [days_before]`
- 範例：`/ssl auto-renew enable 15`

---

## 設定指令（config）

### /config show
顯示目前設定（可指定區段：system、alerts、docker、ssl）。
- 用法：`/config show [section]`

### /config set
更新設定鍵值。
- 用法：`/config set <key> <value>`
- 範例：`/config set update_interval 15`

### /config reload
重新載入設定檔。
- 用法：`/config reload`

### /language（或 /config language）
變更顯示語言或查看可用語言。
- 用法：`/language [language_code]`
- 支援：`en`、`zh`/`zh-tw`、`zh-cn`、`ko`、`ja`、`de`、`ru`

---

## 機器人管理指令（管理權限）

### /restart
重啟機器人（僅 Owner）。

### /shutdown
優雅關閉機器人（僅 Owner）。

### /reload
重載指定模組（cog）。
- 用法：`/reload <cog_name>`

### /sync
同步斜線指令至 Discord。

### /status
顯示機器人狀態與統計（上線時間、伺服器數、資源使用等）。

---

## 說明指令

### /help
顯示說明與分類；可指定分類顯示詳細指令。
- 用法：`/help [category]`
- 分類：`monitoring`、`docker`、`alerts`、`ssl`、`config`、`admin`

---

## 指令分類與權限

### 公開指令
`/monitor`、`/ports`、`/top`、`/smart`、`/docker status|logs|stats`、`/ssl list|check`、`/config show`、`/language`、`/status`、`/help`

### Owner 指令
`/docker start|stop|restart`、`/alerts add|remove`、`/ssl renew|auto-renew`、`/config set|reload`、`/restart|/shutdown|/reload|/sync`

### 伺服器權限需求（Discord）
- 發送訊息：所有指令
- 嵌入連結：輸出 embed 的指令
- 使用斜線指令：所有斜線指令
- 管理訊息：需要編輯/刪除訊息的功能

---

## 使用建議
- 以 `/monitor` 快速總覽系統；搭配 `/alerts add` 建立主動警示
- Docker 管理前先看 `/docker status`，排錯用 `/docker logs`、資源用 `/docker stats`
- 憑證建議啟用 `/ssl auto-renew enable` 並定期 `/ssl list`
- 設定異動後可 `/config reload`，語言以 `/language` 切換

## 錯誤處理
- 權限錯誤：回應所需權限
- 參數錯誤：提供正確用法提示
- 系統錯誤：友善訊息與保護性降級
- 網路錯誤：逾時處理與重試策略
