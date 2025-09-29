"""
Embed Formatter for Logivore
Provides consistent formatting for all Discord embeds
"""
import discord
import datetime
from utils.i18n import i18n

class EmbedFormatter:
    """Handles consistent embed formatting across all cogs"""

    @staticmethod
    def create_embed(title: str, description: str = None, color: int = 0xa2a8a3,
                    command_name: str = None, lang: str = None) -> discord.Embed:
        """
        Create a standardized embed with author and footer

        Args:
            title: Embed title
            description: Embed description
            color: Embed color (default: neutral grey)
            command_name: Name of the command (for author field)
            lang: Language code for localization
        """
        embed = discord.Embed(
            title=title,
            description=description,
            color=color,
            timestamp=datetime.datetime.now(datetime.timezone.utc)
        )

        # Add author if command name provided
        if command_name:
            # Multi-language author text
            if lang in ['zh', 'zh-tw']:
                author_text = f"指令功能：{command_name}"
            elif lang == 'zh-cn':
                author_text = f"指令功能：{command_name}"
            elif lang == 'ko':
                author_text = f"명령 기능: {command_name}"
            elif lang == 'ja':
                author_text = f"コマンド機能: {command_name}"
            elif lang == 'de':
                author_text = f"Befehl: {command_name}"
            elif lang == 'ru':
                author_text = f"Команда: {command_name}"
            else:
                author_text = f"Command: {command_name}"

            embed.set_author(
                name=author_text,
                icon_url="https://cdn.discordapp.com/attachments/1234567890/serelix-icon.png"  # Optional: Add bot icon
            )

        # Add consistent footer with multi-language support
        if lang in ['zh', 'zh-tw']:
            footer_text = "由 Serelix Studio 提供支援"
        elif lang == 'zh-cn':
            footer_text = "由 Serelix Studio 提供支持"
        elif lang == 'ko':
            footer_text = "Serelix Studio에서 제공"
        elif lang == 'ja':
            footer_text = "Serelix Studio 提供"
        elif lang == 'de':
            footer_text = "Powered by Serelix Studio"
        elif lang == 'ru':
            footer_text = "Создано Serelix Studio"
        else:
            footer_text = "Powered by Serelix Studio"

        embed.set_footer(text=footer_text)

        return embed

    @staticmethod
    def success_embed(title: str, description: str = None, command_name: str = None, lang: str = None) -> discord.Embed:
        """Create a success embed (green)"""
        return EmbedFormatter.create_embed(
            title=title,
            description=description,
            color=0x4caf50,
            command_name=command_name,
            lang=lang
        )

    @staticmethod
    def error_embed(title: str, description: str = None, command_name: str = None, lang: str = None) -> discord.Embed:
        """Create an error embed (red)"""
        return EmbedFormatter.create_embed(
            title=title,
            description=description,
            color=0xf44336,
            command_name=command_name,
            lang=lang
        )

    @staticmethod
    def warning_embed(title: str, description: str = None, command_name: str = None, lang: str = None) -> discord.Embed:
        """Create a warning embed (orange)"""
        return EmbedFormatter.create_embed(
            title=title,
            description=description,
            color=0xff9800,
            command_name=command_name,
            lang=lang
        )

    @staticmethod
    def info_embed(title: str, description: str = None, command_name: str = None, lang: str = None) -> discord.Embed:
        """Create an info embed (blue)"""
        return EmbedFormatter.create_embed(
            title=title,
            description=description,
            color=0x2196f3,
            command_name=command_name,
            lang=lang
        )

def create_standard_embed(title: str, description: str = None, color: int = 0xa2a8a3,
                         command_name: str = None, bot=None) -> discord.Embed:
    """
    Convenience function to create standard embed with automatic language detection
    """
    lang = "en"
    if bot and hasattr(bot, 'config'):
        lang = bot.config.get("language", "en")

    return EmbedFormatter.create_embed(title, description, color, command_name, lang)
