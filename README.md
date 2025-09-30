
Languages: English | [繁體中文](documentation/zh-tw/README.md) | [简体中文](documentation/zh-cn/README.md) | [日本語](documentation/ja/README.md) | [한국어](documentation/ko/README.md) | [Deutsch](documentation/de/README.md) | [Русский](documentation/ru/README.md)

<div align="center">

**Advanced System Monitoring & Management Discord Bot**

*Comprehensive real-time monitoring, intelligent alerts, and automated system management*

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Discord.py](https://img.shields.io/badge/discord.py-2.0+-green.svg)](https://discordpy.readthedocs.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Made by](https://img.shields.io/badge/Made%20by-Serelix%20Studio-purple.svg)](https://serelix.xyz)

[🚀 Quick Start](#-quick-start) • [✨ Features](#-features) • [🌍 Languages](#-supported-languages) • [📖 Documentation](#-documentation) • [💬 Support](#-support)

</div>

## 📋 Overview

Logivore is a powerful Discord bot designed for comprehensive system monitoring and management. Built with advanced automation capabilities, it provides real-time insights into your server infrastructure while maintaining enterprise-grade reliability and security.

### 🎯 Key Capabilities

- **🔍 Real-time System Monitoring** - CPU, Memory, Disk, Network statistics
- **🚨 Intelligent Alert System** - Proactive notifications for system issues
- **🐳 Docker Management** - Complete container lifecycle management
- **🔄 Service Recovery** - Automatic service restoration after system events
- **⚡ SSL Certificate Management** - Automated certificate monitoring and renewal
- **🌐 Multi-language Support** - 8 languages with localized interfaces

## ✨ Features

### 🖥️ System Monitoring
```
Real-time dashboard with live updates
Network port monitoring
Disk health checking (SMART)
Process management and monitoring
```

### 🚨 Alert Management
```
CPU/Memory/Disk usage alerts
Process watchdog monitoring
Custom threshold configuration
Multi-channel notification support
```

### 🐳 Docker Integration
```
Container status monitoring
Start/Stop/Restart operations
Resource usage tracking
Log management
```

### 🛡️ System Management
```
Scheduled system reboots
Service recovery automation
SSL certificate monitoring
Nginx Proxy Manager integration
```

## 🌍 Supported Languages

<div align="center">

| Language | Code | Status |
|----------|------|--------|
| 🇺🇸 English | `en` | ✅ Complete |
| 🇹🇼 繁體中文 | `zh`/`zh-tw` | ✅ Complete |
| 🇨🇳 简体中文 | `zh-cn` | ✅ Complete |
| 🇰🇷 한국어 | `ko` | ✅ Complete |
| 🇯🇵 日本語 | `ja` | ✅ Complete |
| 🇩🇪 Deutsch | `de` | ✅ Complete |
| 🇷🇺 Русский | `ru` | ✅ Complete |

</div>

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Discord Bot Token
- Linux/Windows/macOS system

### Installation
```bash
# Clone the repository
git clone https://github.com/kaiyasi/Logivore.git
cd Logivore

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your Discord bot token and settings

# Run the bot
python main.py
```

### Docker Deployment (Optional)
```bash
cd deploy/docker
docker compose up -d --build
```

## 🏗️ Architecture

### 🔧 Technology Stack
- **Backend Framework**: Python 3.8+ with discord.py 2.0+
- **System Monitoring**: psutil, subprocess integration
- **Container Management**: Docker API integration
- **SSL Management**: Let's Encrypt with Nginx Proxy Manager
- **Internationalization**: JSON-based multi-language system
- **Configuration**: JSON with hot-reload capabilities

### 📦 Core Modules
```
├── 🔍 System Monitoring     - Real-time system statistics
├── 🚨 Alert System         - Proactive monitoring alerts
├── 🐳 Docker Management    - Container lifecycle control
├── 🔄 Service Recovery     - Automated service restoration
├── 🛡️ SSL Management       - Certificate monitoring & renewal
├── ⚙️ Configuration        - Dynamic settings management
├── 🤖 Bot Management       - Administrative controls
└── 📚 Help System          - Interactive documentation
```

## 📖 Documentation

- **[Installation Guide](documentation/installation.md)** - Step-by-step setup instructions
- **[Configuration Reference](documentation/configuration.md)** - Complete settings documentation
- **[Command Reference](documentation/commands.md)** - All available bot commands
- **[API Documentation](documentation/api.md)** - Integration and extension guides
- **[Troubleshooting](documentation/troubleshooting.md)** - Common issues and solutions
 - Additional Guides:
  - **[Embed Formatting Guide](documentation/EMBED_FORMAT_GUIDE.md)**
  - **[Management Guide](documentation/MANAGEMENT_GUIDE.md)**
  - **[Setup: Auto-Recovery After Reboot](documentation/SETUP-RECOVERY.md)**

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Deployment

- System (Recommended):
  - Use the files under `deploy/system/` and `systemd-examples/` to run Logivore as a systemd service for full visibility and reliability.
  - See `SETUP-RECOVERY.md` for boot recovery automation.
- Docker (Optional):
  - See `deploy/docker/` – Running in Docker may limit host-level visibility (ports, metrics) and disable host control operations. Review the warning and use host/pid modes if needed.

### Development Setup
```bash
# Clone and setup development environment
git clone https://github.com/kaiyasi/Logivore.git
cd Logivore

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 💬 Support

<div align="center">

### 🔗 Community & Support

[![GitHub Issues](https://img.shields.io/badge/GitHub-Issues-red.svg)](https://github.com/kaiyasi/Logivore/issues)
[![GitHub Discussions](https://img.shields.io/badge/GitHub-Discussions-blue.svg)](https://github.com/kaiyasi/Logivore/discussions)
[![Discord](https://img.shields.io/badge/Discord-Community-purple.svg)](https://discord.gg/serelix)
[![Email](https://img.shields.io/badge/Email-Support-green.svg)](mailto:serelixstudio@gmail.com)

</div>

### 📞 Contact Information

- **Official Website**: [https://serelix.xyz](https://serelix.xyz)
- **GitHub Repository**: [https://github.com/kaiyasi/Logivore](https://github.com/kaiyasi/Logivore)
- **Email**: serelixstudio@gmail.com
- **Instagram**: [@serelix.studio](https://instagram.com/serelix.studio)

---

<div align="center">

**Made with ❤️ by [Serelix Studio](https://serelix.xyz)**

*Empowering server management through intelligent automation*

</div>
