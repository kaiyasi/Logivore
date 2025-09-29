# 커스터마이제이션 가이드

언어: 한국어 | [English](../customization.md) | [繁體中文](../zh-tw/customization.md) | [简体中文](../zh-cn/customization.md)

이 가이드는 Logivore 기능을 요구사항에 맞게 확장/조정하는 방법을 설명합니다.

## 목차

- [아키텍처 이해](#아키텍처-이해)
- [구성 커스터마이즈](#구성-커스터마이즈)
- [커스텀 명령 추가](#커스텀-명령-추가)
- [커스텀 Cog 생성](#커스텀-cog-생성)
- [임베드 및 UI 조정](#임베드-및-ui-조정)
- [새 언어 추가](#새-언어-추가)
- [맞춤 모니터링 기능](#맞춤-모니터링-기능)
- [알림 시스템 확장](#알림-시스템-확장)
- [Docker 통합 확장](#docker-통합-확장)
- [SSL 관리 확장](#ssl-관리-확장)
- [데이터베이스 통합](#데이터베이스-통합)
- [웹 대시보드 구축](#웹-대시보드-구축)
- [플러그인 시스템 개발](#플러그인-시스템-개발)

## 아키텍처 이해

`main.py`(엔트리), `cogs/`(기능), `utils/`(공용), `config/`(설정), `languages/`(i18n)의 역할과 확장 포인트를 파악합니다.

## 구성 커스터마이즈

### `config/bot_config.json`에 사용자 정의 섹션 추가

```json
{
  "custom_features": {
    "weather_monitoring": {
      "enabled": true,
      "api_key": "your_api_key",
      "locations": ["Seoul", "Busan"],
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

### `.env`에 환경 변수 추가

```bash
# API Key
WEATHER_API_KEY=your_weather_api_key
BACKUP_API_TOKEN=your_backup_token
CUSTOM_WEBHOOK_URL=https://your-webhook.com

# Paths
CUSTOM_LOG_PATH=/var/log/custom
BACKUP_STORAGE_PATH=/mnt/backups

# Feature toggles
ENABLE_WEATHER_MONITORING=true
ENABLE_CUSTOM_BACKUP=true
ENABLE_ADVANCED_LOGGING=false
```

### 구성/환경 접근

```python
class CustomFeatureCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config_manager

        self.weather_enabled = self.config.get('custom_features.weather_monitoring.enabled', False)
        self.backup_path = self.config.get('custom_features.backup_system.backup_path', '/backups')

        self.weather_api_key = os.getenv('WEATHER_API_KEY')
```

## 커스텀 명령 추가

### 간단한 예시

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

    @app_commands.command(name="serverinfo", description="서버 정보를 표시")
    async def server_info(self, interaction: discord.Interaction):
        guild = interaction.guild
        lang = self.config.get(f'guilds.{guild.id}.language', 'en')

        embed = EmbedFormatter.create_embed(
            title=f"📊 {guild.name} 서버 정보",
            command_name="serverinfo",
            lang=lang
        )
        embed.add_field(name="👥 멤버", value=f"{guild.member_count:,}", inline=True)
        embed.add_field(name="📚 역할", value=f"{len(guild.roles):,}", inline=True)
        embed.add_field(name="📢 채널", value=f"{len(guild.channels):,}", inline=True)
        await interaction.response.send_message(embed=embed)
```

## 커스텀 Cog 생성

### 백그라운드 작업 포함 템플릿

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
        # 주기 작업
        pass
```

## 임베드 및 UI 조정

- `utils/embed_formatter.py`로 공통 스타일 적용
- 필요 시 `utils/custom_embed_styles.py` 등으로 추가 스타일 정의

```python
from utils.custom_embed_styles import CustomEmbedStyles
embed = CustomEmbedStyles.create_status_embed(
    title="Service Status",
    status="online",
    details={"cpu": "18%", "mem": "42%"}
)
```

## 새 언어 추가

- `languages/`에 새 JSON을 추가하고 `en.json`의 키를 반영

## 맞춤 모니터링 기능

- 네트워크 스캔, Ping 체크, 장치 탐지 예제를 참고해 확장

## 알림 시스템 확장

- 채널, 임계값, 주기 설정을 구성에 추가

## Docker 통합 확장

- Docker API로 추가 작업/메트릭 구현

## SSL 관리 확장

- 인증서 로테이션, NPM API 인증/호출 워크플로 구성

## 데이터베이스 통합

- `utils/database.py` 등으로 영속화 계층 추가

## 웹 대시보드 구축

- HTTP API 및 프론트엔드 연동(인증/권한 고려)

## 플러그인 시스템 개발

- 표준화된 훅/모듈 디스커버리로 확장점 제공

