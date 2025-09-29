# Руководство по форматированию Embed

Языки: Русский (эта страница) | [繁體中文](../../EMBED_FORMAT_GUIDE.md) | [简体中文](../zh-cn/EMBED_FORMAT_GUIDE.md)

## ✅ Единый стиль

- Автор (функция команды)
- Метка времени
- Нижний колонтитул (бренд, зависит от языка)

## Поддерживаемые типы

### Стандартный Embed
```python
from utils.embed_formatter import create_standard_embed
embed = create_standard_embed(title="Заголовок", description="Описание", command_name="monitor", bot=self.bot)
```

### Успех/Ошибка/Предупреждение/Инфо
```python
EmbedFormatter.success_embed(title="✅ Успех", description="...", command_name="...", lang="ru")
EmbedFormatter.error_embed(title="❌ Ошибка", description="...", command_name="...")
EmbedFormatter.warning_embed(title="⚠️ Внимание", description="...", command_name="...")
EmbedFormatter.info_embed(title="ℹ️ Информация", description="...", command_name="...")
```

## Пользовательский футер

```python
embed = create_standard_embed(title="Состояние системы", command_name="monitor", bot=self.bot)
embed.set_footer(text="Создано Serelix Studio • Автообновление каждые 10с")
```

