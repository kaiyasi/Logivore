"""
Alerting Cog for Logivore
Handles system alerts, notifications, and alert management
"""
import discord
from discord.ext import tasks, commands
import psutil
import time
from utils.i18n import i18n
from utils.embed_formatter import create_standard_embed, EmbedFormatter

class AlertingCog(commands.Cog):
    """Handles alerting system and notifications"""

    def __init__(self, bot):
        self.bot = bot
        self.alert_checker_task.start()

    def cog_unload(self):
        """Clean up alert checker task when cog is unloaded"""
        self.alert_checker_task.cancel()

    def get_system_stats_for_alerts(self) -> dict:
        """Get minimal system stats needed for alert checking"""
        cpu_percent = psutil.cpu_percent(interval=0.1)  # Reduced from 1 second

        disks = []
        partitions = psutil.disk_partitions(all=False)
        monitored_disks = self.bot.config.get("monitored_disks") or []
        target_mounts = {p.mountpoint for p in partitions}
        target_mounts.update(monitored_disks)

        for path in target_mounts:
            try:
                usage = psutil.disk_usage(path)
                disks.append({
                    "mountpoint": path,
                    "percent": usage.percent,
                })
            except (PermissionError, FileNotFoundError):
                continue

        return {
            "cpu_percent": cpu_percent,
            "disks": disks,
        }

    async def send_alert_notification(self, alert: dict, current_value_str: str):
        """Send alert notification to configured channel"""
        channel_id = alert.get("channel_id") or self.bot.config.get("alert_channel")
        if not channel_id:
            return

        channel = self.bot.get_channel(channel_id)
        if not channel:
            print(f"Alert channel {channel_id} not found.")
            return

        desc = ""
        if alert['type'] in ['disk', 'cpu']:
            desc = i18n.t('alerts.condition_met', target=alert['target'], threshold=alert['threshold'])
        elif alert['type'] == 'process':
            desc = i18n.t('alerts.process_not_running', target=alert['target'])

        embed = EmbedFormatter.error_embed(
            title=i18n.t('alerts.triggered', name=alert.get('name', alert['id'])),
            description=desc,
            command_name="alert"
        )
        embed.add_field(name=i18n.t('alerts.current_status'), value=current_value_str, inline=False)
        # Override footer to include alert ID
        lang = self.bot.config.get("language", "en")
        if lang == 'zh':
            footer_text = f"由 Serelix Studio 提供支援 • {i18n.t('alerts.alert_id')}: {alert['id']}"
        else:
            footer_text = f"Powered by Serelix Studio • {i18n.t('alerts.alert_id')}: {alert['id']}"
        embed.set_footer(text=footer_text)

        try:
            await channel.send(embed=embed)
        except discord.Forbidden:
            print(f"No permission to send message to channel {channel_id}")
        except Exception as e:
            print(f"Error sending alert notification: {e}")

    async def send_resolved_notification(self, alert: dict, current_value_str: str):
        """Send alert resolved notification to configured channel"""
        channel_id = alert.get("channel_id") or self.bot.config.get("alert_channel")
        if not channel_id:
            return

        channel = self.bot.get_channel(channel_id)
        if not channel:
            return

        desc = ""
        if alert['type'] in ['disk', 'cpu']:
            desc = i18n.t('alerts.condition_not_met', target=alert['target'], threshold=alert['threshold'])
        elif alert['type'] == 'process':
            desc = i18n.t('alerts.process_running', target=alert['target'])

        embed = EmbedFormatter.success_embed(
            title=i18n.t('alerts.resolved', name=alert.get('name', alert['id'])),
            description=desc,
            command_name="alert"
        )
        embed.add_field(name=i18n.t('alerts.current_status'), value=current_value_str, inline=False)
        # Override footer to include alert ID
        lang = self.bot.config.get("language", "en")
        if lang == 'zh':
            footer_text = f"由 Serelix Studio 提供支援 • {i18n.t('alerts.alert_id')}: {alert['id']}"
        else:
            footer_text = f"Powered by Serelix Studio • {i18n.t('alerts.alert_id')}: {alert['id']}"
        embed.set_footer(text=footer_text)

        try:
            await channel.send(embed=embed)
        except discord.Forbidden:
            print(f"No permission to send message to channel {channel_id}")
        except Exception as e:
            print(f"Error sending resolved notification: {e}")

    @tasks.loop(seconds=60)
    async def alert_checker_task(self):
        """Background task to check alert conditions"""
        await self.bot.wait_until_ready()
        alerts = self.bot.config.get("alerts")
        if not alerts:
            return

        stats = None  # Lazily load stats only if needed

        for alert in [a for a in alerts if a.get("enabled", True)]:
            state = self.bot.alert_states.get(alert['id'])
            if not state:
                self.bot.alert_states[alert['id']] = {"status": "normal", "triggered_since": None}
                state = self.bot.alert_states[alert['id']]

            is_triggered = False
            current_value_str = "N/A"

            try:
                if alert['type'] in ['disk', 'cpu']:
                    if not stats:
                        stats = self.get_system_stats_for_alerts()

                    current_value = -1
                    if alert['type'] == 'disk':
                        for disk in stats.get('disks', []):
                            if disk['mountpoint'] == alert['target']:
                                current_value = disk['percent']
                                if current_value > alert['threshold']:
                                    is_triggered = True
                                break
                    elif alert['type'] == 'cpu':
                        current_value = stats.get('cpu_percent', 0)
                        if current_value > alert['threshold']:
                            is_triggered = True

                    current_value_str = f"{current_value:.1f}%" if current_value != -1 else "N/A"

                elif alert['type'] == 'process':
                    is_running = any(
                        p.info['name'].lower() == alert['target'].lower()
                        for p in psutil.process_iter(['name'])
                    )
                    is_triggered = not is_running
                    current_value_str = "Running" if is_running else "Not Running"

            except Exception as e:
                print(f"Error checking alert {alert.get('id')}: {e}")
                continue

            # Handle alert state transitions
            if is_triggered:
                if state['status'] == 'normal':
                    state['status'] = 'triggered'
                    await self.send_alert_notification(alert, current_value_str)
            else:
                if state['status'] == 'triggered':
                    state['status'] = 'normal'
                    await self.send_resolved_notification(alert, current_value_str)

    # Alert management commands
    alert_group = discord.app_commands.Group(name="alert", description="Manage the proactive alerting system.")
    add_alert_group = discord.app_commands.Group(name="add", parent=alert_group, description="Add a new alert.")

    @alert_group.command(name="set_channel", description="Set the default channel for all alerts.")
    @discord.app_commands.describe(channel="The channel to send alerts to.")
    async def alert_set_channel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        """Set default alert channel"""
        self.bot.config.set("alert_channel", channel.id)
        await interaction.response.send_message(
            f"Default alert channel set to {channel.mention}.",
            ephemeral=True
        )

    @alert_group.command(name="list", description="List all configured alerts.")
    async def alert_list(self, interaction: discord.Interaction):
        """List all configured alerts with their status"""
        alerts = self.bot.config.get("alerts")
        if not alerts:
            await interaction.response.send_message(
                i18n.t('alerts.no_alerts'),
                ephemeral=True
            )
            return

        embed = create_standard_embed(
            title=i18n.t('alerts.configured_alerts'),
            command_name="alert list",
            bot=self.bot
        )
        for alert in alerts:
            state = self.bot.alert_states.get(alert['id'], {})
            status_emoji = "🟢" if state.get('status') == 'normal' else "🔴"
            enabled_emoji = "✅" if alert.get("enabled", True) else "❌"
            name = f"{enabled_emoji} {status_emoji} {alert.get('name', alert['id'])}"

            value = f"Type: `{alert['type']}` | Target: `{alert['target']}`"
            if alert['type'] in ['disk', 'cpu']:
                value += f" | Threshold: `> {alert['threshold']}%`"

            embed.add_field(name=name, value=value, inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)

    async def alert_id_autocomplete(self, interaction: discord.Interaction, current: str) -> list[discord.app_commands.Choice[str]]:
        """Autocomplete for alert IDs"""
        alerts = self.bot.config.get("alerts") or []
        return [
            discord.app_commands.Choice(name=alert.get("name", alert["id"]), value=alert["id"])
            for alert in alerts if current.lower() in alert.get("name", alert["id"]).lower()
        ][:25]

    @alert_group.command(name="remove", description="Remove an existing alert.")
    @discord.app_commands.describe(alert_id="The ID of the alert to remove.")
    @discord.app_commands.autocomplete(alert_id=alert_id_autocomplete)
    async def alert_remove(self, interaction: discord.Interaction, alert_id: str):
        """Remove an existing alert"""
        alerts = self.bot.config.get("alerts")
        alert_to_remove = next((a for a in alerts if a["id"] == alert_id), None)

        if not alert_to_remove:
            await interaction.response.send_message(i18n.t('alerts.alert_not_found'), ephemeral=True)
            return

        alerts.remove(alert_to_remove)
        self.bot.config.set("alerts", alerts)
        if alert_id in self.bot.alert_states:
            del self.bot.alert_states[alert_id]

        await interaction.response.send_message(
            i18n.t('alerts.alert_removed', name=alert_to_remove.get('name', alert_id)),
            ephemeral=True
        )

    @add_alert_group.command(name="disk", description="Add a disk usage alert.")
    @discord.app_commands.describe(
        name="A friendly name for the alert.",
        path="The disk mount point to monitor (e.g., / or /mnt/data).",
        threshold="The usage percentage to trigger the alert (e.g., 90)."
    )
    async def add_disk_alert(
        self,
        interaction: discord.Interaction,
        name: str,
        path: str,
        threshold: discord.app_commands.Range[int, 1, 99]
    ):
        """Add a disk usage alert"""
        import os
        if not os.path.isdir(path):
            await interaction.response.send_message(
                f"Path `{path}` is not a valid directory.",
                ephemeral=True
            )
            return

        alerts = self.bot.config.get("alerts")
        alert_id = f"disk_{name.lower().replace(' ', '_')}_{int(time.time())}"
        new_alert = {
            "id": alert_id,
            "name": name,
            "type": "disk",
            "target": path,
            "threshold": threshold,
            "enabled": True,
            "channel_id": interaction.channel.id
        }
        alerts.append(new_alert)
        self.bot.config.set("alerts", alerts)
        self.bot.alert_states[alert_id] = {"status": "normal", "triggered_since": None}

        await interaction.response.send_message(
            f"✅ Disk alert '{name}' created for `{path}` at > {threshold}%.",
            ephemeral=True
        )

    @add_alert_group.command(name="cpu", description="Add a CPU usage alert.")
    @discord.app_commands.describe(
        name="A friendly name for the alert.",
        threshold="The usage percentage to trigger the alert (e.g., 85)."
    )
    async def add_cpu_alert(
        self,
        interaction: discord.Interaction,
        name: str,
        threshold: discord.app_commands.Range[int, 1, 99]
    ):
        """Add a CPU usage alert"""
        alerts = self.bot.config.get("alerts")
        alert_id = f"cpu_{name.lower().replace(' ', '_')}_{int(time.time())}"
        new_alert = {
            "id": alert_id,
            "name": name,
            "type": "cpu",
            "target": "cpu",
            "threshold": threshold,
            "enabled": True,
            "channel_id": interaction.channel.id
        }
        alerts.append(new_alert)
        self.bot.config.set("alerts", alerts)
        self.bot.alert_states[alert_id] = {"status": "normal", "triggered_since": None}

        await interaction.response.send_message(
            f"✅ CPU alert '{name}' created for > {threshold}%.",
            ephemeral=True
        )

    @add_alert_group.command(name="process", description="Add a process watchdog alert.")
    @discord.app_commands.describe(
        name="A friendly name for the alert.",
        process_name="The exact name of the process to monitor."
    )
    async def add_process_alert(self, interaction: discord.Interaction, name: str, process_name: str):
        """Add a process monitoring alert"""
        alerts = self.bot.config.get("alerts")
        alert_id = f"proc_{name.lower().replace(' ', '_')}_{int(time.time())}"
        new_alert = {
            "id": alert_id,
            "name": name,
            "type": "process",
            "target": process_name,
            "enabled": True,
            "channel_id": interaction.channel.id
        }
        alerts.append(new_alert)
        self.bot.config.set("alerts", alerts)
        self.bot.alert_states[alert_id] = {"status": "normal", "triggered_since": None}

        await interaction.response.send_message(
            f"✅ Process alert '{name}' created for process `{process_name}`.",
            ephemeral=True
        )

async def setup(bot):
    """Setup function for loading the cog"""
    await bot.add_cog(AlertingCog(bot))
