# 🤖 Logivore

語言：繁體中文 | [English](README.md) | [简体中文](README.zh-cn.md)

<div align="center">

**進階系統監控與管理 Discord 機器人**

*全面的即時監控、智慧警報和自動化系統管理*

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Discord.py](https://img.shields.io/badge/discord.py-2.0+-green.svg)](https://discordpy.readthedocs.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Made by](https://img.shields.io/badge/Made%20by-Serelix%20Studio-purple.svg)](https://serelix.xyz)

[🚀 快速開始](#-快速開始) • [✨ 功能](#-功能) • [🌍 語言](#-支援語言) • [📖 文件](#-文件) • [💬 支援](#-支援)

</div>

## 📋 概述

Logivore 是一個專為全面系統監控和管理而設計的強大 Discord 機器人。具備進階的自動化功能，為您的伺服器基礎設施提供即時洞察，同時保持企業級的可靠性和安全性。

### 🎯 核心能力

- **🔍 即時系統監控** - CPU、記憶體、磁碟、網路統計
- **🚨 智慧警報系統** - 主動的系統問題通知
- **🐳 Docker 管理** - 完整的容器生命週期管理
- **🔄 服務復原** - 系統事件後的自動服務復原
- **⚡ SSL 憑證管理** - 自動化憑證監控和續期
- **🌐 多語言支援** - 8種語言的本地化介面

## ✨ 功能

### 🖥️ 系統監控
```
即時更新的儀表板
網路埠口監控
磁碟健康檢查 (SMART)
進程管理和監控
```

### 🚨 警報管理
```
CPU/記憶體/磁碟使用率警報
進程監視監控
自訂閾值設定
多頻道通知支援
```

### 🐳 Docker 整合
```
容器狀態監控
啟動/停止/重新啟動操作
資源使用追蹤
日誌管理
```

### 🛡️ 系統管理
```
排程系統重新啟動
服務復原自動化
SSL憑證監控
Nginx Proxy Manager 整合
```

## 🌍 支援語言

<div align="center">

| 語言 | 代碼 | 狀態 |
|----------|------|--------|
| 🇺🇸 English | `en` | ✅ 完成 |
| 🇹🇼 繁體中文 | `zh`/`zh-tw` | ✅ 完成 |
| 🇨🇳 简体中文 | `zh-cn` | ✅ 完成 |
| 🇰🇷 한국어 | `ko` | ✅ 完成 |
| 🇯🇵 日本語 | `ja` | ✅ 完成 |
| 🇩🇪 Deutsch | `de` | ✅ 完成 |
| 🇷🇺 Русский | `ru` | ✅ 完成 |

</div>

## 🚀 快速開始

### 先決條件
- Python 3.8+
- Discord Bot Token
- Linux/Windows/macOS 系統

### 安裝
```bash
# 複製儲存庫
git clone https://github.com/kaiyasi/Logivore.git
cd Logivore

# 安裝相依性
pip install -r requirements.txt

# 設定環境
cp .env.example .env
# 使用您的 Discord 機器人權杖和設定編輯 .env

# 執行機器人
python main.py
```

### Docker 部署（可選）
```bash
cd deploy/docker
docker compose up -d --build
```

### 部署建議

- System（推薦）：
  - 透過 `deploy/system/` 與 `systemd-examples/`，以 systemd 常駐並取得完整的主機可視性與穩定度。
  - 另見 `SETUP-RECOVERY.md` 了解開機恢復流程。
- Docker（可選）：
  - 見 `deploy/docker/`。容器化可能影響主機層級可視性（埠口、指標）與主機控制能力；若需要更準確的監控，請使用 host/pid 模式並審視安全性設定。

## 🏗️ 架構

### 🔧 技術堆疊
- **後端框架**: Python 3.8+ 配合 discord.py 2.0+
- **系統監控**: psutil, subprocess 整合
- **容器管理**: Docker API 整合
- **SSL 管理**: Let's Encrypt 配合 Nginx Proxy Manager
- **國際化**: 基於 JSON 的多語言系統
- **設定**: 支援熱重載的 JSON

### 📦 核心模組
```
├── 🔍 系統監控         - 即時系統統計
├── 🚨 警報系統         - 主動監控警報
├── 🐳 Docker 管理     - 容器生命週期控制
├── 🔄 服務復原         - 自動服務復原
├── 🛡️ SSL 管理        - 憑證監控和續期
├── ⚙️ 設定            - 動態設定管理
├── 🤖 機器人管理       - 管理控制
└── 📚 說明系統         - 互動式文件
```

## 📖 文件

- **[安裝指南](../installation.md)** - 分步設定說明
- **[設定參考](../configuration.md)** - 完整的設定文件
- **[指令參考](../commands.md)** - 所有可用的機器人指令
- **[API 文件](../api.md)** - 整合和擴充指南
- **[疑難排解](../troubleshooting.md)** - 常見問題和解決方案
 - 其他指南：
   - **[Embed 格式化指南](../EMBED_FORMAT_GUIDE.md)**
   - **[管理工具指南](../MANAGEMENT_GUIDE.md)**
   - **[重啟後自動恢復設定](../SETUP-RECOVERY.md)**

## 🤝 貢獻

我們歡迎貢獻！請查看我們的[貢獻指南](CONTRIBUTING.md)了解詳情。

### 開發環境設定
```bash
# 複製並設定開發環境
git clone https://github.com/kaiyasi/Logivore.git
cd Logivore

# 安裝開發相依性
pip install -r requirements-dev.txt

# 執行測試
python -m pytest tests/
```

## 📝 授權

此專案根據 MIT 授權條款授權 - 詳情請查看 [LICENSE](LICENSE) 檔案。

## 💬 支援

<div align="center">

### 🔗 社群與支援

[![GitHub Issues](https://img.shields.io/badge/GitHub-Issues-red.svg)](https://github.com/kaiyasi/Logivore/issues)
[![GitHub Discussions](https://img.shields.io/badge/GitHub-Discussions-blue.svg)](https://github.com/kaiyasi/Logivore/discussions)
[![Discord](https://img.shields.io/badge/Discord-Community-purple.svg)](https://discord.gg/serelix)
[![Email](https://img.shields.io/badge/Email-Support-green.svg)](mailto:serelixstudio@gmail.com)

</div>

### 📞 聯絡資訊

- **官方網站**: [https://serelix.xyz](https://serelix.xyz)
- **GitHub 儲存庫**: [https://github.com/kaiyasi/Logivore](https://github.com/kaiyasi/Logivore)
- **電子郵件**: serelixstudio@gmail.com
- **Instagram**: [@serelix.studio](https://instagram.com/serelix.studio)

---

<div align="center">

**由 ❤️ 製作 [Serelix Studio](https://serelix.xyz)**

*透過智慧自動化賦能伺服器管理*

</div>
