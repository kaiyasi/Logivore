# Embed格式化指南

语言：简体中文（本页） | [繁體中文](../../EMBED_FORMAT_GUIDE.md)

## ✅ 已完成的更新

### 统一的 Embed 格式
所有 Logivore/Serelix Bot 的 Embed 采用统一样式，包括：
- 作者信息：显示执行的命令功能
- 时间戳：自动添加执行时间
- 页脚：品牌标识“Powered by Serelix Studio”

### 支持的格式类型

#### 标准 Embed
```python
from utils.embed_formatter import create_standard_embed

embed = create_standard_embed(
    title="标题",
    description="描述",
    command_name="monitor",
    bot=self.bot
)
```

#### 成功 Embed（绿色）
```python
from utils.embed_formatter import EmbedFormatter

embed = EmbedFormatter.success_embed(
    title="✅ 操作成功",
    description="命令执行完成",
    command_name="ssl renew",
    lang="zh-cn"
)
```

#### 错误 Embed（红色）
```python
embed = EmbedFormatter.error_embed(
    title="❌ 操作失败",
    description="发生错误",
    command_name="docker start",
    lang="zh-cn"
)
```

#### 警告 Embed（橙色）
```python
embed = EmbedFormatter.warning_embed(
    title="⚠️ 注意",
    description="需要注意的信息",
    command_name="reboot now",
    lang="zh-cn"
)
```

#### 信息 Embed（蓝色）
```python
embed = EmbedFormatter.info_embed(
    title="ℹ️ 信息",
    description="一般信息",
    command_name="help",
    lang="zh-cn"
)
```

### 多语言支持

作者与页脚会根据语言自动调整，例如：
- zh-cn：作者“指令功能：monitor”，页脚“由 Serelix Studio 提供支持”
- zh/zh-tw：作者“指令功能：monitor”，页脚“由 Serelix Studio 提供支援”
- en：作者“Command: monitor”，页脚“Powered by Serelix Studio”

### 自定义页脚

部分场景需要覆盖页脚（例如监控页 10 秒自动刷新提示）：

```python
embed = create_standard_embed(
    title="系统状态",
    command_name="monitor",
    bot=self.bot
)

lang = self.bot.config.get("language", "en")
if lang == 'zh-cn':
    footer_text = "由 Serelix Studio 提供支持 • 每10秒自动刷新"
elif lang in ['zh', 'zh-tw']:
    footer_text = "由 Serelix Studio 提供支援 • 每10秒自動刷新"
else:
    footer_text = "Powered by Serelix Studio • Auto-refreshing every 10s"
embed.set_footer(text=footer_text)
```

> 其余语言（ko/ja/de/ru）可参照语言文件在 `utils/embed_formatter.py` 中扩展。

