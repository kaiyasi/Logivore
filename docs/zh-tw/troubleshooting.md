# 疑難排解（Logivore）

語言：繁體中文 | [English](../troubleshooting.md) | [简体中文](../zh-cn/troubleshooting.md)

本指南彙整常見問題、診斷流程與修復步驟，協助你快速定位並解決 Logivore 在不同環境（原生 systemd、Docker）運行時的各式狀況。

## 目錄

- 快速檢查清單
- 取得診斷資訊（Logs / 狀態）
- 常見啟動問題
- 指令與權限問題
- Docker 相關問題
- systemd 服務問題
- SSL / 憑證問題
- 警報（Alerts）相關
- 效能與資源使用
- 錯誤碼與常見訊息
- 復原與回滾
- 常見問答（FAQ）

---

## 快速檢查清單

1) `.env` 是否正確：`DISCORD_TOKEN`、`OWNER_ID` 已填且無多餘空白/引號。
2) 版本與相依：`python --version`（3.8+）與 `pip install -r requirements.txt` 成功。
3) 網路與權限：機器可連 Discord API，Bot 已加入伺服器且具備最小權限（Send Messages / Embed Links / Use Slash Commands）。
4) 檔案與路徑：`logs/`、`config/` 可讀寫；如果使用 Docker，對應卷（volumes）已掛載。
5) 語言與設定：`config.json` JSON 語法正確，`DEFAULT_LANGUAGE` 存在於 `languages/`。

---

## 取得診斷資訊（Logs / 狀態）

### 讀取應用日誌
```bash
tail -f logs/logivore.log
```

### 啟動並保留啟動日誌
```bash
python main.py 2>&1 | tee logs/startup.log
```

### Docker 日誌
```bash
cd deploy/docker
docker compose logs -f logivore
```

### 檢查斜線指令同步
- 啟動後首次同步可能需要數十秒；若遲遲未出現指令，可重啟一次或執行管理指令同步（若有提供）。

---

## 常見啟動問題

### Token 無效或未設定
- 現象：啟動時顯示 LoginFailure 或「DISCORD_TOKEN is not set」。
- 檢查：`.env` 的 `DISCORD_TOKEN` 是否正確，是否有多餘空白或引號。
- 修正：在 Discord Developer Portal 重置 Token，更新 `.env` 後重啟。

### 相依套件缺失
- 現象：ImportError / ModuleNotFoundError。
- 修正：`pip install -r requirements.txt`，確保在虛擬環境內（venv）執行。

### Python/系統版本不符
- 現象：語法錯誤、型別註記錯誤或系統 API 缺少。
- 修正：升級到 Python 3.8+；在容器內使用提供的 Dockerfile（deploy/docker）。

### 指令（Slash Commands）未出現
- 現象：/help /monitor 等看不到。
- 檢查：等待同步、重新啟動、確認 Bot 是否加入伺服器、權限是否勾選 `applications.commands`。

---

## 指令與權限問題

### Bot 無權限發送/嵌入
- 現象：沒有輸出、嵌入被過濾。
- 修正：確認頻道/伺服器權限：Send Messages、Embed Links、Read Message History。

### Owner 限制的指令
- 現象：管理類指令（/restart /shutdown /config set 等）提示無權限。
- 檢查：`.env` 的 `OWNER_ID` 是否為你的 Discord 使用者 ID；右鍵名稱 → Copy ID。

### 長度限制造成 400 Bad Request
- 現象：Invalid Form Body，embeds.*.value 長度 > 1024。
- 修正：我們已在輸出處理加上分頁與附件退回；若仍觸發，請回報使用情境與當前列表長度。

---

## Docker 相關問題

### 容器立即退出
- 讀取日誌：`docker compose logs -f logivore`
- 檢查：環境變數（DISCORD_TOKEN / OWNER_ID）、卷掛載（config/logs）、Docker Socket 是否以唯讀掛載（若需 Docker 管理功能）。

### 監控資料不足（看不到主機層）
- 原因：未使用 `network_mode: host` / `pid: host`。
- 修正：使用 deploy/docker/docker-compose.yml 的預設設定，或按需求開啟 host/pid 模式。

### `/ports` 列表與 Docker 映射不一致
- 現象：同一埠顯示 IPv4/IPv6 重複。
- 修正：已合併顯示（IP 欄位為 v4/v6/*）。若仍有差異，請提供 docker ps 的 Ports 欄與系統 netstat/ss 參考。

---

## systemd 服務問題（Linux）

### 服務無法啟動
```bash
sudo systemctl status logivore
sudo journalctl -u logivore -f
```
- 檢查服務檔 `ExecStart`、`WorkingDirectory`、`User` 是否正確；虛擬環境路徑是否存在。

### 開機自動恢復
- 參考 `systemd-examples/`（`logivore-boot-recovery.service`）與 `SETUP-RECOVERY.md`，確認腳本路徑 `/opt/logivore/scripts/boot-recovery.sh` 存在且可執行。

---

## SSL / 憑證問題

### 列表或續期失敗
- 檢查：NPM 容器名稱（`NPM_CONTAINER`）、憑證路徑（`SSL_CERT_PATH`）、OpenSSL 是否可用。
- 權限：Docker exec 操作需要容器存在且允許執行 openssl。
- 網域：DNS A/AAAA 設定正確；Let’s Encrypt 速率限制未觸發。

---

## 警報（Alerts）相關

### 警報未觸發 / 頻率過高
- 檢查：`alerts` 門檻值（0–100）、`alert_interval`、`alert_channel` 是否設定。
- 資源型警報建議：CPU 80–90%、記憶體 80–90%、磁碟 85–95%。

---

## 效能與資源使用

### Bot 佔用過高
- 降低更新頻率：`UPDATE_INTERVAL`、`ALERT_INTERVAL`
- 關閉不必要功能：停用 Docker 監控或縮小監控面板數量
- 檢查第三方模組與系統負載（top/htop）

---

## 錯誤碼與常見訊息

- 50035 Invalid Form Body：多半是欄位長度超限（已加保護機制）。
- LoginFailure：Token 無效。
- Missing Permissions：頻道/伺服器權限不足。
- JSONDecodeError：config.json 格式錯誤。

---

## 復原與回滾

1) 備份設定與日誌：`cp -r config logs backups/$(date +%F_%T)`
2) 還原舊版設定：將備份檔覆蓋回 `config/` 與 `logs/`（僅在需要時）
3) 重新啟動服務或容器

---

## 常見問答（FAQ）

Q: 指令沒有顯示？
- A: 初次同步需要時間；確認 Bot 加入伺服器、權限完整，重啟後再試。

Q: `/ports` 太長導致錯誤？
- A: 目前已支援分頁與附件退回；若仍出現錯誤，請截圖與貼上輸出供我們調整分頁大小。

Q: Docker 內是否安全？
- A: 預設 read_only/ no-new-privileges/ tmpfs /var/run/docker.sock:ro；請視環境安全政策調整。

---

需要更多協助？
- 追蹤日誌：`tail -f logs/logivore.log`
- Docker：`docker compose logs -f logivore`
- 提交 Issue：<https://github.com/kaiyasi/Logivore/issues>
