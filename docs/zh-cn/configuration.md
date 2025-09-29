# 配置参考（Logivore）

语言：[简体中文](configuration.md) | [English](../configuration.md) | [繁體中文](../zh-tw/configuration.md)

本文档完整说明 Logivore 的全部配置选项，帮助你按需调整机器人行为。

## 目录

- 配置总览
- 环境变量（.env）
- JSON 配置（config.json）
- 语言设置
- 监控设置
- 警报设置
- Docker 设置
- SSL 设置
- 高级设置
- 配置示例
- 配置校验与下一步

## 配置总览

Logivore 采用多层配置，优先顺序如下（上者覆盖下者）：
1) 环境变量（`.env`） → 2) 命令行参数 → 3) `config.json` → 4) 默认值

## 环境变量（.env）

### Discord 核心配置
```bash
DISCORD_TOKEN=your_bot_token_here    # 必填：Bot Token
OWNER_ID=123456789012345678          # 必填：你的 Discord 用户 ID
COMMAND_PREFIX=!                     # 可选：文本命令前缀
BOT_STATUS=Monitoring systems...     # 可选：状态消息
```

### 机器人行为
```bash
DEFAULT_LANGUAGE=zh-cn    # en, zh, zh-cn, zh-tw, ko, ja, de, ru
UPDATE_INTERVAL=10        # 监控面板更新间隔（秒）
ALERT_INTERVAL=60         # 警报检查间隔（秒）
MAX_MONITORS=5            # 监控面板并发上限
DEBUG_MODE=false          # 调试模式
```

### 系统监控
```bash
MONITORED_DISKS=/,/mnt/data,/home   # 监控的磁盘挂载点（逗号分隔）
MAX_UPTIME_DAYS=30                  # 系统连续运行天数警示
ENABLE_SMART_MONITORING=true        # SMART 健康检查
PROCESS_BLACKLIST=kthreadd,ksoftirqd
NETWORK_INTERFACE=                  # 指定网卡（留空自动）
```

### Docker 集成
```bash
DOCKER_HOST=unix:///var/run/docker.sock
DOCKER_API_VERSION=auto
ENABLE_DOCKER_MONITORING=true
DOCKER_CONTAINER_FILTER=nginx,postgres,redis
```

### SSL 证书管理
```bash
NPM_CONTAINER=nginx-proxy-manager
SSL_CERT_PATH=/etc/letsencrypt/live
ENABLE_SSL_MONITORING=true
SSL_WARNING_DAYS=30
```

### 日志
```bash
LOG_LEVEL=INFO                 # DEBUG/INFO/WARNING/ERROR/CRITICAL
LOG_FILE=logs/logivore.log
LOG_MAX_SIZE=10
LOG_BACKUP_COUNT=5
LOG_COLORED=true
```

## JSON 配置（config.json）

默认结构：
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

常用片段：
```json
{ "language": "zh-cn", "update_interval": 10, "alert_interval": 60, "alert_channel": 123456789 }
```
```json
{ "monitored_disks": ["/", "/mnt/data", "/home"] }
```
```json
{
  "alerts": [
    {"id": "cpu_high_usage", "name": "CPU 使用率过高", "type": "cpu", "target": "cpu", "threshold": 80, "enabled": true, "channel_id": 123456789},
    {"id": "disk_space_low", "name": "磁盘空间不足", "type": "disk", "target": "/", "threshold": 85, "enabled": true, "channel_id": null},
    {"id": "nginx_down", "name": "Nginx 进程中断", "type": "process", "target": "nginx", "enabled": true, "channel_id": 123456789}
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

## 语言设置

支持语言：en / zh(zh-tw) / zh-cn / ko / ja / de / ru

新增语言：复制 `languages/en.json` → 翻译 → 在 `.env`/`config.json` 指定 → 在 `config_management.py` 增加选项。

## 监控设置

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

自定义面板：
```json
{ "custom_panels": { "server_room": { "title": "Server Room Monitor", "disks": ["/", "/mnt/storage"], "services": ["nginx", "postgresql"], "update_interval": 5, "alert_thresholds": {"cpu": 70, "memory": 85, "disk": 90} } } }
```

## Docker 设置

```json
{ "docker_monitoring": { "enabled": true, "include_filters": ["app-*", "db-*"] } }
```

## SSL 设置

```json
{ "ssl": { "enabled": true, "warning_days": 30, "auto_renewal": { "enabled": true, "days_before": 7 } } }
```

## 高级设置

性能：
```json
{ "performance": { "max_concurrent_monitors": 10, "cache_enabled": true, "cache_ttl": 30, "batch_updates": true, "update_queue_size": 100, "worker_threads": 4 } }
```

安全：
```json
{ "security": { "rate_limiting": { "enabled": true, "max_requests": 60, "whitelist": [123456789] }, "command_restrictions": { "manage": ["owner"], "reboot": ["owner", "admin"], "config": ["owner"] } } }
```

备份/还原：
```json
{ "backup": { "enabled": true, "interval": 86400, "retention_days": 30, "backup_path": "backups/", "components": ["config", "alerts", "logs"] } }
```

## 配置示例

家用服务器：
```json
{ "language": "zh-cn", "update_interval": 10, "monitored_disks": ["/", "/mnt/storage"], "alerts": [ { "id": "cpu_high", "name": "CPU 过高", "type": "cpu", "target": "cpu", "threshold": 85, "enabled": true }, { "id": "disk_full", "name": "磁盘将满", "type": "disk", "target": "/", "threshold": 90, "enabled": true } ], "auto_recovery_enabled": true, "monitored_services": ["ssh", "nginx"] }
```

企业生产：
```json
{ "language": "zh-cn", "update_interval": 5, "alert_interval": 30, "monitored_disks": ["/", "/var/log", "/mnt/data", "/backup"], "alerts": [ { "id": "cpu_critical", "name": "CPU 临界", "type": "cpu", "threshold": 90, "channel_id": 123456789 }, { "id": "memory_high", "name": "内存过高", "type": "memory", "threshold": 85, "channel_id": 123456789 }, { "id": "nginx_down", "name": "Nginx 中断", "type": "process", "target": "nginx", "channel_id": 987654321 } ], "docker_monitoring": { "enabled": true, "include_filters": ["app-*", "db-*"] }, "ssl": { "enabled": true, "warning_days": 14, "auto_renewal": { "enabled": true, "days_before": 7 } } }
```

开发环境：
```json
{ "language": "zh-cn", "update_interval": 30, "alert_interval": 300, "monitored_disks": ["/"], "alerts": [ { "id": "disk_space", "name": "开发磁盘空间", "type": "disk", "target": "/", "threshold": 95, "enabled": true } ], "docker_monitoring": { "enabled": true, "include_filters": ["dev-*", "test-*"] }, "auto_recovery_enabled": false }
```

## 配置校验与下一步

JSON 语法快速检查：
```python
python -c "import json; json.load(open('config.json')); print('✅ JSON syntax OK')"
```

常见错误：JSON 语法、缺失字段、阈值(0-100)、频道 ID 类型、磁盘路径不存在。

下一步：
- 📚 指令参考：`docs/commands.md`
- 🚨 警报设置：`docs/commands.md#alerts`
- 🐳 Docker 集成：`deploy/docker/`
- 🔍 故障排除：`docs/troubleshooting.md`
