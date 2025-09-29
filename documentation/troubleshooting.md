# Troubleshooting Guide

Languages: English | [繁體中文](zh-tw/troubleshooting.md) | [简体中文](zh-cn/troubleshooting.md) | [日本語](ja/troubleshooting.md) | [한국어](ko/troubleshooting.md) | [Deutsch](de/troubleshooting.md) | [Русский](ru/troubleshooting.md)

This guide helps you diagnose and resolve common issues with Logivore, from installation problems to runtime errors.

## Table of Contents

- [Quick Diagnostics](#quick-diagnostics)
- [Installation Issues](#installation-issues)
- [Configuration Problems](#configuration-problems)
- [Discord API Issues](#discord-api-issues)
- [System Monitoring Problems](#system-monitoring-problems)
- [Docker Integration Issues](#docker-integration-issues)
- [SSL Management Problems](#ssl-management-problems)
- [Performance Issues](#performance-issues)
- [Logging and Debugging](#logging-and-debugging)
- [Common Error Messages](#common-error-messages)
- [Recovery Procedures](#recovery-procedures)
- [Getting Help](#getting-help)

## Quick Diagnostics

Before diving into specific issues, run these quick diagnostic checks:

### Basic Health Check

```bash
# Check if bot process is running
ps aux | grep python | grep main.py

# Check bot logs
tail -f logs/logivore.log

# Check system resources
free -h
df -h
top
```

### Bot Status Check

```bash
# Test Discord connection
python -c "
import discord
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

async def test_connection():
    try:
        client = discord.Client(intents=discord.Intents.default())

        @client.event
        async def on_ready():
            print(f'✅ Connected as {client.user}')
            await client.close()

        await client.start(os.getenv('DISCORD_TOKEN'))
    except Exception as e:
        print(f'❌ Connection failed: {e}')

asyncio.run(test_connection())
"
```

### Configuration Validation

```bash
# Validate JSON configuration
python -c "
import json
try:
    with open('config/bot_config.json', 'r') as f:
        config = json.load(f)
    print('✅ Configuration file is valid JSON')
except Exception as e:
    print(f'❌ Configuration error: {e}')
"
```

## Installation Issues

### Python Version Compatibility

**Problem**: Bot fails to start with Python version errors

**Solution**:
```bash
# Check Python version
python --version

# Required: Python 3.8 or higher
# If using older version, update Python:

# Ubuntu/Debian
sudo apt update
sudo apt install python3.9 python3.9-pip python3.9-venv

# CentOS/RHEL
sudo yum install python39 python39-pip

# macOS (using Homebrew)
brew install python@3.9

# Windows: Download from python.org
```

### Missing Dependencies

**Problem**: ImportError or ModuleNotFoundError when starting

**Solution**:
```bash
# Reinstall all dependencies
pip install --upgrade pip
pip install -r requirements.txt

# If using virtual environment
python -m venv venv --clear
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# For development dependencies
pip install -r requirements-dev.txt
```

### Permission Issues (Linux)

**Problem**: Permission denied errors when running bot

**Solution**:
```bash
# Fix file permissions
chmod +x main.py
chmod 644 .env config/bot_config.json

# Fix directory permissions
chmod 755 . cogs/ utils/ languages/
chmod 766 logs/

# If running as service, ensure correct ownership
sudo chown -R botuser:botuser /path/to/Logivore
```

### Virtual Environment Issues

**Problem**: Virtual environment not working correctly

**Solution**:
```bash
# Remove and recreate virtual environment
rm -rf venv
python -m venv venv

# Activate and reinstall
source venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# Verify installation
pip list | grep discord
```

## Configuration Problems

### Invalid Discord Token

**Problem**: Bot fails to connect with authentication error

**Symptoms**:
- "Invalid token" error messages
- Bot appears offline in Discord
- HTTP 401 errors in logs

**Solution**:
```bash
# Verify token format (should be 70+ characters)
echo $DISCORD_TOKEN | wc -c

# Test token validity
python -c "
import requests
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

headers = {'Authorization': f'Bot {token}'}
response = requests.get('https://discord.com/api/v10/users/@me', headers=headers)

if response.status_code == 200:
    print('✅ Token is valid')
    print(f'Bot: {response.json()[\"username\"]}#{response.json()[\"discriminator\"]}')
else:
    print(f'❌ Token invalid: {response.status_code}')
"

# Regenerate token if invalid:
# 1. Go to Discord Developer Portal
# 2. Select your application
# 3. Go to Bot section
# 4. Click "Reset Token"
# 5. Update .env file with new token
```

### Missing Environment Variables

**Problem**: Bot fails to start due to missing configuration

**Solution**:
```bash
# Check if .env file exists
ls -la .env

# Create from template if missing
cp .env.example .env

# Verify required variables
grep -E "^(DISCORD_TOKEN|OWNER_ID)" .env

# Check environment loading
python -c "
from dotenv import load_dotenv
import os

load_dotenv()
print('DISCORD_TOKEN:', 'SET' if os.getenv('DISCORD_TOKEN') else 'MISSING')
print('OWNER_ID:', 'SET' if os.getenv('OWNER_ID') else 'MISSING')
"
```

### JSON Configuration Errors

**Problem**: Bot fails to load configuration file

**Common Issues**:
- Invalid JSON syntax
- Missing required sections
- Incorrect data types

**Solution**:
```bash
# Validate JSON syntax
python -m json.tool config/bot_config.json

# Reset to default if corrupted
cp config/bot_config.example.json config/bot_config.json

# Check for common JSON errors
python -c "
import json

try:
    with open('config/bot_config.json', 'r') as f:
        config = json.load(f)

    # Validate required sections
    required_sections = ['bot', 'monitoring', 'alerts', 'docker', 'ssl']
    for section in required_sections:
        if section not in config:
            print(f'❌ Missing section: {section}')
        else:
            print(f'✅ Found section: {section}')

except json.JSONDecodeError as e:
    print(f'❌ JSON syntax error: {e}')
except Exception as e:
    print(f'❌ Configuration error: {e}')
"
```

## Discord API Issues

### Rate Limiting

**Problem**: Bot responses are delayed or commands fail

**Symptoms**:
- HTTP 429 errors in logs
- "Rate limited" messages
- Slow command responses

**Solution**:
```python
# Check rate limit status
import aiohttp
import asyncio

async def check_rate_limits():
    headers = {'Authorization': f'Bot {os.getenv("DISCORD_TOKEN")}'}

    async with aiohttp.ClientSession() as session:
        async with session.get('https://discord.com/api/v10/users/@me', headers=headers) as resp:
            print(f'Rate limit remaining: {resp.headers.get("X-RateLimit-Remaining")}')
            print(f'Rate limit reset: {resp.headers.get("X-RateLimit-Reset")}')

# Run: asyncio.run(check_rate_limits())
```

**Prevention**:
- Reduce command frequency
- Implement proper cooldowns
- Use bulk operations where possible

### Missing Permissions

**Problem**: Bot cannot execute commands or send messages

**Solution**:
```bash
# Check bot permissions in server
# 1. Right-click on bot in member list
# 2. Click "View Server Profile"
# 3. Check assigned roles and permissions

# Required permissions:
# - Send Messages
# - Embed Links
# - Use Slash Commands
# - Read Message History
# - View Channels

# Re-invite bot with correct permissions:
# Use Discord Developer Portal OAuth2 URL Generator
```

### Slash Command Sync Issues

**Problem**: Slash commands not appearing in Discord

**Solution**:
```python
# Manually sync commands
@app_commands.command(name="sync", description="Sync slash commands")
async def sync_commands(interaction: discord.Interaction):
    if interaction.user.id != int(os.getenv('OWNER_ID')):
        return await interaction.response.send_message("Only owner can sync commands.", ephemeral=True)

    try:
        synced = await interaction.client.tree.sync()
        await interaction.response.send_message(f"Synced {len(synced)} commands.")
    except Exception as e:
        await interaction.response.send_message(f"Failed to sync: {e}", ephemeral=True)
```

## System Monitoring Problems

### PSUtil Errors

**Problem**: System monitoring fails with psutil errors

**Common Issues**:
- Permission denied accessing system information
- Missing system dependencies
- Cross-platform compatibility

**Solution**:
```bash
# Install system dependencies
# Ubuntu/Debian
sudo apt install python3-dev build-essential

# CentOS/RHEL
sudo yum groupinstall "Development Tools"
sudo yum install python3-devel

# Reinstall psutil
pip uninstall psutil
pip install psutil

# Test psutil functionality
python -c "
import psutil
try:
    print('CPU:', psutil.cpu_percent())
    print('Memory:', psutil.virtual_memory().percent)
    print('Disk:', psutil.disk_usage('/').percent)
    print('✅ PSUtil working correctly')
except Exception as e:
    print(f'❌ PSUtil error: {e}')
"
```

### Disk Monitoring Issues

**Problem**: Disk monitoring fails or shows incorrect information

**Solution**:
```bash
# Check disk permissions
ls -la /
df -h

# Test disk access
python -c "
import psutil
import os

# Test all disk partitions
for partition in psutil.disk_partitions():
    try:
        usage = psutil.disk_usage(partition.mountpoint)
        print(f'✅ {partition.mountpoint}: {usage.percent:.1f}% used')
    except PermissionError:
        print(f'❌ Permission denied: {partition.mountpoint}')
    except Exception as e:
        print(f'❌ Error accessing {partition.mountpoint}: {e}')
"

# Fix permissions for mounted drives
sudo chmod 755 /mnt/*
```

### Network Monitoring Problems

**Problem**: Network statistics are incorrect or unavailable

**Solution**:
```bash
# Check network interfaces
ip addr show
ifconfig

# Test network monitoring
python -c "
import psutil

# List network interfaces
print('Network interfaces:')
for interface, addrs in psutil.net_if_addrs().items():
    print(f'  {interface}: {len(addrs)} addresses')

# Test network I/O
net_io = psutil.net_io_counters()
print(f'Network I/O: {net_io.bytes_sent} sent, {net_io.bytes_recv} received')
"
```

## Docker Integration Issues

### Docker Connection Problems

**Problem**: Bot cannot connect to Docker daemon

**Symptoms**:
- "Cannot connect to Docker daemon" errors
- Docker commands fail
- Container monitoring unavailable

**Solution**:
```bash
# Check Docker daemon status
sudo systemctl status docker

# Start Docker if stopped
sudo systemctl start docker
sudo systemctl enable docker

# Check Docker socket permissions
ls -la /var/run/docker.sock
sudo chmod 666 /var/run/docker.sock

# Test Docker connection
docker version
docker ps

# Test Python Docker connection
python -c "
import docker
try:
    client = docker.from_env()
    client.ping()
    print('✅ Docker connection successful')
    containers = client.containers.list()
    print(f'Found {len(containers)} containers')
except Exception as e:
    print(f'❌ Docker connection failed: {e}')
"
```

### Docker Permission Issues

**Problem**: Bot cannot access Docker without sudo

**Solution**:
```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Reload groups (or logout/login)
newgrp docker

# Test Docker access without sudo
docker ps

# For systemd service, ensure user is in docker group
sudo usermod -aG docker botuser
```

### Container Not Found Errors

**Problem**: Bot cannot find or manage specific containers

**Solution**:
```bash
# List all containers (including stopped)
docker ps -a

# Check container names/IDs
docker container ls --format "table {{.Names}}\t{{.ID}}\t{{.Status}}"

# Test container access
python -c "
import docker

client = docker.from_env()
containers = client.containers.list(all=True)

print('Available containers:')
for container in containers:
    print(f'  Name: {container.name}, ID: {container.id[:12]}, Status: {container.status}')
"
```

## SSL Management Problems

### Nginx Proxy Manager Connection

**Problem**: Cannot connect to Nginx Proxy Manager API

**Solution**:
```bash
# Check NPM service status
docker ps | grep nginx-proxy-manager

# Test API connection
curl -X POST http://localhost:81/api/tokens \
  -H "Content-Type: application/json" \
  -d '{"identity":"your-email","secret":"your-password"}'

# Check firewall settings
sudo ufw status
sudo ufw allow 81/tcp

# Verify NPM configuration
python -c "
import requests
import os

npm_url = os.getenv('NPM_API_URL', 'http://localhost:81/api')
npm_email = os.getenv('NPM_EMAIL')
npm_password = os.getenv('NPM_PASSWORD')

try:
    response = requests.post(f'{npm_url}/tokens',
        json={'identity': npm_email, 'secret': npm_password},
        timeout=10)

    if response.status_code == 200:
        print('✅ NPM connection successful')
    else:
        print(f'❌ NPM connection failed: {response.status_code}')
        print(response.text)
except Exception as e:
    print(f'❌ NPM connection error: {e}')
"
```

### Certificate Renewal Issues

**Problem**: SSL certificates fail to renew

**Solution**:
```bash
# Check Let's Encrypt logs
sudo tail -f /var/log/letsencrypt/letsencrypt.log

# Manual certificate renewal test
sudo certbot renew --dry-run

# Check certificate expiry
openssl x509 -in /etc/letsencrypt/live/domain.com/cert.pem -noout -dates

# Verify domain DNS
nslookup domain.com
dig domain.com

# Check port 80/443 accessibility
curl -I http://domain.com
curl -I https://domain.com
```

## Performance Issues

### High Memory Usage

**Problem**: Bot consumes excessive memory

**Diagnosis**:
```bash
# Monitor memory usage
ps aux | grep python
top -p $(pgrep -f main.py)

# Check for memory leaks
python -c "
import psutil
import os

process = psutil.Process(os.getpid())
print(f'Memory usage: {process.memory_info().rss / 1024 / 1024:.1f} MB')
print(f'Memory percent: {process.memory_percent():.1f}%')
"
```

**Solutions**:
```python
# Optimize monitoring intervals
# In config/bot_config.json:
{
  "monitoring": {
    "update_interval": 30,  # Increase from 10 seconds
    "enable_detailed_stats": false,  # Disable if not needed
    "cache_timeout": 60  # Add caching
  }
}

# Implement memory cleanup in monitoring loop
import gc

@tasks.loop(seconds=300)
async def cleanup_task():
    gc.collect()  # Force garbage collection
```

### High CPU Usage

**Problem**: Bot causes high CPU utilization

**Diagnosis**:
```bash
# Monitor CPU usage
htop
iostat 1 5

# Profile Python performance
python -m cProfile -o profile.stats main.py
python -c "
import pstats
stats = pstats.Stats('profile.stats')
stats.sort_stats('cumulative').print_stats(10)
"
```

**Solutions**:
```python
# Optimize psutil calls
# Reduce blocking operations
cpu_percent = psutil.cpu_percent(interval=0.1)  # Reduce from 1.0

# Use asyncio for non-blocking operations
import asyncio

async def get_system_stats():
    # Run CPU-intensive operations in thread pool
    loop = asyncio.get_event_loop()
    cpu_stats = await loop.run_in_executor(None, psutil.cpu_percent, 0.1)
    return cpu_stats
```

### Slow Command Response

**Problem**: Commands take too long to respond

**Solution**:
```python
# Use defer for long-running commands
@app_commands.command(name="slowcommand")
async def slow_command(interaction: discord.Interaction):
    await interaction.response.defer()  # Acknowledge immediately

    # Perform long operation
    result = await some_long_operation()

    await interaction.followup.send(result)

# Implement timeout handling
import asyncio

try:
    result = await asyncio.wait_for(some_operation(), timeout=30.0)
except asyncio.TimeoutError:
    await interaction.followup.send("Operation timed out")
```

## Logging and Debugging

### Enable Debug Logging

```python
# utils/logging_config.py
import logging
import colorlog

def setup_logging(level=logging.INFO):
    """Setup colored logging with detailed format"""

    # Create formatter
    formatter = colorlog.ColoredFormatter(
        '%(log_color)s%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        }
    )

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # File handler
    file_handler = logging.FileHandler('logs/debug.log')
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s'
    ))

    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    # Discord.py debug
    logging.getLogger('discord').setLevel(logging.WARNING)
    logging.getLogger('discord.http').setLevel(logging.WARNING)

# Enable debug mode
setup_logging(logging.DEBUG)
```

### Debug Configuration

```bash
# Add to .env for debug mode
DEBUG_MODE=true
LOG_LEVEL=DEBUG

# Run with debug output
python main.py --debug

# Check specific logger output
python -c "
import logging
logging.basicConfig(level=logging.DEBUG)

# Test specific component
from utils.config_manager import ConfigManager
config = ConfigManager('config/bot_config.json')
print('Debug logging enabled')
"
```

### Error Tracking

```python
# utils/error_tracker.py
import traceback
import logging
from datetime import datetime

class ErrorTracker:
    def __init__(self):
        self.errors = []
        self.logger = logging.getLogger('error_tracker')

    def log_error(self, error: Exception, context: str = None):
        """Log error with full traceback"""
        error_info = {
            'timestamp': datetime.now().isoformat(),
            'error_type': type(error).__name__,
            'error_message': str(error),
            'context': context,
            'traceback': traceback.format_exc()
        }

        self.errors.append(error_info)
        self.logger.error(f"Error in {context}: {error}")
        self.logger.debug(f"Full traceback:\n{error_info['traceback']}")

        # Keep only last 100 errors
        if len(self.errors) > 100:
            self.errors = self.errors[-100:]

    def get_recent_errors(self, count: int = 10):
        """Get recent errors"""
        return self.errors[-count:]

# Usage in cogs
error_tracker = ErrorTracker()

try:
    # Some operation
    pass
except Exception as e:
    error_tracker.log_error(e, 'system_monitoring')
    raise
```

## Common Error Messages

### "Cannot connect to Discord"

**Error**: `aiohttp.client_exceptions.ClientConnectorError`

**Causes**:
- Network connectivity issues
- Firewall blocking connections
- Invalid proxy settings

**Solution**:
```bash
# Test connectivity
ping discord.com
curl -I https://discord.com/api/v10

# Check proxy settings
echo $HTTP_PROXY
echo $HTTPS_PROXY

# Bypass proxy if needed
unset HTTP_PROXY HTTPS_PROXY
```

### "Permission denied" errors

**Error**: `PermissionError: [Errno 13] Permission denied`

**Solution**:
```bash
# Check file ownership
ls -la logs/
ls -la config/

# Fix permissions
chmod 644 config/bot_config.json
chmod 755 logs/
chmod 666 logs/logivore.log

# For service users
sudo chown -R botuser:botuser /path/to/bot
```

### "Module not found" errors

**Error**: `ModuleNotFoundError: No module named 'discord'`

**Solution**:
```bash
# Check Python path
python -c "import sys; print('\n'.join(sys.path))"

# Verify virtual environment
which python
pip list | grep discord

# Reinstall in correct environment
source venv/bin/activate
pip install discord.py
```

### "JSON decode error"

**Error**: `json.decoder.JSONDecodeError`

**Solution**:
```bash
# Validate JSON files
python -m json.tool config/bot_config.json
python -m json.tool languages/en.json

# Common fixes:
# - Remove trailing commas
# - Fix quotes (use double quotes)
# - Escape backslashes
# - Check bracket/brace matching
```

## Recovery Procedures

### Emergency Bot Restart

```bash
#!/bin/bash
# emergency_restart.sh

echo "🚨 Emergency bot restart procedure"

# Kill existing bot processes
pkill -f "python.*main.py"
sleep 5

# Backup current logs
cp logs/logivore.log logs/logivore.log.backup.$(date +%Y%m%d_%H%M%S)

# Start bot with logging
nohup python main.py > logs/startup.log 2>&1 &

# Monitor startup
tail -f logs/startup.log
```

### Configuration Reset

```bash
#!/bin/bash
# reset_config.sh

echo "🔄 Resetting configuration to defaults"

# Backup current config
cp config/bot_config.json config/bot_config.json.backup.$(date +%Y%m%d_%H%M%S)

# Restore from template
cp config/bot_config.example.json config/bot_config.json

echo "✅ Configuration reset. Please update with your settings."
```

### Database Recovery

```bash
#!/bin/bash
# recover_database.sh

echo "🗄️ Database recovery procedure"

# Backup corrupted database
mv data/logivore.db data/logivore.db.corrupted.$(date +%Y%m%d_%H%M%S)

# Recreate database schema
python -c "
from utils.database import DatabaseManager
import asyncio

async def recreate_db():
    db = DatabaseManager(config_manager)
    await db.connect()
    await db.create_tables()
    await db.disconnect()
    print('✅ Database recreated')

asyncio.run(recreate_db())
"
```

### Full System Recovery

```bash
#!/bin/bash
# full_recovery.sh

echo "🆘 Full system recovery procedure"

# 1. Stop all bot processes
pkill -f "python.*main.py"

# 2. Backup current state
mkdir -p backups/$(date +%Y%m%d_%H%M%S)
cp -r config/ logs/ data/ backups/$(date +%Y%m%d_%H%M%S)/

# 3. Reset virtual environment
rm -rf venv
python -m venv venv
source venv/bin/activate

# 4. Reinstall dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 5. Reset configuration
cp config/bot_config.example.json config/bot_config.json

# 6. Clear logs
> logs/logivore.log

# 7. Start bot
python main.py

echo "✅ System recovery complete. Please reconfigure settings."
```

## Performance Monitoring

### System Resource Monitoring

```bash
#!/bin/bash
# monitor_bot_performance.sh

echo "📊 Bot Performance Monitor"

while true; do
    # Get bot process ID
    BOT_PID=$(pgrep -f "python.*main.py")

    if [ -n "$BOT_PID" ]; then
        # Memory usage
        MEM_USAGE=$(ps -o pid,pmem,rss -p $BOT_PID | tail -1)

        # CPU usage
        CPU_USAGE=$(ps -o pid,pcpu -p $BOT_PID | tail -1)

        # File descriptors
        FD_COUNT=$(lsof -p $BOT_PID 2>/dev/null | wc -l)

        echo "$(date): PID:$BOT_PID CPU:$CPU_USAGE MEM:$MEM_USAGE FD:$FD_COUNT"
    else
        echo "$(date): Bot process not running"
    fi

    sleep 60
done
```

### Log Analysis

```bash
#!/bin/bash
# analyze_logs.sh

echo "📋 Log Analysis"

LOG_FILE="logs/logivore.log"

if [ -f "$LOG_FILE" ]; then
    echo "Error summary:"
    grep -i error "$LOG_FILE" | tail -10

    echo -e "\nWarning summary:"
    grep -i warning "$LOG_FILE" | tail -10

    echo -e "\nCommand usage:"
    grep "Command executed" "$LOG_FILE" | cut -d'|' -f4 | sort | uniq -c | sort -nr

    echo -e "\nLast 10 log entries:"
    tail -10 "$LOG_FILE"
else
    echo "Log file not found: $LOG_FILE"
fi
```

## Getting Help

### Information to Gather

When seeking help, please gather this information:

```bash
#!/bin/bash
# gather_debug_info.sh

echo "🔍 Logivore Debug Information"
echo "================================"

echo "System Information:"
echo "OS: $(uname -a)"
echo "Python: $(python --version)"
echo "Pip: $(pip --version)"

echo -e "\nBot Information:"
echo "Git commit: $(git rev-parse HEAD 2>/dev/null || echo 'Not a git repository')"
echo "Git status: $(git status --porcelain 2>/dev/null || echo 'Not a git repository')"

echo -e "\nEnvironment:"
echo "Virtual env: $VIRTUAL_ENV"
echo "Python path: $(which python)"
echo "Working directory: $(pwd)"

echo -e "\nDependencies:"
pip list | grep -E "(discord|psutil|docker|aiohttp)"

echo -e "\nConfiguration check:"
ls -la config/ .env

echo -e "\nRecent errors:"
grep -i error logs/logivore.log | tail -5

echo -e "\nProcess status:"
ps aux | grep python | grep -v grep
```

### Support Channels

1. **Discord Community**: [Join our Discord](https://discord.gg/serelix)
   - Real-time support
   - Community discussions
   - Feature requests

2. **GitHub Issues**: [Report bugs](https://github.com/kaiyasi/Logivore/issues)
   - Bug reports
   - Feature requests
   - Technical discussions

3. **Email Support**: serelixstudio@gmail.com
   - Private support
   - Security issues
   - Business inquiries

### Before Asking for Help

1. **Check this troubleshooting guide**
2. **Search existing GitHub issues**
3. **Review recent logs**
4. **Try basic diagnostic steps**
5. **Gather debug information**

### Creating Effective Bug Reports

Include the following in your bug report:

1. **Environment details** (OS, Python version, bot version)
2. **Steps to reproduce** the issue
3. **Expected behavior** vs **actual behavior**
4. **Error messages** and **log excerpts**
5. **Configuration details** (remove sensitive information)
6. **Debug information** from the script above

### Example Bug Report Template

```markdown
**Environment:**
- OS: Ubuntu 20.04
- Python: 3.9.7
- Bot version: commit abc123
- Docker: 20.10.12

**Issue Description:**
Bot fails to start with "Permission denied" error when accessing /var/run/docker.sock

**Steps to Reproduce:**
1. Start bot with `python main.py`
2. Bot attempts to connect to Docker
3. Error occurs immediately

**Expected Behavior:**
Bot should connect to Docker successfully

**Actual Behavior:**
Bot crashes with permission error

**Error Messages:**
```
2024-01-15 10:30:25 | ERROR | docker_manager | Permission denied: /var/run/docker.sock
```

**Configuration:**
- DOCKER_ENABLED=true
- Running as user 'botuser'
- Docker service is running

**Additional Context:**
Issue started after updating Docker to version 20.10.12
```

---

This troubleshooting guide covers the most common issues and their solutions. If you encounter an issue not covered here, please refer to the support channels listed above or contribute to this guide by submitting a pull request.

Remember: most issues can be resolved by checking logs, verifying configuration, and ensuring proper permissions. Always backup your configuration before making changes.
