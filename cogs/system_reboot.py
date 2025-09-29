"""
System Reboot Management Cog for Logivore
Handles scheduled reboots, uptime monitoring, and graceful shutdowns
"""
import discord
from discord.ext import commands, tasks
import subprocess
import asyncio
import datetime
import psutil
import time
from utils.i18n import i18n
from utils.embed_formatter import create_standard_embed, EmbedFormatter

class SystemRebootCog(commands.Cog):
    """Handles system reboot management and scheduling"""

    def __init__(self, bot):
        self.bot = bot
        self.reboot_scheduler_task.start()
        self.uptime_checker_task.start()

    def cog_unload(self):
        """Clean up tasks when cog is unloaded"""
        self.reboot_scheduler_task.cancel()
        self.uptime_checker_task.cancel()

    def get_system_uptime(self):
        """Get system uptime in seconds"""
        return time.time() - psutil.boot_time()

    def format_uptime_days(self, seconds):
        """Format uptime in days, hours, minutes"""
        days = int(seconds // 86400)
        hours = int((seconds % 86400) // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{days}天 {hours}小時 {minutes}分鐘"

    async def send_reboot_notification(self, channel_id, message, color=0xffa500):
        """Send reboot notification to configured channel"""
        if not channel_id:
            return

        channel = self.bot.get_channel(channel_id)
        if not channel:
            return

        # Use warning format for reboot notifications
        embed = EmbedFormatter.warning_embed(
            title="🔄 系統重啟通知",
            description=message,
            command_name="reboot"
        )
        # Override color if specified
        if color != 0xffa500:
            embed.color = color

        try:
            await channel.send(embed=embed)
        except Exception as e:
            print(f"Failed to send reboot notification: {e}")

    async def graceful_shutdown_services(self):
        """Gracefully shutdown services before reboot"""
        services_to_stop = self.bot.config.get("reboot_stop_services", [])
        stopped_services = []

        for service in services_to_stop:
            try:
                result = subprocess.run(
                    ["sudo", "systemctl", "stop", service],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                if result.returncode == 0:
                    stopped_services.append(service)
            except Exception as e:
                print(f"Failed to stop service {service}: {e}")

        return stopped_services

    async def execute_reboot(self, delay_minutes=1):
        """Execute system reboot with delay"""
        try:
            # Send notification
            alert_channel = self.bot.config.get("alert_channel")
            if alert_channel:
                await self.send_reboot_notification(
                    alert_channel,
                    f"系統將在 {delay_minutes} 分鐘後重啟...",
                    0xff5722
                )

            # Graceful shutdown
            stopped_services = await self.graceful_shutdown_services()
            if stopped_services:
                print(f"Stopped services: {', '.join(stopped_services)}")

            # Schedule reboot
            subprocess.run([
                "sudo", "shutdown", "-r", f"+{delay_minutes}",
                "Scheduled reboot by Logivore"
            ], timeout=10)

            return True

        except Exception as e:
            print(f"Failed to execute reboot: {e}")
            return False

    @tasks.loop(hours=1)
    async def uptime_checker_task(self):
        """Check system uptime and suggest reboot if needed"""
        await self.bot.wait_until_ready()

        max_uptime_days = self.bot.config.get("max_uptime_days", 30)
        uptime_seconds = self.get_system_uptime()
        uptime_days = uptime_seconds / 86400

        if uptime_days >= max_uptime_days:
            alert_channel = self.bot.config.get("alert_channel")
            if alert_channel:
                uptime_str = self.format_uptime_days(uptime_seconds)
                await self.send_reboot_notification(
                    alert_channel,
                    f"⚠️ 系統已運行 {uptime_str}\n建議考慮重啟系統以保持最佳效能",
                    0xff9800
                )

    @tasks.loop(minutes=30)
    async def reboot_scheduler_task(self):
        """Check for scheduled reboots"""
        await self.bot.wait_until_ready()

        scheduled_reboots = self.bot.config.get("scheduled_reboots", [])
        current_time = datetime.datetime.now()

        for reboot_config in scheduled_reboots[:]:  # Copy list to avoid modification during iteration
            if not reboot_config.get("enabled", True):
                continue

            # Parse scheduled time
            try:
                scheduled_time = datetime.datetime.fromisoformat(reboot_config["time"])
                if current_time >= scheduled_time:
                    # Execute reboot
                    success = await self.execute_reboot(reboot_config.get("delay", 5))

                    # Remove from schedule after execution
                    scheduled_reboots.remove(reboot_config)
                    self.bot.config.set("scheduled_reboots", scheduled_reboots)

                    if success:
                        print(f"Scheduled reboot executed at {current_time}")

            except Exception as e:
                print(f"Error processing scheduled reboot: {e}")
                # Remove invalid entries
                scheduled_reboots.remove(reboot_config)
                self.bot.config.set("scheduled_reboots", scheduled_reboots)

    # Reboot command group
    reboot_group = discord.app_commands.Group(name="reboot", description="系統重啟管理")

    @reboot_group.command(name="now", description="立即重啟系統")
    @discord.app_commands.describe(delay="延遲分鐘數 (預設: 1分鐘)")
    async def reboot_now(self, interaction: discord.Interaction, delay: int = 1):
        """Immediately schedule a system reboot"""
        if delay < 0 or delay > 60:
            await interaction.response.send_message(
                "延遲時間必須在 0-60 分鐘之間",
                ephemeral=True
            )
            return

        await interaction.response.defer(ephemeral=True)

        try:
            success = await self.execute_reboot(delay)

            if success:
                embed = EmbedFormatter.success_embed(
                    title="✅ 重啟已排程",
                    description=f"系統將在 {delay} 分鐘後重啟",
                    command_name="reboot now"
                )
            else:
                embed = EmbedFormatter.error_embed(
                    title="❌ 重啟失敗",
                    description="無法排程系統重啟，請檢查權限",
                    command_name="reboot now"
                )

            await interaction.followup.send(embed=embed, ephemeral=True)

        except Exception as e:
            await interaction.followup.send(
                f"執行重啟時發生錯誤: {str(e)}",
                ephemeral=True
            )

    @reboot_group.command(name="schedule", description="排程系統重啟")
    @discord.app_commands.describe(
        hours="小時後重啟 (0-168小時)",
        delay="重啟前延遲分鐘數 (預設: 5分鐘)"
    )
    async def reboot_schedule(self, interaction: discord.Interaction, hours: int, delay: int = 5):
        """Schedule a system reboot"""
        if hours <= 0 or hours > 168:  # Max 1 week
            await interaction.response.send_message(
                "小時數必須在 1-168 之間 (最多一週)",
                ephemeral=True
            )
            return

        if delay < 0 or delay > 60:
            await interaction.response.send_message(
                "延遲時間必須在 0-60 分鐘之間",
                ephemeral=True
            )
            return

        # Calculate scheduled time
        scheduled_time = datetime.datetime.now() + datetime.timedelta(hours=hours)

        # Add to scheduled reboots
        scheduled_reboots = self.bot.config.get("scheduled_reboots", [])
        reboot_config = {
            "time": scheduled_time.isoformat(),
            "delay": delay,
            "enabled": True,
            "scheduled_by": interaction.user.id
        }
        scheduled_reboots.append(reboot_config)
        self.bot.config.set("scheduled_reboots", scheduled_reboots)

        embed = EmbedFormatter.info_embed(
            title="📅 重啟已排程",
            description=f"系統將在 {scheduled_time.strftime('%Y-%m-%d %H:%M:%S')} 重啟",
            command_name="reboot schedule"
        )
        embed.add_field(
            name="延遲時間",
            value=f"{delay} 分鐘",
            inline=True
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @reboot_group.command(name="cancel", description="取消所有排程的重啟")
    async def reboot_cancel(self, interaction: discord.Interaction):
        """Cancel all scheduled reboots"""
        try:
            # Cancel system scheduled reboots
            subprocess.run(["sudo", "shutdown", "-c"], timeout=10)

            # Clear from config
            self.bot.config.set("scheduled_reboots", [])

            embed = EmbedFormatter.success_embed(
                title="✅ 重啟已取消",
                description="所有排程的重啟已被取消",
                command_name="reboot cancel"
            )

            await interaction.response.send_message(embed=embed, ephemeral=True)

        except Exception as e:
            await interaction.response.send_message(
                f"取消重啟時發生錯誤: {str(e)}",
                ephemeral=True
            )

    @reboot_group.command(name="status", description="檢查系統運行時間和重啟狀態")
    async def reboot_status(self, interaction: discord.Interaction):
        """Show system uptime and reboot status"""
        uptime_seconds = self.get_system_uptime()
        uptime_str = self.format_uptime_days(uptime_seconds)
        uptime_days = uptime_seconds / 86400

        scheduled_reboots = self.bot.config.get("scheduled_reboots", [])
        max_uptime_days = self.bot.config.get("max_uptime_days", 30)

        embed = create_standard_embed(
            title="🖥️ 系統運行狀態",
            command_name="reboot status",
            bot=self.bot
        )

        # Uptime status
        uptime_color = "🟢" if uptime_days < max_uptime_days else "🟡" if uptime_days < max_uptime_days * 1.5 else "🔴"
        embed.add_field(
            name="系統運行時間",
            value=f"{uptime_color} {uptime_str} ({uptime_days:.1f} 天)",
            inline=False
        )

        # Reboot recommendation
        if uptime_days >= max_uptime_days:
            embed.add_field(
                name="建議",
                value="⚠️ 建議重啟系統以保持最佳效能",
                inline=False
            )

        # Scheduled reboots
        if scheduled_reboots:
            reboot_list = []
            for reboot in scheduled_reboots:
                if reboot.get("enabled", True):
                    time_str = datetime.datetime.fromisoformat(reboot["time"]).strftime("%m-%d %H:%M")
                    reboot_list.append(f"• {time_str} (延遲: {reboot.get('delay', 5)}分鐘)")

            if reboot_list:
                embed.add_field(
                    name="排程重啟",
                    value="\n".join(reboot_list),
                    inline=False
                )
        else:
            embed.add_field(
                name="排程重啟",
                value="無排程的重啟",
                inline=False
            )

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @reboot_group.command(name="config", description="配置重啟設定")
    @discord.app_commands.describe(
        max_uptime_days="最大運行天數，超過後會發出警告",
        stop_services="重啟前要停止的服務，用逗號分隔"
    )
    async def reboot_config(self, interaction: discord.Interaction, max_uptime_days: int = None, stop_services: str = None):
        """Configure reboot settings"""
        if max_uptime_days is not None:
            if max_uptime_days < 1 or max_uptime_days > 365:
                await interaction.response.send_message(
                    "最大運行天數必須在 1-365 之間",
                    ephemeral=True
                )
                return
            self.bot.config.set("max_uptime_days", max_uptime_days)

        if stop_services is not None:
            services_list = [s.strip() for s in stop_services.split(",") if s.strip()]
            self.bot.config.set("reboot_stop_services", services_list)

        # Show current config
        current_max_days = self.bot.config.get("max_uptime_days", 30)
        current_services = self.bot.config.get("reboot_stop_services", [])

        embed = create_standard_embed(
            title="⚙️ 重啟配置",
            command_name="reboot config",
            bot=self.bot
        )
        embed.add_field(
            name="最大運行天數",
            value=f"{current_max_days} 天",
            inline=True
        )
        embed.add_field(
            name="停止服務",
            value=", ".join(current_services) if current_services else "無",
            inline=False
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    """Setup function for loading the cog"""
    await bot.add_cog(SystemRebootCog(bot))
