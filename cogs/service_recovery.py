"""
Service Recovery Cog for Logivore
Handles automatic service and container recovery after system reboot
"""
import discord
from discord.ext import commands, tasks
import subprocess
import asyncio
import json
import time
import os
import datetime
from utils.i18n import i18n
from utils.embed_formatter import create_standard_embed, EmbedFormatter

class ServiceRecoveryCog(commands.Cog):
    """Handles service recovery and auto-start management"""

    def __init__(self, bot):
        self.bot = bot
        self.recovery_check_task.start()

    def cog_unload(self):
        """Clean up tasks when cog is unloaded"""
        self.recovery_check_task.cancel()

    async def get_docker_containers(self):
        """Get all Docker containers and their states"""
        try:
            result = subprocess.run([
                "docker", "ps", "-a",
                "--format", "{{.Names}}\t{{.State}}\t{{.Status}}\t{{.Image}}"
            ], capture_output=True, text=True, timeout=10)

            containers = []
            if result.returncode == 0:
                for line in result.stdout.strip().split('\n'):
                    if line:
                        parts = line.split('\t')
                        if len(parts) >= 4:
                            containers.append({
                                'name': parts[0],
                                'state': parts[1],
                                'status': parts[2],
                                'image': parts[3]
                            })
            return containers
        except Exception as e:
            print(f"Error getting Docker containers: {e}")
            return []

    async def get_systemd_services(self):
        """Get systemd services and their states"""
        try:
            result = subprocess.run([
                "systemctl", "list-units", "--type=service", "--all",
                "--no-pager", "--plain", "--no-legend"
            ], capture_output=True, text=True, timeout=15)

            services = []
            if result.returncode == 0:
                for line in result.stdout.strip().split('\n'):
                    if line and not line.startswith('●'):
                        parts = line.split()
                        if len(parts) >= 4:
                            services.append({
                                'name': parts[0],
                                'loaded': parts[1],
                                'active': parts[2],
                                'sub': parts[3],
                                'description': ' '.join(parts[4:]) if len(parts) > 4 else ''
                            })
            return services
        except Exception as e:
            print(f"Error getting systemd services: {e}")
            return []

    async def start_docker_container(self, container_name):
        """Start a Docker container"""
        try:
            result = subprocess.run([
                "docker", "start", container_name
            ], capture_output=True, text=True, timeout=30)
            return result.returncode == 0, result.stderr
        except Exception as e:
            return False, str(e)

    async def start_systemd_service(self, service_name):
        """Start a systemd service"""
        try:
            result = subprocess.run([
                "sudo", "systemctl", "start", service_name
            ], capture_output=True, text=True, timeout=30)
            return result.returncode == 0, result.stderr
        except Exception as e:
            return False, str(e)

    async def save_current_state(self):
        """Save current running services and containers state"""
        state = {
            'timestamp': time.time(),
            'docker_containers': [],
            'systemd_services': []
        }

        # Save running Docker containers
        containers = await self.get_docker_containers()
        for container in containers:
            if container['state'] == 'running':
                state['docker_containers'].append({
                    'name': container['name'],
                    'image': container['image']
                })

        # Save active systemd services (user-defined ones)
        monitored_services = self.bot.config.get("monitored_services", [])
        services = await self.get_systemd_services()
        for service in services:
            if (service['name'] in monitored_services and
                service['active'] == 'active' and
                service['sub'] == 'running'):
                state['systemd_services'].append(service['name'])

        # Save to config
        self.bot.config.set("last_known_state", state)
        return state

    async def recover_services(self):
        """Recover services based on last known state"""
        last_state = self.bot.config.get("last_known_state")
        if not last_state:
            return {"success": False, "message": "無保存的狀態資料"}

        recovery_results = {
            "docker_started": [],
            "docker_failed": [],
            "services_started": [],
            "services_failed": []
        }

        # Recover Docker containers
        if last_state.get("docker_containers"):
            current_containers = await self.get_docker_containers()
            current_running = {c['name'] for c in current_containers if c['state'] == 'running'}

            for container in last_state["docker_containers"]:
                container_name = container['name']
                if container_name not in current_running:
                    success, error = await self.start_docker_container(container_name)
                    if success:
                        recovery_results["docker_started"].append(container_name)
                    else:
                        recovery_results["docker_failed"].append(f"{container_name}: {error}")

        # Recover systemd services
        if last_state.get("systemd_services"):
            current_services = await self.get_systemd_services()
            current_active = {s['name'] for s in current_services
                            if s['active'] == 'active' and s['sub'] == 'running'}

            for service_name in last_state["systemd_services"]:
                if service_name not in current_active:
                    success, error = await self.start_systemd_service(service_name)
                    if success:
                        recovery_results["services_started"].append(service_name)
                    else:
                        recovery_results["services_failed"].append(f"{service_name}: {error}")

        return recovery_results

    @tasks.loop(minutes=5)
    async def recovery_check_task(self):
        """Check if system was recently rebooted and recover services"""
        await self.bot.wait_until_ready()

        # Check if auto-recovery is enabled
        if not self.bot.config.get("auto_recovery_enabled", True):
            return

        # Check if system was recently rebooted (within last 10 minutes)
        import psutil
        boot_time = psutil.boot_time()
        current_time = time.time()

        if current_time - boot_time < 600:  # 10 minutes
            # Check if we already recovered for this boot
            last_recovery = self.bot.config.get("last_recovery_boot", 0)
            if last_recovery < boot_time:
                # Perform recovery
                recovery_results = await self.recover_services()

                # Mark recovery as done for this boot
                self.bot.config.set("last_recovery_boot", boot_time)

                # Send notification
                await self.send_recovery_notification(recovery_results)

    async def send_recovery_notification(self, results):
        """Send recovery notification to alert channel"""
        alert_channel_id = self.bot.config.get("alert_channel")
        if not alert_channel_id:
            return

        channel = self.bot.get_channel(alert_channel_id)
        if not channel:
            return

        embed = EmbedFormatter.success_embed(
            title="🔄 系統重啟後服務恢復",
            command_name="recovery"
        )

        if results["docker_started"]:
            embed.add_field(
                name="✅ Docker 容器已啟動",
                value="\n".join([f"• {name}" for name in results["docker_started"]]),
                inline=False
            )

        if results["services_started"]:
            embed.add_field(
                name="✅ 系統服務已啟動",
                value="\n".join([f"• {name}" for name in results["services_started"]]),
                inline=False
            )

        if results["docker_failed"]:
            embed.add_field(
                name="❌ Docker 容器啟動失敗",
                value="\n".join([f"• {error}" for error in results["docker_failed"]]),
                inline=False
            )
            embed.color = 0xff9800

        if results["services_failed"]:
            embed.add_field(
                name="❌ 系統服務啟動失敗",
                value="\n".join([f"• {error}" for error in results["services_failed"]]),
                inline=False
            )
            embed.color = 0xff9800

        if not any([results["docker_started"], results["services_started"],
                   results["docker_failed"], results["services_failed"]]):
            embed.description = "所有服務已正常運行，無需恢復"

        try:
            await channel.send(embed=embed)
        except Exception as e:
            print(f"Failed to send recovery notification: {e}")

    # Recovery command group
    recovery_group = discord.app_commands.Group(name="recovery", description="服務恢復管理")

    @recovery_group.command(name="save_state", description="保存當前服務狀態")
    async def recovery_save_state(self, interaction: discord.Interaction):
        """Save current service state"""
        await interaction.response.defer(ephemeral=True)

        try:
            state = await self.save_current_state()

            docker_count = len(state.get("docker_containers", []))
            service_count = len(state.get("systemd_services", []))

            embed = EmbedFormatter.success_embed(
                title="💾 狀態已保存",
                description=f"已保存 {docker_count} 個 Docker 容器和 {service_count} 個系統服務的狀態",
                command_name="recovery save_state"
            )

            if docker_count > 0:
                container_names = [c['name'] for c in state["docker_containers"]]
                embed.add_field(
                    name="Docker 容器",
                    value=", ".join(container_names),
                    inline=False
                )

            if service_count > 0:
                embed.add_field(
                    name="系統服務",
                    value=", ".join(state["systemd_services"]),
                    inline=False
                )

            await interaction.followup.send(embed=embed, ephemeral=True)

        except Exception as e:
            await interaction.followup.send(
                f"保存狀態時發生錯誤: {str(e)}",
                ephemeral=True
            )

    @recovery_group.command(name="recover_now", description="立即恢復服務")
    async def recovery_recover_now(self, interaction: discord.Interaction):
        """Manually trigger service recovery"""
        await interaction.response.defer(ephemeral=True)

        try:
            results = await self.recover_services()

            embed = EmbedFormatter.success_embed(
                title="🔄 服務恢復完成",
                command_name="recovery recover_now"
            )

            if results["docker_started"]:
                embed.add_field(
                    name="✅ Docker 容器已啟動",
                    value="\n".join([f"• {name}" for name in results["docker_started"]]),
                    inline=False
                )

            if results["services_started"]:
                embed.add_field(
                    name="✅ 系統服務已啟動",
                    value="\n".join([f"• {name}" for name in results["services_started"]]),
                    inline=False
                )

            if results["docker_failed"]:
                embed.add_field(
                    name="❌ Docker 容器啟動失敗",
                    value="\n".join([f"• {error}" for error in results["docker_failed"]]),
                    inline=False
                )
                embed.color = 0xff9800

            if results["services_failed"]:
                embed.add_field(
                    name="❌ 系統服務啟動失敗",
                    value="\n".join([f"• {error}" for error in results["services_failed"]]),
                    inline=False
                )
                embed.color = 0xff9800

            if not any([results["docker_started"], results["services_started"],
                       results["docker_failed"], results["services_failed"]]):
                embed.description = "所有服務已正常運行，無需恢復"

            await interaction.followup.send(embed=embed, ephemeral=True)

        except Exception as e:
            await interaction.followup.send(
                f"恢復服務時發生錯誤: {str(e)}",
                ephemeral=True
            )

    @recovery_group.command(name="config", description="配置自動恢復設定")
    @discord.app_commands.describe(
        auto_recovery="是否啟用自動恢復",
        monitored_services="要監控的系統服務，用逗號分隔"
    )
    async def recovery_config(self, interaction: discord.Interaction,
                            auto_recovery: bool = None,
                            monitored_services: str = None):
        """Configure recovery settings"""
        if auto_recovery is not None:
            self.bot.config.set("auto_recovery_enabled", auto_recovery)

        if monitored_services is not None:
            services_list = [s.strip() for s in monitored_services.split(",") if s.strip()]
            self.bot.config.set("monitored_services", services_list)

        # Show current config
        current_auto = self.bot.config.get("auto_recovery_enabled", True)
        current_services = self.bot.config.get("monitored_services", [])

        embed = create_standard_embed(
            title="⚙️ 恢復配置",
            command_name="recovery config",
            bot=self.bot
        )
        embed.add_field(
            name="自動恢復",
            value="✅ 啟用" if current_auto else "❌ 停用",
            inline=True
        )
        embed.add_field(
            name="監控服務",
            value=", ".join(current_services) if current_services else "無",
            inline=False
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @recovery_group.command(name="status", description="查看恢復狀態")
    async def recovery_status(self, interaction: discord.Interaction):
        """Show recovery status and last saved state"""
        last_state = self.bot.config.get("last_known_state")
        auto_recovery = self.bot.config.get("auto_recovery_enabled", True)
        last_recovery = self.bot.config.get("last_recovery_boot", 0)

        embed = create_standard_embed(
            title="📊 恢復狀態",
            command_name="recovery status",
            bot=self.bot
        )

        embed.add_field(
            name="自動恢復",
            value="✅ 啟用" if auto_recovery else "❌ 停用",
            inline=True
        )

        if last_state:
            timestamp = datetime.datetime.fromtimestamp(last_state['timestamp'])
            embed.add_field(
                name="最後保存狀態",
                value=timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                inline=True
            )

            docker_count = len(last_state.get("docker_containers", []))
            service_count = len(last_state.get("systemd_services", []))

            embed.add_field(
                name="保存的服務數量",
                value=f"Docker: {docker_count}, 系統服務: {service_count}",
                inline=False
            )

        if last_recovery > 0:
            recovery_time = datetime.datetime.fromtimestamp(last_recovery)
            embed.add_field(
                name="最後恢復時間",
                value=recovery_time.strftime("%Y-%m-%d %H:%M:%S"),
                inline=True
            )

        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    """Setup function for loading the cog"""
    await bot.add_cog(ServiceRecoveryCog(bot))
