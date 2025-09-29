"""
Configuration Management Cog for Logivore
Handles bot configuration, settings, and disk monitoring setup
"""
import discord
from discord.ext import commands
import os
from utils.i18n import i18n
from utils.embed_formatter import create_standard_embed, EmbedFormatter

class ConfigManagementCog(commands.Cog):
    """Handles bot configuration and settings management"""

    def __init__(self, bot):
        self.bot = bot

    # Configuration command group
    config_group = discord.app_commands.Group(name="config", description="Configure the monitoring bot.")

    @config_group.command(name="language", description="Set the bot's display language.")
    @discord.app_commands.describe(language="The language to use.")
    @discord.app_commands.choices(language=[
        discord.app_commands.Choice(name="English", value="en"),
        discord.app_commands.Choice(name="中文（繁體）", value="zh"),
        discord.app_commands.Choice(name="简体中文", value="zh-cn"),
        discord.app_commands.Choice(name="繁體中文", value="zh-tw"),
        discord.app_commands.Choice(name="한국어", value="ko"),
        discord.app_commands.Choice(name="日本語", value="ja"),
        discord.app_commands.Choice(name="Deutsch", value="de"),
        discord.app_commands.Choice(name="Русский", value="ru"),
    ])
    async def config_language(self, interaction: discord.Interaction, language: discord.app_commands.Choice[str]):
        """Set the bot's display language"""
        await interaction.response.defer(ephemeral=True)

        lang_code = language.value

        # Check if language is available
        available_langs = i18n.get_available_languages()
        if lang_code not in available_langs:
            await interaction.followup.send(
                f"Language '{lang_code}' is not available. Available languages: {', '.join(available_langs)}",
                ephemeral=True
            )
            return

        # Store language preference in config
        self.bot.config.set("language", lang_code)

        # Update i18n default language
        i18n.default_language = lang_code

        # Reload all cogs to apply new language to command descriptions
        try:
            # Reload all cogs with new language
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

            reload_results = []
            for module in cog_modules:
                try:
                    if module in self.bot.extensions:
                        await self.bot.reload_extension(module)
                        reload_results.append(f"✅ {module.split('.')[-1]}")
                    else:
                        await self.bot.load_extension(module)
                        reload_results.append(f"🔄 {module.split('.')[-1]}")
                except Exception as e:
                    reload_results.append(f"❌ {module.split('.')[-1]}: {str(e)[:50]}")

            # Sync commands with Discord
            synced = await self.bot.tree.sync()

            embed = EmbedFormatter.success_embed(
                title="✅ Language Updated & Commands Reloaded",
                description=f"Language set to {language.name} ({lang_code})",
                command_name="config language"
            )

            embed.add_field(
                name="Modules Reloaded",
                value="\n".join(reload_results),
                inline=False
            )

            embed.add_field(
                name="Commands Synced",
                value=f"{len(synced)} commands synced with Discord",
                inline=False
            )

            await interaction.followup.send(embed=embed, ephemeral=True)

        except Exception as e:
            embed = EmbedFormatter.warning_embed(
                title="⚠️ Language Updated (Partial)",
                description=f"Language set to {language.name} but some modules failed to reload",
                command_name="config language"
            )
            embed.add_field(
                name="Error",
                value=str(e)[:1000],
                inline=False
            )
            await interaction.followup.send(embed=embed, ephemeral=True)

    @config_group.command(name="language_info", description="Show current language settings.")
    async def config_language_info(self, interaction: discord.Interaction):
        """Show current language configuration"""
        current_lang = self.bot.config.get("language", "en")
        available_langs = i18n.get_available_languages()

        embed = create_standard_embed(
            title="Language Configuration",
            command_name="config language_info",
            bot=self.bot
        )
        embed.add_field(
            name="Current Language",
            value=f"`{current_lang}`",
            inline=True
        )
        embed.add_field(
            name="Available Languages",
            value=", ".join([f"`{lang}`" for lang in available_langs]),
            inline=True
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @config_group.command(name="interval", description="Set the update interval for the monitor panel.")
    @discord.app_commands.describe(seconds="The update interval in seconds (minimum 5).")
    async def config_interval(self, interaction: discord.Interaction, seconds: int):
        """Set the monitoring update interval"""
        if seconds < 5:
            await interaction.response.send_message(
                "Update interval must be 5 seconds or more.",
                ephemeral=True
            )
            return

        self.bot.config.set("update_interval", seconds)
        await interaction.response.send_message(
            f"Update interval set to {seconds} seconds. This will apply to new monitors.",
            ephemeral=True
        )

    @config_group.command(name="disks", description="Manage the list of monitored disk paths.")
    @discord.app_commands.describe(
        action="Choose an action.",
        path="The disk path to add or remove (e.g., /mnt/data)."
    )
    @discord.app_commands.choices(action=[
        discord.app_commands.Choice(name="add", value="add"),
        discord.app_commands.Choice(name="remove", value="remove"),
        discord.app_commands.Choice(name="list", value="list"),
        discord.app_commands.Choice(name="auto", value="auto"),
    ])
    async def config_disks(
        self,
        interaction: discord.Interaction,
        action: discord.app_commands.Choice[str],
        path: str = None
    ):
        """Manage monitored disk paths"""
        current_disks = self.bot.config.get("monitored_disks") or []

        if action.value == "add":
            if not path:
                await interaction.response.send_message(
                    "Path parameter is required for add action.",
                    ephemeral=True
                )
                return

            if not os.path.isdir(path):
                await interaction.response.send_message(
                    f"Invalid path provided: `{path}` is not a valid directory.",
                    ephemeral=True
                )
                return

            if path in current_disks:
                await interaction.response.send_message(
                    "Path already monitored.",
                    ephemeral=True
                )
                return

            current_disks.append(path)
            self.bot.config.set("monitored_disks", current_disks)
            await interaction.response.send_message(
                f"Added `{path}` to monitored disks.",
                ephemeral=True
            )

        elif action.value == "remove":
            if not path:
                await interaction.response.send_message(
                    "Path parameter is required for remove action.",
                    ephemeral=True
                )
                return

            if path not in current_disks:
                await interaction.response.send_message(
                    "Path not found in monitored disks list.",
                    ephemeral=True
                )
                return

            current_disks.remove(path)
            self.bot.config.set("monitored_disks", current_disks)
            await interaction.response.send_message(
                f"Removed `{path}` from monitored disks.",
                ephemeral=True
            )

        elif action.value == "list":
            if not current_disks:
                await interaction.response.send_message(
                    "No custom disk paths configured. Using auto-detection.",
                    ephemeral=True
                )
                return

            disk_list = "\n".join([f"- `{d}`" for d in current_disks])
            await interaction.response.send_message(
                f"**Monitored Disks:**\n{disk_list}",
                ephemeral=True
            )

        elif action.value == "auto":
            self.bot.config.set("monitored_disks", [])
            await interaction.response.send_message(
                "Disk monitoring set to auto-detection mode.",
                ephemeral=True
            )

    @config_group.command(name="alert_interval", description="Set the alert checking interval.")
    @discord.app_commands.describe(seconds="The alert checking interval in seconds (minimum 30).")
    async def config_alert_interval(self, interaction: discord.Interaction, seconds: int):
        """Set the alert checking interval"""
        if seconds < 30:
            await interaction.response.send_message(
                "Alert interval must be 30 seconds or more.",
                ephemeral=True
            )
            return

        self.bot.config.set("alert_interval", seconds)
        await interaction.response.send_message(
            f"Alert checking interval set to {seconds} seconds. Restart required to take effect.",
            ephemeral=True
        )

    @config_group.command(name="show", description="Show current bot configuration.")
    async def config_show(self, interaction: discord.Interaction):
        """Display current bot configuration"""
        config = self.bot.config.config

        embed = create_standard_embed(
            title="Bot Configuration",
            command_name="config show",
            bot=self.bot
        )

        # Basic settings
        embed.add_field(
            name="Update Interval",
            value=f"{config.get('update_interval', 10)} seconds",
            inline=True
        )

        embed.add_field(
            name="Alert Interval",
            value=f"{config.get('alert_interval', 60)} seconds",
            inline=True
        )

        # Alert channel
        alert_channel_id = config.get('alert_channel')
        if alert_channel_id:
            channel = self.bot.get_channel(alert_channel_id)
            channel_name = channel.mention if channel else f"Unknown ({alert_channel_id})"
        else:
            channel_name = "Not set"

        embed.add_field(
            name="Alert Channel",
            value=channel_name,
            inline=True
        )

        # Monitored disks
        monitored_disks = config.get('monitored_disks', [])
        if monitored_disks:
            disk_list = "\n".join([f"• `{disk}`" for disk in monitored_disks])
        else:
            disk_list = "Auto-detection enabled"

        embed.add_field(
            name="Monitored Disks",
            value=disk_list,
            inline=False
        )

        # Alerts count
        alerts_count = len(config.get('alerts', []))
        enabled_alerts = len([a for a in config.get('alerts', []) if a.get('enabled', True)])

        embed.add_field(
            name="Alerts",
            value=f"{enabled_alerts}/{alerts_count} enabled",
            inline=True
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @config_group.command(name="reset", description="Reset configuration to defaults.")
    @discord.app_commands.describe(
        confirm="Type 'CONFIRM' to reset all configuration to defaults."
    )
    async def config_reset(self, interaction: discord.Interaction, confirm: str):
        """Reset configuration to default values"""
        if confirm != "CONFIRM":
            await interaction.response.send_message(
                "To reset configuration, you must type exactly 'CONFIRM' as the confirm parameter.",
                ephemeral=True
            )
            return

        defaults = {
            "update_interval": 10,
            "monitored_disks": [],
            "alerts": [],
            "alert_channel": None,
            "alert_interval": 60
        }

        # Clear alert states
        self.bot.alert_states.clear()

        # Save default config
        self.bot.config.save_config(defaults)
        self.bot.config.config = defaults

        embed = EmbedFormatter.warning_embed(
            title="Configuration Reset",
            description="All configuration has been reset to default values.",
            command_name="config reset"
        )

        embed.add_field(
            name="Default Values",
            value=(
                "• Update Interval: 10 seconds\n"
                "• Alert Interval: 60 seconds\n"
                "• Monitored Disks: Auto-detection\n"
                "• Alert Channel: Not set\n"
                "• Alerts: None"
            ),
            inline=False
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @config_group.command(name="export", description="Export current configuration.")
    async def config_export(self, interaction: discord.Interaction):
        """Export current configuration as JSON"""
        import json

        config_data = self.bot.config.config.copy()

        # Remove sensitive or non-portable data
        if 'alert_channel' in config_data:
            config_data['alert_channel'] = None

        # Format JSON nicely
        config_json = json.dumps(config_data, indent=2, ensure_ascii=False)

        # Create a file-like object
        import io
        config_file = io.BytesIO(config_json.encode('utf-8'))

        await interaction.response.send_message(
            "Current configuration exported:",
            file=discord.File(config_file, filename="serelix_config.json"),
            ephemeral=True
        )

    @config_group.command(name="backup", description="Create a backup of current configuration.")
    async def config_backup(self, interaction: discord.Interaction):
        """Create a backup of the current configuration"""
        import shutil
        from datetime import datetime

        try:
            # Create backup filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"config_backup_{timestamp}.json"

            # Copy current config file
            shutil.copy2(self.bot.config.file_path, backup_filename)

            await interaction.response.send_message(
                f"Configuration backed up to `{backup_filename}`",
                ephemeral=True
            )

        except Exception as e:
            await interaction.response.send_message(
                f"Failed to create backup: {e}",
                ephemeral=True
            )

async def setup(bot):
    """Setup function for loading the cog"""
    await bot.add_cog(ConfigManagementCog(bot))
