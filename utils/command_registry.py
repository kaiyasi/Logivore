"""
Dynamic Command Registry for Logivore
Handles command registration with i18n support
"""
import discord
from discord.ext import commands
from utils.i18n import i18n

class DynamicCommandRegistry:
    """Manages dynamic command registration with language support"""

    def __init__(self, bot):
        self.bot = bot
        self.registered_commands = {}

    def get_localized_description(self, command_key: str, lang: str = None) -> str:
        """Get localized description for a command"""
        if lang is None:
            lang = self.bot.config.get("language", "en")
        return i18n.get_text(f"commands.{command_key}", lang)

    async def register_commands_with_language(self, lang: str = None):
        """Register all commands with specified language"""
        if lang is None:
            lang = self.bot.config.get("language", "en")

        # Clear existing commands
        self.bot.tree.clear_commands()

        # Re-register all cogs to get fresh command descriptions
        await self._reload_all_cogs_commands(lang)

        # Sync commands with Discord
        try:
            synced = await self.bot.tree.sync()
            self.bot.logger.info(f"Synced {len(synced)} commands with language: {lang}")
            return len(synced)
        except Exception as e:
            self.bot.logger.error(f"Failed to sync commands: {e}")
            return 0

    async def _reload_all_cogs_commands(self, lang: str):
        """Reload all cog commands with new language"""
        # Store current cogs
        loaded_cogs = list(self.bot.cogs.keys())

        # Temporarily set the i18n language
        original_lang = i18n.default_language
        i18n.default_language = lang

        try:
            # Unload and reload each cog to get new command descriptions
            for cog_name in loaded_cogs:
                cog = self.bot.get_cog(cog_name)
                if cog:
                    # Get the module name
                    module_name = cog.__module__

                    # Unload the cog
                    await self.bot.remove_cog(cog_name)

                    # Reload the module
                    import importlib
                    import sys
                    if module_name in sys.modules:
                        importlib.reload(sys.modules[module_name])

                    # Reload the cog
                    await self.bot.load_extension(module_name)

        except Exception as e:
            self.bot.logger.error(f"Error reloading cogs for language change: {e}")
        finally:
            # Restore original language
            i18n.default_language = original_lang

    def create_localized_command(self, name: str, description_key: str, **kwargs):
        """Create a command with localized description"""
        lang = self.bot.config.get("language", "en")
        description = self.get_localized_description(description_key, lang)

        return discord.app_commands.Command(
            name=name,
            description=description,
            **kwargs
        )

    def create_localized_group(self, name: str, description_key: str, **kwargs):
        """Create a command group with localized description"""
        lang = self.bot.config.get("language", "en")
        description = self.get_localized_description(description_key, lang)

        return discord.app_commands.Group(
            name=name,
            description=description,
            **kwargs
        )

# Helper function to create localized commands
def localized_command(description_key: str, **kwargs):
    """Decorator to create localized commands"""
    def decorator(func):
        # This will be processed when the cog is loaded
        func._localized_description_key = description_key
        func._localized_kwargs = kwargs
        return func
    return decorator

def localized_group(description_key: str, **kwargs):
    """Decorator to create localized groups"""
    def decorator(cls):
        cls._localized_description_key = description_key
        cls._localized_kwargs = kwargs
        return cls
    return decorator
