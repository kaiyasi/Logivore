# 設定リファレンス（Logivore）

言語：[日本語](configuration.md) | [English](../configuration.md) | [繁體中文](../zh-tw/configuration.md) | [简体中文](../zh-cn/configuration.md)

本ドキュメントは Logivore の全設定項目を解説します。

## 目次
- 概要
- 環境変数（.env）
- JSON 設定（config.json）
- 言語設定
- 監視設定
- アラート設定
- Docker 設定
- SSL 設定
- 高度な設定（性能/安全/バックアップ）
- 設定例
- 検証と次のステップ

## 概要
設定優先順位：1) 環境変数 → 2) コマンドライン引数 → 3) config.json → 4) 既定値

## 環境変数（.env）

```bash
DISCORD_TOKEN=your_bot_token_here   # 必須
OWNER_ID=123456789012345678          # 必須
COMMAND_PREFIX=!                     # 任意
BOT_STATUS=Monitoring systems...     # 任意

DEFAULT_LANGUAGE=ja
UPDATE_INTERVAL=10
ALERT_INTERVAL=60
MAX_MONITORS=5
DEBUG_MODE=false

MONITORED_DISKS=/,/mnt/data,/home
MAX_UPTIME_DAYS=30
ENABLE_SMART_MONITORING=true
PROCESS_BLACKLIST=kthreadd,ksoftirqd
NETWORK_INTERFACE=

DOCKER_HOST=unix:///var/run/docker.sock
DOCKER_API_VERSION=auto
ENABLE_DOCKER_MONITORING=true
DOCKER_CONTAINER_FILTER=nginx,postgres,redis

NPM_CONTAINER=nginx-proxy-manager
SSL_CERT_PATH=/etc/letsencrypt/live
ENABLE_SSL_MONITORING=true
SSL_WARNING_DAYS=30

LOG_LEVEL=INFO
LOG_FILE=logs/logivore.log
LOG_MAX_SIZE=10
LOG_BACKUP_COUNT=5
LOG_COLORED=true
```

## JSON 設定（config.json）

既定構造：
```json
{ "language":"ja","update_interval":10,"alert_interval":60,
  "monitored_disks":[],"alerts":[],"alert_channel":null,
  "max_uptime_days":30,
  "auto_recovery_enabled":true,
  "monitored_services":[],"reboot_stop_services":[],
  "scheduled_reboots":[],"last_known_state":{},"last_recovery_boot":0 }
```

例：
```json
{ "language":"ja", "update_interval":10, "alert_interval":60, "alert_channel":123456789 }
{ "monitored_disks":["/","/mnt/data","/home"] }
{
  "alerts":[
    {"id":"cpu_high","name":"CPU 高負荷","type":"cpu","target":"cpu","threshold":80,"enabled":true,"channel_id":123456789},
    {"id":"disk_low","name":"ディスク残量低下","type":"disk","target":"/","threshold":85,"enabled":true}
  ]
}
```

## 言語設定
対応：en / zh-tw / zh-cn / ko / ja / de / ru
カスタム言語：`languages/en.json` を複製 → 翻訳 → `.env`/`config.json` で指定 → `config_management.py` に選択肢を追加。

## 監視設定
```json
{"monitoring":{"cpu_interval":0.1,"memory_warnings":true,"disk_smart_check":true,
  "network_speed_calc":true,
  "process_monitoring":{"enabled":true,"top_count":10,"cpu_threshold":80,"memory_threshold":80}}}
```

## Docker 設定
```json
{"docker_monitoring":{"enabled":true,"include_filters":["app-*","db-*"]}}
```

## SSL 設定
```json
{"ssl":{"enabled":true,"warning_days":30,
  "auto_renewal":{"enabled":true,"days_before":7}}}
```

## 高度な設定
性能：
```json
{"performance":{"max_concurrent_monitors":10,"cache_enabled":true,"cache_ttl":30,
  "batch_updates":true,"update_queue_size":100,"worker_threads":4}}
```
安全：
```json
{"security":{"rate_limiting":{"enabled":true,"max_requests":60,"whitelist":[123456789]},
  "command_restrictions":{"manage":["owner"],"reboot":["owner","admin"],"config":["owner"]}}}
```
バックアップ：
```json
{"backup":{"enabled":true,"interval":86400,"retention_days":30,
  "backup_path":"backups/","components":["config","alerts","logs"]}}
```

## 設定例
家庭用：
```json
{"language":"ja","update_interval":10,
 "monitored_disks":["/","/mnt/storage"],
 "alerts":[{"id":"cpu_high","name":"CPU 高負荷","type":"cpu","threshold":85},
            {"id":"disk_full","name":"ディスクほぼ満","type":"disk","target":"/","threshold":90}],
 "auto_recovery_enabled":true,
 "monitored_services":["ssh","nginx"]}
```

## 検証と次のステップ
JSON 構文チェック：
```bash
python -c "import json; json.load(open('config.json')); print('✅ JSON syntax OK')"
```
次へ：`docs/commands.md` / `deploy/docker/` / `docs/troubleshooting.md`
