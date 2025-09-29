import discord
from discord.ext import commands
import os
import asyncio
import json
import logging
from dotenv import load_dotenv
from utils import setup_bot_logging, log_startup_banner, log_system_info, log_cog_status, log_discord_event

# --- CONFIGURATION MANAGEMENT ---
# This is a simplified version for the main file
class ConfigManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.config = self.load_config()

    def load_config(self):
        defaults = {
            "update_interval": 10, 
            "monitored_disks": [],
            "alerts": [],
            "alert_channel": None,
            "alert_interval": 60
        }
        if not os.path.exists(self.file_path):
            self.save_config(defaults)
            return defaults
        try:
            with open(self.file_path, 'r') as f:
                config = json.load(f)
                for key, value in defaults.items():
                    config.setdefault(key, value)
                return config
        except (json.JSONDecodeError, IOError):
            self.save_config(defaults)
            return defaults

    def save_config(self, data):
        try:
            with open(self.file_path, 'w') as f:
                json.dump(data, f, indent=4)
        except IOError as e:
            logger = logging.getLogger("logivore.config")
            logger.error(f"Error saving config file: {e}")

    def get(self, key, default=None):
        return self.config.get(key, default)

    def set(self, key, value):
        self.config[key] = value
        self.save_config(self.config)

# --- BOT INITIALIZATION ---
class Logivore(commands.Bot):
    def __init__(self):
        # Load environment variables first
        load_dotenv()

        # Setup logging
        self.bot_logger = setup_bot_logging()
        self.logger = self.bot_logger.get_logger()

        intents = discord.Intents.default()
        intents.messages = True # Required for some interactions
        super().__init__(command_prefix='/', intents=intents)

        # Attach config and states to the bot instance so Cogs can access them
        self.config = ConfigManager("config.json")
        self.alert_states = {}

        # Initialize i18n with configured language
        from utils.i18n import i18n
        default_lang = self.config.get("language", "en")
        i18n.default_language = default_lang
        self.logger.info(f"Language set to: {default_lang}")

        # Set owner ID from environment variable
        owner_id = os.getenv("BOT_OWNER_ID")
        if owner_id:
            try:
                self.owner_id = int(owner_id)
                self.logger.info(f"Bot owner ID set to: {self.owner_id}")
            except ValueError:
                self.logger.warning(f"Invalid BOT_OWNER_ID format: {owner_id}")
                self.owner_id = None
        else:
            self.owner_id = None
            self.logger.warning("BOT_OWNER_ID not set in .env file")

    async def setup_hook(self):
        self.logger.info("Starting cog loading process...")

        # Define the new cog modules to load
        cog_modules = [
            'cogs.system_monitoring',
            'cogs.alerting',
            'cogs.docker_management',
            'cogs.config_management',
            'cogs.bot_management',
            'cogs.system_reboot',
            'cogs.service_recovery',
            'cogs.help_system',
            'cogs.ssl_management'
        ]

        # Load each cog module
        loaded_count = 0
        for module in cog_modules:
            try:
                await self.load_extension(module)
                log_cog_status(module.split('.')[-1], "loaded")
                loaded_count += 1
            except Exception as e:
                log_cog_status(module.split('.')[-1], "failed", str(e))

        self.logger.info(f"Loaded {loaded_count}/{len(cog_modules)} cogs successfully")

        # Sync slash commands
        try:
            synced = await self.tree.sync()
            self.logger.info(f"Synced {len(synced)} slash commands globally")
        except Exception as e:
            self.logger.error(f"Failed to sync slash commands: {e}")

    async def on_ready(self):
        log_discord_event("🤖 Bot connected successfully!")
        self.logger.info(f"Logged in as {self.user.name} (ID: {self.user.id})")
        self.logger.info(f"Connected to {len(self.guilds)} guild(s)")

        # Log some basic stats
        total_users = sum(guild.member_count for guild in self.guilds if guild.member_count)
        self.logger.info(f"Serving {total_users} total users")

        # Start performance monitoring task
        if not hasattr(self, '_perf_task'):
            self._perf_task = asyncio.create_task(self._performance_monitor())

        log_discord_event("🚀 Bot is ready to serve!")

    async def _performance_monitor(self):
        """Background task to monitor performance"""
        from utils import log_performance_stats
        while True:
            try:
                await asyncio.sleep(300)  # Every 5 minutes
                log_performance_stats()
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.debug(f"Performance monitor error: {e}")

    async def on_guild_join(self, guild):
        """Log when bot joins a new guild"""
        log_discord_event(f"📥 Joined guild: {guild.name} (ID: {guild.id})")

    async def on_guild_remove(self, guild):
        """Log when bot leaves a guild"""
        log_discord_event(f"📤 Left guild: {guild.name} (ID: {guild.id})")

    async def on_command_error(self, ctx, error):
        """Log command errors"""
        self.logger.error(f"Command error in {ctx.command}: {error}")

    async def on_application_command_error(self, interaction, error):
        """Log slash command errors"""
        command_name = interaction.command.name if interaction.command else "unknown"
        self.logger.error(f"Slash command error in /{command_name}: {error}")

    async def close(self):
        """Enhanced close method with cleanup"""
        self.logger.info("🛑 Bot shutdown initiated...")

        # Cancel performance monitoring
        if hasattr(self, '_perf_task'):
            self._perf_task.cancel()

        # Call parent close
        await super().close()
        self.logger.info("👋 Bot shutdown completed")

async def main():
    # Display startup banner
    log_startup_banner()

    # Load environment variables first
    load_dotenv()

    # Setup basic logging for startup
    temp_logger = setup_bot_logging()

    # Log system information
    log_system_info()

    # Check token
    token = os.getenv("DISCORD_TOKEN")
    if not token or token == "YOUR_BOT_TOKEN":
        temp_logger.error("DISCORD_TOKEN is not set. Please check your .env file.")
        return

    temp_logger.info("Environment variables loaded successfully")
    temp_logger.info("Initializing Logivore...")

    bot = Logivore()
    try:
        await bot.start(token)
    except discord.errors.LoginFailure:
        temp_logger.error("Invalid Discord token. Please check your .env file.")
    except KeyboardInterrupt:
        temp_logger.info("Bot shutdown requested by user")
    except Exception as e:
        temp_logger.critical(f"Unexpected error during bot startup: {e}")
        import traceback
        temp_logger.debug(traceback.format_exc())

if __name__ == "__main__":
    asyncio.run(main())
