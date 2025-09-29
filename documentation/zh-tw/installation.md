# 安裝指南（Logivore）

語言：繁體中文 | [English](../installation.md) | [简体中文](../zh-cn/installation.md)

本指南將帶你從零開始完成 Logivore 的安裝與部署（含 Docker 與 systemd 建議做法），並提供常見問題排解。

## 目錄

- 先決條件
- 系統需求
- 建立 Discord Bot
- 本機安裝（非容器）
- Docker 安裝（可選）
- 環境變數設定（.env）
- 首次啟動
- 作為系統服務（Linux, systemd）
- 疑難排解

## 先決條件

在開始前請確認已安裝下列工具：

- Python 3.8 以上
- Git
- pip（通常隨 Python 附帶）

可選（提升功能與可用性）：
- Docker、Docker Compose
- systemd（Linux）
- smartmontools（Linux，用於磁碟 SMART 健康檢查）

## 系統需求

最小需求：
- 記憶體：可用 512MB
- 磁碟：可用 1GB
- CPU：單核心（建議雙核心）
- 網路：穩定的網路連線

建議需求：
- 記憶體：1GB 以上
- 磁碟：2GB 以上
- CPU：雙核心或更高
- 作業系統：Linux（Ubuntu 20.04+）、Windows 10+ 或 macOS 10.15+

## 建立 Discord Bot

1) 進入 [Discord Developer Portal](https://discord.com/developers/applications)
2) 新增應用程式（New Application），命名為「Logivore」或你喜歡的名稱
3) 在 Bot 分頁新增 Bot（Add Bot）
4) 啟用 Privileged Gateway Intents：Server Members Intent、Message Content Intent
5) 重新產生 Token 並妥善保存（之後填入 `.env`）
6) 在 OAuth2 → URL Generator 勾選 `bot` 與 `applications.commands`，並選擇必要的權限（Send Messages、Embed Links、Use Slash Commands、Read Message History、View Channels）後邀請進你的伺服器

## 本機安裝（非容器）

```bash
# 取得原始碼
git clone https://github.com/kaiyasi/Logivore.git
cd Logivore

# 建議：建立虛擬環境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安裝相依
pip install -r requirements.txt

# 產生環境檔
cp .env.example .env
# 編輯 .env，填入 DISCORD_TOKEN、OWNER_ID、LOG_LEVEL 等

# 啟動
python main.py
```

## Docker 安裝（可選）

Docker 方式部署簡單，但可能影響主機層級可視性（例如 /ports、完整系統指標）與主機控制能力；若需最完整能力，建議使用 systemd 方案。

```bash
cd deploy/docker
# 建議先於專案根目錄複製 .env 並填好 Token：cp .env.example .env
docker compose up -d --build
```

預設 compose 使用 `network_mode: host` 與 `pid: host` 以提升可視性，並掛載 `/var/run/docker.sock:ro` 讓 Bot 能查詢與管理容器。

## 環境變數設定（.env）

請將 `.env.example` 複製為 `.env`，常用變數：

```bash
DISCORD_TOKEN=你的BotToken
OWNER_ID=你的Discord使用者ID
LOG_LEVEL=INFO
LOG_FILE=logs/logivore.log
```

更多可用設定請參考 `docs/configuration.md`。

## 首次啟動

啟動後觀察主控台應會看到：

```
✅ Bot is ready!
✅ Logged in as: <你的Bot>#1234
✅ Connected to X guilds
```

在 Discord 測試：

```
/help
/config show
/monitor
```

## 作為系統服務（Linux, systemd）

若要在主機層獲得最佳可視性與可靠性，建議使用 systemd 常駐 Logivore，並結合開機恢復範例：

1) 建立服務檔：

```bash
sudo nano /etc/systemd/system/logivore.service
```

2) 內容範例：

```ini
[Unit]
Description=Logivore - System Monitoring Discord Bot
After=network.target

[Service]
Type=simple
User=logivore
WorkingDirectory=/home/logivore/Logivore
ExecStart=/home/logivore/Logivore/venv/bin/python main.py
Restart=always
RestartSec=10

Environment=PYTHONPATH=/home/logivore/Logivore
Environment=DISCORD_TOKEN=your_token_here
Environment=OWNER_ID=your_user_id

[Install]
WantedBy=multi-user.target
```

3) 啟用服務：

```bash
sudo systemctl daemon-reload
sudo systemctl enable logivore
sudo systemctl start logivore
sudo systemctl status logivore
```

開機恢復與 sudoers 範例請見：
- `systemd-examples/`（`logivore-boot-recovery.service`、`logivore-bot-sudoers` 等）
- `SETUP-RECOVERY.md`

## 疑難排解

常見狀況：

- 找不到 discord.py：`pip install -r requirements.txt`
- Token 錯誤：重新確認 `.env` 的 `DISCORD_TOKEN` 是否正確
- Bot 不回應：檢查是否上線、權限是否足夠、重新邀請權限
- 權限問題（Linux）：

```bash
chmod +x main.py
chmod 644 .env
sudo chown -R $USER:$USER .
```

- Docker 容器立刻退出：
  1) 檢視容器日誌 `docker compose logs -f logivore`
  2) 檢查環境變數是否填寫正確

啟用除錯：將 `.env` 設 `LOG_LEVEL=DEBUG`，或以 `python main.py 2>&1 | tee logs/startup.log` 啟動。
