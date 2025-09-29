# Embed フォーマットガイド

言語: 日本語（本ページ） | [繁體中文](../../EMBED_FORMAT_GUIDE.md) | [简体中文](../zh-cn/EMBED_FORMAT_GUIDE.md)

## ✅ 統一スタイル

- 作者情報（コマンド機能）
- タイムスタンプ（実行時間）
- フッター（言語別ブランド表記）

## サポートするタイプ

### 標準 Embed
```python
from utils.embed_formatter import create_standard_embed
embed = create_standard_embed(title="タイトル", description="説明", command_name="monitor", bot=self.bot)
```

### 成功/エラー/警告/情報
```python
EmbedFormatter.success_embed(title="✅ 成功", description="...", command_name="...", lang="ja")
EmbedFormatter.error_embed(title="❌ エラー", description="...", command_name="...")
EmbedFormatter.warning_embed(title="⚠️ 注意", description="...", command_name="...")
EmbedFormatter.info_embed(title="ℹ️ 情報", description="...", command_name="...")
```

## カスタムフッター

```python
embed = create_standard_embed(title="システム状態", command_name="monitor", bot=self.bot)
embed.set_footer(text="Serelix Studio 提供 • 10秒ごとに自動更新")
```

