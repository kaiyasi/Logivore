# Installation Guide

Languages: English | [繁體中文](zh-tw/installation.md) | [简体中文](zh-cn/installation.md) | [日本語](ja/installation.md) | [한국어](ko/installation.md) | [Deutsch](de/installation.md) | [Русский](ru/installation.md)

This guide will walk you through setting up Logivore from scratch, including all dependencies and configuration options.

## Table of Contents

- [Prerequisites](#prerequisites)
- [System Requirements](#system-requirements)
- [Discord Bot Setup](#discord-bot-setup)
- [Local Installation](#local-installation)
- [Docker Installation](#docker-installation)
- [Environment Configuration](#environment-configuration)
- [First Run](#first-run)
- [Troubleshooting](#troubleshooting)

## Prerequisites

Before installing Logivore, ensure you have the following:

### Required Software
- **Python 3.8 or higher** - [Download Python](https://python.org/downloads/)
- **Git** - [Install Git](https://git-scm.com/downloads)
- **pip** (usually comes with Python)

### Optional (for enhanced features)
- **Docker** - [Install Docker](https://docs.docker.com/get-docker/)
- **Docker Compose** - [Install Docker Compose](https://docs.docker.com/compose/install/)
- **systemd** (Linux) - For service management
- **smartmontools** (Linux) - For disk health monitoring

## System Requirements

### Minimum Requirements
- **RAM**: 512MB available memory
- **Storage**: 1GB free disk space
- **CPU**: Single core (dual core recommended)
- **Network**: Stable internet connection

### Recommended Requirements
- **RAM**: 1GB+ available memory
- **Storage**: 2GB+ free disk space
- **CPU**: Dual core or higher
- **OS**: Linux (Ubuntu 20.04+), Windows 10+, or macOS 10.15+

## Discord Bot Setup

### Step 1: Create Discord Application

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click **"New Application"**
3. Enter your bot name (e.g., "Logivore")
4. Click **"Create"**

### Step 2: Configure Bot Settings

1. Navigate to the **"Bot"** section
2. Click **"Add Bot"**
3. Under **"Privileged Gateway Intents"**, enable:
   - ✅ **Server Members Intent**
   - ✅ **Message Content Intent**
4. Click **"Reset Token"** to generate your bot token
5. **Copy and save the token immediately** (you won't see it again)

### Step 3: Set Bot Permissions

1. Go to **"OAuth2" → "URL Generator"**
2. Under **"Scopes"**, select:
   - ✅ `bot`
   - ✅ `applications.commands`
3. Under **"Bot Permissions"**, select:
   - ✅ `Send Messages`
   - ✅ `Embed Links`
   - ✅ `Use Slash Commands`
   - ✅ `Read Message History`
   - ✅ `View Channels`

### Step 4: Invite Bot to Server

1. Copy the generated URL from the bottom of the page
2. Open the URL in your browser
3. Select your Discord server
4. Click **"Authorize"**

## Local Installation

### Method 1: Direct Installation

```bash
# Clone the repository
git clone https://github.com/kaiyasi/Logivore.git
cd Logivore

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Method 2: Development Installation

```bash
# Clone for development
git clone https://github.com/kaiyasi/Logivore.git
cd Logivore

# Install development dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # If available

# Install pre-commit hooks (optional)
pre-commit install
```

## Docker Installation

### Method 1: Docker Compose (Recommended)

1. **Create docker-compose.yml**:
```yaml
version: '3.8'

services:
  logivore:
    build: .
    container_name: logivore
    restart: unless-stopped
    volumes:
      - ./config:/app/config
      - ./logs:/app/logs
    environment:
      - DISCORD_TOKEN=${DISCORD_TOKEN}
      - OWNER_ID=${OWNER_ID}
    networks:
      - logivore-network

networks:
  logivore-network:
    driver: bridge
```

2. **Run with Docker Compose**:
```bash
# Start the bot
docker compose up -d

# View logs
docker compose logs -f logivore

# Stop the bot
docker compose down
```

### Method 2: Direct Docker

```bash
# Build the image
docker build -t logivore .

# Run the container
docker run -d \
  --name logivore \
  --restart unless-stopped \
  -v $(pwd)/config:/app/config \
  -v $(pwd)/logs:/app/logs \
  -e DISCORD_TOKEN=your_token_here \
  -e OWNER_ID=your_user_id \
  logivore
```

## Environment Configuration

### Step 1: Create Environment File

```bash
# Copy the example environment file
cp .env.example .env
```

### Step 2: Configure .env File

Edit `.env` with your favorite text editor:

```bash
# Discord Configuration
DISCORD_TOKEN=your_bot_token_here
OWNER_ID=your_discord_user_id

# Bot Configuration
DEFAULT_LANGUAGE=en
UPDATE_INTERVAL=10
ALERT_INTERVAL=60

# System Configuration
MONITORED_DISKS=/,/mnt/data
MAX_UPTIME_DAYS=30

# Docker Configuration (if using Docker)
DOCKER_HOST=unix:///var/run/docker.sock

# SSL Configuration (optional)
NPM_CONTAINER=nginx-proxy-manager
SSL_CERT_PATH=/etc/letsencrypt/live

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=logs/logivore.log
```

### Step 3: Get Your Discord User ID

1. Enable Developer Mode in Discord:
   - User Settings → Advanced → Developer Mode ✅
2. Right-click your username and select "Copy ID"
3. Paste this ID as `OWNER_ID` in your `.env` file

## First Run

### Verify Installation

```bash
# Check Python version
python --version  # Should be 3.8+

# Check dependencies
pip list | grep discord.py  # Should show discord.py version

# Validate configuration
python -c "import os; print('✅ Python working')"
```

### Start the Bot

```bash
# Method 1: Direct execution
python main.py

# Method 2: Using module
python main.py

# Method 3: With logging
python main.py 2>&1 | tee logs/startup.log
```

### Verify Bot is Working

1. Check console output for:
   ```
   ✅ Bot is ready!
   ✅ Logged in as: YourBotName#1234
   ✅ Connected to X guilds
   ```

2. In Discord, test basic commands:
   ```
   /help
   /config show
   /monitor
   ```

## Service Installation (Linux)

### Create systemd Service

1. **Create service file**:
```bash
sudo nano /etc/systemd/system/logivore.service
```

2. **Add service configuration**:
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

3. **Enable and start service**:
```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service
sudo systemctl enable logivore

# Start service
sudo systemctl start logivore

# Check status
sudo systemctl status logivore
```

## Troubleshooting

### Common Issues

#### Issue: "discord.py not found"
**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

#### Issue: "Invalid token"
**Solutions**:
1. Verify token in `.env` file
2. Regenerate token in Discord Developer Portal
3. Check for extra spaces or quotes

#### Issue: "Bot not responding to commands"
**Solutions**:
1. Verify bot has proper permissions
2. Check if bot is online in Discord
3. Try re-inviting bot with updated permissions

#### Issue: "Permission denied" (Linux)
**Solutions**:
```bash
# Fix file permissions
chmod +x main.py
chmod 644 .env

# Run with proper user
sudo chown -R $USER:$USER .
```

#### Issue: Docker container exits immediately
**Solutions**:
1. Check logs: `docker logs logivore`
2. Verify environment variables
3. Check if token is properly set

### Debug Mode

Enable debug logging by modifying `.env`:
```bash
LOG_LEVEL=DEBUG
```

Or run with debug flags:
```bash
python main.py --debug
```

### Getting Help

If you encounter issues:

1. **Check logs**: `tail -f logs/logivore.log`
2. **Discord community**: [Join our Discord](https://discord.gg/serelix)
3. **GitHub Issues**: [Report bugs](https://github.com/kaiyasi/Logivore/issues)
4. **Documentation**: Read other guides in `/docs`

### Performance Optimization

For better performance:

1. **Use SSD storage** for faster file operations
2. **Increase RAM** if monitoring many servers
3. **Use Docker** for containerized deployment
4. **Enable caching** in configuration
5. **Adjust update intervals** based on needs

## Next Steps

After successful installation:

1. 📖 Read the [Configuration Guide](configuration.md)
2. 🎯 Check [Command Reference](commands.md)
3. 🚨 Set up [Alerts](alerts.md)
4. 🐳 Configure [Docker Integration](docker.md)
5. 🔧 Explore [Customization Options](customization.md)

---

**Need help?** Join our [Discord community](https://discord.gg/serelix) or check [GitHub Issues](https://github.com/kaiyasi/Logivore/issues).
