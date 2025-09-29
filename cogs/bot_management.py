"""
Bot Management Cog for Logivore
Handles bot administration, module reloading, and system management
"""
import discord
from discord.ext import commands
import sys
import importlib
import traceback
import psutil
import os
import subprocess
import datetime
import asyncio
import logging
from utils import log_cog_status
from utils.i18n import i18n
from utils.embed_formatter import create_standard_embed, EmbedFormatter

class BotManagementCog(commands.Cog):
    """Handles bot administration and management functions"""

    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger("logivore.management")
        self.available_cogs = [
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

    def cog_check(self, ctx):
        """Only allow bot owner to use management commands"""
        return ctx.author.id == self.bot.owner_id

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        """Only allow bot owner to use management slash commands"""
        if not self.bot.owner_id:
            # If owner_id is not set, try to get it
            app_info = await self.bot.application_info()
            self.bot.owner_id = app_info.owner.id

        if interaction.user.id != self.bot.owner_id:
            await interaction.response.send_message(
                i18n.t('management.owner_only'),
                ephemeral=True
            )
            return False
        return True

    # Management command group
    manage_group = discord.app_commands.Group(name="manage", description="Bot management commands (Owner only)")

    @manage_group.command(name="reload", description="Reload a specific cog module.")
    @discord.app_commands.describe(module="The cog module to reload.")
    @discord.app_commands.choices(module=[
        discord.app_commands.Choice(name="System Monitoring", value="cogs.system_monitoring"),
        discord.app_commands.Choice(name="Alerting", value="cogs.alerting"),
        discord.app_commands.Choice(name="Docker Management", value="cogs.docker_management"),
        discord.app_commands.Choice(name="Config Management", value="cogs.config_management"),
        discord.app_commands.Choice(name="Bot Management", value="cogs.bot_management"),
        discord.app_commands.Choice(name="System Reboot", value="cogs.system_reboot"),
        discord.app_commands.Choice(name="Service Recovery", value="cogs.service_recovery"),
        discord.app_commands.Choice(name="Help System", value="cogs.help_system"),
        discord.app_commands.Choice(name="SSL Management", value="cogs.ssl_management"),
    ])
    async def reload_cog(self, interaction: discord.Interaction, module: discord.app_commands.Choice[str]):
        """Reload a specific cog module"""
        await interaction.response.defer(ephemeral=True)

        try:
            # Unload the extension if it's loaded
            if module.value in self.bot.extensions:
                await self.bot.unload_extension(module.value)

            # Reload the Python module
            if module.value in sys.modules:
                importlib.reload(sys.modules[module.value])

            # Load the extension again
            await self.bot.load_extension(module.value)

            # Log the reload
            log_cog_status(module.name, "reloaded")
            self.logger.info(f"Module {module.name} reloaded by {interaction.user.name}")

            embed = EmbedFormatter.success_embed(
                title=i18n.t('management.module_reloaded'),
                description=i18n.t('management.reload_success', module=module.name),
                command_name="manage reload"
            )

            await interaction.followup.send(embed=embed, ephemeral=True)

        except Exception as e:
            error_trace = traceback.format_exc()
            embed = EmbedFormatter.error_embed(
                title=i18n.t('management.reload_failed'),
                description=i18n.t('management.reload_error', module=module.name),
                command_name="manage reload"
            )
            embed.add_field(
                name=i18n.t('common.error'),
                value=f"```python\n{str(e)[:1000]}\n```",
                inline=False
            )
            embed.add_field(
                name="Traceback",
                value=f"```python\n{error_trace[-1000:]}\n```",
                inline=False
            )

            await interaction.followup.send(embed=embed, ephemeral=True)

    @manage_group.command(name="reload_all", description="Reload all cog modules.")
    async def reload_all_cogs(self, interaction: discord.Interaction):
        """Reload all cog modules"""
        await interaction.response.defer(ephemeral=True)

        results = []
        for module in self.available_cogs:
            try:
                # Unload the extension if it's loaded
                if module in self.bot.extensions:
                    await self.bot.unload_extension(module)

                # Reload the Python module
                if module in sys.modules:
                    importlib.reload(sys.modules[module])

                # Load the extension again
                await self.bot.load_extension(module)
                results.append(f"✅ {module}")

            except Exception as e:
                results.append(f"❌ {module}: {str(e)[:100]}")

        embed = EmbedFormatter.warning_embed(
            title="🔄 Bulk Reload Results",
            description="\n".join(results),
            command_name="manage reload_all"
        )

        await interaction.followup.send(embed=embed, ephemeral=True)

    @manage_group.command(name="sync", description="Sync slash commands with Discord.")
    async def sync_commands(self, interaction: discord.Interaction):
        """Manually sync slash commands"""
        await interaction.response.defer(ephemeral=True)

        try:
            synced = await self.bot.tree.sync()
            embed = EmbedFormatter.success_embed(
                title="✅ Commands Synced",
                description=f"Successfully synced {len(synced)} commands",
                command_name="manage sync"
            )

            await interaction.followup.send(embed=embed, ephemeral=True)

        except Exception as e:
            embed = EmbedFormatter.error_embed(
                title="❌ Sync Failed",
                description=f"Failed to sync commands: {str(e)}",
                command_name="manage sync"
            )

            await interaction.followup.send(embed=embed, ephemeral=True)

    @manage_group.command(name="sync_commands_lang", description="Sync commands with current language descriptions.")
    async def sync_commands_lang(self, interaction: discord.Interaction):
        """Sync commands with current language"""
        await interaction.response.defer(ephemeral=True)

        try:
            current_lang = self.bot.config.get("language", "en")

            # Show warning about Discord limitations
            embed = EmbedFormatter.warning_embed(
                title="⚠️ Discord Limitation",
                description="Discord does not allow dynamic command description changes. Command descriptions are set when the bot starts.",
                command_name="manage sync_commands_lang"
            )

            embed.add_field(
                name="Current Language",
                value=f"`{current_lang}`",
                inline=True
            )

            embed.add_field(
                name="Solution",
                value="1. Change language with `/config language`\n2. Restart the bot to apply new command descriptions\n3. Or use `/manage reload_all` to reload all modules",
                inline=False
            )

            embed.add_field(
                name="Note",
                value="All command responses are already using the selected language, only the descriptions shown in Discord are fixed.",
                inline=False
            )

            await interaction.followup.send(embed=embed, ephemeral=True)

        except Exception as e:
            await interaction.followup.send(
                f"Error: {str(e)}",
                ephemeral=True
            )

    @manage_group.command(name="status", description="Show bot status and information.")
    async def bot_status(self, interaction: discord.Interaction):
        """Display comprehensive bot status"""
        await interaction.response.defer(ephemeral=True)

        # Bot information
        uptime = discord.utils.utcnow() - self.bot.user.created_at if self.bot.user else None

        # System information
        process = psutil.Process()
        memory_usage = process.memory_info().rss / 1024 / 1024  # MB
        cpu_percent = process.cpu_percent()

        # Loaded extensions
        loaded_cogs = list(self.bot.extensions.keys())

        # Guild count
        guild_count = len(self.bot.guilds)

        embed = create_standard_embed(
            title="🤖 Bot Status",
            command_name="manage status",
            bot=self.bot
        )

        embed.add_field(
            name="Bot Information",
            value=(
                f"• Name: {self.bot.user.name}\n"
                f"• ID: {self.bot.user.id}\n"
                f"• Guilds: {guild_count}\n"
                f"• Python: {sys.version.split()[0]}"
            ),
            inline=True
        )

        embed.add_field(
            name="System Resources",
            value=(
                f"• Memory: {memory_usage:.1f} MB\n"
                f"• CPU: {cpu_percent:.1f}%\n"
                f"• Latency: {self.bot.latency*1000:.1f}ms"
            ),
            inline=True
        )

        embed.add_field(
            name="Loaded Modules",
            value="\n".join([f"• `{cog.split('.')[-1]}`" for cog in loaded_cogs]) or "None",
            inline=False
        )

        # Configuration status
        config_status = []
        config_status.append(f"• Update Interval: {self.bot.config.get('update_interval')}s")
        config_status.append(f"• Alert Interval: {self.bot.config.get('alert_interval')}s")
        config_status.append(f"• Alerts: {len(self.bot.config.get('alerts', []))}")
        config_status.append(f"• Alert States: {len(self.bot.alert_states)}")

        embed.add_field(
            name="Configuration",
            value="\n".join(config_status),
            inline=False
        )

        await interaction.followup.send(embed=embed, ephemeral=True)

    @manage_group.command(name="logs", description="Show recent bot logs.")
    @discord.app_commands.describe(lines="Number of lines to show (default: 20)")
    async def show_logs(self, interaction: discord.Interaction, lines: int = 20):
        """Show recent log output"""
        await interaction.response.defer(ephemeral=True)

        try:
            # Try to read from systemd logs if available
            try:
                result = subprocess.run(
                    ["journalctl", "-u", "serelix-bot", "-n", str(lines), "--no-pager"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0:
                    logs = result.stdout
                else:
                    raise subprocess.CalledProcessError(result.returncode, "journalctl")
            except (subprocess.CalledProcessError, FileNotFoundError):
                # Fallback to checking for log files
                log_files = ["/var/log/logivore.log", "bot.log", "logivore.log"]
                logs = None

                for log_file in log_files:
                    if os.path.exists(log_file):
                        with open(log_file, 'r') as f:
                            lines_list = f.readlines()
                            logs = ''.join(lines_list[-lines:])
                        break

                if not logs:
                    logs = "No log files found. Consider setting up logging."

            # Truncate if too long for Discord
            if len(logs) > 1900:
                logs = "..." + logs[-1900:]

            embed = create_standard_embed(
                title="📋 Recent Logs",
                description=f"```\n{logs}\n```",
                command_name="manage logs",
                bot=self.bot
            )

            await interaction.followup.send(embed=embed, ephemeral=True)

        except Exception as e:
            await interaction.followup.send(
                f"Error retrieving logs: {str(e)}",
                ephemeral=True
            )

    @manage_group.command(name="restart", description="Restart the bot (if running as systemd service).")
    async def restart_bot(self, interaction: discord.Interaction):
        """Restart the bot if running as a systemd service"""
        await interaction.response.defer(ephemeral=True)

        try:
            # Check if running as systemd service
            result = subprocess.run(
                ["systemctl", "is-active", "logivore"],
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode == 0:
                # Service is active, restart it
                embed = EmbedFormatter.warning_embed(
                    title="🔄 Restarting Bot",
                    description="Attempting to restart bot service...",
                    command_name="manage restart"
                )
                await interaction.followup.send(embed=embed, ephemeral=True)

                # Restart the service
                subprocess.run(
                    ["sudo", "systemctl", "restart", "logivore"],
                    timeout=10
                )

            else:
                embed = EmbedFormatter.error_embed(
                    title="❌ Restart Failed",
                    description="Bot is not running as a systemd service. Manual restart required.",
                    command_name="manage restart"
                )
                await interaction.followup.send(embed=embed, ephemeral=True)

        except subprocess.TimeoutExpired:
            await interaction.followup.send(
                "Restart command timed out.",
                ephemeral=True
            )
        except Exception as e:
            await interaction.followup.send(
                f"Error during restart: {str(e)}",
                ephemeral=True
            )

    @manage_group.command(name="shutdown", description="Gracefully shutdown the bot.")
    async def shutdown_bot(self, interaction: discord.Interaction):
        """Gracefully shutdown the bot"""
        embed = EmbedFormatter.error_embed(
            title="🛑 Shutting Down",
            description="Bot is shutting down gracefully...",
            command_name="manage shutdown"
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)

        # Give time for the response to send
        await asyncio.sleep(1)

        # Close the bot
        await self.bot.close()

    @manage_group.command(name="eval", description="Evaluate Python code (DANGEROUS - Owner only).")
    @discord.app_commands.describe(code="Python code to evaluate")
    async def eval_code(self, interaction: discord.Interaction, code: str):
        """Evaluate Python code - for debugging only"""
        await interaction.response.defer(ephemeral=True)

        try:
            # Create a safe environment
            env = {
                'bot': self.bot,
                'interaction': interaction,
                'discord': discord,
                'self': self,
                '__import__': __import__
            }

            # Execute the code
            result = eval(code, env)

            # Handle async results
            if hasattr(result, '__await__'):
                result = await result

            embed = EmbedFormatter.success_embed(
                title="✅ Code Executed",
                command_name="manage eval"
            )
            embed.add_field(
                name="Input",
                value=f"```python\n{code[:500]}\n```",
                inline=False
            )
            embed.add_field(
                name="Output",
                value=f"```python\n{str(result)[:1000]}\n```",
                inline=False
            )

            await interaction.followup.send(embed=embed, ephemeral=True)

        except Exception as e:
            embed = EmbedFormatter.error_embed(
                title="❌ Execution Error",
                command_name="manage eval"
            )
            embed.add_field(
                name="Input",
                value=f"```python\n{code[:500]}\n```",
                inline=False
            )
            embed.add_field(
                name="Error",
                value=f"```python\n{str(e)[:1000]}\n```",
                inline=False
            )

            await interaction.followup.send(embed=embed, ephemeral=True)

async def setup(bot):
    """Setup function for loading the cog"""
    await bot.add_cog(BotManagementCog(bot))
