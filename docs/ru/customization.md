# Руководство по кастомизации

Языки: Русский | [English](../customization.md) | [繁體中文](../zh-tw/customization.md) | [简体中文](../zh-cn/customization.md)

Это руководство объясняет, как адаптировать Logivore под ваши задачи: добавить новые
возможности, модифицировать существующие и расширять потенциал бота.

## Содержание

- [Понимание архитектуры](#понимание-архитектуры)
- [Настройка конфигурации](#настройка-конфигурации)
- [Добавление пользовательских команд](#добавление-пользовательских-команд)
- [Создание собственных Cog](#создание-собственных-cog)
- [Настройка Embed и UI](#настройка-embed-и-ui)
- [Добавление новых языков](#добавление-новых-языков)
- [Пользовательские функции мониторинга](#пользовательские-функции-мониторинга)
- [Кастомизация системы оповещений](#кастомизация-системы-оповещений)
- [Расширение интеграции Docker](#расширение-интеграции-docker)
- [Расширения управления SSL](#расширения-управления-ssl)
- [Интеграция базы данных](#интеграция-базы-данных)
- [Создание веб‑дашборда](#создание-вебдашборда)
- [Разработка плагин‑системы](#разработка-плагинсистемы)

## Понимание архитектуры

Роли `main.py` (входная точка), `cogs/` (функции), `utils/` (общие утилиты),
`config/` (настройки), `languages/` (i18n) и точки расширения.

## Настройка конфигурации

### Пользовательские секции в `config/bot_config.json`

```json
{
  "custom_features": {
    "weather_monitoring": {
      "enabled": true,
      "api_key": "your_api_key",
      "locations": ["Moscow", "Saint Petersburg"],
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

### Переменные окружения в `.env`

```bash
# API‑ключи
WEATHER_API_KEY=your_weather_api_key
BACKUP_API_TOKEN=your_backup_token
CUSTOM_WEBHOOK_URL=https://your-webhook.com

# Пути
CUSTOM_LOG_PATH=/var/log/custom
BACKUP_STORAGE_PATH=/mnt/backups

# Флаги функций
ENABLE_WEATHER_MONITORING=true
ENABLE_CUSTOM_BACKUP=true
ENABLE_ADVANCED_LOGGING=false
```

### Доступ к настройкам и окружению

```python
class CustomFeatureCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config_manager

        self.weather_enabled = self.config.get('custom_features.weather_monitoring.enabled', False)
        self.backup_path = self.config.get('custom_features.backup_system.backup_path', '/backups')

        self.weather_api_key = os.getenv('WEATHER_API_KEY')
```

## Добавление пользовательских команд

### Простой пример

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

    @app_commands.command(name="serverinfo", description="Показать информацию о сервере")
    async def server_info(self, interaction: discord.Interaction):
        guild = interaction.guild
        lang = self.config.get(f'guilds.{guild.id}.language', 'en')

        embed = EmbedFormatter.create_embed(
            title=f"📊 {guild.name} — информация",
            command_name="serverinfo",
            lang=lang
        )
        embed.add_field(name="👥 Участники", value=f"{guild.member_count:,}", inline=True)
        embed.add_field(name="📚 Роли", value=f"{len(guild.roles):,}", inline=True)
        embed.add_field(name="📢 Каналы", value=f"{len(guild.channels):,}", inline=True)
        await interaction.response.send_message(embed=embed)
```

## Создание собственных Cog

### Шаблон с фоновыми задачами

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
        # Периодическая задача
        pass
```

## Настройка Embed и UI

- Единый стиль через `utils/embed_formatter.py`
- При необходимости — собственные стили, например `utils/custom_embed_styles.py`

```python
from utils.custom_embed_styles import CustomEmbedStyles
embed = CustomEmbedStyles.create_status_embed(
    title="Service Status",
    status="online",
    details={"cpu": "18%", "mem": "42%"}
)
```

## Добавление новых языков

- Создайте JSON в `languages/` и перенесите ключи из `en.json`

## Пользовательские функции мониторинга

- Скан сети, ping‑проверки, обнаружение устройств — см. примеры и расширяйте под свои цели

## Кастомизация системы оповещений

- Каналы, пороги и интервалы в конфигурации

## Расширение интеграции Docker

- Дополнительные операции/метрики через Docker API

## Расширения управления SSL

- Ротация сертификатов, аутентификация и вызовы NPM API

## Интеграция базы данных

- Добавьте слой персистентности (например, SQLite/PostgreSQL)

## Создание веб‑дашборда

- Свяжите HTTP API с фронтендом, учтите аутентификацию/авторизацию

## Разработка плагин‑системы

- Точки расширения через унифицированные хуки и обнаружение модулей

