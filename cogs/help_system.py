"""
Help System Cog for Logivore
Provides comprehensive help and command documentation
"""
import discord
from discord.ext import commands
from utils.i18n import i18n
from utils.embed_formatter import create_standard_embed

class HelpSystemCog(commands.Cog):
    """Provides help and documentation for bot commands"""

    def __init__(self, bot):
        self.bot = bot

    def get_command_categories(self, lang='en'):
        """Get categorized commands with descriptions"""
        return {
            "system": {
                "title": i18n.t("help.system_monitoring", lang),
                "emoji": "🖥️",
                "commands": [
                    {
                        "name": "/monitor",
                        "desc": i18n.t("commands.monitor_desc", lang)
                    },
                    {
                        "name": "/ports",
                        "desc": i18n.t("commands.ports_desc", lang)
                    }
                ]
            },
            "alerts": {
                "title": i18n.t("help.alert_system", lang),
                "emoji": "🚨",
                "commands": [
                    {
                        "name": "/alert add disk",
                        "desc": i18n.t("commands.alert_add_disk_desc", lang)
                    },
                    {
                        "name": "/alert add cpu",
                        "desc": i18n.t("commands.alert_add_cpu_desc", lang)
                    },
                    {
                        "name": "/alert add process",
                        "desc": i18n.t("commands.alert_add_process_desc", lang)
                    },
                    {
                        "name": "/alert list",
                        "desc": i18n.t("commands.alert_list_desc", lang)
                    },
                    {
                        "name": "/alert remove",
                        "desc": i18n.t("commands.alert_remove_desc", lang)
                    },
                    {
                        "name": "/alert set_channel",
                        "desc": i18n.t("commands.alert_set_channel_desc", lang)
                    }
                ]
            },
            "docker": {
                "title": i18n.t("help.docker_management", lang),
                "emoji": "🐳",
                "commands": [
                    {
                        "name": "/docker start",
                        "desc": i18n.t("commands.docker_start_desc", lang)
                    },
                    {
                        "name": "/docker stop",
                        "desc": i18n.t("commands.docker_stop_desc", lang)
                    },
                    {
                        "name": "/docker restart",
                        "desc": i18n.t("commands.docker_restart_desc", lang)
                    },
                    {
                        "name": "/docker ps",
                        "desc": i18n.t("commands.docker_ps_desc", lang)
                    },
                    {
                        "name": "/docker stats",
                        "desc": i18n.t("commands.docker_stats_desc", lang)
                    },
                    {
                        "name": "/docker logs",
                        "desc": i18n.t("commands.docker_logs_desc", lang)
                    }
                ]
            },
            "reboot": {
                "title": i18n.t("help.system_reboot", lang),
                "emoji": "🔄",
                "commands": [
                    {
                        "name": "/reboot now",
                        "desc": i18n.t("commands.reboot_now_desc", lang)
                    },
                    {
                        "name": "/reboot schedule",
                        "desc": i18n.t("commands.reboot_schedule_desc", lang)
                    },
                    {
                        "name": "/reboot status",
                        "desc": i18n.t("commands.reboot_status_desc", lang)
                    },
                    {
                        "name": "/reboot cancel",
                        "desc": i18n.t("commands.reboot_cancel_desc", lang)
                    },
                    {
                        "name": "/reboot config",
                        "desc": i18n.t("commands.reboot_config_desc", lang)
                    }
                ]
            },
            "recovery": {
                "title": i18n.t("help.service_recovery", lang),
                "emoji": "🛠️",
                "commands": [
                    {
                        "name": "/recovery save_state",
                        "desc": i18n.t("commands.recovery_save_state_desc", lang)
                    },
                    {
                        "name": "/recovery recover_now",
                        "desc": i18n.t("commands.recovery_recover_now_desc", lang)
                    },
                    {
                        "name": "/recovery status",
                        "desc": i18n.t("commands.recovery_status_desc", lang)
                    },
                    {
                        "name": "/recovery config",
                        "desc": i18n.t("commands.recovery_config_desc", lang)
                    }
                ]
            },
            "config": {
                "title": i18n.t("help.configuration", lang),
                "emoji": "⚙️",
                "commands": [
                    {
                        "name": "/config language",
                        "desc": i18n.t("commands.config_language_desc", lang)
                    },
                    {
                        "name": "/config language_info",
                        "desc": i18n.t("commands.config_language_info_desc", lang)
                    },
                    {
                        "name": "/config interval",
                        "desc": i18n.t("commands.config_interval_desc", lang)
                    }
                ]
            },
            "management": {
                "title": i18n.t("help.bot_management", lang),
                "emoji": "🔧",
                "commands": [
                    {
                        "name": "/manage reload",
                        "desc": i18n.t("commands.manage_reload_desc", lang)
                    },
                    {
                        "name": "/manage status",
                        "desc": i18n.t("commands.manage_status_desc", lang)
                    },
                    {
                        "name": "/manage sync",
                        "desc": i18n.t("commands.manage_sync_desc", lang)
                    },
                    {
                        "name": "/manage logs",
                        "desc": i18n.t("commands.manage_logs_desc", lang)
                    }
                ]
            }
        }

    @discord.app_commands.command(name="help", description="Show comprehensive help for all bot commands")
    @discord.app_commands.describe(category="Show help for a specific category")
    @discord.app_commands.choices(category=[
        discord.app_commands.Choice(name="🖥️ System Monitoring", value="system"),
        discord.app_commands.Choice(name="🚨 Alert System", value="alerts"),
        discord.app_commands.Choice(name="🐳 Docker Management", value="docker"),
        discord.app_commands.Choice(name="🔄 System Reboot", value="reboot"),
        discord.app_commands.Choice(name="🛠️ Service Recovery", value="recovery"),
        discord.app_commands.Choice(name="⚙️ Configuration", value="config"),
        discord.app_commands.Choice(name="🔧 Bot Management", value="management"),
    ])
    async def help(self, interaction: discord.Interaction, category: str = None):
        """Show comprehensive help for bot commands"""
        lang = self.bot.config.get("language", "en")
        categories = self.get_command_categories(lang)

        if category and category in categories:
            # Show specific category
            cat_info = categories[category]
            embed = create_standard_embed(
                title=f"{cat_info['emoji']} {cat_info['title']}",
                command_name="help",
                bot=self.bot
            )

            commands_text = ""
            for cmd in cat_info['commands']:
                commands_text += f"**{cmd['name']}**\n{cmd['desc']}\n\n"

            embed.description = commands_text
            embed.set_footer(text=i18n.t("help.use_help_for_all", lang))

        else:
            # Show main help menu
            embed = create_standard_embed(
                title=f"🤖 {i18n.t('help.serelix_bot_help', lang)}",
                description=i18n.t("help.main_description", lang),
                command_name="help",
                bot=self.bot
            )

            # Add category overview
            for cat_key, cat_info in categories.items():
                commands_list = [cmd['name'] for cmd in cat_info['commands'][:3]]
                if len(cat_info['commands']) > 3:
                    commands_list.append(f"+ {len(cat_info['commands']) - 3} more...")

                embed.add_field(
                    name=f"{cat_info['emoji']} {cat_info['title']}",
                    value="\n".join([f"`{cmd}`" for cmd in commands_list]),
                    inline=True
                )

            # Add usage instructions
            embed.add_field(
                name=f"📖 {i18n.t('help.usage', lang)}",
                value=i18n.t("help.usage_instructions", lang),
                inline=False
            )

            # Add quick start
            embed.add_field(
                name=f"🚀 {i18n.t('help.quick_start', lang)}",
                value=i18n.t("help.quick_start_commands", lang),
                inline=False
            )

        # Override footer with language info
        footer_text = f"Powered by Serelix Studio • {i18n.t('help.language', lang)}: {lang.upper()}"
        embed.set_footer(text=footer_text)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.app_commands.command(name="about", description="Show information about Logivore")
    async def about(self, interaction: discord.Interaction):
        """Show bot information and credits"""
        lang = self.bot.config.get("language", "en")

        embed = create_standard_embed(
            title="🤖 Logivore",
            description=i18n.t("help.about_description", lang),
            command_name="about",
            bot=self.bot
        )

        # Bot info
        embed.add_field(
            name=f"📊 {i18n.t('help.statistics', lang)}",
            value=f"• {i18n.t('help.servers', lang)}: {len(self.bot.guilds)}\n"
                  f"• {i18n.t('help.commands', lang)}: {len(self.bot.tree.get_commands())}\n"
                  f"• {i18n.t('help.modules', lang)}: {len(self.bot.cogs)}",
            inline=True
        )

        # Features
        embed.add_field(
            name=f"⭐ {i18n.t('help.features', lang)}",
            value=f"• {i18n.t('help.real_time_monitoring', lang)}\n"
                  f"• {i18n.t('help.smart_alerts', lang)}\n"
                  f"• {i18n.t('help.docker_management', lang)}\n"
                  f"• {i18n.t('help.auto_recovery', lang)}\n"
                  f"• {i18n.t('help.multilingual', lang)}",
            inline=True
        )

        # Support info
        embed.add_field(
            name=f"🆘 {i18n.t('help.support', lang)}",
            value=f"• {i18n.t('help.help_command', lang)}: `/help`\n"
                  f"• {i18n.t('help.language_switch', lang)}: `/config language`\n"
                  f"• {i18n.t('help.bot_status', lang)}: `/manage status`",
            inline=False
        )

        embed.set_thumbnail(url=self.bot.user.avatar.url if self.bot.user.avatar else None)

        # Override footer with version info
        footer_text = f"Powered by Serelix Studio • v2.0 | {i18n.t('help.powered_by_claude', lang)}"
        embed.set_footer(text=footer_text)

        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    """Setup function for loading the cog"""
    await bot.add_cog(HelpSystemCog(bot))
