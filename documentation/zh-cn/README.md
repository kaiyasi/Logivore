# 🤖 Logivore

语言：简体中文 | [English](README.md) | [繁體中文](README.zh-tw.md)

<div align="center">

**高级系统监控与管理 Discord 机器人**

*全面的实时监控、智能警报和自动化系统管理*

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Discord.py](https://img.shields.io/badge/discord.py-2.0+-green.svg)](https://discordpy.readthedocs.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Made by](https://img.shields.io/badge/Made%20by-Serelix%20Studio-purple.svg)](https://serelix.xyz)

[🚀 快速开始](#-快速开始) • [✨ 功能](#-功能) • [🌍 语言](#-支持语言) • [📖 文档](#-文档) • [💬 支持](#-支持)

</div>

## 📋 概述

Logivore 是一个专为全面系统监控和管理而设计的强大 Discord 机器人。具备先进的自动化功能，为您的服务器基础设施提供实时洞察，同时保持企业级的可靠性和安全性。

### 🎯 核心能力

- **🔍 实时系统监控** - CPU、内存、磁盘、网络统计
- **🚨 智能警报系统** - 主动的系统问题通知
- **🐳 Docker 管理** - 完整的容器生命周期管理
- **🔄 服务恢复** - 系统事件后的自动服务恢复
- **⚡ SSL 证书管理** - 自动化证书监控和续期
- **🌐 多语言支持** - 8种语言的本地化界面

## ✨ 功能

### 🖥️ 系统监控
```
实时更新的仪表板
网络端口监控
磁盘健康检查 (SMART)
进程管理和监控
```

### 🚨 警报管理
```
CPU/内存/磁盘使用率警报
进程监视监控
自定义阈值配置
多频道通知支持
```

### 🐳 Docker 集成
```
容器状态监控
启动/停止/重启操作
资源使用跟踪
日志管理
```

### 🛡️ 系统管理
```
计划系统重启
服务恢复自动化
SSL证书监控
Nginx Proxy Manager 集成
```

## 🌍 支持语言

<div align="center">

| 语言 | 代码 | 状态 |
|----------|------|--------|
| 🇺🇸 English | `en` | ✅ 完成 |
| 🇹🇼 繁體中文 | `zh`/`zh-tw` | ✅ 完成 |
| 🇨🇳 简体中文 | `zh-cn` | ✅ 完成 |
| 🇰🇷 한국어 | `ko` | ✅ 完成 |
| 🇯🇵 日本語 | `ja` | ✅ 完成 |
| 🇩🇪 Deutsch | `de` | ✅ 完成 |
| 🇷🇺 Русский | `ru` | ✅ 完成 |

</div>

## 🚀 快速开始

### 先决条件
- Python 3.8+
- Discord Bot Token
- Linux/Windows/macOS 系统

### 安装
```bash
# 克隆仓库
git clone https://github.com/kaiyasi/Logivore.git
cd Logivore

# 安装依赖
pip install -r requirements.txt

# 配置环境
cp .env.example .env
# 使用您的 Discord 机器人令牌和设置编辑 .env

# 运行机器人
python main.py
```

### Docker 部署（可选）
```bash
cd deploy/docker
docker compose up -d --build
```

### 部署建议

- System（推荐）：
  - 使用 `deploy/system/` 和 `systemd-examples/`，以 systemd 方式常驻，获得完整主机可视性与更高可靠性。
  - 参见 `SETUP-RECOVERY.md` 了解开机恢复流程。
- Docker（可选）：
  - 见 `deploy/docker/`。容器化可能影响主机层级可视性（端口、指标）与主机控制能力；如需更准确监控，请使用 host/pid 模式并审视安全设置。

## 🏗️ 架构

### 🔧 技术栈
- **后端框架**: Python 3.8+ 配合 discord.py 2.0+
- **系统监控**: psutil, subprocess 集成
- **容器管理**: Docker API 集成
- **SSL 管理**: Let's Encrypt 配合 Nginx Proxy Manager
- **国际化**: 基于 JSON 的多语言系统
- **配置**: 支持热重载的 JSON

### 📦 核心模块
```
├── 🔍 系统监控         - 实时系统统计
├── 🚨 警报系统         - 主动监控警报
├── 🐳 Docker 管理     - 容器生命周期控制
├── 🔄 服务恢复         - 自动服务恢复
├── 🛡️ SSL 管理        - 证书监控和续期
├── ⚙️ 配置            - 动态设置管理
├── 🤖 机器人管理       - 管理控制
└── 📚 帮助系统         - 交互式文档
```

## 📖 文档

- **[安装指南](../installation.md)** - 分步设置说明
- **[配置参考](../configuration.md)** - 完整的设置文档
- **[命令参考](../commands.md)** - 所有可用的机器人命令
- **[API 文档](../api.md)** - 集成和扩展指南
- **[故障排除](../troubleshooting.md)** - 常见问题和解决方案
 - 附加指南：
   - **[Embed 格式化指南](EMBED_FORMAT_GUIDE.md)**
   - **[管理工具指南](MANAGEMENT_GUIDE.md)**
   - **[重启后自动恢复设置](SETUP-RECOVERY.md)**

## 🤝 贡献

我们欢迎贡献！请查看我们的[贡献指南](CONTRIBUTING.md)了解详情。

### 开发环境设置
```bash
# 克隆并设置开发环境
git clone https://github.com/kaiyasi/Logivore.git
cd Logivore

# 安装开发依赖
pip install -r requirements-dev.txt

# 运行测试
python -m pytest tests/
```

## 📝 许可证

此项目根据 MIT 许可证授权 - 详情请查看 [LICENSE](LICENSE) 文件。

## 💬 支持

<div align="center">

### 🔗 社区与支持

[![GitHub Issues](https://img.shields.io/badge/GitHub-Issues-red.svg)](https://github.com/kaiyasi/Logivore/issues)
[![GitHub Discussions](https://img.shields.io/badge/GitHub-Discussions-blue.svg)](https://github.com/kaiyasi/Logivore/discussions)
[![Discord](https://img.shields.io/badge/Discord-Community-purple.svg)](https://discord.gg/serelix)
[![Email](https://img.shields.io/badge/Email-Support-green.svg)](mailto:serelixstudio@gmail.com)

</div>

### 📞 联系信息

- **官方网站**: [https://serelix.xyz](https://serelix.xyz)
- **GitHub 仓库**: [https://github.com/kaiyasi/Logivore](https://github.com/kaiyasi/Logivore)
- **邮箱**: serelixstudio@gmail.com
- **Instagram**: [@serelix.studio](https://instagram.com/serelix.studio)

---

<div align="center">

**由 ❤️ 制作 [Serelix Studio](https://serelix.xyz)**

*通过智能自动化赋能服务器管理*

</div>
