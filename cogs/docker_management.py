"""
Docker Management Cog for Logivore
Handles Docker container operations and monitoring
"""
import discord
from discord.ext import commands, tasks
import subprocess
import asyncio
import json
import time
from utils.i18n import i18n
from utils.embed_formatter import create_standard_embed, EmbedFormatter

class DockerManagementCog(commands.Cog):
    """Handles Docker container management operations"""

    def __init__(self, bot):
        self.bot = bot

    async def docker_container_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str
    ) -> list[discord.app_commands.Choice[str]]:
        """Autocomplete for Docker container names"""
        try:
            proc = subprocess.run(
                ["docker", "ps", "-a", "--format", "{{.Names}}"],
                capture_output=True,
                text=True,
                check=True,
                timeout=5
            )
            containers = proc.stdout.strip().splitlines()
            return [
                discord.app_commands.Choice(name=container, value=container)
                for container in containers if current.lower() in container.lower()
            ][:25]
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return []

    async def run_docker_command(self, interaction: discord.Interaction, container: str, action: str):
        """Execute Docker command with proper error handling"""
        await interaction.response.defer(ephemeral=True)
        action_verb = {"start": "started", "stop": "stopped", "restart": "restarted"}.get(action, "run")

        try:
            # Check if docker is available
            subprocess.run(["which", "docker"], check=True, capture_output=True, timeout=5)

            # Execute the docker command
            cmd = ["docker", action, container]
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
                timeout=30
            )

            embed = EmbedFormatter.success_embed(
                title=f"Container {action_verb.capitalize()}",
                description=f"Successfully {action_verb} container `{container}`.",
                command_name="docker"
            )
            await interaction.followup.send(embed=embed, ephemeral=True)

        except FileNotFoundError:
            await interaction.followup.send(
                "`docker` command not found. Is it installed and in your PATH?",
                ephemeral=True
            )
        except subprocess.TimeoutExpired:
            await interaction.followup.send(
                f"Docker command timed out. Container `{container}` may be unresponsive.",
                ephemeral=True
            )
        except subprocess.CalledProcessError as e:
            error_message = e.stderr.strip() if e.stderr else "Unknown error"
            embed = EmbedFormatter.error_embed(
                title="Docker Command Failed",
                description=f"Failed to {action} container `{container}`.",
                command_name="docker"
            )
            embed.add_field(
                name="Error",
                value=f"```\n{error_message[:1000]}\n```",
                inline=False
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
        except Exception as e:
            await interaction.followup.send(
                f"An unexpected error occurred: {e}",
                ephemeral=True
            )

    # Docker command group
    docker_group = discord.app_commands.Group(name="docker", description="Docker container management")

    @docker_group.command(name="start", description="Start a stopped Docker container.")
    @discord.app_commands.describe(container="The name of the container to start.")
    @discord.app_commands.autocomplete(container=docker_container_autocomplete)
    async def docker_start(self, interaction: discord.Interaction, container: str):
        """Start a Docker container"""
        await self.run_docker_command(interaction, container, "start")

    @docker_group.command(name="stop", description="Stop a running Docker container.")
    @discord.app_commands.describe(container="The name of the container to stop.")
    @discord.app_commands.autocomplete(container=docker_container_autocomplete)
    async def docker_stop(self, interaction: discord.Interaction, container: str):
        """Stop a Docker container"""
        await self.run_docker_command(interaction, container, "stop")

    @docker_group.command(name="restart", description="Restart a Docker container.")
    @discord.app_commands.describe(container="The name of the container to restart.")
    @discord.app_commands.autocomplete(container=docker_container_autocomplete)
    async def docker_restart(self, interaction: discord.Interaction, container: str):
        """Restart a Docker container"""
        await self.run_docker_command(interaction, container, "restart")

    @docker_group.command(name="ps", description="List running Docker containers.")
    async def docker_ps(self, interaction: discord.Interaction):
        """List running Docker containers"""
        await interaction.response.defer(ephemeral=True)

        try:
            # Check if docker is available
            subprocess.run(["which", "docker"], check=True, capture_output=True, timeout=5)

            # Get container list
            cmd = ["docker", "ps", "--format", "{{.Names}}\t{{.Image}}\t{{.Status}}"]
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
                timeout=10
            )
            output = proc.stdout.strip()

            embed = create_standard_embed(
                title="Running Docker Containers",
                command_name="docker list",
                bot=self.bot
            )

            if not output:
                embed.description = "No running containers found."
            else:
                description = "```\n{:<30} {:<40} {:<30}\n".format("NAME", "IMAGE", "STATUS")
                description += "-" * 90 + "\n"

                for line in output.splitlines():
                    try:
                        name, image, status = line.split('\t')
                        description += "{:<30} {:<40} {:<30}\n".format(
                            name[:28], image[:38], status[:28]
                        )
                    except ValueError:
                        continue

                embed.description = description + "```"

            await interaction.followup.send(embed=embed, ephemeral=True)

        except FileNotFoundError:
            await interaction.followup.send(
                "`docker` not found or error running command.",
                ephemeral=True
            )
        except subprocess.TimeoutExpired:
            await interaction.followup.send(
                "Docker command timed out.",
                ephemeral=True
            )
        except subprocess.CalledProcessError:
            await interaction.followup.send(
                "`docker` not found or error running command.",
                ephemeral=True
            )
        except Exception as e:
            await interaction.followup.send(
                f"An unexpected error occurred: {e}",
                ephemeral=True
            )

    @docker_group.command(name="stats", description="Show resource usage of running containers.")
    async def docker_stats(self, interaction: discord.Interaction):
        """Show Docker container resource usage statistics"""
        await interaction.response.defer(ephemeral=True)

        try:
            # Check if docker is available
            subprocess.run(["which", "docker"], check=True, capture_output=True, timeout=5)

            # Get container stats
            cmd = ["docker", "stats", "--no-stream", "--format", "{{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"]
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
                timeout=15
            )
            output = proc.stdout.strip()

            embed = create_standard_embed(
                title="Docker Container Stats",
                command_name="docker stats",
                bot=self.bot
            )

            if not output:
                embed.description = "No running containers to get stats for."
            else:
                description = "```\n{:<30} {:<15} {:<30}\n".format("NAME", "CPU %", "MEMORY USAGE")
                description += "-" * 75 + "\n"

                for line in output.splitlines():
                    try:
                        name, cpu, mem = line.split('\t')
                        description += "{:<30} {:<15} {:<30}\n".format(
                            name[:28], cpu, mem
                        )
                    except ValueError:
                        continue

                embed.description = description + "```"

            await interaction.followup.send(embed=embed, ephemeral=True)

        except FileNotFoundError:
            await interaction.followup.send(
                "`docker` not found or error running command.",
                ephemeral=True
            )
        except subprocess.TimeoutExpired:
            await interaction.followup.send(
                "Docker stats command timed out.",
                ephemeral=True
            )
        except subprocess.CalledProcessError:
            await interaction.followup.send(
                "`docker` not found or error running command.",
                ephemeral=True
            )
        except Exception as e:
            await interaction.followup.send(
                f"An unexpected error occurred: {e}",
                ephemeral=True
            )

    @docker_group.command(name="logs", description="Get logs from a Docker container.")
    @discord.app_commands.describe(
        container="The name of the container to get logs from.",
        lines="Number of lines to retrieve (default: 50)."
    )
    @discord.app_commands.autocomplete(container=docker_container_autocomplete)
    async def docker_logs(
        self,
        interaction: discord.Interaction,
        container: str,
        lines: discord.app_commands.Range[int, 1, 100] = 50
    ):
        """Get logs from a Docker container"""
        await interaction.response.defer(ephemeral=True)

        try:
            # Check if docker is available
            subprocess.run(["which", "docker"], check=True, capture_output=True, timeout=5)

            # Get container logs
            cmd = ["docker", "logs", "--tail", str(lines), container]
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
                timeout=10
            )

            logs = proc.stdout.strip()
            if proc.stderr.strip():
                logs += "\n" + proc.stderr.strip()

            embed = create_standard_embed(
                title=f"Docker Logs: {container}",
                command_name="docker logs",
                bot=self.bot
            )

            if not logs:
                embed.description = "No logs found."
            else:
                # Truncate logs if too long for Discord
                max_length = 4000
                if len(logs) > max_length:
                    logs = logs[-max_length:] + "\n... (truncated)"

                embed.description = f"```\n{logs}\n```"

            await interaction.followup.send(embed=embed, ephemeral=True)

        except FileNotFoundError:
            await interaction.followup.send(
                "`docker` command not found.",
                ephemeral=True
            )
        except subprocess.TimeoutExpired:
            await interaction.followup.send(
                "Docker logs command timed out.",
                ephemeral=True
            )
        except subprocess.CalledProcessError as e:
            error_message = e.stderr.strip() if e.stderr else "Container not found or error getting logs"
            await interaction.followup.send(
                f"Failed to get logs: {error_message}",
                ephemeral=True
            )
        except Exception as e:
            await interaction.followup.send(
                f"An unexpected error occurred: {e}",
                ephemeral=True
            )

async def setup(bot):
    """Setup function for loading the cog"""
    await bot.add_cog(DockerManagementCog(bot))
