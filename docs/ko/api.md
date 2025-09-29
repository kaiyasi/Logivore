# API 문서

언어: 한국어 | [English](../api.md) | [繁體中文](../zh-tw/api.md) | [简体中文](../zh-cn/api.md)

이 문서는 Logivore를 확장/통합하거나 기여하려는 개발자를 위한 기술 가이드입니다.

## 목차

- [아키텍처 개요](#아키텍처-개요)
- [핵심 구성 요소](#핵심-구성-요소)
- [Cog 개발](#cog-개발)
- [국제화 (i18n)](#국제화-i18n)
- [구성 시스템](#구성-시스템)
- [임베드 포맷팅](#임베드-포맷팅)
- [시스템 모니터링 API](#시스템-모니터링-api)
- [Docker 통합 API](#docker-통합-api)
- [SSL 관리 API](#ssl-관리-api)
- [알림 시스템 API](#알림-시스템-api)
- [오류 처리](#오류-처리)
- [이벤트 시스템](#이벤트-시스템)
- [테스트 프레임워크](#테스트-프레임워크)

## 아키텍처 개요

Logivore는 Discord.py의 Cog 시스템을 기반으로 한 모듈식 구조를 채택합니다.
관심사 분리와 확장성을 보장하여 유지보수가 용이합니다.

### 프로젝트 구조
```
Logivore/
├── main.py                 # 봇 초기화와 코어 설정
├── config/
│   ├── bot_config.json    # 주요 구성 파일
│   └── .env               # 환경 변수
├── cogs/                  # 기능 모듈
│   ├── system_monitoring.py
│   ├── docker_management.py
│   ├── alert_management.py
│   ├── ssl_management.py
│   ├── configuration.py
│   ├── bot_management.py
│   └── help_system.py
├── utils/                 # 유틸리티
│   ├── embed_formatter.py
│   ├── i18n.py
│   └── config_manager.py
├── languages/             # 다국어 파일
│   ├── en.json
│   ├── zh-tw.json
│   └── ...
└── logs/                  # 로그
```

### 주요 설계 원칙

1. 모듈화(Cog 단위)
2. Async-first(비동기/논블로킹)
3. 다국어(i18n) 지원
4. 구성 주도(JSON 기반 제어)
5. 견고한 오류 복원력

## 핵심 구성 요소

### 봇 초기화

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
        """시작 시 Cog 로드"""
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

### 구성 매니저

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
        """JSON 구성 불러오기"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self._config = json.load(f)
        except FileNotFoundError:
            self.create_default_config()
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in config file: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """점 표기법으로 값 조회"""
        keys = key.split('.')
        value = self._config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def set(self, key: str, value: Any) -> None:
        """점 표기법으로 값 설정"""
        keys = key.split('.')
        config = self._config

        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]

        config[keys[-1]] = value
        self.save_config()

    def save_config(self) -> None:
        """구성 저장"""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self._config, f, indent=4, ensure_ascii=False)
```

## Cog 개발

### 기본 템플릿

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
        """Slash 명령 예시"""
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
        """표준 오류 처리"""
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

### 응용: 백그라운드 작업

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
            # 주기 작업
            pass
        except Exception as e:
            print(f"Background task error: {e}")

    @background_task.before_loop
    async def before_background_task(self):
        await self.bot.wait_until_ready()
```

## 국제화 (i18n)

### 구현

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

### 언어 파일 구조 예시

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

## 구성 시스템

### 스키마 (발췌)

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

## 시스템 모니터링 API

### SystemMonitor: 전체 수집

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

### CPU/네트워크 (발췌)

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

## Docker 통합 API

### 기본 동작

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

### CPU 비율 계산

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

## SSL 관리 API

### 인증서 점검

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

## 알림 시스템 API

### 설정 구조 (예)

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

## 오류 처리 / 이벤트 / 테스트

- `EmbedFormatter`로 표준 오류 응답, 사용자 메시지와 내부 로그를 분리
- 상태 변화 이벤트(예: 컨테이너 재시작) 발생 시 알림/로그/Webhook 연동
- Pytest + `pytest-asyncio`로 비동기 경로를 검증, 외부 의존성은 목 처리
