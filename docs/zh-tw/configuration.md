# 設定參考（Logivore）

語言：繁體中文 | [English](../configuration.md) | [简体中文](../zh-cn/configuration.md)

本文件完整說明 Logivore 的所有設定選項，協助你依照需求調整機器人行為。

## 目錄

- 設定總覽
- 環境變數（.env）
- JSON 設定（config.json）
- 語言設定
- 監控設定
- 警報設定
- Docker 設定
- SSL 設定
- 進階設定
- 設定範例
- 設定驗證與下一步

## 設定總覽

Logivore 使用多層次的設定架構，優先序如下（上者覆蓋下者）：
1) 環境變數（`.env`） → 2) 指令列引數 → 3) `config.json` → 4) 預設值

## 環境變數（.env）

### Discord 核心設定
```bash
DISCORD_TOKEN=your_bot_token_here    # 必填：Bot Token
OWNER_ID=123456789012345678          # 必填：你的 Discord 使用者 ID
COMMAND_PREFIX=!                     # 選填：文字指令前綴
BOT_STATUS=Monitoring systems...     # 選填：狀態訊息
```

### 機器人行為
```bash
DEFAULT_LANGUAGE=zh-tw    # en, zh, zh-cn, zh-tw, ko, ja, de, ru
UPDATE_INTERVAL=10        # 監控面板更新間隔（秒）
ALERT_INTERVAL=60         # 警報檢查間隔（秒）
MAX_MONITORS=5            # 監控面板同時上限
DEBUG_MODE=false          # 除錯模式
```

### 系統監控
```bash
MONITORED_DISKS=/,/mnt/data,/home   # 監控的磁碟掛載點（逗號分隔）
MAX_UPTIME_DAYS=30                  # 系統連續運作天數警示
ENABLE_SMART_MONITORING=true        # SMART 健康檢查
PROCESS_BLACKLIST=kthreadd,ksoftirqd
NETWORK_INTERFACE=                  # 指定網卡（留空自動）
```

### Docker 整合
```bash
DOCKER_HOST=unix:///var/run/docker.sock
DOCKER_API_VERSION=auto
ENABLE_DOCKER_MONITORING=true
DOCKER_CONTAINER_FILTER=nginx,postgres,redis
```

### SSL 憑證管理
```bash
NPM_CONTAINER=nginx-proxy-manager
SSL_CERT_PATH=/etc/letsencrypt/live
ENABLE_SSL_MONITORING=true
SSL_WARNING_DAYS=30
```

### 日誌
```bash
LOG_LEVEL=INFO                 # DEBUG/INFO/WARNING/ERROR/CRITICAL
LOG_FILE=logs/logivore.log
LOG_MAX_SIZE=10
LOG_BACKUP_COUNT=5
LOG_COLORED=true
```

## JSON 設定（config.json）

預設結構：
```json
{
  "language": "en",
  "update_interval": 10,
  "alert_interval": 60,
  "monitored_disks": [],
  "alerts": [],
  "alert_channel": null,
  "max_uptime_days": 30,
  "auto_recovery_enabled": true,
  "monitored_services": [],
  "reboot_stop_services": [],
  "scheduled_reboots": [],
  "last_known_state": {},
  "last_recovery_boot": 0
}
```

常用設定片段：

```json
{ "language": "zh-tw", "update_interval": 10, "alert_interval": 60, "alert_channel": 123456789 }
```

```json
{ "monitored_disks": ["/", "/mnt/data", "/home"] }
```

```json
{
  "alerts": [
    {"id": "cpu_high_usage", "name": "CPU 使用率過高", "type": "cpu", "target": "cpu", "threshold": 80, "enabled": true, "channel_id": 123456789},
    {"id": "disk_space_low", "name": "磁碟空間不足", "type": "disk", "target": "/", "threshold": 85, "enabled": true, "channel_id": null},
    {"id": "nginx_down", "name": "Nginx 行程中斷", "type": "process", "target": "nginx", "enabled": true, "channel_id": 123456789}
  ]
}
```

```json
{
  "auto_recovery_enabled": true,
  "monitored_services": ["nginx", "postgresql", "redis-server"],
  "last_known_state": {
    "timestamp": 1635789123,
    "docker_containers": [{"name": "nginx", "image": "nginx:latest"}],
    "systemd_services": ["nginx", "postgresql"]
  }
}
```

