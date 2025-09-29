# Customization Guide

Languages: [English](customization.md) | [繁體中文](zh-tw/customization.md) | [简体中文](zh-cn/customization.md)

This guide explains how to customize Logivore to meet your specific needs, including adding new features, modifying existing functionality, and extending the bot's capabilities.

## Table of Contents

- [Understanding the Architecture](#understanding-the-architecture)
- [Configuration Customization](#configuration-customization)
- [Adding Custom Commands](#adding-custom-commands)
- [Creating Custom Cogs](#creating-custom-cogs)
- [Customizing Embeds and UI](#customizing-embeds-and-ui)
- [Adding New Languages](#adding-new-languages)
- [Custom Monitoring Features](#custom-monitoring-features)
- [Alert System Customization](#alert-system-customization)
- [Docker Integration Expansion](#docker-integration-expansion)
- [SSL Management Extensions](#ssl-management-extensions)
- [Database Integration](#database-integration)
- [Web Dashboard Creation](#web-dashboard-creation)
- [Plugin System Development](#plugin-system-development)

## Understanding the Architecture

Before customizing the bot, it's important to understand its modular architecture:

### Core Components
- **main.py**: Bot initialization and core setup
- **cogs/**: Individual feature modules (system monitoring, Docker, alerts, etc.)
- **utils/**: Shared utilities (configuration, i18n, embed formatting)
- **config/**: Configuration files and environment variables
- **languages/**: Multi-language support files

### Key Design Patterns
1. **Cog-based Architecture**: Features are organized into Discord.py cogs
2. **Configuration-driven**: Behavior controlled through JSON configuration
3. **Async-first**: Non-blocking operations using async/await
4. **Multi-language**: Full internationalization support
5. **Modular**: Easy to add, remove, or modify components

## Configuration Customization

### Custom Configuration Options

Add your own configuration sections to `config/bot_config.json`:

```json
{
  "custom_features": {
    "weather_monitoring": {
      "enabled": true,
      "api_key": "your_api_key",
      "locations": ["New York", "London", "Tokyo"],
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

### Environment Variable Extensions

Add custom environment variables to `.env`:

```bash
# Custom API Keys
WEATHER_API_KEY=your_weather_api_key
BACKUP_API_TOKEN=your_backup_token
CUSTOM_WEBHOOK_URL=https://your-webhook.com

# Custom Paths
CUSTOM_LOG_PATH=/var/log/custom
BACKUP_STORAGE_PATH=/mnt/backups

# Feature Toggles
ENABLE_WEATHER_MONITORING=true
ENABLE_CUSTOM_BACKUP=true
ENABLE_ADVANCED_LOGGING=false
```

### Accessing Custom Configuration

```python
# In your cog or utility class
class CustomFeatureCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config_manager

        # Access custom configuration
        self.weather_enabled = self.config.get('custom_features.weather_monitoring.enabled', False)
        self.backup_path = self.config.get('custom_features.backup_system.backup_path', '/backups')

        # Access environment variables
        self.weather_api_key = os.getenv('WEATHER_API_KEY')
```

## Adding Custom Commands

### Simple Custom Command

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

    @app_commands.command(name="serverinfo", description="Display detailed server information")
    async def server_info(self, interaction: discord.Interaction):
        """Custom command to show server information"""
        guild = interaction.guild
        lang = self.config.get(f'guilds.{guild.id}.language', 'en')

        # Gather server information
        member_count = guild.member_count
        role_count = len(guild.roles)
        channel_count = len(guild.channels)
        emoji_count = len(guild.emojis)
        boost_level = guild.premium_tier
        boost_count = guild.premium_subscription_count

        embed = EmbedFormatter.create_embed(
            title=f"📊 {guild.name} Server Information",
            command_name="serverinfo",
            lang=lang
        )

        embed.add_field(name="👥 Members", value=f"{member_count:,}", inline=True)
        embed.add_field(name="📚 Roles", value=f"{role_count:,}", inline=True)
        embed.add_field(name="📢 Channels", value=f"{channel_count:,}", inline=True)
        embed.add_field(name="😀 Emojis", value=f"{emoji_count:,}", inline=True)
        embed.add_field(name="💎 Boost Level", value=f"Level {boost_level}", inline=True)
        embed.add_field(name="🚀 Boosts", value=f"{boost_count:,}", inline=True)

        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)

        embed.add_field(
            name="📅 Created",
            value=f"<t:{int(guild.created_at.timestamp())}:F>",
            inline=False
        )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="weather", description="Get weather information for a city")
    @app_commands.describe(city="City name to get weather for")
    async def weather(self, interaction: discord.Interaction, city: str):
        """Custom weather command"""
        if not self.config.get('custom_features.weather_monitoring.enabled', False):
            await interaction.response.send_message("❌ Weather monitoring is disabled.", ephemeral=True)
            return

        api_key = os.getenv('WEATHER_API_KEY')
        if not api_key:
            await interaction.response.send_message("❌ Weather API key not configured.", ephemeral=True)
            return

        try:
            # Call weather API (example with OpenWeatherMap)
            import aiohttp

            async with aiohttp.ClientSession() as session:
                url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()

                        temp = data['main']['temp']
                        feels_like = data['main']['feels_like']
                        humidity = data['main']['humidity']
                        description = data['weather'][0]['description']

                        lang = self.config.get(f'guilds.{interaction.guild_id}.language', 'en')

                        embed = EmbedFormatter.create_embed(
                            title=f"🌤️ Weather in {city.title()}",
                            description=description.title(),
                            command_name="weather",
                            lang=lang
                        )

                        embed.add_field(name="🌡️ Temperature", value=f"{temp}°C", inline=True)
                        embed.add_field(name="🤔 Feels Like", value=f"{feels_like}°C", inline=True)
                        embed.add_field(name="💧 Humidity", value=f"{humidity}%", inline=True)

                        await interaction.response.send_message(embed=embed)
                    else:
                        await interaction.response.send_message(f"❌ Could not get weather for {city}")

        except Exception as e:
            await interaction.response.send_message(f"❌ Error getting weather: {str(e)}")

async def setup(bot):
    await bot.add_cog(CustomCommandsCog(bot))
```

### Command with Subcommands

```python
class BackupCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="backup", description="Backup management commands")
    async def backup_group(self, interaction: discord.Interaction):
        """Base backup command - shows help"""
        embed = EmbedFormatter.create_embed(
            title="💾 Backup Management",
            description="Use the subcommands to manage backups",
            command_name="backup"
        )
        embed.add_field(name="/backup create", value="Create a new backup", inline=False)
        embed.add_field(name="/backup list", value="List available backups", inline=False)
        embed.add_field(name="/backup restore", value="Restore from backup", inline=False)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="backup-create", description="Create a new system backup")
    @app_commands.describe(name="Name for the backup")
    async def backup_create(self, interaction: discord.Interaction, name: str = None):
        """Create a backup"""
        # Implementation here
        pass

    @app_commands.command(name="backup-list", description="List available backups")
    async def backup_list(self, interaction: discord.Interaction):
        """List backups"""
        # Implementation here
        pass
```

## Creating Custom Cogs

### Complete Custom Cog Template

```python
# cogs/network_monitoring.py
import discord
from discord.ext import commands, tasks
from discord import app_commands
from utils.embed_formatter import EmbedFormatter
import asyncio
import subprocess
import json
from typing import Dict, List, Any

class NetworkMonitoringCog(commands.Cog):
    """Custom cog for network monitoring and management"""

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config_manager
        self.i18n = bot.i18n

        # Custom configuration
        self.enabled = self.config.get('custom_features.network_monitoring.enabled', False)
        self.scan_interval = self.config.get('custom_features.network_monitoring.scan_interval', 300)
        self.target_hosts = self.config.get('custom_features.network_monitoring.hosts', [])

        # Start background tasks if enabled
        if self.enabled:
            self.network_monitor_task.start()

    def cog_unload(self):
        """Cleanup when cog is unloaded"""
        if hasattr(self, 'network_monitor_task'):
            self.network_monitor_task.cancel()

    @tasks.loop(seconds=300)  # Run every 5 minutes
    async def network_monitor_task(self):
        """Background task to monitor network connectivity"""
        try:
            await self.check_network_connectivity()
        except Exception as e:
            print(f"Network monitoring error: {e}")

    @network_monitor_task.before_loop
    async def before_network_monitor(self):
        """Wait for bot to be ready"""
        await self.bot.wait_until_ready()

    async def check_network_connectivity(self):
        """Check connectivity to target hosts"""
        results = []

        for host in self.target_hosts:
            try:
                # Ping the host
                result = await asyncio.create_subprocess_exec(
                    'ping', '-c', '1', '-W', '5', host,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                stdout, stderr = await result.communicate()

                is_reachable = result.returncode == 0
                results.append({
                    'host': host,
                    'reachable': is_reachable,
                    'response_time': self._parse_ping_time(stdout.decode()) if is_reachable else None
                })
            except Exception as e:
                results.append({
                    'host': host,
                    'reachable': False,
                    'error': str(e)
                })

        # Send alerts for unreachable hosts
        await self._check_connectivity_alerts(results)

    def _parse_ping_time(self, ping_output: str) -> float:
        """Parse ping response time from output"""
        try:
            # Extract time from ping output
            import re
            match = re.search(r'time=(\d+\.?\d*)', ping_output)
            return float(match.group(1)) if match else None
        except:
            return None

    async def _check_connectivity_alerts(self, results: List[Dict]):
        """Check if any hosts are down and send alerts"""
        unreachable_hosts = [r for r in results if not r['reachable']]

        if unreachable_hosts:
            # Send alert to configured channel
            alert_channel_id = self.config.get('custom_features.network_monitoring.alert_channel')
            if alert_channel_id:
                channel = self.bot.get_channel(alert_channel_id)
                if channel:
                    embed = EmbedFormatter.create_embed(
                        title="🔴 Network Connectivity Alert",
                        description=f"{len(unreachable_hosts)} host(s) are unreachable",
                        color=0xff0000
                    )

                    for host in unreachable_hosts:
                        embed.add_field(
                            name=f"❌ {host['host']}",
                            value=host.get('error', 'No response'),
                            inline=True
                        )

                    await channel.send(embed=embed)

    @app_commands.command(name="netcheck", description="Check network connectivity to configured hosts")
    async def network_check(self, interaction: discord.Interaction):
        """Manual network connectivity check"""
        if not self.enabled:
            await interaction.response.send_message("❌ Network monitoring is disabled.", ephemeral=True)
            return

        await interaction.response.defer()

        # Check connectivity
        results = []
        for host in self.target_hosts:
            try:
                result = await asyncio.create_subprocess_exec(
                    'ping', '-c', '1', '-W', '5', host,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                stdout, stderr = await result.communicate()

                is_reachable = result.returncode == 0
                response_time = self._parse_ping_time(stdout.decode()) if is_reachable else None

                results.append({
                    'host': host,
                    'reachable': is_reachable,
                    'response_time': response_time
                })
            except Exception as e:
                results.append({
                    'host': host,
                    'reachable': False,
                    'error': str(e)
                })

        # Create response embed
        lang = self.config.get(f'guilds.{interaction.guild_id}.language', 'en')
        embed = EmbedFormatter.create_embed(
            title="🌐 Network Connectivity Check",
            command_name="netcheck",
            lang=lang
        )

        reachable_count = sum(1 for r in results if r['reachable'])
        total_count = len(results)

        embed.add_field(
            name="📊 Summary",
            value=f"{reachable_count}/{total_count} hosts reachable",
            inline=False
        )

        for result in results:
            status = "✅" if result['reachable'] else "❌"
            if result['reachable'] and result.get('response_time'):
                value = f"{result['response_time']}ms"
            else:
                value = result.get('error', 'No response')

            embed.add_field(
                name=f"{status} {result['host']}",
                value=value,
                inline=True
            )

        await interaction.followup.send(embed=embed)

    @app_commands.command(name="netscan", description="Scan local network for devices")
    @app_commands.describe(subnet="Subnet to scan (e.g., 192.168.1.0/24)")
    async def network_scan(self, interaction: discord.Interaction, subnet: str = None):
        """Scan network for devices"""
        if not self.enabled:
            await interaction.response.send_message("❌ Network monitoring is disabled.", ephemeral=True)
            return

        await interaction.response.defer()

        if not subnet:
            # Try to detect local subnet
            try:
                import netifaces
                gws = netifaces.gateways()
                default_gw = gws['default'][netifaces.AF_INET][0]
                # Simple subnet detection - this is basic
                subnet = f"{'.'.join(default_gw.split('.')[:-1])}.0/24"
            except:
                subnet = "192.168.1.0/24"  # Fallback

        try:
            # Use nmap for network scanning
            result = await asyncio.create_subprocess_exec(
                'nmap', '-sn', subnet,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout, stderr = await result.communicate()

            if result.returncode == 0:
                # Parse nmap output
                devices = self._parse_nmap_output(stdout.decode())

                lang = self.config.get(f'guilds.{interaction.guild_id}.language', 'en')
                embed = EmbedFormatter.create_embed(
                    title=f"🔍 Network Scan Results",
                    description=f"Subnet: {subnet}",
                    command_name="netscan",
                    lang=lang
                )

                embed.add_field(
                    name="📊 Summary",
                    value=f"Found {len(devices)} devices",
                    inline=False
                )

                for i, device in enumerate(devices[:10]):  # Limit to 10 devices
                    embed.add_field(
                        name=f"🖥️ Device {i+1}",
                        value=device,
                        inline=True
                    )

                if len(devices) > 10:
                    embed.add_field(
                        name="ℹ️ Note",
                        value=f"Showing first 10 of {len(devices)} devices",
                        inline=False
                    )

                await interaction.followup.send(embed=embed)
            else:
                await interaction.followup.send("❌ Network scan failed. Make sure nmap is installed.")

        except Exception as e:
            await interaction.followup.send(f"❌ Error during network scan: {str(e)}")

    def _parse_nmap_output(self, output: str) -> List[str]:
        """Parse nmap output to extract device IPs"""
        devices = []
        lines = output.split('\n')

        for line in lines:
            if 'Nmap scan report for' in line:
                # Extract IP address
                import re
                ip_match = re.search(r'(\d+\.\d+\.\d+\.\d+)', line)
                if ip_match:
                    devices.append(ip_match.group(1))

        return devices

    @app_commands.command(name="netconfig", description="Configure network monitoring settings")
    @app_commands.describe(
        enabled="Enable or disable network monitoring",
        add_host="Add a host to monitor",
        remove_host="Remove a host from monitoring"
    )
    async def network_config(
        self,
        interaction: discord.Interaction,
        enabled: bool = None,
        add_host: str = None,
        remove_host: str = None
    ):
        """Configure network monitoring"""
        # Check permissions (owner only for this example)
        if interaction.user.id != int(os.getenv('OWNER_ID', 0)):
            await interaction.response.send_message("❌ Only the bot owner can configure network monitoring.", ephemeral=True)
            return

        lang = self.config.get(f'guilds.{interaction.guild_id}.language', 'en')

        if enabled is not None:
            self.config.set('custom_features.network_monitoring.enabled', enabled)
            self.enabled = enabled

            if enabled and not self.network_monitor_task.is_running():
                self.network_monitor_task.start()
            elif not enabled and self.network_monitor_task.is_running():
                self.network_monitor_task.cancel()

        if add_host:
            current_hosts = self.config.get('custom_features.network_monitoring.hosts', [])
            if add_host not in current_hosts:
                current_hosts.append(add_host)
                self.config.set('custom_features.network_monitoring.hosts', current_hosts)
                self.target_hosts = current_hosts

        if remove_host:
            current_hosts = self.config.get('custom_features.network_monitoring.hosts', [])
            if remove_host in current_hosts:
                current_hosts.remove(remove_host)
                self.config.set('custom_features.network_monitoring.hosts', current_hosts)
                self.target_hosts = current_hosts

        # Show current configuration
        embed = EmbedFormatter.create_embed(
            title="⚙️ Network Monitoring Configuration",
            command_name="netconfig",
            lang=lang
        )

        embed.add_field(
            name="Status",
            value="✅ Enabled" if self.enabled else "❌ Disabled",
            inline=True
        )

        embed.add_field(
            name="Monitored Hosts",
            value=f"{len(self.target_hosts)} hosts" if self.target_hosts else "None",
            inline=True
        )

        if self.target_hosts:
            hosts_list = '\n'.join(f"• {host}" for host in self.target_hosts[:5])
            if len(self.target_hosts) > 5:
                hosts_list += f"\n... and {len(self.target_hosts) - 5} more"

            embed.add_field(
                name="Host List",
                value=hosts_list,
                inline=False
            )

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(NetworkMonitoringCog(bot))
```

## Customizing Embeds and UI

### Custom Embed Styles

```python
# utils/custom_embed_styles.py
import discord
from datetime import datetime
from typing import Optional

class CustomEmbedStyles:
    """Custom embed styles for different use cases"""

    # Custom color schemes
    COLORS = {
        'success': 0x00ff88,
        'warning': 0xffaa00,
        'error': 0xff4444,
        'info': 0x44aaff,
        'critical': 0xaa0000,
        'maintenance': 0x888888,
        'custom_brand': 0x7c4dff  # Your custom brand color
    }

    @staticmethod
    def create_status_embed(
        title: str,
        status: str,
        details: dict,
        style: str = 'default'
    ) -> discord.Embed:
        """Create a status embed with custom styling"""

        color_map = {
            'online': CustomEmbedStyles.COLORS['success'],
            'warning': CustomEmbedStyles.COLORS['warning'],
            'offline': CustomEmbedStyles.COLORS['error'],
            'maintenance': CustomEmbedStyles.COLORS['maintenance']
        }

        color = color_map.get(status, CustomEmbedStyles.COLORS['info'])

        embed = discord.Embed(
            title=f"🔵 {title}" if status == 'online' else f"🔴 {title}",
            color=color,
            timestamp=datetime.now()
        )

        # Add status indicator
        status_emoji = {
            'online': '🟢',
            'warning': '🟡',
            'offline': '🔴',
            'maintenance': '🔧'
        }

        embed.add_field(
            name="Status",
            value=f"{status_emoji.get(status, '⚪')} {status.title()}",
            inline=True
        )

        # Add details
        for key, value in details.items():
            embed.add_field(
                name=key.replace('_', ' ').title(),
                value=str(value),
                inline=True
            )

        # Custom footer
        embed.set_footer(
            text="Custom Monitoring System",
            icon_url="https://your-custom-icon-url.com/icon.png"
        )

        return embed

    @staticmethod
    def create_progress_embed(
        title: str,
        progress: float,
        total: float,
        description: str = None
    ) -> discord.Embed:
        """Create an embed with a progress bar"""

        percentage = (progress / total) * 100 if total > 0 else 0

        # Create progress bar
        filled = int(percentage / 10)
        empty = 10 - filled
        progress_bar = "█" * filled + "░" * empty

        embed = discord.Embed(
            title=title,
            description=description,
            color=CustomEmbedStyles.COLORS['custom_brand']
        )

        embed.add_field(
            name="Progress",
            value=f"```{progress_bar}``` {percentage:.1f}% ({progress}/{total})",
            inline=False
        )

        return embed
```

### Custom View Components

```python
# utils/custom_views.py
import discord
from discord.ext import commands

class ConfirmationView(discord.ui.View):
    """Custom confirmation dialog with buttons"""

    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
        self.value = None

    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green, emoji='✅')
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = True
        self.stop()

    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.red, emoji='❌')
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = False
        self.stop()

class PaginationView(discord.ui.View):
    """Custom pagination view for long lists"""

    def __init__(self, embeds: list, *, timeout=300):
        super().__init__(timeout=timeout)
        self.embeds = embeds
        self.current_page = 0
        self.max_page = len(embeds) - 1

    @discord.ui.button(label='◀', style=discord.ButtonStyle.grey)
    async def previous_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page > 0:
            self.current_page -= 1
            embed = self.embeds[self.current_page]
            embed.set_footer(text=f"Page {self.current_page + 1}/{len(self.embeds)}")
            await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label='▶', style=discord.ButtonStyle.grey)
    async def next_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page < self.max_page:
            self.current_page += 1
            embed = self.embeds[self.current_page]
            embed.set_footer(text=f"Page {self.current_page + 1}/{len(self.embeds)}")
            await interaction.response.edit_message(embed=embed, view=self)

# Usage example
@app_commands.command(name="customlist", description="Show a paginated list")
async def custom_list(self, interaction: discord.Interaction):
    # Create multiple embeds
    embeds = []
    for i in range(5):
        embed = discord.Embed(title=f"Page {i+1}", description=f"Content for page {i+1}")
        embeds.append(embed)

    # Create pagination view
    view = PaginationView(embeds)
    embed = embeds[0]
    embed.set_footer(text=f"Page 1/{len(embeds)}")

    await interaction.response.send_message(embed=embed, view=view)
```

## Adding New Languages

### Language File Creation

Create a new language file in the `languages/` directory:

```json
// languages/es.json (Spanish)
{
  "commands": {
    "monitor": {
      "name": "monitor",
      "description": "Mostrar panel de monitoreo del sistema",
      "response": {
        "title": "🖥️ Monitor del Sistema - Panel en Vivo",
        "cpu": "💾 Uso de CPU",
        "memory": "🧠 Memoria",
        "disk": "💽 Disco",
        "network": "🌐 Red",
        "updated": "Última Actualización"
      }
    },
    "help": {
      "title": "📚 Sistema de Ayuda",
      "description": "Comandos disponibles del bot",
      "categories": {
        "monitoring": "Monitoreo del Sistema",
        "docker": "Gestión de Docker",
        "alerts": "Gestión de Alertas"
      }
    }
  },
  "errors": {
    "generic": "Ocurrió un error",
    "permission_denied": "No tienes permisos para usar este comando",
    "invalid_parameter": "Parámetro inválido: {parameter}"
  },
  "common": {
    "success": "Éxito",
    "failed": "Falló",
    "loading": "Cargando...",
    "enabled": "Habilitado",
    "disabled": "Deshabilitado"
  }
}
```

### Update Embed Formatter

Add the new language to the embed formatter:

```python
# utils/embed_formatter.py
class EmbedFormatter:
    COMMAND_AUTHORS = {
        'en': {
            'monitor': '🔍 System Monitoring',
            'docker': '🐳 Docker Management'
        },
        'es': {
            'monitor': '🔍 Monitoreo del Sistema',
            'docker': '🐳 Gestión de Docker'
        }
        # Add other languages...
    }

    FOOTER_TEXTS = {
        'en': 'Powered by Serelix Studio',
        'es': 'Desarrollado por Serelix Studio',
        # Add other languages...
    }
```

### Language Selection Command

```python
@app_commands.command(name="language", description="Change bot language")
@app_commands.describe(language="Language code (en, es, fr, de, etc.)")
@app_commands.choices(language=[
    app_commands.Choice(name="English", value="en"),
    app_commands.Choice(name="Español", value="es"),
    app_commands.Choice(name="Français", value="fr"),
    app_commands.Choice(name="Deutsch", value="de")
])
async def change_language(self, interaction: discord.Interaction, language: str = None):
    if language:
        # Set language for this guild
        self.config.set(f'guilds.{interaction.guild_id}.language', language)

        # Confirm in the new language
        title = self.i18n.get('language.changed.title', language)
        description = self.i18n.get('language.changed.description', language)

        embed = EmbedFormatter.create_embed(
            title=title,
            description=description,
            command_name="language",
            lang=language
        )

        await interaction.response.send_message(embed=embed)
```

## Custom Monitoring Features

### Custom System Metrics

```python
# utils/custom_metrics.py
import psutil
import asyncio
import aiofiles
from typing import Dict, Any

class CustomMetricsCollector:
    """Collect custom system metrics beyond basic monitoring"""

    async def get_temperature_data(self) -> Dict[str, float]:
        """Get system temperature data"""
        try:
            temps = psutil.sensors_temperatures()
            temperature_data = {}

            for name, entries in temps.items():
                for entry in entries:
                    label = entry.label or name
                    temperature_data[f"{name}_{label}"] = entry.current

            return temperature_data
        except:
            return {}

    async def get_gpu_info(self) -> Dict[str, Any]:
        """Get GPU information using nvidia-ml-py"""
        try:
            import pynvml
            pynvml.nvmlInit()

            device_count = pynvml.nvmlDeviceGetCount()
            gpu_info = {}

            for i in range(device_count):
                handle = pynvml.nvmlDeviceGetHandleByIndex(i)
                name = pynvml.nvmlDeviceGetName(handle).decode()

                # Memory info
                mem_info = pynvml.nvmlDeviceGetMemoryInfo(handle)

                # Temperature
                temp = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)

                # Utilization
                util = pynvml.nvmlDeviceGetUtilizationRates(handle)

                gpu_info[f"gpu_{i}"] = {
                    'name': name,
                    'memory_total': mem_info.total,
                    'memory_used': mem_info.used,
                    'memory_percent': (mem_info.used / mem_info.total) * 100,
                    'temperature': temp,
                    'gpu_utilization': util.gpu,
                    'memory_utilization': util.memory
                }

            return gpu_info
        except:
            return {}

    async def get_service_status(self, services: list) -> Dict[str, str]:
        """Get status of system services"""
        service_status = {}

        for service in services:
            try:
                result = await asyncio.create_subprocess_exec(
                    'systemctl', 'is-active', service,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                stdout, _ = await result.communicate()
                status = stdout.decode().strip()
                service_status[service] = status
            except:
                service_status[service] = 'unknown'

        return service_status

    async def get_security_metrics(self) -> Dict[str, Any]:
        """Get security-related metrics"""
        security_data = {}

        try:
            # Failed login attempts (example for Linux)
            result = await asyncio.create_subprocess_exec(
                'grep', 'Failed password', '/var/log/auth.log',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, _ = await result.communicate()
            failed_logins = len(stdout.decode().split('\n')) - 1
            security_data['failed_logins_today'] = failed_logins

            # Open ports
            result = await asyncio.create_subprocess_exec(
                'ss', '-tuln',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, _ = await result.communicate()
            open_ports = len([line for line in stdout.decode().split('\n') if 'LISTEN' in line])
            security_data['open_ports'] = open_ports

        except:
            pass

        return security_data
```

### Custom Monitoring Dashboard

```python
# cogs/custom_monitoring.py
@app_commands.command(name="advanced-monitor", description="Advanced system monitoring dashboard")
async def advanced_monitor(self, interaction: discord.Interaction):
    """Advanced monitoring with custom metrics"""
    await interaction.response.defer()

    metrics_collector = CustomMetricsCollector()

    # Collect all metrics
    basic_stats = await self.system_monitor.get_system_stats()
    temperature_data = await metrics_collector.get_temperature_data()
    gpu_info = await metrics_collector.get_gpu_info()

    # Configured services to monitor
    services = self.config.get('custom_features.monitoring.services', ['nginx', 'mysql', 'redis'])
    service_status = await metrics_collector.get_service_status(services)

    security_metrics = await metrics_collector.get_security_metrics()

    lang = self.config.get(f'guilds.{interaction.guild_id}.language', 'en')

    # Create comprehensive embed
    embed = EmbedFormatter.create_embed(
        title="🔍 Advanced System Monitor",
        command_name="advanced-monitor",
        lang=lang
    )

    # Basic system info
    cpu_percent = basic_stats['cpu']['usage_percent']
    memory_percent = basic_stats['memory']['percent']

    embed.add_field(
        name="💾 System Resources",
        value=f"CPU: {cpu_percent}%\nMemory: {memory_percent}%",
        inline=True
    )

    # Temperature info
    if temperature_data:
        temp_str = "\n".join([f"{name}: {temp}°C" for name, temp in list(temperature_data.items())[:3]])
        embed.add_field(
            name="🌡️ Temperatures",
            value=temp_str or "N/A",
            inline=True
        )

    # GPU info
    if gpu_info:
        gpu_str = "\n".join([f"{data['name']}: {data['gpu_utilization']}%" for data in list(gpu_info.values())[:2]])
        embed.add_field(
            name="🎮 GPU Usage",
            value=gpu_str or "N/A",
            inline=True
        )

    # Service status
    if service_status:
        status_emojis = {'active': '🟢', 'inactive': '🔴', 'failed': '❌', 'unknown': '⚪'}
        service_str = "\n".join([
            f"{status_emojis.get(status, '⚪')} {service}: {status}"
            for service, status in service_status.items()
        ])
        embed.add_field(
            name="🔧 Services",
            value=service_str,
            inline=False
        )

    # Security metrics
    if security_metrics:
        security_str = "\n".join([
            f"Failed logins: {security_metrics.get('failed_logins_today', 'N/A')}",
            f"Open ports: {security_metrics.get('open_ports', 'N/A')}"
        ])
        embed.add_field(
            name="🛡️ Security",
            value=security_str,
            inline=True
        )

    await interaction.followup.send(embed=embed)
```

## Alert System Customization

### Custom Alert Types

```python
# utils/custom_alerts.py
from enum import Enum
from typing import Dict, Any, Callable
import aiohttp

class CustomAlertType(Enum):
    TEMPERATURE = "temperature"
    GPU_USAGE = "gpu_usage"
    SERVICE_DOWN = "service_down"
    SECURITY_BREACH = "security_breach"
    CUSTOM_METRIC = "custom_metric"

class CustomAlertHandler:
    """Handle custom alert types and notification methods"""

    def __init__(self, config_manager):
        self.config = config_manager
        self.webhook_url = config_manager.get('custom_features.custom_alerts.webhook_url')
        self.email_enabled = config_manager.get('custom_features.custom_alerts.email_notifications', False)

    async def send_webhook_alert(self, alert_data: Dict[str, Any]):
        """Send alert via webhook"""
        if not self.webhook_url:
            return

        try:
            payload = {
                "text": f"🚨 {alert_data['title']}",
                "attachments": [{
                    "color": "danger" if alert_data['severity'] == 'critical' else "warning",
                    "fields": [
                        {
                            "title": "Details",
                            "value": alert_data['description'],
                            "short": False
                        },
                        {
                            "title": "Timestamp",
                            "value": alert_data['timestamp'],
                            "short": True
                        }
                    ]
                }]
            }

            async with aiohttp.ClientSession() as session:
                await session.post(self.webhook_url, json=payload)
        except Exception as e:
            print(f"Failed to send webhook alert: {e}")

    async def send_email_alert(self, alert_data: Dict[str, Any]):
        """Send alert via email"""
        if not self.email_enabled:
            return

        # Implement email sending logic here
        # You could use aiosmtplib or similar library
        pass

    async def handle_temperature_alert(self, temperature_data: Dict[str, float]):
        """Handle temperature alerts"""
        threshold = self.config.get('custom_features.alerts.temperature_threshold', 70)

        for sensor, temp in temperature_data.items():
            if temp > threshold:
                alert_data = {
                    'title': f'High Temperature Alert: {sensor}',
                    'description': f'Temperature {temp}°C exceeds threshold {threshold}°C',
                    'severity': 'critical' if temp > threshold + 10 else 'warning',
                    'timestamp': datetime.now().isoformat()
                }

                await self.send_webhook_alert(alert_data)
                await self.send_email_alert(alert_data)

    async def handle_service_alert(self, service_status: Dict[str, str]):
        """Handle service status alerts"""
        critical_services = self.config.get('custom_features.alerts.critical_services', [])

        for service, status in service_status.items():
            if service in critical_services and status not in ['active', 'running']:
                alert_data = {
                    'title': f'Service Down: {service}',
                    'description': f'Critical service {service} is {status}',
                    'severity': 'critical',
                    'timestamp': datetime.now().isoformat()
                }

                await self.send_webhook_alert(alert_data)
                await self.send_email_alert(alert_data)
```

### Custom Alert Commands

```python
@app_commands.command(name="custom-alert", description="Configure custom alerts")
@app_commands.describe(
    alert_type="Type of custom alert",
    threshold="Alert threshold",
    enabled="Enable or disable alert"
)
@app_commands.choices(alert_type=[
    app_commands.Choice(name="Temperature", value="temperature"),
    app_commands.Choice(name="GPU Usage", value="gpu_usage"),
    app_commands.Choice(name="Service Status", value="service_down")
])
async def custom_alert_config(
    self,
    interaction: discord.Interaction,
    alert_type: str,
    threshold: float = None,
    enabled: bool = None
):
    """Configure custom alerts"""
    # Owner check
    if interaction.user.id != int(os.getenv('OWNER_ID', 0)):
        await interaction.response.send_message("❌ Only the bot owner can configure alerts.", ephemeral=True)
        return

    config_key = f'custom_features.alerts.{alert_type}'

    if threshold is not None:
        self.config.set(f'{config_key}.threshold', threshold)

    if enabled is not None:
        self.config.set(f'{config_key}.enabled', enabled)

    # Show current configuration
    current_config = self.config.get(config_key, {})

    embed = EmbedFormatter.create_embed(
        title=f"⚙️ Custom Alert Configuration: {alert_type.title()}",
        command_name="custom-alert"
    )

    embed.add_field(
        name="Status",
        value="✅ Enabled" if current_config.get('enabled', False) else "❌ Disabled",
        inline=True
    )

    embed.add_field(
        name="Threshold",
        value=str(current_config.get('threshold', 'Not set')),
        inline=True
    )

    await interaction.response.send_message(embed=embed)
```

## Database Integration

### Database Setup

```python
# utils/database.py
import asyncpg
import sqlite3
import aiosqlite
from typing import Optional, Dict, Any, List

class DatabaseManager:
    """Database manager for storing bot data"""

    def __init__(self, config_manager):
        self.config = config_manager
        self.db_type = config_manager.get('database.type', 'sqlite')
        self.db_path = config_manager.get('database.path', 'data/logivore.db')
        self.db_url = config_manager.get('database.url')

        self.connection = None

    async def connect(self):
        """Connect to database"""
        if self.db_type == 'sqlite':
            self.connection = await aiosqlite.connect(self.db_path)
        elif self.db_type == 'postgresql':
            self.connection = await asyncpg.connect(self.db_url)

        await self.create_tables()

    async def disconnect(self):
        """Disconnect from database"""
        if self.connection:
            await self.connection.close()

    async def create_tables(self):
        """Create necessary tables"""
        if self.db_type == 'sqlite':
            await self._create_sqlite_tables()
        elif self.db_type == 'postgresql':
            await self._create_postgresql_tables()

    async def _create_sqlite_tables(self):
        """Create SQLite tables"""
        await self.connection.execute('''
            CREATE TABLE IF NOT EXISTS monitoring_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                guild_id INTEGER,
                cpu_usage REAL,
                memory_usage REAL,
                disk_usage REAL,
                network_rx INTEGER,
                network_tx INTEGER
            )
        ''')

        await self.connection.execute('''
            CREATE TABLE IF NOT EXISTS alert_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                guild_id INTEGER,
                alert_type TEXT,
                message TEXT,
                severity TEXT,
                resolved BOOLEAN DEFAULT FALSE
            )
        ''')

        await self.connection.commit()

    async def save_monitoring_data(self, guild_id: int, stats: Dict[str, Any]):
        """Save monitoring data to database"""
        if self.db_type == 'sqlite':
            await self.connection.execute('''
                INSERT INTO monitoring_history
                (guild_id, cpu_usage, memory_usage, disk_usage, network_rx, network_tx)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                guild_id,
                stats.get('cpu', {}).get('usage_percent', 0),
                stats.get('memory', {}).get('percent', 0),
                stats.get('disk', [{}])[0].get('percent', 0),
                stats.get('network', {}).get('bytes_recv', 0),
                stats.get('network', {}).get('bytes_sent', 0)
            ))
            await self.connection.commit()

    async def get_monitoring_history(self, guild_id: int, hours: int = 24) -> List[Dict]:
        """Get monitoring history from database"""
        if self.db_type == 'sqlite':
            async with self.connection.execute('''
                SELECT * FROM monitoring_history
                WHERE guild_id = ? AND timestamp > datetime('now', '-{} hours')
                ORDER BY timestamp DESC
            '''.format(hours), (guild_id,)) as cursor:
                rows = await cursor.fetchall()
                columns = [description[0] for description in cursor.description]
                return [dict(zip(columns, row)) for row in rows]
```

### Database Commands

```python
@app_commands.command(name="history", description="View system monitoring history")
@app_commands.describe(hours="Hours of history to show (default: 24)")
async def monitoring_history(self, interaction: discord.Interaction, hours: int = 24):
    """Show monitoring history from database"""
    await interaction.response.defer()

    # Get data from database
    history = await self.bot.database.get_monitoring_history(interaction.guild_id, hours)

    if not history:
        await interaction.followup.send("No monitoring history found.")
        return

    # Create chart or summary
    avg_cpu = sum(record['cpu_usage'] for record in history) / len(history)
    avg_memory = sum(record['memory_usage'] for record in history) / len(history)
    max_cpu = max(record['cpu_usage'] for record in history)
    max_memory = max(record['memory_usage'] for record in history)

    embed = EmbedFormatter.create_embed(
        title=f"📊 System History ({hours} hours)",
        command_name="history"
    )

    embed.add_field(
        name="CPU Usage",
        value=f"Avg: {avg_cpu:.1f}%\nMax: {max_cpu:.1f}%",
        inline=True
    )

    embed.add_field(
        name="Memory Usage",
        value=f"Avg: {avg_memory:.1f}%\nMax: {max_memory:.1f}%",
        inline=True
    )

    embed.add_field(
        name="Data Points",
        value=f"{len(history)} records",
        inline=True
    )

    await interaction.followup.send(embed=embed)
```

## Web Dashboard Creation

### Flask Dashboard

```python
# web/dashboard.py
from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
import asyncio
import json

class WebDashboard:
    """Web dashboard for Logivore"""

    def __init__(self, bot):
        self.bot = bot
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'your-secret-key'
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")

        self.setup_routes()
        self.setup_socketio()

    def setup_routes(self):
        """Setup Flask routes"""

        @self.app.route('/')
        def dashboard():
            return render_template('dashboard.html')

        @self.app.route('/api/stats')
        def get_stats():
            """API endpoint for current system stats"""
            # This would need to be called from the main async loop
            return jsonify({
                'cpu': 45.2,
                'memory': 67.8,
                'disk': 23.1,
                'status': 'online'
            })

        @self.app.route('/api/containers')
        def get_containers():
            """API endpoint for Docker containers"""
            return jsonify([
                {'name': 'nginx', 'status': 'running'},
                {'name': 'mysql', 'status': 'running'},
                {'name': 'redis', 'status': 'stopped'}
            ])

    def setup_socketio(self):
        """Setup SocketIO events"""

        @self.socketio.on('connect')
        def handle_connect():
            print('Client connected to dashboard')
            emit('status', {'message': 'Connected to Logivore Dashboard'})

        @self.socketio.on('disconnect')
        def handle_disconnect():
            print('Client disconnected from dashboard')

    def emit_update(self, data_type: str, data: dict):
        """Emit real-time updates to connected clients"""
        self.socketio.emit('update', {
            'type': data_type,
            'data': data
        })

    def run(self, host='0.0.0.0', port=5000, debug=False):
        """Run the dashboard"""
        self.socketio.run(self.app, host=host, port=port, debug=debug)

# templates/dashboard.html
"""
<!DOCTYPE html>
<html>
<head>
    <title>Logivore Dashboard</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #1a1a1a; color: white; }
        .dashboard { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
        .card { background: #2a2a2a; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
        .stat { font-size: 2em; font-weight: bold; color: #4CAF50; }
        .chart-container { position: relative; height: 200px; }
    </style>
</head>
<body>
    <h1>🤖 Logivore Dashboard</h1>

    <div class="dashboard">
        <div class="card">
            <h3>💾 CPU Usage</h3>
            <div class="stat" id="cpu-usage">--</div>
        </div>

        <div class="card">
            <h3>🧠 Memory Usage</h3>
            <div class="stat" id="memory-usage">--</div>
        </div>

        <div class="card">
            <h3>💽 Disk Usage</h3>
            <div class="stat" id="disk-usage">--</div>
        </div>

        <div class="card">
            <h3>📊 System Performance</h3>
            <div class="chart-container">
                <canvas id="performance-chart"></canvas>
            </div>
        </div>
    </div>

    <script>
        const socket = io();

        // Chart setup
        const ctx = document.getElementById('performance-chart').getContext('2d');
        const chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'CPU %',
                    data: [],
                    borderColor: '#4CAF50',
                    tension: 0.4
                }, {
                    label: 'Memory %',
                    data: [],
                    borderColor: '#2196F3',
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { labels: { color: 'white' } }
                },
                scales: {
                    x: { ticks: { color: 'white' } },
                    y: { ticks: { color: 'white' }, max: 100 }
                }
            }
        });

        // Socket event handlers
        socket.on('connect', function() {
            console.log('Connected to dashboard');
        });

        socket.on('update', function(data) {
            if (data.type === 'system_stats') {
                updateStats(data.data);
                updateChart(data.data);
            }
        });

        function updateStats(stats) {
            document.getElementById('cpu-usage').textContent = stats.cpu.toFixed(1) + '%';
            document.getElementById('memory-usage').textContent = stats.memory.toFixed(1) + '%';
            document.getElementById('disk-usage').textContent = stats.disk.toFixed(1) + '%';
        }

        function updateChart(stats) {
            const now = new Date().toLocaleTimeString();

            chart.data.labels.push(now);
            chart.data.datasets[0].data.push(stats.cpu);
            chart.data.datasets[1].data.push(stats.memory);

            // Keep only last 20 data points
            if (chart.data.labels.length > 20) {
                chart.data.labels.shift();
                chart.data.datasets[0].data.shift();
                chart.data.datasets[1].data.shift();
            }

            chart.update();
        }

        // Fetch initial data
        fetch('/api/stats')
            .then(response => response.json())
            .then(data => updateStats(data));
    </script>
</body>
</html>
"""

# Integration with bot
@app_commands.command(name="dashboard", description="Get web dashboard URL")
async def dashboard_url(self, interaction: discord.Interaction):
    """Provide web dashboard access"""
    embed = EmbedFormatter.create_embed(
        title="🌐 Web Dashboard",
        description="Access the Logivore web dashboard",
        command_name="dashboard"
    )

    dashboard_url = self.config.get('web_dashboard.url', 'http://localhost:5000')
    embed.add_field(
        name="Dashboard URL",
        value=f"[Open Dashboard]({dashboard_url})",
        inline=False
    )

    embed.add_field(
        name="Features",
        value="• Real-time system monitoring\n• Container management\n• Alert history\n• Performance charts",
        inline=False
    )

    await interaction.response.send_message(embed=embed)
```

## Plugin System Development

### Plugin Framework

```python
# utils/plugin_system.py
import importlib
import os
from typing import Dict, Any, List
from abc import ABC, abstractmethod

class Plugin(ABC):
    """Base class for all plugins"""

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config_manager
        self.name = self.__class__.__name__
        self.version = "1.0.0"
        self.description = "A Logivore plugin"

    @abstractmethod
    async def initialize(self):
        """Initialize the plugin"""
        pass

    @abstractmethod
    async def cleanup(self):
        """Cleanup when plugin is unloaded"""
        pass

    def get_commands(self) -> List:
        """Return list of commands provided by this plugin"""
        return []

    def get_tasks(self) -> List:
        """Return list of background tasks provided by this plugin"""
        return []

class PluginManager:
    """Manage plugins for Logivore"""

    def __init__(self, bot):
        self.bot = bot
        self.plugins: Dict[str, Plugin] = {}
        self.plugin_dir = "plugins"

    async def load_all_plugins(self):
        """Load all plugins from the plugins directory"""
        if not os.path.exists(self.plugin_dir):
            os.makedirs(self.plugin_dir)
            return

        for filename in os.listdir(self.plugin_dir):
            if filename.endswith('.py') and not filename.startswith('_'):
                plugin_name = filename[:-3]
                await self.load_plugin(plugin_name)

    async def load_plugin(self, plugin_name: str) -> bool:
        """Load a specific plugin"""
        try:
            # Import the plugin module
            module = importlib.import_module(f"{self.plugin_dir}.{plugin_name}")

            # Find the plugin class
            plugin_class = None
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (isinstance(attr, type) and
                    issubclass(attr, Plugin) and
                    attr != Plugin):
                    plugin_class = attr
                    break

            if not plugin_class:
                print(f"No plugin class found in {plugin_name}")
                return False

            # Instantiate and initialize the plugin
            plugin_instance = plugin_class(self.bot)
            await plugin_instance.initialize()

            self.plugins[plugin_name] = plugin_instance
            print(f"✅ Loaded plugin: {plugin_name}")
            return True

        except Exception as e:
            print(f"❌ Failed to load plugin {plugin_name}: {e}")
            return False

    async def unload_plugin(self, plugin_name: str) -> bool:
        """Unload a specific plugin"""
        if plugin_name not in self.plugins:
            return False

        try:
            plugin = self.plugins[plugin_name]
            await plugin.cleanup()
            del self.plugins[plugin_name]
            print(f"🔄 Unloaded plugin: {plugin_name}")
            return True
        except Exception as e:
            print(f"❌ Failed to unload plugin {plugin_name}: {e}")
            return False

    async def reload_plugin(self, plugin_name: str) -> bool:
        """Reload a specific plugin"""
        if plugin_name in self.plugins:
            await self.unload_plugin(plugin_name)

        # Reload the module
        try:
            module = importlib.import_module(f"{self.plugin_dir}.{plugin_name}")
            importlib.reload(module)
        except Exception as e:
            print(f"Failed to reload module {plugin_name}: {e}")
            return False

        return await self.load_plugin(plugin_name)
```

### Example Plugin

```python
# plugins/weather_plugin.py
import aiohttp
from utils.plugin_system import Plugin
from utils.embed_formatter import EmbedFormatter
from discord.ext import commands
from discord import app_commands
import discord

class WeatherPlugin(Plugin):
    """Weather monitoring plugin for Logivore"""

    def __init__(self, bot):
        super().__init__(bot)
        self.name = "Weather Plugin"
        self.version = "1.0.0"
        self.description = "Provides weather monitoring and alerts"

        self.api_key = self.config.get('plugins.weather.api_key')
        self.enabled = self.config.get('plugins.weather.enabled', False)

    async def initialize(self):
        """Initialize the weather plugin"""
        if not self.enabled:
            print("Weather plugin is disabled")
            return

        if not self.api_key:
            print("Weather API key not configured")
            return

        # Add commands to the bot
        await self._register_commands()
        print("Weather plugin initialized successfully")

    async def cleanup(self):
        """Cleanup weather plugin"""
        # Remove commands and cleanup resources
        print("Weather plugin cleaned up")

    async def _register_commands(self):
        """Register plugin commands"""
        @app_commands.command(name="weather", description="Get weather information")
        @app_commands.describe(location="Location to get weather for")
        async def weather_command(interaction: discord.Interaction, location: str):
            await self.get_weather(interaction, location)

        # Add command to bot's command tree
        self.bot.tree.add_command(weather_command)

    async def get_weather(self, interaction: discord.Interaction, location: str):
        """Get weather information for a location"""
        await interaction.response.defer()

        try:
            async with aiohttp.ClientSession() as session:
                url = f"http://api.openweathermap.org/data/2.5/weather"
                params = {
                    'q': location,
                    'appid': self.api_key,
                    'units': 'metric'
                }

                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()

                        embed = EmbedFormatter.create_embed(
                            title=f"🌤️ Weather in {data['name']}",
                            description=data['weather'][0]['description'].title()
                        )

                        embed.add_field(
                            name="🌡️ Temperature",
                            value=f"{data['main']['temp']}°C",
                            inline=True
                        )

                        embed.add_field(
                            name="🤔 Feels Like",
                            value=f"{data['main']['feels_like']}°C",
                            inline=True
                        )

                        embed.add_field(
                            name="💧 Humidity",
                            value=f"{data['main']['humidity']}%",
                            inline=True
                        )

                        await interaction.followup.send(embed=embed)
                    else:
                        await interaction.followup.send(f"❌ Could not get weather for {location}")

        except Exception as e:
            await interaction.followup.send(f"❌ Error getting weather: {str(e)}")
```

### Plugin Management Commands

```python
# cogs/plugin_management.py
@app_commands.command(name="plugins", description="Manage bot plugins")
@app_commands.describe(
    action="Action to perform",
    plugin_name="Name of the plugin"
)
@app_commands.choices(action=[
    app_commands.Choice(name="List", value="list"),
    app_commands.Choice(name="Load", value="load"),
    app_commands.Choice(name="Unload", value="unload"),
    app_commands.Choice(name="Reload", value="reload")
])
async def manage_plugins(
    self,
    interaction: discord.Interaction,
    action: str,
    plugin_name: str = None
):
    """Manage plugins"""
    # Owner check
    if interaction.user.id != int(os.getenv('OWNER_ID', 0)):
        await interaction.response.send_message("❌ Only the bot owner can manage plugins.", ephemeral=True)
        return

    plugin_manager = self.bot.plugin_manager

    if action == "list":
        embed = EmbedFormatter.create_embed(
            title="🔌 Installed Plugins",
            command_name="plugins"
        )

        if not plugin_manager.plugins:
            embed.description = "No plugins loaded"
        else:
            for name, plugin in plugin_manager.plugins.items():
                embed.add_field(
                    name=f"📦 {plugin.name}",
                    value=f"Version: {plugin.version}\n{plugin.description}",
                    inline=False
                )

        await interaction.response.send_message(embed=embed)

    elif action in ["load", "unload", "reload"]:
        if not plugin_name:
            await interaction.response.send_message("❌ Plugin name is required for this action.", ephemeral=True)
            return

        await interaction.response.defer()

        if action == "load":
            success = await plugin_manager.load_plugin(plugin_name)
        elif action == "unload":
            success = await plugin_manager.unload_plugin(plugin_name)
        elif action == "reload":
            success = await plugin_manager.reload_plugin(plugin_name)

        if success:
            await interaction.followup.send(f"✅ {action.title()}ed plugin: {plugin_name}")
        else:
            await interaction.followup.send(f"❌ Failed to {action} plugin: {plugin_name}")
```

---

This comprehensive customization guide provides everything you need to extend and modify Logivore according to your specific requirements. Each section includes practical examples and can be implemented independently or combined for more complex customizations.

For additional support or to share your customizations with the community, join our [Discord community](https://discord.gg/serelix) or contribute to the [GitHub repository](https://github.com/kaiyasi/Logivore).
