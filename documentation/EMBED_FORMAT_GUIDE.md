# Embed格式化指南

語言：繁體中文（本頁） | [English](EMBED_FORMAT_GUIDE.md) | [简体中文](zh-cn/EMBED_FORMAT_GUIDE.md)

## ✅ 已完成的更新

### **統一的Embed格式**
所有Serelix Bot的embed現在都使用統一的格式，包含：
- **作者信息**: 顯示執行的命令功能
- **時間戳**: 自動添加執行時間
- **頁尾**: "Powered by Serelix Studio" 品牌標識

### **支援的格式類型**

#### **標準Embed**
```python
from utils.embed_formatter import create_standard_embed

embed = create_standard_embed(
    title="標題",
    description="描述",
    command_name="monitor",  # 會顯示為 "Command: monitor"
    bot=self.bot
)
```

#### **成功Embed (綠色)**
```python
from utils.embed_formatter import EmbedFormatter

embed = EmbedFormatter.success_embed(
    title="✅ 操作成功",
    description="命令執行完成",
    command_name="ssl renew",
    lang="zh"
)
```

#### **錯誤Embed (紅色)**
```python
embed = EmbedFormatter.error_embed(
    title="❌ 操作失敗",
    description="發生錯誤",
    command_name="docker start",
    lang="zh"
)
```

#### **警告Embed (橙色)**
```python
embed = EmbedFormatter.warning_embed(
    title="⚠️ 注意",
    description="需要注意的訊息",
    command_name="reboot now",
    lang="zh"
)
```

#### **資訊Embed (藍色)**
```python
embed = EmbedFormatter.info_embed(
    title="ℹ️ 資訊",
    description="一般資訊",
    command_name="help",
    lang="zh"
)
```

### **多語言支援**

作者和頁尾會根據語言自動調整：

**英文 (en)**:
- Author: "Command: monitor"
- Footer: "Powered by Serelix Studio"

**繁體中文 (zh/zh-tw)**:
- Author: "指令功能：monitor"
- Footer: "由 Serelix Studio 提供支援"

**簡體中文 (zh-cn)**:
- Author: "指令功能：monitor"
- Footer: "由 Serelix Studio 提供支持"

**韓文 (ko)**:
- Author: "명령 기능: monitor"
- Footer: "Serelix Studio에서 제공"

**日文 (ja)**:
- Author: "コマンド機能: monitor"
- Footer: "Serelix Studio 提供"

**德文 (de)**:
- Author: "Befehl: monitor"
- Footer: "Powered by Serelix Studio"

**俄文 (ru)**:
- Author: "Команда: monitor"
- Footer: "Создано Serelix Studio"

### **自定義頁尾**

某些特殊情況下需要自定義頁尾（如monitor的自動刷新信息）：

```python
embed = create_standard_embed(
    title="系統狀態",
    command_name="monitor",
    bot=self.bot
)

# 覆蓋頁尾
lang = self.bot.config.get("language", "en")
if lang in ['zh', 'zh-tw']:
    footer_text = f"由 Serelix Studio 提供支援 • 每10秒自動刷新"
elif lang == 'zh-cn':
    footer_text = f"由 Serelix Studio 提供支持 • 每10秒自动刷新"
elif lang == 'ko':
    footer_text = f"Serelix Studio에서 제공 • 10초마다 자동 새로고침"
elif lang == 'ja':
    footer_text = f"Serelix Studio 提供 • 10秒ごとに自動更新"
elif lang == 'de':
    footer_text = f"Powered by Serelix Studio • Automatische Aktualisierung alle 10s"
elif lang == 'ru':
    footer_text = f"Создано Serelix Studio • Автообновление каждые 10с"
else:
    footer_text = f"Powered by Serelix Studio • Auto-refreshing every 10s"
embed.set_footer(text=footer_text)
```

### **已更新的模組**

✅ **system_monitoring.py** - 系統監控面板 (所有embed已標準化)
✅ **help_system.py** - 幫助系統 (所有embed已標準化)
✅ **ssl_management.py** - SSL證書管理 (所有embed已標準化)
✅ **alerting.py** - 警報系統 (所有embed已標準化)
✅ **docker_management.py** - Docker管理 (所有embed已標準化)
✅ **config_management.py** - 配置管理 (所有embed已標準化)
✅ **bot_management.py** - 機器人管理 (所有embed已標準化)
✅ **system_reboot.py** - 系統重啟 (所有embed已標準化)
✅ **service_recovery.py** - 服務恢復 (所有embed已標準化)

🎉 **所有模組都已完成標準化更新！**

### **支援的語言**

Serelix Bot 現在支援以下8種語言：

- 🇺🇸 **English** (`en`) - 英文
- 🇹🇼 **繁體中文** (`zh`/`zh-tw`) - Traditional Chinese
- 🇨🇳 **简体中文** (`zh-cn`) - Simplified Chinese
- 🇰🇷 **한국어** (`ko`) - Korean
- 🇯🇵 **日本語** (`ja`) - Japanese
- 🇩🇪 **Deutsch** (`de`) - German
- 🇷🇺 **Русский** (`ru`) - Russian

使用 `/config language` 指令可以隨時切換語言，所有embed的作者欄位和頁尾都會自動適應所選語言。

### **效果預覽**

現在所有的Discord embed都會顯示：

```
👤 Command: ssl list                    [作者欄位]
🔐 SSL證書列表                          [標題]
共找到3個證書...                        [內容]

📋 Certificate 1: ✅ npm.gonets.top
📋 Certificate 2: 🟡 example.com
📋 Certificate 3: 🟢 test.domain

Powered by Serelix Studio • 2024-09-28 19:30:15  [頁尾 + 時間戳]
```

這樣提供了統一、專業的用戶體驗！
