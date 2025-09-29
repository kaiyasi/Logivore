# 설정 참고서 (Logivore)

언어: [한국어](configuration.md) | [English](../configuration.md) | [繁體中文](../zh-tw/configuration.md) | [简体中文](../zh-cn/configuration.md)

이 문서는 Logivore의 모든 설정을 설명합니다.

## 목차
- 개요
- 환경 변수(.env)
- JSON 설정(config.json)
- 언어 설정
- 모니터링 설정
- 알림 설정
- Docker 설정
- SSL 설정
- 고급 설정(성능/보안/백업)
- 설정 예시
- 검증 및 다음 단계

## 개요
우선순위: 1) .env → 2) CLI 인자 → 3) config.json → 4) 기본값

## 환경 변수(.env)
```bash
DISCORD_TOKEN=your_bot_token_here   # 필수
OWNER_ID=123456789012345678          # 필수
COMMAND_PREFIX=!
BOT_STATUS=Monitoring systems...

DEFAULT_LANGUAGE=ko
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

## JSON 설정(config.json)
```json
{ "language":"ko","update_interval":10,"alert_interval":60,
  "monitored_disks":[],"alerts":[],"alert_channel":null,
  "max_uptime_days":30,
  "auto_recovery_enabled":true,
  "monitored_services":[],"reboot_stop_services":[],
  "scheduled_reboots":[],"last_known_state":{},"last_recovery_boot":0 }
```
예시:
```json
{ "language":"ko","update_interval":10,"alert_interval":60,"alert_channel":123456789 }
{ "monitored_disks":["/","/mnt/data","/home"] }
{
  "alerts":[
    {"id":"cpu_high","name":"CPU 과다 사용","type":"cpu","target":"cpu","threshold":80,"enabled":true,"channel_id":123456789},
    {"id":"disk_low","name":"디스크 공간 부족","type":"disk","target":"/","threshold":85,"enabled":true}
  ]
}
```

## 언어 설정
지원: en/zh-tw/zh-cn/ko/ja/de/ru
커스텀: `languages/en.json` 복제 → 번역 → `.env`/`config.json` 지정 → `config_management.py` 추가

## 모니터링 설정
```json
{"monitoring":{"cpu_interval":0.1,"memory_warnings":true,"disk_smart_check":true,
  "network_speed_calc":true,
  "process_monitoring":{"enabled":true,"top_count":10,"cpu_threshold":80,"memory_threshold":80}}}
```

## Docker 설정
```json
{"docker_monitoring":{"enabled":true,"include_filters":["app-*","db-*"]}}
```

## SSL 설정
```json
{"ssl":{"enabled":true,"warning_days":30,
  "auto_renewal":{"enabled":true,"days_before":7}}}
```

## 고급 설정
성능:
```json
{"performance":{"max_concurrent_monitors":10,"cache_enabled":true,"cache_ttl":30,
  "batch_updates":true,"update_queue_size":100,"worker_threads":4}}
```
보안:
```json
{"security":{"rate_limiting":{"enabled":true,"max_requests":60,"whitelist":[123456789]},
  "command_restrictions":{"manage":["owner"],"reboot":["owner","admin"],"config":["owner"]}}}
```
백업:
```json
{"backup":{"enabled":true,"interval":86400,"retention_days":30,
  "backup_path":"backups/","components":["config","alerts","logs"]}}
```

## 설정 예시
가정용:
```json
{"language":"ko","update_interval":10,
 "monitored_disks":["/","/mnt/storage"],
 "alerts":[{"id":"cpu_high","name":"CPU 과다","type":"cpu","threshold":85},
            {"id":"disk_full","name":"디스크 거의 가득참","type":"disk","target":"/","threshold":90}],
 "auto_recovery_enabled":true,
 "monitored_services":["ssh","nginx"]}
```

## 검증 및 다음 단계
```bash
python -c "import json; json.load(open('config.json')); print('✅ JSON syntax OK')"
```
다음: `docs/commands.md` / `deploy/docker/` / `docs/troubleshooting.md`
