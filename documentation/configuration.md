# Configuration Reference

Languages: [English](configuration.md) | [繁體中文](zh-tw/configuration.md) | [简体中文](zh-cn/configuration.md) | [日本語](ja/configuration.md) | [한국어](ko/configuration.md) | [Deutsch](de/configuration.md) | [Русский](ru/configuration.md)

This comprehensive guide covers all configuration options available in Logivore, allowing you to customize the bot's behavior to match your specific requirements.

## Table of Contents

- [Configuration Overview](#configuration-overview)
- [Environment Variables](#environment-variables)
- [JSON Configuration](#json-configuration)
- [Language Settings](#language-settings)
- [Monitoring Configuration](#monitoring-configuration)
- [Alert Configuration](#alert-configuration)
- [Docker Configuration](#docker-configuration)
- [SSL Configuration](#ssl-configuration)
- [Advanced Settings](#advanced-settings)
- [Configuration Examples](#configuration-examples)

## Configuration Overview

Logivore uses a multi-layered configuration system:

1. **Environment Variables** (`.env` file) - Core settings and secrets
2. **JSON Configuration** (`config.json`) - Dynamic runtime settings
3. **Language Files** (`languages/`) - Internationalization settings
4. **Cog-specific Settings** - Module-specific configurations

### Configuration Priority

Settings are loaded in this order (higher priority overrides lower):
1. Environment variables
2. Command-line arguments
3. JSON configuration file
4. Default values

## Environment Variables

### Core Discord Settings

```bash
# Required: Discord bot token from Discord Developer Portal
DISCORD_TOKEN=your_bot_token_here

# Required: Your Discord user ID (right-click username → Copy ID)
OWNER_ID=123456789012345678

# Optional: Default command prefix (for text commands)
COMMAND_PREFIX=!

# Optional: Bot status message
BOT_STATUS=Monitoring systems...
```

### Bot Behavior Settings

```bash
# Default language (en, zh, zh-cn, zh-tw, ko, ja, de, ru)
DEFAULT_LANGUAGE=en

# Update interval for monitoring panels (seconds)
UPDATE_INTERVAL=10

# Alert checking interval (seconds)
ALERT_INTERVAL=60

# Maximum number of concurrent monitoring panels
MAX_MONITORS=5

# Enable debug logging (true/false)
DEBUG_MODE=false
```

### System Monitoring Settings

```bash
# Disk paths to monitor (comma-separated)
MONITORED_DISKS=/,/mnt/data,/home

# Maximum system uptime before warning (days)
MAX_UPTIME_DAYS=30

# Enable SMART disk monitoring (true/false)
ENABLE_SMART_MONITORING=true

# Process monitoring blacklist (comma-separated)
PROCESS_BLACKLIST=kthreadd,ksoftirqd

# Network interface to monitor (auto-detect if empty)
NETWORK_INTERFACE=
```

### Docker Integration

```bash
# Docker socket path
DOCKER_HOST=unix:///var/run/docker.sock

# Docker API version
DOCKER_API_VERSION=auto

# Enable Docker container monitoring
ENABLE_DOCKER_MONITORING=true

# Docker container name filters (comma-separated)
DOCKER_CONTAINER_FILTER=nginx,postgres,redis
```

### SSL Certificate Management

```bash
# Nginx Proxy Manager container name
NPM_CONTAINER=nginx-proxy-manager

# SSL certificate storage path
SSL_CERT_PATH=/etc/letsencrypt/live

# Enable SSL monitoring
ENABLE_SSL_MONITORING=true

# Certificate expiry warning threshold (days)
SSL_WARNING_DAYS=30
```

### Logging Configuration

```bash
# Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_LEVEL=INFO

# Log file path
LOG_FILE=logs/logivore.log

# Maximum log file size (MB)
LOG_MAX_SIZE=10

# Number of log files to keep
LOG_BACKUP_COUNT=5

# Enable colored console output
LOG_COLORED=true
```

## JSON Configuration

The `config.json` file stores dynamic settings that can be modified during runtime.

### Default Configuration Structure

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

### Configuration Details

#### Basic Settings
```json
{
  "language": "en",              // Bot language (en, zh, ko, ja, de, ru)
  "update_interval": 10,         // Monitoring update frequency (seconds)
  "alert_interval": 60,          // Alert check frequency (seconds)
  "alert_channel": 123456789     // Default alert channel ID
}
```

#### Disk Monitoring
```json
{
  "monitored_disks": [           // Specific disk paths to monitor
    "/",                         // Root filesystem
    "/mnt/data",                 // Data mount point
    "/home"                      // Home directory
  ]
}
```

#### Alert Configuration
```json
{
  "alerts": [
    {
      "id": "cpu_high_usage",     // Unique alert identifier
      "name": "High CPU Usage",   // Human-readable name
      "type": "cpu",              // Alert type (cpu, disk, process)
      "target": "cpu",            // Monitoring target
      "threshold": 80,            // Trigger threshold (percentage)
      "enabled": true,            // Enable/disable alert
      "channel_id": 123456789     // Specific channel for this alert
    },
    {
      "id": "disk_space_low",
      "name": "Low Disk Space",
      "type": "disk",
      "target": "/",
      "threshold": 85,
      "enabled": true,
      "channel_id": null          // Use default alert channel
    },
    {
      "id": "nginx_down",
      "name": "Nginx Process Down",
      "type": "process",
      "target": "nginx",
      "enabled": true,
      "channel_id": 123456789
    }
  ]
}
```

#### Service Recovery
```json
{
  "auto_recovery_enabled": true,  // Enable automatic service recovery
  "monitored_services": [         // systemd services to monitor
    "nginx",
    "postgresql",
    "redis-server"
  ],
  "last_known_state": {           // Saved system state for recovery
    "timestamp": 1635789123,
    "docker_containers": [
      {"name": "nginx", "image": "nginx:latest"}
    ],
    "systemd_services": ["nginx", "postgresql"]
  }
}
```

#### System Reboot Management
```json
{
  "max_uptime_days": 30,          // Warning threshold for system uptime
  "reboot_stop_services": [       // Services to stop before reboot
    "nginx",
    "postgresql"
  ],
  "scheduled_reboots": [          // Scheduled reboot entries
    {
      "time": "2024-01-01T02:00:00",
      "delay": 5,
      "enabled": true,
      "scheduled_by": 123456789
    }
  ]
}
```

## Language Settings

### Supported Languages

| Language | Code | File | Status |
|----------|------|------|--------|
| English | `en` | `languages/en.json` | ✅ Complete |
| Traditional Chinese | `zh` or `zh-tw` | `languages/zh.json` | ✅ Complete |
| Simplified Chinese | `zh-cn` | `languages/zh-cn.json` | ✅ Complete |
| Korean | `ko` | `languages/ko.json` | ✅ Complete |
| Japanese | `ja` | `languages/ja.json` | ✅ Complete |
| German | `de` | `languages/de.json` | ✅ Complete |
| Russian | `ru` | `languages/ru.json` | ✅ Complete |

### Language File Structure

Each language file follows this structure:

```json
{
  "system": {
    "status": "SYSTEM STATUS",
    "cpu": "CPU",
    "memory": "Memory"
  },
  "alerts": {
    "triggered": "🚨 Alert Triggered: {name}",
    "resolved": "✅ Alert Resolved: {name}"
  },
  "commands": {
    "monitor_desc": "Display real-time system monitoring panel"
  },
  "help": {
    "serelix_bot_help": "Logivore Help"
  }
}
```

### Adding Custom Languages

1. **Create language file**:
```bash
cp languages/en.json languages/your-lang.json
```

2. **Translate all entries**:
```json
{
  "system": {
    "status": "Your Translation Here"
  }
}
```

3. **Update configuration**:
```bash
# In .env or config.json
DEFAULT_LANGUAGE=your-lang
```

4. **Add language choice** in `config_management.py`:
```python
@discord.app_commands.choices(language=[
    # ... existing choices ...
    discord.app_commands.Choice(name="Your Language", value="your-lang"),
])
```

## Monitoring Configuration

### System Monitoring Options

```json
{
  "monitoring": {
    "cpu_interval": 0.1,          // CPU sampling interval
    "memory_warnings": true,      // Enable memory warnings
    "disk_smart_check": true,     // Enable SMART disk monitoring
    "network_speed_calc": true,   // Calculate network speeds
    "process_monitoring": {
      "enabled": true,
      "top_count": 10,            // Number of top processes to show
      "cpu_threshold": 80,        // CPU threshold for process alerts
      "memory_threshold": 80      // Memory threshold for process alerts
    }
  }
}
```

### Custom Monitoring Panels

```json
{
  "custom_panels": {
    "server_room": {              // Custom panel name
      "title": "Server Room Monitor",
      "disks": ["/", "/mnt/storage"],
      "services": ["nginx", "postgresql"],
      "update_interval": 5,
      "alert_thresholds": {
        "cpu": 70,
        "memory": 85,
        "disk": 90
      }
    }
  }
}
```

## Alert Configuration

### Alert Types

#### CPU Alerts
```json
{
  "type": "cpu",
  "target": "cpu",                // Always "cpu" for CPU alerts
  "threshold": 80,                // Percentage threshold
  "duration": 300                 // Sustained duration (seconds)
}
```

#### Memory Alerts
```json
{
  "type": "memory",
  "target": "memory",             // Always "memory" for memory alerts
  "threshold": 85,                // Percentage threshold
  "include_swap": false           // Include swap in calculation
}
```

#### Disk Alerts
```json
{
  "type": "disk",
  "target": "/",                  // Mount point to monitor
  "threshold": 90,                // Percentage threshold
  "check_inodes": true            // Also check inode usage
}
```

#### Process Alerts
```json
{
  "type": "process",
  "target": "nginx",              // Process name to monitor
  "check_memory": true,           // Monitor process memory
  "memory_threshold": 500         // Memory threshold (MB)
}
```

#### Custom Service Alerts
```json
{
  "type": "service",
  "target": "nginx.service",      // systemd service name
  "restart_on_failure": true,    // Auto-restart failed services
  "max_restarts": 3              // Maximum restart attempts
}
```

### Alert Channels

```json
{
  "alert_channels": {
    "critical": 123456789,        // Critical alerts channel
    "warning": 987654321,         // Warning alerts channel
    "info": 555666777            // Information alerts channel
  },
  "alert_routing": {
    "cpu": "critical",            // Route CPU alerts to critical channel
    "disk": "warning",            // Route disk alerts to warning channel
    "process": "critical"         // Route process alerts to critical channel
  }
}
```

## Docker Configuration

### Docker Connection Settings

```json
{
  "docker": {
    "enabled": true,              // Enable Docker integration
    "socket_path": "unix:///var/run/docker.sock",
    "api_version": "auto",        // Docker API version
    "timeout": 30,                // Connection timeout (seconds)
    "tls_config": {              // TLS configuration for remote Docker
      "enabled": false,
      "cert_path": "/path/to/cert.pem",
      "key_path": "/path/to/key.pem",
      "ca_path": "/path/to/ca.pem"
    }
  }
}
```

### Container Monitoring

```json
{
  "docker_monitoring": {
    "auto_discover": true,        // Auto-discover containers
    "include_filters": [          // Include containers matching these patterns
      "nginx*",
      "postgres*"
    ],
    "exclude_filters": [          // Exclude containers matching these patterns
      "*test*",
      "*temp*"
    ],
    "monitor_resources": {
      "cpu": true,                // Monitor CPU usage
      "memory": true,             // Monitor memory usage
      "network": true,            // Monitor network I/O
      "disk": true               // Monitor disk I/O
    },
    "alerts": {
      "cpu_threshold": 80,        // Container CPU alert threshold
      "memory_threshold": 90      // Container memory alert threshold
    }
  }
}
```

## SSL Configuration

### SSL Monitoring Settings

```json
{
  "ssl": {
    "enabled": true,              // Enable SSL monitoring
    "check_interval": 3600,       // Check interval (seconds)
    "warning_days": 30,           // Warning threshold (days)
    "critical_days": 7,           // Critical threshold (days)
    "auto_renewal": {
      "enabled": true,            // Enable automatic renewal
      "days_before": 14,          // Renew N days before expiry
      "restart_services": [       // Services to restart after renewal
        "nginx",
        "apache2"
      ]
    }
  }
}
```

### Nginx Proxy Manager Integration

```json
{
  "npm": {
    "container_name": "nginx-proxy-manager",
    "api_endpoint": "http://localhost:81/api",
    "credentials": {
      "username": "admin@example.com",
      "password": "stored_securely"  // Use environment variable
    },
    "certificate_path": "/etc/letsencrypt/live",
    "reload_command": "nginx -s reload"
  }
}
```

## Advanced Settings

### Performance Tuning

```json
{
  "performance": {
    "max_concurrent_monitors": 10,   // Maximum active monitors
    "cache_enabled": true,           // Enable caching
    "cache_ttl": 30,                // Cache TTL (seconds)
    "batch_updates": true,           // Batch Discord API calls
    "update_queue_size": 100,        // Update queue size
    "worker_threads": 4              // Worker thread count
  }
}
```

### Security Settings

```json
{
  "security": {
    "rate_limiting": {
      "enabled": true,             // Enable rate limiting
      "max_requests": 60,          // Max requests per minute
      "whitelist": [               // Rate limit whitelist
        123456789                  // Owner ID
      ]
    },
    "command_restrictions": {
      "manage": ["owner"],         // Restrict manage commands to owner
      "reboot": ["owner", "admin"], // Restrict reboot to owner/admin
      "config": ["owner"]          // Restrict config to owner
    }
  }
}
```

### Backup and Recovery

```json
{
  "backup": {
    "enabled": true,               // Enable automatic backups
    "interval": 86400,             // Backup interval (seconds)
    "retention_days": 30,          // Keep backups for N days
    "backup_path": "backups/",     // Backup directory
    "components": [                // Components to backup
      "config",
      "alerts",
      "logs"
    ]
  }
}
```

## Configuration Examples

### Basic Home Server Setup

```json
{
  "language": "en",
  "update_interval": 10,
  "monitored_disks": ["/", "/mnt/storage"],
  "alerts": [
    {
      "id": "cpu_high",
      "name": "High CPU Usage",
      "type": "cpu",
      "target": "cpu",
      "threshold": 85,
      "enabled": true
    },
    {
      "id": "disk_full",
      "name": "Disk Almost Full",
      "type": "disk",
      "target": "/",
      "threshold": 90,
      "enabled": true
    }
  ],
  "auto_recovery_enabled": true,
  "monitored_services": ["ssh", "nginx"]
}
```

### Enterprise Production Setup

```json
{
  "language": "en",
  "update_interval": 5,
  "alert_interval": 30,
  "monitored_disks": ["/", "/var/log", "/mnt/data", "/backup"],
  "alerts": [
    {
      "id": "cpu_critical",
      "name": "Critical CPU Usage",
      "type": "cpu",
      "threshold": 90,
      "channel_id": 123456789
    },
    {
      "id": "memory_high",
      "name": "High Memory Usage",
      "type": "memory",
      "threshold": 85,
      "channel_id": 123456789
    },
    {
      "id": "nginx_down",
      "name": "Nginx Service Down",
      "type": "process",
      "target": "nginx",
      "channel_id": 987654321
    }
  ],
  "docker_monitoring": {
    "enabled": true,
    "include_filters": ["app-*", "db-*"],
    "alerts": {
      "cpu_threshold": 80,
      "memory_threshold": 85
    }
  },
  "ssl": {
    "enabled": true,
    "warning_days": 14,
    "auto_renewal": {
      "enabled": true,
      "days_before": 7
    }
  }
}
```

### Development Environment

```json
{
  "language": "en",
  "update_interval": 30,
  "alert_interval": 300,
  "monitored_disks": ["/"],
  "alerts": [
    {
      "id": "disk_space",
      "name": "Development Disk Space",
      "type": "disk",
      "target": "/",
      "threshold": 95,
      "enabled": true
    }
  ],
  "docker_monitoring": {
    "enabled": true,
    "include_filters": ["dev-*", "test-*"]
  },
  "auto_recovery_enabled": false
}
```

## Configuration Validation

### Validate Configuration

```python
# Built-in validation
python -c "
import json
from utils.config import ConfigManager

config = ConfigManager('config.json')
if config.validate():
    print('✅ Configuration is valid')
else:
    print('❌ Configuration has errors')
"
```

### Common Validation Issues

1. **Invalid JSON syntax**
2. **Missing required fields**
3. **Invalid threshold values** (must be 0-100)
4. **Invalid channel IDs** (must be Discord snowflakes)
5. **Invalid disk paths** (must exist on system)

## Next Steps

- 📚 [Command Reference](commands.md) - Learn all available commands
- 🚨 [Alert Setup Guide](alerts.md) - Configure advanced alerting
- 🐳 [Docker Integration](docker.md) - Set up Docker monitoring
- 🔧 [Customization Guide](customization.md) - Customize bot behavior
- 🔍 [Troubleshooting](troubleshooting.md) - Solve common issues

---

**Need help?** Join our [Discord community](https://discord.gg/serelix) or check [GitHub Issues](https://github.com/kaiyasi/Logivore/issues).
