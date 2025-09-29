# Anpassungsleitfaden

Sprachen: Deutsch | [English](../customization.md) | [繁體中文](../zh-tw/customization.md) | [简体中文](../zh-cn/customization.md)

Hinweis: Diese Übersetzung wird derzeit erstellt. Für vollständige Details verweise vorläufig auf die englische Version.

## Inhaltsverzeichnis

- [Architektur verstehen](#architektur-verstehen)
- [Konfigurationsanpassung](#konfigurationsanpassung)
- [Eigene Befehle hinzufügen](#eigene-befehle-hinzufügen)
- [Eigene Cogs erstellen](#eigene-cogs-erstellen)
- [Embeds und UI anpassen](#embeds-und-ui-anpassen)
- [Neue Sprachen hinzufügen](#neue-sprachen-hinzufügen)
- [Benutzerdefiniertes Monitoring](#benutzerdefiniertes-monitoring)
- [Alarm-System anpassen](#alarm-system-anpassen)
- [Docker-Integration erweitern](#docker-integration-erweitern)
- [SSL-Management-Erweiterungen](#ssl-management-erweiterungen)
- [Datenbank-Integration](#datenbank-integration)
- [Web-Dashboard erstellen](#web-dashboard-erstellen)
- [Plugin-System entwickeln](#plugin-system-entwickeln)

## Architektur verstehen

Überblick über `main.py`, `cogs/`, `utils/`, `config/`, `languages/` und ihre Rollen bei Erweiterbarkeit und i18n.

## Konfigurationsanpassung

### Eigene Optionen in `config/bot_config.json`

Beispiel:

```json
{
  "custom_features": {
    "weather_monitoring": {
      "enabled": true,
      "api_key": "your_api_key",
      "locations": ["Berlin", "Zürich", "Wien"],
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

### Umgebungsvariablen in `.env`

```bash
# API-Schlüssel
WEATHER_API_KEY=your_weather_api_key
BACKUP_API_TOKEN=your_backup_token
CUSTOM_WEBHOOK_URL=https://your-webhook.com

# Pfade
CUSTOM_LOG_PATH=/var/log/custom
BACKUP_STORAGE_PATH=/mnt/backups

# Feature-Schalter
ENABLE_WEATHER_MONITORING=true
ENABLE_CUSTOM_BACKUP=true
ENABLE_ADVANCED_LOGGING=false
```

### Zugriff auf Konfiguration/Umgebung

```python
# in einem Cog oder Util
class CustomFeatureCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config_manager

        self.weather_enabled = self.config.get('custom_features.weather_monitoring.enabled', False)
        self.backup_path = self.config.get('custom_features.backup_system.backup_path', '/backups')

        self.weather_api_key = os.getenv('WEATHER_API_KEY')
```

## Eigene Befehle hinzufügen

### Einfacher Command

```python
# cogs/custom_commands.py
import discord
from discord.ext import commands
from discord import app_commands
from utils.embed_formatter import EmbedFormatter

class CustomCommandsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config_manager
        self.i18n = bot.i18n

    @app_commands.command(name="serverinfo", description="Serverinformationen anzeigen")
    async def server_info(self, interaction: discord.Interaction):
        guild = interaction.guild
        lang = self.config.get(f'guilds.{guild.id}.language', 'en')

        embed = EmbedFormatter.create_embed(
            title=f"📊 {guild.name} Serverinformationen",
            command_name="serverinfo",
            lang=lang
        )
        embed.add_field(name="👥 Mitglieder", value=f"{guild.member_count:,}", inline=True)
        embed.add_field(name="📚 Rollen", value=f"{len(guild.roles):,}", inline=True)
        embed.add_field(name="📢 Kanäle", value=f"{len(guild.channels):,}", inline=True)
        await interaction.response.send_message(embed=embed)
```

## Eigene Cogs erstellen

### Vorlage mit Hintergrund-Task

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
        # periodische Arbeit
        pass
```

## Embeds und UI anpassen

- Einheitliches Branding über `utils/embed_formatter.py`
- Eigene Stilhilfen z. B. `utils/custom_embed_styles.py`

```python
from utils.custom_embed_styles import CustomEmbedStyles
embed = CustomEmbedStyles.create_status_embed(
    title="Service Status",
    status="online",
    details={"cpu": "18%", "mem": "42%"}
)
```

## Neue Sprachen hinzufügen

- Neue JSON-Datei in `languages/` anlegen und Schlüssel aus `en.json` übernehmen

## Benutzerdefiniertes Monitoring

- Netzwerkscans, Ping-Checks, Gerätesuche als Beispiel-Cogs

## Alarm-System anpassen

- Kanäle, Schwellwerte und Intervalle definieren

## Docker-Integration erweitern

- Zusätzliche Operationen und Metriken per Docker-API

## SSL-Management-Erweiterungen

- Zertifikatsrotation, NPM-API-Workflows

## Datenbank-Integration

- Persistenzschicht ergänzen (z. B. SQLite/PostgreSQL) mit `utils/database.py`

## Web-Dashboard erstellen

- HTTP-API und Frontend anbinden; Authentifizierung beachten

## Plugin-System entwickeln

- Erweiterungen über standardisierte Hook-Punkte und Modul-Discovery
