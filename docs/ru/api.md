# Документация API

Языки: Русский | [English](../api.md) | [繁體中文](../zh-tw/api.md) | [简体中文](../zh-cn/api.md)

Этот документ предназначен для разработчиков, которые хотят расширять Logivore,
интегрировать его с другими системами или вносить вклад в кодовую базу.

## Содержание

- [Обзор архитектуры](#обзор-архитектуры)
- [Основные компоненты](#основные-компоненты)
- [Разработка Cog](#разработка-cog)
- [Интернационализация (i18n)](#интернационализация-i18n)
- [Система конфигурации](#система-конфигурации)
- [Форматирование Embed](#форматирование-embed)
- [API мониторинга системы](#api-мониторинга-системы)
- [API интеграции Docker](#api-интеграции-docker)
- [API управления SSL](#api-управления-ssl)
- [API системы оповещений](#api-системы-оповещений)
- [Обработка ошибок](#обработка-ошибок)
- [Система событий](#система-событий)
- [Тестовый фреймворк](#тестовый-фреймворк)

## Обзор архитектуры

Logivore использует модульную архитектуру на основе Cog из Discord.py.
Такой подход обеспечивает чёткое разделение обязанностей и лёгкую расширяемость.

### Структура проекта
```
Logivore/
├── main.py                 # Инициализация бота и базовая настройка
├── config/
│   ├── bot_config.json    # Основной конфигурационный файл
│   └── .env               # Переменные окружения
├── cogs/                  # Модульные функции бота
│   ├── system_monitoring.py
│   ├── docker_management.py
│   ├── alert_management.py
│   ├── ssl_management.py
│   ├── configuration.py
│   ├── bot_management.py
│   └── help_system.py
├── utils/                 # Утилиты
│   ├── embed_formatter.py
│   ├── i18n.py
│   └── config_manager.py
├── languages/             # Файлы локализации
│   ├── en.json
│   ├── zh-tw.json
│   └── ...
└── logs/                  # Журналы
```

### Ключевые принципы

1. Модульность (по Cog)
2. Async-first (неблокирующее выполнение)
3. Полноценная многоязычность
4. Управление через конфигурацию (JSON)
5. Устойчивость к ошибкам

## Основные компоненты

### Инициализация бота

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
        """Загрузка Cogs при старте"""
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

### Менеджер конфигурации

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
        """Загрузка конфигурации из JSON"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self._config = json.load(f)
        except FileNotFoundError:
            self.create_default_config()
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in config file: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """Чтение значений по точечной нотации"""
        keys = key.split('.')
        value = self._config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def set(self, key: str, value: Any) -> None:
        """Запись значений по точечной нотации"""
        keys = key.split('.')
        config = self._config

        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]

        config[keys[-1]] = value
        self.save_config()

    def save_config(self) -> None:
        """Сохранение конфигурации"""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self._config, f, indent=4, ensure_ascii=False)
```

## Разработка Cog

### Базовый шаблон

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
        """Пример slash-команды"""
        try:
            lang = self.config.get(f'guilds.{interaction.guild_id}.language', 'en')
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
        """Стандартная обработка ошибок"""
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

### Расширенный пример (фоновые задачи)

```python
from discord.ext import tasks

class AdvancedCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config_manager
        self.i18n = bot.i18n
        self.background_task.start()

    def cog_unload(self):
        self.background_task.cancel()

    @tasks.loop(seconds=30)
    async def background_task(self):
        try:
            # Периодические операции
            pass
        except Exception as e:
            print(f"Background task error: {e}")

    @background_task.before_loop
    async def before_background_task(self):
        await self.bot.wait_until_ready()
```

## Интернационализация (i18n)

### Реализация

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
        if not os.path.exists(self.languages_dir):
            os.makedirs(self.languages_dir)
            return

        for filename in os.listdir(self.languages_dir):
            if filename.endswith('.json'):
                lang_code = filename[:-5]
                try:
                    with open(os.path.join(self.languages_dir, filename), 'r', encoding='utf-8') as f:
                        self.languages[lang_code] = json.load(f)
                except Exception as e:
                    print(f"Error loading language {lang_code}: {e}")

    def get(self, key: str, lang: str = None, **kwargs) -> str:
        if lang is None:
            lang = self.default_language
        if lang in self.languages:
            text = self._get_nested_key(self.languages[lang], key)
            if text:
                return self._interpolate(text, **kwargs)
        if self.default_language in self.languages:
            text = self._get_nested_key(self.languages[self.default_language], key)
            if text:
                return self._interpolate(text, **kwargs)
        return key

    def _get_nested_key(self, data: Dict, key: str) -> str:
        keys = key.split('.')
        value = data
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return None
        return value if isinstance(value, str) else None

    def _interpolate(self, text: str, **kwargs) -> str:
        for key, value in kwargs.items():
            text = text.replace(f"{{{key}}}", str(value))
        return text
```

### Структура языкового файла

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

## Система конфигурации

### Схема (фрагмент)

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
  "alerts": { "enabled": true },
  "docker": { "enabled": true },
  "ssl": { "enabled": true }
}
```

## API мониторинга системы

### SystemMonitor: сбор сводной статистики

```python
import psutil, asyncio, datetime
from typing import Dict, Any

class SystemMonitor:
    def __init__(self):
        self.previous_net_io = None

    async def get_system_stats(self) -> Dict[str, Any]:
        return {
            'cpu': await self._get_cpu_stats(),
            'memory': await self._get_memory_stats(),
            'disk': await self._get_disk_stats(),
            'network': await self._get_network_stats(),
            'processes': await self._get_process_stats(),
            'timestamp': datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
```

### CPU/сеть (фрагменты)

```python
    async def _get_cpu_stats(self) -> Dict[str, Any]:
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
```

```python
    async def _get_network_stats(self) -> Dict[str, Any]:
        net_io = psutil.net_io_counters()
        now = asyncio.get_event_loop().time()
        stats = {'bytes_sent': net_io.bytes_sent, 'bytes_recv': net_io.bytes_recv}
        if self.previous_net_io and 'timestamp' in self.previous_net_io:
            delta = now - self.previous_net_io['timestamp']
            if delta > 0:
                stats['speed'] = {
                    'upload': max(0, round((net_io.bytes_sent - self.previous_net_io['bytes_sent']) / delta, 1)),
                    'download': max(0, round((net_io.bytes_recv - self.previous_net_io['bytes_recv']) / delta, 1))
                }
        self.previous_net_io = {
            'bytes_sent': net_io.bytes_sent,
            'bytes_recv': net_io.bytes_recv,
            'timestamp': now
        }
        return stats
```

## API интеграции Docker

### Базовые операции

```python
import docker, asyncio

class DockerManager:
    def __init__(self):
        self.client = docker.from_env()

    async def start_container(self, name: str) -> bool:
        c = self.client.containers.get(name)
        await asyncio.get_event_loop().run_in_executor(None, c.start)
        return True

    async def stop_container(self, name: str, timeout: int = 10) -> bool:
        c = self.client.containers.get(name)
        await asyncio.get_event_loop().run_in_executor(None, lambda: c.stop(timeout=timeout))
        return True
```

### Расчёт CPU‑процентов

```python
    def _calculate_cpu_percent(self, stats: Dict) -> float:
        cpu_stats = stats['cpu_stats']
        precpu_stats = stats['precpu_stats']
        cpu_delta = cpu_stats['cpu_usage']['total_usage'] - precpu_stats['cpu_usage']['total_usage']
        system_delta = cpu_stats['system_cpu_usage'] - precpu_stats['system_cpu_usage']
        if system_delta > 0 and cpu_delta > 0:
            return min((cpu_delta / system_delta) * len(cpu_stats['cpu_usage']['percpu_usage']) * 100, 100.0)
        return 0.0
```

## API управления SSL

### Проверка сертификатов

```python
import ssl, socket
from datetime import datetime

class SSLManager:
    async def check_certificate(self, domain: str, port: int = 443) -> Dict[str, Any]:
        ctx = ssl.create_default_context()
        with socket.create_connection((domain, port), timeout=10) as sock:
            with ctx.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
        not_after = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
        return {
            'subject': dict(x[0] for x in cert['subject']),
            'issuer': dict(x[0] for x in cert['issuer']),
            'not_after': not_after.isoformat()
        }
```

## API системы оповещений

### Структура конфигурации (пример)

```json
{
  "alerts": {
    "enabled": true,
    "check_interval": 60,
    "thresholds": { "cpu": 85, "memory": 90, "disk": 95 },
    "channels": { "default": null, "critical": null }
  }
}
```

## Ошибки, события и тесты

- Единые Embed‑ответы об ошибках через `EmbedFormatter`, разделение пользовательского и технического контента
- События при изменении состояния (например, перезапуск контейнера), интеграция с логами и вебхуками
- Pytest + `pytest-asyncio` для асинхронных путей, внешние зависимости мокируются