```json
{
  "max_uptime_days": 30,
  "reboot_stop_services": ["nginx", "postgresql"],
  "scheduled_reboots": [{"time": "2024-01-01T02:00:00", "delay": 5, "enabled": true, "scheduled_by": 123456789}]
}
```

## 語言設定

支援語言：en / zh(zh-tw) / zh-cn / ko / ja / de / ru

新增語言步驟：複製 `languages/en.json` → 翻譯 → 在 `.env`/`config.json` 指定 → 在 `config_management.py` 增加選項。

## 監控設定

```json
{
  "monitoring": {
    "cpu_interval": 0.1,
    "memory_warnings": true,
    "disk_smart_check": true,
    "network_speed_calc": true,
    "process_monitoring": {"enabled": true, "top_count": 10, "cpu_threshold": 80, "memory_threshold": 80}
  }
}
```

自訂面板：
```json
{ "custom_panels": { "server_room": { "title": "Server Room Monitor", "disks": ["/", "/mnt/storage"], "services": ["nginx", "postgresql"], "update_interval": 5, "alert_thresholds": {"cpu": 70, "memory": 85, "disk": 90} } } }
```

## Docker 設定

```json
{ "docker_monitoring": { "enabled": true, "include_filters": ["app-*", "db-*"] } }
```

## SSL 設定

```json
{ "ssl": { "enabled": true, "warning_days": 30, "auto_renewal": { "enabled": true, "days_before": 7 } } }
```

## 進階設定

效能：
```json
{ "performance": { "max_concurrent_monitors": 10, "cache_enabled": true, "cache_ttl": 30, "batch_updates": true, "update_queue_size": 100, "worker_threads": 4 } }
```

安全：
```json
{ "security": { "rate_limiting": { "enabled": true, "max_requests": 60, "whitelist": [123456789] }, "command_restrictions": { "manage": ["owner"], "reboot": ["owner", "admin"], "config": ["owner"] } } }
```

備份/還原：
```json
{ "backup": { "enabled": true, "interval": 86400, "retention_days": 30, "backup_path": "backups/", "components": ["config", "alerts", "logs"] } }
```

## 設定範例

家用伺服器：
```json
{ "language": "zh-tw", "update_interval": 10, "monitored_disks": ["/", "/mnt/storage"], "alerts": [ { "id": "cpu_high", "name": "CPU 過高", "type": "cpu", "target": "cpu", "threshold": 85, "enabled": true }, { "id": "disk_full", "name": "磁碟將滿", "type": "disk", "target": "/", "threshold": 90, "enabled": true } ], "auto_recovery_enabled": true, "monitored_services": ["ssh", "nginx"] }
```

企業生產：
```json
{ "language": "zh-tw", "update_interval": 5, "alert_interval": 30, "monitored_disks": ["/", "/var/log", "/mnt/data", "/backup"], "alerts": [ { "id": "cpu_critical", "name": "CPU 臨界", "type": "cpu", "threshold": 90, "channel_id": 123456789 }, { "id": "memory_high", "name": "記憶體過高", "type": "memory", "threshold": 85, "channel_id": 123456789 }, { "id": "nginx_down", "name": "Nginx 中斷", "type": "process", "target": "nginx", "channel_id": 987654321 } ], "docker_monitoring": { "enabled": true, "include_filters": ["app-*", "db-*"] }, "ssl": { "enabled": true, "warning_days": 14, "auto_renewal": { "enabled": true, "days_before": 7 } } }
```

開發環境：
```json
{ "language": "zh-tw", "update_interval": 30, "alert_interval": 300, "monitored_disks": ["/"], "alerts": [ { "id": "disk_space", "name": "開發磁碟空間", "type": "disk", "target": "/", "threshold": 95, "enabled": true } ], "docker_monitoring": { "enabled": true, "include_filters": ["dev-*", "test-*"] }, "auto_recovery_enabled": false }
```

## 設定驗證與下一步

JSON 語法快速檢查：
```python
python -c "import json; json.load(open('config.json')); print('✅ JSON syntax OK')"
```

常見錯誤：JSON 語法、缺少欄位、門檻值(0-100)、頻道 ID 類型、磁碟路徑不存在。

下一步：
- 📚 指令參考：`docs/commands.md`
- 🚨 警報設定：`docs/commands.md#alerts`
- 🐳 Docker 整合：`deploy/docker/`
- 🔍 疑難排解：`docs/troubleshooting.md`
