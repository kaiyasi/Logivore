# Embed 포맷팅 가이드

언어: 한국어(본 문서) | [繁體中文](../../EMBED_FORMAT_GUIDE.md) | [简体中文](../zh-cn/EMBED_FORMAT_GUIDE.md)

## ✅ 통일된 스타일

- 작성자 정보(명령 기능)
- 타임스탬프
- 푸터(언어별 브랜드 텍스트)

## 지원 타입

### 표준 Embed
```python
from utils.embed_formatter import create_standard_embed
embed = create_standard_embed(title="제목", description="설명", command_name="monitor", bot=self.bot)
```

### 성공/오류/경고/정보
```python
EmbedFormatter.success_embed(title="✅ 성공", description="...", command_name="...", lang="ko")
EmbedFormatter.error_embed(title="❌ 오류", description="...", command_name="...")
EmbedFormatter.warning_embed(title="⚠️ 주의", description="...", command_name="...")
EmbedFormatter.info_embed(title="ℹ️ 정보", description="...", command_name="...")
```

## 커스텀 푸터

```python
embed = create_standard_embed(title="시스템 상태", command_name="monitor", bot=self.bot)
embed.set_footer(text="Serelix Studio에서 제공 • 10초마다 자동 새로고침")
```

