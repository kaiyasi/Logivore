# Embed-Formatierungsleitfaden

Sprachen: Deutsch (diese Seite) | [繁體中文](../../EMBED_FORMAT_GUIDE.md) | [简体中文](../zh-cn/EMBED_FORMAT_GUIDE.md)

## ✅ Einheitlicher Embed-Stil

- Autorinfo: zeigt die ausgeführte Befehlsfunktion
- Zeitstempel: automatische Ausführungszeit
- Footer: Markenangabe „Powered by Serelix Studio“ (sprachabhängig)

## Unterstützte Embed-Typen

### Standard-Embed
```python
from utils.embed_formatter import create_standard_embed

embed = create_standard_embed(
    title="Titel",
    description="Beschreibung",
    command_name="monitor",
    bot=self.bot
)
```

### Erfolgs-Embed (grün)
```python
from utils.embed_formatter import EmbedFormatter

embed = EmbedFormatter.success_embed(
    title="✅ Erfolg",
    description="Ausführung abgeschlossen",
    command_name="ssl renew",
    lang="de"
)
```

### Fehler-/Warn-/Info-Embed
```python
EmbedFormatter.error_embed(title="❌ Fehler", description="...", command_name="...")
EmbedFormatter.warning_embed(title="⚠️ Hinweis", description="...", command_name="...")
EmbedFormatter.info_embed(title="ℹ️ Info", description="...", command_name="...")
```

## Mehrsprachigkeit

Autor- und Footertexte werden anhand der Sprache gesetzt (z. B. `de`, `en`, `zh-cn`, `zh-tw`, `ja`, `ko`, `ru`).

## Benutzerdefinierter Footer

```python
embed = create_standard_embed(title="Systemstatus", command_name="monitor", bot=self.bot)
footer_text = "Powered by Serelix Studio • Automatische Aktualisierung alle 10s"
embed.set_footer(text=footer_text)
```

