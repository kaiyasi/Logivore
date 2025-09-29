# Command Reference

Languages: [English](commands.md) | [繁體中文](zh-tw/commands.md) | [简体中文](zh-cn/commands.md) | [日本語](ja/commands.md) | [한국어](ko/commands.md) | [Deutsch](de/commands.md) | [Русский](ru/commands.md)

This comprehensive guide covers all available commands in Logivore, their usage, parameters, and examples.

## Table of Contents

- [System Monitoring Commands](#system-monitoring-commands)
- [Docker Management Commands](#docker-management-commands)
- [Alert Management Commands](#alert-management-commands)
- [SSL Management Commands](#ssl-management-commands)
- [Configuration Commands](#configuration-commands)
- [Bot Management Commands](#bot-management-commands)
- [Help Commands](#help-commands)
- [Command Categories](#command-categories)
- [Permission Levels](#permission-levels)

## System Monitoring Commands

### /monitor

**Description**: Display real-time system monitoring dashboard with live updates

**Usage**: `/monitor`

**Parameters**: None

**Features**:
- Real-time CPU, memory, disk, and network statistics
- Auto-refreshes every 10 seconds
- Beautiful formatted dashboard with progress bars
- Multi-language support

**Example Output**:
```
🖥️ System Monitor - Live Dashboard
Updated: 2024-01-15 14:30:25

💾 CPU Usage: ████████░░ 45.2% (8 cores)
🧠 Memory: ██████████ 67.8% (5.4GB / 8.0GB)
💽 Disk (/): ███░░░░░░░ 23.1% (115GB / 500GB)
🌐 Network: ↗️ 2.3 MB/s ↙️ 1.8 MB/s

Last Updated: Just now
```

### /ports

**Description**: Scan and display open network ports on the system

**Usage**: `/ports [port_range]`

**Parameters**:
- `port_range` (optional): Port range to scan (e.g., "1-1000", "80,443,22")

**Examples**:
- `/ports` - Scan common ports (22, 80, 443, 3306, 5432)
- `/ports 1-1000` - Scan ports 1 to 1000
- `/ports 80,443,22,3306` - Scan specific ports

### /processes

**Description**: Display running processes with resource usage

**Usage**: `/processes [filter]`

**Parameters**:
- `filter` (optional): Filter processes by name or PID

**Examples**:
- `/processes` - Show all processes
- `/processes python` - Show processes containing "python"
- `/processes 1234` - Show process with PID 1234

### /disk

**Description**: Show detailed disk usage and health information

**Usage**: `/disk [path]`

**Parameters**:
- `path` (optional): Specific disk path to check

**Features**:
- Disk usage statistics
- SMART health status (Linux)
- File system information
- Mount point details

## Docker Management Commands

### /docker status

**Description**: Display status of all Docker containers

**Usage**: `/docker status`

**Features**:
- Container status (running, stopped, exited)
- Image information
- Port mappings
- Resource usage

### /docker start

**Description**: Start a Docker container

**Usage**: `/docker start <container_name>`

**Parameters**:
- `container_name` (required): Name or ID of the container

**Example**: `/docker start nginx-proxy`

### /docker stop

**Description**: Stop a running Docker container

**Usage**: `/docker stop <container_name>`

**Parameters**:
- `container_name` (required): Name or ID of the container

**Example**: `/docker stop nginx-proxy`

### /docker restart

**Description**: Restart a Docker container

**Usage**: `/docker restart <container_name>`

**Parameters**:
- `container_name` (required): Name or ID of the container

**Example**: `/docker restart nginx-proxy`

### /docker logs

**Description**: View logs from a Docker container

**Usage**: `/docker logs <container_name> [lines]`

**Parameters**:
- `container_name` (required): Name or ID of the container
- `lines` (optional): Number of log lines to display (default: 50)

**Example**: `/docker logs nginx-proxy 100`

### /docker stats

**Description**: Display real-time resource usage statistics for containers

**Usage**: `/docker stats [container_name]`

**Parameters**:
- `container_name` (optional): Specific container to monitor

## Alert Management Commands

### /alerts list

**Description**: Display all configured alerts and their status

**Usage**: `/alerts list`

**Features**:
- Alert type and thresholds
- Current status (active/inactive)
- Last triggered time
- Target channels

### /alerts add

**Description**: Add a new system alert

**Usage**: `/alerts add <type> <threshold> [channel]`

**Parameters**:
- `type` (required): Alert type (cpu, memory, disk, process)
- `threshold` (required): Threshold value (percentage or specific value)
- `channel` (optional): Target channel for notifications

**Examples**:
- `/alerts add cpu 90` - Alert when CPU usage exceeds 90%
- `/alerts add memory 85 #alerts` - Memory alert to specific channel
- `/alerts add disk 95` - Disk usage alert

### /alerts remove

**Description**: Remove an existing alert

**Usage**: `/alerts remove <alert_id>`

**Parameters**:
- `alert_id` (required): ID of the alert to remove

**Example**: `/alerts remove 12345`

### /alerts test

**Description**: Test alert notification system

**Usage**: `/alerts test [type]`

**Parameters**:
- `type` (optional): Specific alert type to test

## SSL Management Commands

### /ssl list

**Description**: List all SSL certificates and their status

**Usage**: `/ssl list`

**Features**:
- Certificate domains
- Expiration dates
- Days until expiration
- Certificate authority
- Status (valid/expired/expiring)

### /ssl check

**Description**: Check specific SSL certificate status

**Usage**: `/ssl check <domain>`

**Parameters**:
- `domain` (required): Domain name to check

**Example**: `/ssl check example.com`

### /ssl renew

**Description**: Renew SSL certificate for a domain

**Usage**: `/ssl renew <domain>`

**Parameters**:
- `domain` (required): Domain to renew certificate for

**Requirements**:
- Nginx Proxy Manager integration
- Proper DNS configuration
- Valid Let's Encrypt account

### /ssl auto-renew

**Description**: Configure automatic SSL certificate renewal

**Usage**: `/ssl auto-renew <enable|disable> [days_before]`

**Parameters**:
- `enable|disable` (required): Enable or disable auto-renewal
- `days_before` (optional): Days before expiration to trigger renewal (default: 30)

**Example**: `/ssl auto-renew enable 15`

## Configuration Commands

### /config show

**Description**: Display current bot configuration

**Usage**: `/config show [section]`

**Parameters**:
- `section` (optional): Specific configuration section (system, alerts, docker, ssl)

### /config set

**Description**: Update configuration value

**Usage**: `/config set <key> <value>`

**Parameters**:
- `key` (required): Configuration key to update
- `value` (required): New value

**Example**: `/config set update_interval 15`

### /config reload

**Description**: Reload configuration from file

**Usage**: `/config reload`

**Note**: Owner-only command

### /language

**Description**: Change bot language or view available languages

**Usage**: `/language [language_code]`

**Parameters**:
- `language_code` (optional): Language code to switch to

**Supported Languages**:
- `en` - English
- `zh` / `zh-tw` - Traditional Chinese
- `zh-cn` - Simplified Chinese
- `ko` - Korean
- `ja` - Japanese
- `de` - German
- `ru` - Russian

**Examples**:
- `/language` - Show current language and available options
- `/language en` - Switch to English
- `/language zh-cn` - Switch to Simplified Chinese

## Bot Management Commands

### /restart

**Description**: Restart the bot (owner only)

**Usage**: `/restart`

**Requirements**: Bot owner permissions

### /shutdown

**Description**: Shutdown the bot gracefully (owner only)

**Usage**: `/shutdown`

**Requirements**: Bot owner permissions

### /reload

**Description**: Reload a specific cog module

**Usage**: `/reload <cog_name>`

**Parameters**:
- `cog_name` (required): Name of the cog to reload

**Example**: `/reload system_monitoring`

### /sync

**Description**: Sync slash commands with Discord

**Usage**: `/sync`

**Requirements**: Bot owner permissions

### /status

**Description**: Display bot status and statistics

**Usage**: `/status`

**Features**:
- Bot uptime
- Server count
- User count
- System resources
- Version information

## Help Commands

### /help

**Description**: Display help information and command categories

**Usage**: `/help [category]`

**Parameters**:
- `category` (optional): Specific command category

**Categories**:
- `monitoring` - System monitoring commands
- `docker` - Docker management commands
- `alerts` - Alert management commands
- `ssl` - SSL certificate management
- `config` - Configuration commands
- `admin` - Administrative commands

**Examples**:
- `/help` - Show all categories
- `/help monitoring` - Show monitoring commands
- `/help docker` - Show Docker commands

## Command Categories

### 🔍 System Monitoring
Commands for monitoring system resources and performance.

**Commands**: `/monitor`, `/ports`, `/processes`, `/disk`

**Purpose**: Real-time system insights and resource tracking

### 🐳 Docker Management
Complete Docker container lifecycle management.

**Commands**: `/docker status`, `/docker start`, `/docker stop`, `/docker restart`, `/docker logs`, `/docker stats`

**Purpose**: Container orchestration and monitoring

### 🚨 Alert Management
Proactive monitoring and notification system.

**Commands**: `/alerts list`, `/alerts add`, `/alerts remove`, `/alerts test`

**Purpose**: Automated system health notifications

### 🛡️ SSL Management
SSL certificate monitoring and management.

**Commands**: `/ssl list`, `/ssl check`, `/ssl renew`, `/ssl auto-renew`

**Purpose**: Automated certificate lifecycle management

### ⚙️ Configuration
Bot configuration and customization.

**Commands**: `/config show`, `/config set`, `/config reload`, `/language`

**Purpose**: Dynamic bot configuration management

### 🤖 Administration
Bot management and administrative functions.

**Commands**: `/restart`, `/shutdown`, `/reload`, `/sync`, `/status`

**Purpose**: Bot administration and maintenance

## Permission Levels

### Public Commands
Available to all users with bot access:
- `/monitor`
- `/ports`
- `/processes`
- `/disk`
- `/docker status`
- `/docker logs`
- `/docker stats`
- `/ssl list`
- `/ssl check`
- `/config show`
- `/language`
- `/status`
- `/help`

### Owner Commands
Restricted to bot owner (configured via `OWNER_ID`):
- `/docker start`
- `/docker stop`
- `/docker restart`
- `/alerts add`
- `/alerts remove`
- `/ssl renew`
- `/ssl auto-renew`
- `/config set`
- `/config reload`
- `/restart`
- `/shutdown`
- `/reload`
- `/sync`

### Server Permissions
Some commands may require specific Discord permissions:
- **Send Messages**: All commands
- **Embed Links**: All commands with rich embeds
- **Use Slash Commands**: All slash commands
- **Manage Messages**: Commands that edit/delete messages

## Usage Tips

### 1. Monitoring Best Practices
- Use `/monitor` for real-time system overview
- Set up alerts with `/alerts add` for proactive monitoring
- Check `/processes` regularly for resource-heavy applications

### 2. Docker Management
- Always check `/docker status` before starting/stopping containers
- Use `/docker logs` to troubleshoot container issues
- Monitor resource usage with `/docker stats`

### 3. SSL Management
- Enable auto-renewal with `/ssl auto-renew enable`
- Check certificate status monthly with `/ssl list`
- Test renewal process before certificates expire

### 4. Configuration Management
- Use `/config show` to verify settings
- Reload configuration with `/config reload` after manual edits
- Change language with `/language` for localized experience

### 5. Troubleshooting
- Check bot status with `/status` if commands aren't working
- Use `/help` to verify command syntax
- Restart bot with `/restart` if experiencing issues

## Command Aliases

Some commands support shorter aliases for convenience:

- `/mon` → `/monitor`
- `/ps` → `/processes`
- `/d` → `/docker`
- `/cfg` → `/config`
- `/lang` → `/language`

## Error Handling

All commands include comprehensive error handling:

- **Permission Errors**: Clear messages about required permissions
- **Invalid Parameters**: Helpful suggestions for correct usage
- **System Errors**: Graceful degradation with informative messages
- **Network Issues**: Timeout handling and retry mechanisms

## Multi-Language Support

All commands support the following languages:
- English (en)
- Traditional Chinese (zh-tw)
- Simplified Chinese (zh-cn)
- Korean (ko)
- Japanese (ja)
- German (de)
- Russian (ru)

Command descriptions, error messages, and output are automatically localized based on the server's language setting.

---

For additional help or feature requests, join our [Discord community](https://discord.gg/serelix) or check [GitHub Issues](https://github.com/kaiyasi/Logivore/issues).
