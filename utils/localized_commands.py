"""
Localized Commands Module for Logivore
Provides decorators and utilities for creating commands with localized descriptions
"""
import discord
from discord.ext import commands
from utils.i18n import i18n

def get_current_language(bot):
    """Get the current language setting"""
    return bot.config.get("language", "en")

def localized_command(description_key: str, **kwargs):
    """
    Decorator for creating commands with localized descriptions
    The description will be set based on the bot's language at startup
    """
    def decorator(func):
        # Store the description key for potential future use
        func._description_key = description_key
        func._command_kwargs = kwargs
        return func
    return decorator

def localized_group(description_key: str, **kwargs):
    """
    Decorator for creating command groups with localized descriptions
    """
    def decorator(cls):
        cls._description_key = description_key
        cls._group_kwargs = kwargs
        return cls
    return decorator

def create_localized_command(bot, name: str, description_key: str, callback, **kwargs):
    """Create a command with localized description"""
    lang = get_current_language(bot)
    description = i18n.get_text(f"commands.{description_key}", lang)

    return discord.app_commands.Command(
        name=name,
        description=description,
        callback=callback,
        **kwargs
    )

def create_localized_group(bot, name: str, description_key: str, **kwargs):
    """Create a command group with localized description"""
    lang = get_current_language(bot)
    description = i18n.get_text(f"commands.{description_key}", lang)

    return discord.app_commands.Group(
        name=name,
        description=description,
        **kwargs
    )

def update_command_descriptions_at_startup(bot):
    """
    Update command descriptions based on current language at startup
    This should be called during bot initialization
    """
    lang = get_current_language(bot)
    i18n.default_language = lang

    # The commands will automatically use the current language
    # when they are registered during cog loading
