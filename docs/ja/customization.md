# カスタマイズガイド

言語: 日本語 | [English](../customization.md) | [繁體中文](../zh-tw/customization.md) | [简体中文](../zh-cn/customization.md)

本ガイドは、Logivore の機能を用途に合わせて拡張・調整する方法を解説します。

## 目次

- [アーキテクチャの理解](#アーキテクチャの理解)
- [設定のカスタマイズ](#設定のカスタマイズ)
- [カスタムコマンドの追加](#カスタムコマンドの追加)
- [カスタム Cog の作成](#カスタム-cog-の作成)
- [Embed と UI の調整](#embed-と-ui-の調整)
- [新しい言語の追加](#新しい言語の追加)
- [カスタム監視機能](#カスタム監視機能)
- [アラートシステムの拡張](#アラートシステムの拡張)
- [Docker 統合の拡張](#docker-統合の拡張)
- [SSL 管理の拡張](#ssl-管理の拡張)
- [データベース統合](#データベース統合)
- [Web ダッシュボードの作成](#web-ダッシュボードの作成)
- [プラグインシステムの開発](#プラグインシステムの開発)

## アーキテクチャの理解

`main.py`（エントリポイント）、`cogs/`（機能）、`utils/`（共通ユーティリティ）、`config/`（設定）、`languages/`（i18n）の役割と拡張ポイントを把握します。

## 設定のカスタマイズ

### `config/bot_config.json` に独自設定を追加

```json
{
  "custom_features": {
    "weather_monitoring": {
      "enabled": true,
      "api_key": "your_api_key",
      "locations": ["Tokyo", "Osaka"],
      "update_interval": 3600
    },
    "backup_system": {
      "enabled": true,
      "backup_path": "/backups",
      "schedule": "0 2 * * *",
      "retention_days": 30
    },
    "custom_alerts": {
      "webhook_url": "https://your-webhook-url.com",
      "email_notifications": true,
      "sms_alerts": false
    }
  }
}
```

### `.env` に環境変数を追加

```bash
# API キー
WEATHER_API_KEY=your_weather_api_key
BACKUP_API_TOKEN=your_backup_token
CUSTOM_WEBHOOK_URL=https://your-webhook.com

# パス
CUSTOM_LOG_PATH=/var/log/custom
BACKUP_STORAGE_PATH=/mnt/backups

# 機能トグル
ENABLE_WEATHER_MONITORING=true
ENABLE_CUSTOM_BACKUP=true
ENABLE_ADVANCED_LOGGING=false
```

### 設定・環境変数の参照

```python
class CustomFeatureCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config_manager

        self.weather_enabled = self.config.get('custom_features.weather_monitoring.enabled', False)
        self.backup_path = self.config.get('custom_features.backup_system.backup_path', '/backups')

        self.weather_api_key = os.getenv('WEATHER_API_KEY')
```

## カスタムコマンドの追加

### シンプルなコマンド

```python
import discord
from discord.ext import commands
from discord import app_commands
from utils.embed_formatter import EmbedFormatter

class CustomCommandsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config_manager
        self.i18n = bot.i18n

    @app_commands.command(name="serverinfo", description="サーバー情報を表示")
    async def server_info(self, interaction: discord.Interaction):
        guild = interaction.guild
        lang = self.config.get(f'guilds.{guild.id}.language', 'en')

        embed = EmbedFormatter.create_embed(
            title=f"📊 {guild.name} サーバー情報",
            command_name="serverinfo",
            lang=lang
        )
        embed.add_field(name="👥 メンバー", value=f"{guild.member_count:,}", inline=True)
        embed.add_field(name="📚 ロール", value=f"{len(guild.roles):,}", inline=True)
        embed.add_field(name="📢 チャンネル", value=f"{len(guild.channels):,}", inline=True)
        await interaction.response.send_message(embed=embed)
```

## カスタム Cog の作成

### バックグラウンドタスク付きテンプレート

```python
from discord.ext import commands, tasks

class SampleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config_manager
        self.enabled = self.config.get('custom_features.sample.enabled', False)
        if self.enabled:
            self.worker.start()

    def cog_unload(self):
        if hasattr(self, 'worker'):
            self.worker.cancel()

    @tasks.loop(seconds=300)
    async def worker(self):
        # 定期処理
        pass
```

## Embed と UI の調整

- `utils/embed_formatter.py` による共通スタイル
- 必要に応じてカスタムスタイル（例：`utils/custom_embed_styles.py`）

```python
from utils.custom_embed_styles import CustomEmbedStyles
embed = CustomEmbedStyles.create_status_embed(
    title="Service Status",
    status="online",
    details={"cpu": "18%", "mem": "42%"}
)
```
