# API Documentation

Languages: English | [繁體中文](zh-tw/api.md) | [简体中文](zh-cn/api.md)

This guide provides comprehensive information for developers who want to extend, integrate with, or contribute to Logivore.

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Core Components](#core-components)
- [Cog Development](#cog-development)
- [Internationalization (i18n)](#internationalization-i18n)
- [Configuration System](#configuration-system)
- [Embed Formatting](#embed-formatting)
- [System Monitoring API](#system-monitoring-api)
- [Docker Integration API](#docker-integration-api)
- [SSL Management API](#ssl-management-api)
- [Alert System API](#alert-system-api)
- [Error Handling](#error-handling)
- [Event System](#event-system)
- [Testing Framework](#testing-framework)

## Architecture Overview

Logivore follows a modular architecture using Discord.py's Cog system, allowing for clean separation of concerns and easy extensibility.

### Project Structure
```
Logivore/
├── main.py                 # Bot initialization and core setup
├── config/
│   ├── bot_config.json    # Main configuration file
│   └── .env               # Environment variables
├── cogs/                  # Modular bot functionality
│   ├── system_monitoring.py
│   ├── docker_management.py
│   ├── alert_management.py
│   ├── ssl_management.py
│   ├── configuration.py
│   ├── bot_management.py
│   └── help_system.py
├── utils/                 # Utility modules
│   ├── embed_formatter.py
│   ├── i18n.py
│   └── config_manager.py
├── languages/             # Internationalization files
│   ├── en.json
│   ├── zh-tw.json
│   └── ...
└── logs/                  # Log files
```

### Key Design Principles

1. **Modularity**: Each feature is implemented as a separate cog
2. **Async-First**: All operations use async/await for non-blocking execution
3. **Internationalization**: Full multi-language support from the ground up
4. **Configuration-Driven**: Behavior controlled through JSON configuration
5. **Error Resilience**: Comprehensive error handling and graceful degradation

## Core Components

### Bot Initialization

```python
# main.py
import discord
from discord.ext import commands
from utils.config_manager import ConfigManager
from utils.i18n import I18n

class SerelixBot(commands.Bot):
    def __init__(self):
        self.config_manager = ConfigManager('config/bot_config.json')
        self.i18n = I18n()

        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True

        super().__init__(
            command_prefix='!',
            intents=intents,
            case_insensitive=True
        )

    async def setup_hook(self):
        """Load all cogs during bot startup"""
        cogs = [
            'cogs.system_monitoring',
            'cogs.docker_management',
            'cogs.alert_management',
            'cogs.ssl_management',
            'cogs.configuration',
            'cogs.bot_management',
            'cogs.help_system'
        ]

        for cog in cogs:
            try:
                await self.load_extension(cog)
                print(f"✅ Loaded {cog}")
            except Exception as e:
                print(f"❌ Failed to load {cog}: {e}")
```

### Configuration Manager

```python
# utils/config_manager.py
import json
import os
from typing import Any, Dict, Optional

class ConfigManager:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self._config = {}
        self.load_config()

    def load_config(self) -> None:
        """Load configuration from JSON file"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self._config = json.load(f)
        except FileNotFoundError:
            self.create_default_config()
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in config file: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value with dot notation support"""
        keys = key.split('.')
        value = self._config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def set(self, key: str, value: Any) -> None:
        """Set configuration value with dot notation support"""
        keys = key.split('.')
        config = self._config

        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]

        config[keys[-1]] = value
        self.save_config()

    def save_config(self) -> None:
        """Save configuration to file"""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self._config, f, indent=4, ensure_ascii=False)
```

## Cog Development

### Basic Cog Template

```python
import discord
from discord.ext import commands
from discord import app_commands
from utils.embed_formatter import EmbedFormatter
from typing import Optional

class ExampleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config_manager
        self.i18n = bot.i18n

    @app_commands.command(name="example", description="Example command")
    async def example_command(self, interaction: discord.Interaction):
        """Example slash command implementation"""
        try:
            # Get user's language preference
            lang = self.config.get(f'guilds.{interaction.guild_id}.language', 'en')

            # Create localized embed
            title = self.i18n.get('example.title', lang)
            description = self.i18n.get('example.description', lang)

            embed = EmbedFormatter.create_embed(
                title=title,
                description=description,
                command_name="example",
                lang=lang
            )

            await interaction.response.send_message(embed=embed)

        except Exception as e:
            await self.handle_error(interaction, e)

    async def handle_error(self, interaction: discord.Interaction, error: Exception):
        """Standard error handling for cog commands"""
        lang = self.config.get(f'guilds.{interaction.guild_id}.language', 'en')

        embed = EmbedFormatter.create_embed(
            title=self.i18n.get('error.title', lang),
            description=f"{self.i18n.get('error.generic', lang)}: {str(error)}",
            color=0xff0000,
            command_name="error",
            lang=lang
        )

        if interaction.response.is_done():
            await interaction.followup.send(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(ExampleCog(bot))
```

### Advanced Cog Features

```python
class AdvancedCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config_manager
        self.i18n = bot.i18n
        self.background_task.start()  # Start background task

    def cog_unload(self):
        """Cleanup when cog is unloaded"""
        self.background_task.cancel()

    @tasks.loop(seconds=30)
    async def background_task(self):
        """Example background task"""
        try:
            # Perform periodic operations
            pass
        except Exception as e:
            print(f"Background task error: {e}")

    @background_task.before_loop
    async def before_background_task(self):
        """Wait for bot to be ready before starting task"""
        await self.bot.wait_until_ready()

    @app_commands.command(name="advanced", description="Advanced command with options")
    @app_commands.describe(
        option1="Description for option 1",
        option2="Description for option 2"
    )
    async def advanced_command(
        self,
        interaction: discord.Interaction,
        option1: str,
        option2: Optional[int] = None
    ):
        """Advanced command with parameters and validation"""
        # Parameter validation
        if len(option1) > 100:
            return await self.send_error(interaction, "option1_too_long")

        if option2 and (option2 < 1 or option2 > 100):
            return await self.send_error(interaction, "option2_out_of_range")

        # Command logic here
        await interaction.response.send_message("Success!")
```

## Internationalization (i18n)

### I18n System Implementation

```python
# utils/i18n.py
import json
import os
from typing import Dict, Any

class I18n:
    def __init__(self, languages_dir: str = 'languages'):
        self.languages_dir = languages_dir
        self.languages: Dict[str, Dict[str, Any]] = {}
        self.default_language = 'en'
        self.load_languages()

    def load_languages(self) -> None:
        """Load all language files"""
        if not os.path.exists(self.languages_dir):
            os.makedirs(self.languages_dir)
            return

        for filename in os.listdir(self.languages_dir):
            if filename.endswith('.json'):
                lang_code = filename[:-5]  # Remove .json extension
                try:
                    with open(os.path.join(self.languages_dir, filename), 'r', encoding='utf-8') as f:
                        self.languages[lang_code] = json.load(f)
                except Exception as e:
                    print(f"Error loading language {lang_code}: {e}")

    def get(self, key: str, lang: str = None, **kwargs) -> str:
        """Get localized string with interpolation support"""
        if lang is None:
            lang = self.default_language

        # Try requested language first
        if lang in self.languages:
            text = self._get_nested_key(self.languages[lang], key)
            if text:
                return self._interpolate(text, **kwargs)

        # Fallback to default language
        if self.default_language in self.languages:
            text = self._get_nested_key(self.languages[self.default_language], key)
            if text:
                return self._interpolate(text, **kwargs)

        # Return key if no translation found
        return key

    def _get_nested_key(self, data: Dict, key: str) -> str:
        """Get value from nested dictionary using dot notation"""
        keys = key.split('.')
        value = data

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return None

        return value if isinstance(value, str) else None

    def _interpolate(self, text: str, **kwargs) -> str:
        """Interpolate variables into text"""
        for key, value in kwargs.items():
            text = text.replace(f"{{{key}}}", str(value))
        return text
```

### Language File Structure

```json
{
  "commands": {
    "monitor": {
      "name": "monitor",
      "description": "Display system monitoring dashboard",
      "response": {
        "title": "🖥️ System Monitor - Live Dashboard",
        "cpu": "💾 CPU Usage",
        "memory": "🧠 Memory",
        "disk": "💽 Disk",
        "network": "🌐 Network",
        "updated": "Last Updated"
      }
    }
  },
  "errors": {
    "generic": "An error occurred",
    "permission_denied": "You don't have permission to use this command",
    "invalid_parameter": "Invalid parameter: {parameter}"
  },
  "common": {
    "success": "Success",
    "failed": "Failed",
    "loading": "Loading...",
    "enabled": "Enabled",
    "disabled": "Disabled"
  }
}
```

## Configuration System

### Configuration Schema

```json
{
  "bot": {
    "default_language": "en",
    "owner_id": "759651999036997672",
    "command_prefix": "!",
    "status": "Monitoring systems..."
  },
  "monitoring": {
    "update_interval": 10,
    "enable_smart_monitoring": true,
    "monitored_disks": ["/", "/mnt/data"],
    "network_interfaces": ["eth0", "wlan0"],
    "process_monitoring": {
      "enabled": true,
      "watchdog_processes": ["nginx", "mysql", "redis"]
    }
  },
  "alerts": {
    "enabled": true,
    "check_interval": 60,
    "thresholds": {
      "cpu": 85,
      "memory": 90,
      "disk": 95,
      "temperature": 70
    },
    "channels": {
      "default": null,
      "critical": null
    }
  },
  "docker": {
    "enabled": true,
    "socket_path": "unix:///var/run/docker.sock",
    "auto_restart": true,
    "monitoring": {
      "enabled": true,
      "stats_interval": 30
    }
  },
  "ssl": {
    "enabled": true,
    "nginx_proxy_manager": {
      "enabled": true,
      "api_url": "http://localhost:81/api",
      "email": "admin@example.com",
      "password": "secure_password"
    },
    "auto_renewal": {
      "enabled": true,
      "days_before_expiry": 30,
      "notification_channel": null
    }
  },
  "logging": {
    "level": "INFO",
    "file": "logs/logivore.log",
    "max_size": "10MB",
    "backup_count": 5,
    "format": "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
  },
  "guilds": {}
}
```

### Dynamic Configuration Access

```python
# Example usage in cogs
class ConfigurableCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config_manager

    @app_commands.command(name="settings")
    async def show_settings(self, interaction: discord.Interaction):
        # Get guild-specific or global settings
        guild_id = interaction.guild_id
        update_interval = self.config.get(f'guilds.{guild_id}.monitoring.update_interval') or \
                         self.config.get('monitoring.update_interval', 10)

        # Use the setting
        await self.start_monitoring(update_interval)
```

## Embed Formatting

### Unified Embed System

```python
# utils/embed_formatter.py
import discord
import datetime
from typing import Optional, Dict, Any

class EmbedFormatter:
    # Brand colors
    COLORS = {
        'default': 0xa2a8a3,
        'success': 0x00ff00,
        'warning': 0xffff00,
        'error': 0xff0000,
        'info': 0x0099ff
    }

    # Multi-language author mappings
    COMMAND_AUTHORS = {
        'en': {
            'monitor': '🔍 System Monitoring',
            'docker': '🐳 Docker Management',
            'alerts': '🚨 Alert Management',
            'ssl': '🛡️ SSL Management',
            'config': '⚙️ Configuration',
            'help': '📚 Help System'
        },
        # Add other languages...
    }

    # Multi-language footer texts
    FOOTER_TEXTS = {
        'en': 'Powered by Serelix Studio',
        'zh-tw': '由 Serelix Studio 強力驅動',
        'zh-cn': '由 Serelix Studio 强力驱动',
        'ko': 'Serelix Studio에서 제공',
        'ja': 'Serelix Studio が提供',
        'de': 'Powered by Serelix Studio',
        'ru': 'Работает на Serelix Studio'
    }

    @staticmethod
    def create_embed(
        title: str,
        description: str = None,
        color: int = None,
        command_name: str = None,
        lang: str = 'en',
        **kwargs
    ) -> discord.Embed:
        """Create standardized embed with branding"""
        if color is None:
            color = EmbedFormatter.COLORS['default']

        embed = discord.Embed(
            title=title,
            description=description,
            color=color,
            timestamp=datetime.datetime.now(datetime.timezone.utc)
        )

        # Set author based on command and language
        if command_name and lang in EmbedFormatter.COMMAND_AUTHORS:
            authors = EmbedFormatter.COMMAND_AUTHORS[lang]
            if command_name in authors:
                embed.set_author(name=authors[command_name])

        # Set footer with language support
        footer_text = EmbedFormatter.FOOTER_TEXTS.get(lang, EmbedFormatter.FOOTER_TEXTS['en'])
        embed.set_footer(text=footer_text)

        # Add any additional fields
        for key, value in kwargs.items():
            if key.startswith('field_'):
                field_name = key.replace('field_', '').replace('_', ' ').title()
                embed.add_field(name=field_name, value=value, inline=True)

        return embed

    @staticmethod
    def create_success_embed(title: str, description: str, lang: str = 'en') -> discord.Embed:
        """Create success-styled embed"""
        return EmbedFormatter.create_embed(
            title=f"✅ {title}",
            description=description,
            color=EmbedFormatter.COLORS['success'],
            lang=lang
        )

    @staticmethod
    def create_error_embed(title: str, description: str, lang: str = 'en') -> discord.Embed:
        """Create error-styled embed"""
        return EmbedFormatter.create_embed(
            title=f"❌ {title}",
            description=description,
            color=EmbedFormatter.COLORS['error'],
            lang=lang
        )
```

## System Monitoring API

### System Stats Collection

```python
import psutil
import asyncio
from typing import Dict, List, Any

class SystemMonitor:
    def __init__(self):
        self.network_counters = {}
        self.previous_net_io = None

    async def get_system_stats(self) -> Dict[str, Any]:
        """Get comprehensive system statistics"""
        try:
            # CPU Information
            cpu_stats = await self._get_cpu_stats()

            # Memory Information
            memory_stats = await self._get_memory_stats()

            # Disk Information
            disk_stats = await self._get_disk_stats()

            # Network Information
            network_stats = await self._get_network_stats()

            # Process Information
            process_stats = await self._get_process_stats()

            return {
                'cpu': cpu_stats,
                'memory': memory_stats,
                'disk': disk_stats,
                'network': network_stats,
                'processes': process_stats,
                'timestamp': datetime.datetime.now(datetime.timezone.utc).isoformat()
            }

        except Exception as e:
            raise SystemMonitorError(f"Failed to collect system stats: {e}")

    async def _get_cpu_stats(self) -> Dict[str, Any]:
        """Get CPU statistics"""
        # Use minimal interval to prevent blocking
        cpu_percent = psutil.cpu_percent(interval=0.1)
        cpu_count = psutil.cpu_count()
        cpu_freq = psutil.cpu_freq()

        return {
            'usage_percent': round(cpu_percent, 1),
            'core_count': cpu_count,
            'frequency': {
                'current': round(cpu_freq.current, 1) if cpu_freq else None,
                'min': round(cpu_freq.min, 1) if cpu_freq else None,
                'max': round(cpu_freq.max, 1) if cpu_freq else None
            },
            'load_average': list(psutil.getloadavg()) if hasattr(psutil, 'getloadavg') else None
        }

    async def _get_memory_stats(self) -> Dict[str, Any]:
        """Get memory statistics"""
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()

        return {
            'total': memory.total,
            'available': memory.available,
            'used': memory.used,
            'percent': round(memory.percent, 1),
            'swap': {
                'total': swap.total,
                'used': swap.used,
                'percent': round(swap.percent, 1)
            }
        }

    async def _get_disk_stats(self) -> List[Dict[str, Any]]:
        """Get disk statistics for all mounted disks"""
        disks = []

        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)

                # Get disk I/O statistics
                disk_io = psutil.disk_io_counters(perdisk=True)
                device_name = partition.device.split('/')[-1]
                io_stats = disk_io.get(device_name, None)

                disk_info = {
                    'device': partition.device,
                    'mountpoint': partition.mountpoint,
                    'filesystem': partition.fstype,
                    'total': usage.total,
                    'used': usage.used,
                    'free': usage.free,
                    'percent': round(usage.percent, 1)
                }

                if io_stats:
                    disk_info['io'] = {
                        'read_bytes': io_stats.read_bytes,
                        'write_bytes': io_stats.write_bytes,
                        'read_count': io_stats.read_count,
                        'write_count': io_stats.write_count
                    }

                disks.append(disk_info)

            except PermissionError:
                # Skip inaccessible disks
                continue

        return disks

    async def _get_network_stats(self) -> Dict[str, Any]:
        """Get network statistics with speed calculation"""
        net_io = psutil.net_io_counters()
        current_time = asyncio.get_event_loop().time()

        stats = {
            'bytes_sent': net_io.bytes_sent,
            'bytes_recv': net_io.bytes_recv,
            'packets_sent': net_io.packets_sent,
            'packets_recv': net_io.packets_recv,
            'errors_in': net_io.errin,
            'errors_out': net_io.errout,
            'drops_in': net_io.dropin,
            'drops_out': net_io.dropout
        }

        # Calculate network speed if we have previous data
        if self.previous_net_io and 'timestamp' in self.previous_net_io:
            time_delta = current_time - self.previous_net_io['timestamp']

            if time_delta > 0:
                sent_speed = (net_io.bytes_sent - self.previous_net_io['bytes_sent']) / time_delta
                recv_speed = (net_io.bytes_recv - self.previous_net_io['bytes_recv']) / time_delta

                stats['speed'] = {
                    'upload': max(0, round(sent_speed, 1)),
                    'download': max(0, round(recv_speed, 1))
                }

        # Store current stats for next calculation
        self.previous_net_io = {
            'bytes_sent': net_io.bytes_sent,
            'bytes_recv': net_io.bytes_recv,
            'timestamp': current_time
        }

        return stats

class SystemMonitorError(Exception):
    """Custom exception for system monitoring errors"""
    pass
```

## Docker Integration API

### Docker Manager

```python
import docker
from typing import List, Dict, Any, Optional
import asyncio

class DockerManager:
    def __init__(self):
        try:
            self.client = docker.from_env()
            self.client.ping()  # Test connection
        except Exception as e:
            raise DockerManagerError(f"Failed to connect to Docker: {e}")

    async def get_containers(self, all_containers: bool = True) -> List[Dict[str, Any]]:
        """Get list of containers with their information"""
        try:
            containers = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.client.containers.list(all=all_containers)
            )

            container_info = []
            for container in containers:
                info = {
                    'id': container.id[:12],
                    'name': container.name,
                    'status': container.status,
                    'image': container.image.tags[0] if container.image.tags else container.image.id[:12],
                    'created': container.attrs['Created'],
                    'ports': self._format_ports(container.attrs.get('NetworkSettings', {}).get('Ports', {})),
                    'labels': container.labels
                }

                # Get resource stats for running containers
                if container.status == 'running':
                    try:
                        stats = await self._get_container_stats(container)
                        info['stats'] = stats
                    except Exception:
                        info['stats'] = None

                container_info.append(info)

            return container_info

        except Exception as e:
            raise DockerManagerError(f"Failed to get containers: {e}")

    async def _get_container_stats(self, container) -> Dict[str, Any]:
        """Get real-time stats for a container"""
        stats = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: container.stats(stream=False)
        )

        # Calculate CPU percentage
        cpu_percent = self._calculate_cpu_percent(stats)

        # Calculate memory usage
        memory_usage = stats['memory_stats'].get('usage', 0)
        memory_limit = stats['memory_stats'].get('limit', 0)
        memory_percent = (memory_usage / memory_limit * 100) if memory_limit > 0 else 0

        # Network I/O
        network_rx = 0
        network_tx = 0
        networks = stats.get('networks', {})
        for interface in networks.values():
            network_rx += interface.get('rx_bytes', 0)
            network_tx += interface.get('tx_bytes', 0)

        # Block I/O
        blkio_stats = stats.get('blkio_stats', {})
        block_read = 0
        block_write = 0

        for entry in blkio_stats.get('io_service_bytes_recursive', []):
            if entry['op'] == 'Read':
                block_read += entry['value']
            elif entry['op'] == 'Write':
                block_write += entry['value']

        return {
            'cpu_percent': round(cpu_percent, 1),
            'memory': {
                'usage': memory_usage,
                'limit': memory_limit,
                'percent': round(memory_percent, 1)
            },
            'network': {
                'rx_bytes': network_rx,
                'tx_bytes': network_tx
            },
            'block_io': {
                'read_bytes': block_read,
                'write_bytes': block_write
            }
        }

    def _calculate_cpu_percent(self, stats: Dict) -> float:
        """Calculate CPU percentage from Docker stats"""
        cpu_stats = stats['cpu_stats']
        precpu_stats = stats['precpu_stats']

        cpu_delta = cpu_stats['cpu_usage']['total_usage'] - precpu_stats['cpu_usage']['total_usage']
        system_delta = cpu_stats['system_cpu_usage'] - precpu_stats['system_cpu_usage']

        if system_delta > 0 and cpu_delta > 0:
            cpu_percent = (cpu_delta / system_delta) * len(cpu_stats['cpu_usage']['percpu_usage']) * 100
            return min(cpu_percent, 100.0)

        return 0.0

    async def start_container(self, container_name: str) -> bool:
        """Start a Docker container"""
        try:
            container = self.client.containers.get(container_name)
            await asyncio.get_event_loop().run_in_executor(None, container.start)
            return True
        except docker.errors.NotFound:
            raise DockerManagerError(f"Container '{container_name}' not found")
        except Exception as e:
            raise DockerManagerError(f"Failed to start container: {e}")

    async def stop_container(self, container_name: str, timeout: int = 10) -> bool:
        """Stop a Docker container"""
        try:
            container = self.client.containers.get(container_name)
            await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: container.stop(timeout=timeout)
            )
            return True
        except docker.errors.NotFound:
            raise DockerManagerError(f"Container '{container_name}' not found")
        except Exception as e:
            raise DockerManagerError(f"Failed to stop container: {e}")

    async def restart_container(self, container_name: str, timeout: int = 10) -> bool:
        """Restart a Docker container"""
        try:
            container = self.client.containers.get(container_name)
            await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: container.restart(timeout=timeout)
            )
            return True
        except docker.errors.NotFound:
            raise DockerManagerError(f"Container '{container_name}' not found")
        except Exception as e:
            raise DockerManagerError(f"Failed to restart container: {e}")

    async def get_container_logs(self, container_name: str, lines: int = 50) -> str:
        """Get logs from a Docker container"""
        try:
            container = self.client.containers.get(container_name)
            logs = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: container.logs(tail=lines, timestamps=True)
            )
            return logs.decode('utf-8', errors='replace')
        except docker.errors.NotFound:
            raise DockerManagerError(f"Container '{container_name}' not found")
        except Exception as e:
            raise DockerManagerError(f"Failed to get container logs: {e}")

class DockerManagerError(Exception):
    """Custom exception for Docker manager errors"""
    pass
```

## SSL Management API

### SSL Certificate Manager

```python
import ssl
import socket
import requests
import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

class SSLManager:
    def __init__(self, npm_config: Dict[str, Any] = None):
        self.npm_config = npm_config or {}
        self.session = requests.Session()

        if npm_config:
            self._authenticate_npm()

    def _authenticate_npm(self) -> None:
        """Authenticate with Nginx Proxy Manager"""
        try:
            auth_data = {
                'identity': self.npm_config.get('email'),
                'secret': self.npm_config.get('password')
            }

            response = self.session.post(
                f"{self.npm_config['api_url']}/tokens",
                json=auth_data,
                timeout=10
            )
            response.raise_for_status()

            token = response.json()['token']
            self.session.headers.update({'Authorization': f'Bearer {token}'})

        except Exception as e:
            raise SSLManagerError(f"Failed to authenticate with NPM: {e}")

    async def check_certificate(self, domain: str, port: int = 443) -> Dict[str, Any]:
        """Check SSL certificate for a domain"""
        try:
            context = ssl.create_default_context()

            # Get certificate info
            with socket.create_connection((domain, port), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()

            # Parse certificate information
            not_after = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
            not_before = datetime.strptime(cert['notBefore'], '%b %d %H:%M:%S %Y %Z')

            days_until_expiry = (not_after - datetime.now()).days

            return {
                'domain': domain,
                'subject': dict(x[0] for x in cert['subject']),
                'issuer': dict(x[0] for x in cert['issuer']),
                'version': cert['version'],
                'not_before': not_before.isoformat(),
                'not_after': not_after.isoformat(),
                'days_until_expiry': days_until_expiry,
                'is_valid': days_until_expiry > 0,
                'is_expiring_soon': days_until_expiry <= 30,
                'serial_number': cert['serialNumber'],
                'signature_algorithm': cert.get('signatureAlgorithm'),
                'subject_alt_names': [name[1] for name in cert.get('subjectAltName', [])]
            }

        except Exception as e:
            raise SSLManagerError(f"Failed to check certificate for {domain}: {e}")

    async def get_npm_certificates(self) -> List[Dict[str, Any]]:
        """Get certificates from Nginx Proxy Manager"""
        if not self.npm_config:
            raise SSLManagerError("NPM not configured")

        try:
            response = self.session.get(
                f"{self.npm_config['api_url']}/nginx/certificates",
                timeout=10
            )
            response.raise_for_status()

            certificates = []
            for cert in response.json():
                expires_on = datetime.fromisoformat(cert['expires_on'].replace('Z', '+00:00'))
                days_until_expiry = (expires_on - datetime.now()).days

                certificates.append({
                    'id': cert['id'],
                    'name': cert['nice_name'],
                    'domain_names': cert['domain_names'],
                    'provider': cert['provider'],
                    'expires_on': cert['expires_on'],
                    'days_until_expiry': days_until_expiry,
                    'is_valid': days_until_expiry > 0,
                    'is_expiring_soon': days_until_expiry <= 30
                })

            return certificates

        except Exception as e:
            raise SSLManagerError(f"Failed to get NPM certificates: {e}")

    async def renew_certificate(self, certificate_id: int) -> bool:
        """Renew a certificate in Nginx Proxy Manager"""
        if not self.npm_config:
            raise SSLManagerError("NPM not configured")

        try:
            response = self.session.post(
                f"{self.npm_config['api_url']}/nginx/certificates/{certificate_id}/renew",
                timeout=30
            )
            response.raise_for_status()

            return True

        except Exception as e:
            raise SSLManagerError(f"Failed to renew certificate {certificate_id}: {e}")

class SSLManagerError(Exception):
    """Custom exception for SSL manager errors"""
    pass
```

## Alert System API

### Alert Manager

```python
import asyncio
from typing import Dict, List, Any, Callable, Optional
from datetime import datetime, timedelta
from enum import Enum

class AlertType(Enum):
    CPU = "cpu"
    MEMORY = "memory"
    DISK = "disk"
    NETWORK = "network"
    PROCESS = "process"
    SSL = "ssl"
    DOCKER = "docker"

class AlertSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"

class Alert:
    def __init__(
        self,
        alert_id: str,
        alert_type: AlertType,
        threshold: float,
        severity: AlertSeverity,
        message: str,
        channel_id: Optional[int] = None,
        enabled: bool = True
    ):
        self.id = alert_id
        self.type = alert_type
        self.threshold = threshold
        self.severity = severity
        self.message = message
        self.channel_id = channel_id
        self.enabled = enabled
        self.last_triggered = None
        self.trigger_count = 0
        self.created_at = datetime.now()

class AlertManager:
    def __init__(self, bot, config_manager):
        self.bot = bot
        self.config = config_manager
        self.alerts: Dict[str, Alert] = {}
        self.alert_history: List[Dict[str, Any]] = []
        self.cooldown_period = timedelta(minutes=5)  # Prevent spam

        # Load alerts from config
        self._load_alerts()

    def _load_alerts(self) -> None:
        """Load alerts from configuration"""
        alert_configs = self.config.get('alerts.configured', {})

        for alert_id, config in alert_configs.items():
            alert = Alert(
                alert_id=alert_id,
                alert_type=AlertType(config['type']),
                threshold=config['threshold'],
                severity=AlertSeverity(config.get('severity', 'warning')),
                message=config['message'],
                channel_id=config.get('channel_id'),
                enabled=config.get('enabled', True)
            )
            self.alerts[alert_id] = alert

    def add_alert(
        self,
        alert_type: AlertType,
        threshold: float,
        message: str,
        severity: AlertSeverity = AlertSeverity.WARNING,
        channel_id: Optional[int] = None
    ) -> str:
        """Add a new alert"""
        alert_id = f"{alert_type.value}_{int(datetime.now().timestamp())}"

        alert = Alert(
            alert_id=alert_id,
            alert_type=alert_type,
            threshold=threshold,
            severity=severity,
            message=message,
            channel_id=channel_id
        )

        self.alerts[alert_id] = alert
        self._save_alerts()

        return alert_id

    def remove_alert(self, alert_id: str) -> bool:
        """Remove an alert"""
        if alert_id in self.alerts:
            del self.alerts[alert_id]
            self._save_alerts()
            return True
        return False

    def _save_alerts(self) -> None:
        """Save alerts to configuration"""
        alert_configs = {}

        for alert_id, alert in self.alerts.items():
            alert_configs[alert_id] = {
                'type': alert.type.value,
                'threshold': alert.threshold,
                'severity': alert.severity.value,
                'message': alert.message,
                'channel_id': alert.channel_id,
                'enabled': alert.enabled
            }

        self.config.set('alerts.configured', alert_configs)

    async def check_alerts(self, system_stats: Dict[str, Any]) -> None:
        """Check all alerts against current system stats"""
        for alert in self.alerts.values():
            if not alert.enabled:
                continue

            should_trigger = await self._should_trigger_alert(alert, system_stats)

            if should_trigger:
                await self._trigger_alert(alert, system_stats)

    async def _should_trigger_alert(self, alert: Alert, stats: Dict[str, Any]) -> bool:
        """Check if an alert should be triggered"""
        # Check cooldown period
        if alert.last_triggered:
            time_since_last = datetime.now() - alert.last_triggered
            if time_since_last < self.cooldown_period:
                return False

        # Check alert conditions based on type
        if alert.type == AlertType.CPU:
            current_value = stats.get('cpu', {}).get('usage_percent', 0)
        elif alert.type == AlertType.MEMORY:
            current_value = stats.get('memory', {}).get('percent', 0)
        elif alert.type == AlertType.DISK:
            # Check worst disk usage
            disks = stats.get('disk', [])
            current_value = max((disk.get('percent', 0) for disk in disks), default=0)
        else:
            return False

        return current_value >= alert.threshold

    async def _trigger_alert(self, alert: Alert, stats: Dict[str, Any]) -> None:
        """Trigger an alert notification"""
        alert.last_triggered = datetime.now()
        alert.trigger_count += 1

        # Create alert message
        embed = self._create_alert_embed(alert, stats)

        # Send to configured channel or default channel
        channel_id = alert.channel_id or self.config.get('alerts.channels.default')

        if channel_id:
            try:
                channel = self.bot.get_channel(channel_id)
                if channel:
                    await channel.send(embed=embed)

                    # Add to history
                    self.alert_history.append({
                        'alert_id': alert.id,
                        'triggered_at': alert.last_triggered.isoformat(),
                        'message': alert.message,
                        'stats': stats
                    })

                    # Limit history size
                    if len(self.alert_history) > 100:
                        self.alert_history = self.alert_history[-100:]

            except Exception as e:
                print(f"Failed to send alert {alert.id}: {e}")

    def _create_alert_embed(self, alert: Alert, stats: Dict[str, Any]) -> discord.Embed:
        """Create embed for alert notification"""
        color_map = {
            AlertSeverity.INFO: 0x0099ff,
            AlertSeverity.WARNING: 0xffff00,
            AlertSeverity.CRITICAL: 0xff0000
        }

        embed = discord.Embed(
            title=f"🚨 {alert.severity.value.upper()} Alert",
            description=alert.message,
            color=color_map[alert.severity],
            timestamp=datetime.now()
        )

        # Add relevant stats
        if alert.type == AlertType.CPU:
            current_value = stats.get('cpu', {}).get('usage_percent', 0)
            embed.add_field(
                name="CPU Usage",
                value=f"{current_value}% (Threshold: {alert.threshold}%)",
                inline=True
            )
        elif alert.type == AlertType.MEMORY:
            current_value = stats.get('memory', {}).get('percent', 0)
            embed.add_field(
                name="Memory Usage",
                value=f"{current_value}% (Threshold: {alert.threshold}%)",
                inline=True
            )

        embed.set_footer(text=f"Alert ID: {alert.id}")

        return embed
```

## Error Handling

### Global Error Handler

```python
import traceback
import logging
from discord.ext import commands
import discord

class GlobalErrorHandler:
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger('logivore.errors')

    async def handle_command_error(self, ctx, error):
        """Handle errors from traditional commands"""
        if isinstance(error, commands.CommandNotFound):
            return  # Ignore unknown commands

        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You don't have permission to use this command.")

        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send("❌ I don't have the necessary permissions to execute this command.")

        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"⏱️ Command is on cooldown. Try again in {error.retry_after:.1f}s")

        else:
            # Log unexpected errors
            self.logger.error(f"Unexpected error in command {ctx.command}: {error}")
            self.logger.error(traceback.format_exc())

            await ctx.send("❌ An unexpected error occurred. The issue has been logged.")

    async def handle_app_command_error(self, interaction: discord.Interaction, error):
        """Handle errors from slash commands"""
        if isinstance(error, discord.app_commands.MissingPermissions):
            embed = discord.Embed(
                title="❌ Permission Error",
                description="You don't have permission to use this command.",
                color=0xff0000
            )

        elif isinstance(error, discord.app_commands.CommandOnCooldown):
            embed = discord.Embed(
                title="⏱️ Cooldown",
                description=f"Command is on cooldown. Try again in {error.retry_after:.1f}s",
                color=0xffff00
            )

        else:
            # Log unexpected errors
            self.logger.error(f"Unexpected error in app command {interaction.command}: {error}")
            self.logger.error(traceback.format_exc())

            embed = discord.Embed(
                title="❌ Error",
                description="An unexpected error occurred. The issue has been logged.",
                color=0xff0000
            )

        try:
            if interaction.response.is_done():
                await interaction.followup.send(embed=embed, ephemeral=True)
            else:
                await interaction.response.send_message(embed=embed, ephemeral=True)
        except:
            pass  # Interaction might have timed out
```

## Event System

### Event Dispatcher

```python
from typing import Dict, List, Callable, Any
import asyncio

class EventDispatcher:
    def __init__(self):
        self.listeners: Dict[str, List[Callable]] = {}

    def on(self, event_name: str):
        """Decorator to register event listeners"""
        def decorator(func):
            if event_name not in self.listeners:
                self.listeners[event_name] = []
            self.listeners[event_name].append(func)
            return func
        return decorator

    async def emit(self, event_name: str, *args, **kwargs):
        """Emit an event to all registered listeners"""
        if event_name in self.listeners:
            tasks = []
            for listener in self.listeners[event_name]:
                if asyncio.iscoroutinefunction(listener):
                    tasks.append(listener(*args, **kwargs))
                else:
                    # Run sync functions in executor
                    task = asyncio.get_event_loop().run_in_executor(
                        None, lambda: listener(*args, **kwargs)
                    )
                    tasks.append(task)

            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)

# Usage example
events = EventDispatcher()

@events.on('system_alert')
async def handle_system_alert(alert_data):
    """Handle system alert events"""
    print(f"System alert: {alert_data}")

@events.on('container_status_change')
async def handle_container_change(container_name, old_status, new_status):
    """Handle Docker container status changes"""
    print(f"Container {container_name} changed from {old_status} to {new_status}")
```

## Testing Framework

### Test Utilities

```python
import pytest
import asyncio
import discord
from unittest.mock import AsyncMock, MagicMock
from bot import SerelixBot

class TestBot:
    """Test utilities for Logivore"""

    @pytest.fixture
    async def bot(self):
        """Create a test bot instance"""
        bot = SerelixBot()

        # Mock Discord client methods
        bot.get_channel = MagicMock(return_value=AsyncMock())
        bot.get_user = MagicMock(return_value=AsyncMock())

        yield bot

        await bot.close()

    @pytest.fixture
    def mock_interaction(self):
        """Create a mock Discord interaction"""
        interaction = AsyncMock(spec=discord.Interaction)
        interaction.guild_id = 12345
        interaction.user.id = 67890
        interaction.response = AsyncMock()
        interaction.followup = AsyncMock()

        return interaction

    async def test_system_monitoring_cog(self, bot, mock_interaction):
        """Test system monitoring cog"""
        from cogs.system_monitoring import SystemMonitoringCog

        cog = SystemMonitoringCog(bot)

        # Test monitor command
        await cog.monitor(mock_interaction)

        # Verify interaction was responded to
        assert mock_interaction.response.send_message.called

    async def test_config_manager(self):
        """Test configuration manager"""
        from utils.config_manager import ConfigManager

        config = ConfigManager('test_config.json')

        # Test setting and getting values
        config.set('test.value', 123)
        assert config.get('test.value') == 123

        # Test default values
        assert config.get('nonexistent.key', 'default') == 'default'

    async def test_i18n_system(self):
        """Test internationalization system"""
        from utils.i18n import I18n

        i18n = I18n('test_languages')

        # Test translation
        text = i18n.get('test.message', 'en')
        assert isinstance(text, str)

        # Test interpolation
        text = i18n.get('test.interpolated', 'en', name='TestBot')
        assert 'TestBot' in text

# Run tests
if __name__ == '__main__':
    pytest.main([__file__])
```

## Development Workflow

### Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/kaiyasi/Logivore.git
cd Logivore

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies

# Set up pre-commit hooks
pre-commit install

# Copy configuration template
cp .env.example .env
cp config/bot_config.example.json config/bot_config.json

# Edit configuration files with your settings
nano .env
nano config/bot_config.json
```

### Creating a New Cog

1. **Create the cog file**:
```python
# cogs/my_new_cog.py
import discord
from discord.ext import commands
from discord import app_commands
from utils.embed_formatter import EmbedFormatter

class MyNewCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config_manager
        self.i18n = bot.i18n

    @app_commands.command(name="mynewcommand", description="My new command")
    async def my_new_command(self, interaction: discord.Interaction):
        lang = self.config.get(f'guilds.{interaction.guild_id}.language', 'en')

        embed = EmbedFormatter.create_embed(
            title=self.i18n.get('mynewcog.title', lang),
            description=self.i18n.get('mynewcog.description', lang),
            command_name="mynewcommand",
            lang=lang
        )

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(MyNewCog(bot))
```

2. **Add language strings**:
```json
// languages/en.json
{
  "mynewcog": {
    "title": "My New Feature",
    "description": "This is my new cog functionality"
  }
}
```

3. **Load the cog in main.py**:
```python
# Add to the cogs list in main.py
cogs = [
    'cogs.system_monitoring',
    'cogs.docker_management',
    # ... other cogs
    'cogs.my_new_cog'  # Add your new cog
]
```

### Contributing Guidelines

1. **Code Style**: Follow PEP 8 and use type hints
2. **Documentation**: Document all public methods and classes
3. **Testing**: Write tests for new functionality
4. **Internationalization**: Add translations for all user-facing strings
5. **Error Handling**: Implement proper error handling and logging
6. **Performance**: Use async/await for I/O operations

### Deployment

```bash
# Production deployment with Docker
docker-compose up -d --build

# Monitor logs
docker-compose logs -f logivore

# Update deployment
git pull
docker-compose up -d --build --force-recreate
```

---

This API documentation provides comprehensive information for developers to extend and customize Logivore. For additional help, join our [Discord community](https://discord.gg/serelix) or check [GitHub Issues](https://github.com/kaiyasi/Logivore/issues).
