# Konfigurationsreferenz (Logivore)

Sprachen: [Deutsch](configuration.md) | [English](../configuration.md) | [繁體中文](../zh-tw/configuration.md) | [简体中文](../zh-cn/configuration.md) | [日本語](../ja/configuration.md) | [한국어](../ko/configuration.md)

Diese Referenz beschreibt alle Konfigurationsoptionen von Logivore.

## Inhalte
- Überblick & Priorität
- Umgebungsvariablen (.env)
- JSON‑Konfiguration (config.json)
- Spracheinstellungen
- Monitoring‑Optionen
- Alert‑Einstellungen
- Docker‑Einstellungen
- SSL‑Einstellungen
- Erweiterte Einstellungen (Performance/Security/Backup)
- Beispiele
- Validierung & Nächste Schritte

## Überblick & Priorität
1) .env → 2) CLI‑Argumente → 3) config.json → 4) Defaults

## Umgebungsvariablen (.env)
```bash
DISCORD_TOKEN=your_bot_token_here   # erforderlich
OWNER_ID=123456789012345678          # erforderlich
COMMAND_PREFIX=!
BOT_STATUS=Monitoring systems...

DEFAULT_LANGUAGE=de
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

## JSON‑Konfiguration (config.json)
```json
{ "language":"de","update_interval":10,"alert_interval":60,
  "monitored_disks":[],"alerts":[],"alert_channel":null,
  "max_uptime_days":30,
  "auto_recovery_enabled":true,
  "monitored_services":[],"reboot_stop_services":[],
  "scheduled_reboots":[],"last_known_state":{},"last_recovery_boot":0 }
```
Beispiele:
```json
{ "language":"de","update_interval":10,"alert_interval":60,"alert_channel":123456789 }
{ "monitored_disks":["/","/mnt/data","/home"] }
{
  "alerts":[
    {"id":"cpu_high","name":"Hohe CPU‑Auslastung","type":"cpu","target":"cpu","threshold":80,"enabled":true,"channel_id":123456789},
    {"id":"disk_low","name":"Wenig Speicherplatz","type":"disk","target":"/","threshold":85,"enabled":true}
  ]
}
```

## Spracheinstellungen
Unterstützt: en / zh‑tw / zh‑cn / ko / ja / de / ru
Eigene Sprache: `languages/en.json` kopieren → übersetzen → in `.env`/`config.json` setzen → Option in `config_management.py` ergänzen.

## Monitoring‑Optionen
```json
{"monitoring":{"cpu_interval":0.1,"memory_warnings":true,"disk_smart_check":true,
  "network_speed_calc":true,
  "process_monitoring":{"enabled":true,"top_count":10,"cpu_threshold":80,"memory_threshold":80}}}
```

## Docker‑Einstellungen
```json
{"docker_monitoring":{"enabled":true,"include_filters":["app-*","db-*"]}}
```

## SSL‑Einstellungen
```json
{"ssl":{"enabled":true,"warning_days":30,
  "auto_renewal":{"enabled":true,"days_before":7}}}
```

## Erweiterte Einstellungen
Performance:
```json
{"performance":{"max_concurrent_monitors":10,"cache_enabled":true,"cache_ttl":30,
  "batch_updates":true,"update_queue_size":100,"worker_threads":4}}
```
Security:
```json
{"security":{"rate_limiting":{"enabled":true,"max_requests":60,"whitelist":[123456789]},
  "command_restrictions":{"manage":["owner"],"reboot":["owner","admin"],"config":["owner"]}}}
```
Backup:
```json
{"backup":{"enabled":true,"interval":86400,"retention_days":30,
  "backup_path":"backups/","components":["config","alerts","logs"]}}
```

## Beispiele
Heimserver:
```json
{"language":"de","update_interval":10,
 "monitored_disks":["/","/mnt/storage"],
 "alerts":[{"id":"cpu_high","name":"Hohe CPU","type":"cpu","threshold":85},
            {"id":"disk_full","name":"Fast volle Platte","type":"disk","target":"/","threshold":90}],
 "auto_recovery_enabled":true,
 "monitored_services":["ssh","nginx"]}
```

## Validierung & Nächste Schritte
```bash
python -c "import json; json.load(open('config.json')); print('✅ JSON syntax OK')"
```
Weiter: `docs/commands.md` / `deploy/docker/` / `docs/troubleshooting.md`
