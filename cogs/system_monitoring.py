"""
System Monitoring Cog for Logivore
Handles system stats collection, monitoring panels, and background tasks
"""
import discord
from discord.ext import tasks, commands
import psutil
import socket
import subprocess
import datetime
import time
import re
import asyncio
from utils import get_bar, format_bytes, format_uptime, get_core_bars
from typing import List
from utils.i18n import i18n
from utils.embed_formatter import create_standard_embed

class SystemMonitoringCog(commands.Cog):
    """Handles system monitoring and real-time panels"""

    def __init__(self, bot):
        self.bot = bot
        self.monitoring_tasks = {}

    def cog_unload(self):
        """Clean up monitoring tasks when cog is unloaded"""
        if hasattr(self, '_monitor_update_task'):
            self._monitor_update_task.cancel()

    def get_system_stats(self) -> dict:
        """Collect comprehensive system statistics"""
        hostname = socket.gethostname()
        uptime_seconds = datetime.datetime.now().timestamp() - psutil.boot_time()
        cpu_percent = psutil.cpu_percent(interval=0.1)  # Reduced from 1 second to 0.1 second
        per_cpu_percent = psutil.cpu_percent(interval=None, percpu=True)

        # CPU Temperature
        temps = psutil.sensors_temperatures()
        cpu_temp = "N/A"
        if temps:
            for name in temps:
                if any(keyword in name.lower() for keyword in ["coretemp", "cpu", "k10temp"]):
                    for entry in temps[name]:
                        if any(keyword in entry.label.lower() for keyword in ["package", "input"]) or entry.label == '':
                            cpu_temp = f"{entry.current}°C"
                            break
                    break

        # Memory and Swap
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()

        # Disk Information
        disks = []
        disk_io = psutil.disk_io_counters(perdisk=True)
        monitored_disks = self.bot.config.get("monitored_disks")

        partitions = psutil.disk_partitions(all=False)
        target_mounts = {p.mountpoint for p in partitions}
        if monitored_disks:
            target_mounts.update(monitored_disks)

        for path in target_mounts:
            try:
                usage = psutil.disk_usage(path)
                device_name = next(
                    (p.device.replace('/dev/', '') for p in partitions if p.mountpoint == path),
                    None
                )
                io = disk_io.get(device_name) if device_name else None
                disks.append({
                    "device": device_name or path,
                    "mountpoint": path,
                    "percent": usage.percent,
                    "used_gb": usage.used / (1024**3),
                    "total_gb": usage.total / (1024**3),
                    "read_gb": io.read_bytes / (1024**3) if io else 0,
                    "write_gb": io.write_bytes / (1024**3) if io else 0,
                })
            except (PermissionError, FileNotFoundError):
                continue

        # Network Information
        net_io = psutil.net_io_counters()
        listening_ports = [
            conn for conn in psutil.net_connections(kind='inet')
            if conn.status == 'LISTEN'
        ]

        # Docker containers count
        try:
            docker_count_proc = subprocess.run(
                "docker ps -q | wc -l",
                shell=True,
                capture_output=True,
                text=True,
                timeout=2  # Reduced timeout
            )
            docker_count = int(docker_count_proc.stdout.strip())
        except (FileNotFoundError, ValueError, subprocess.TimeoutExpired):
            docker_count = "N/A"

        # Public IP - skip for faster loading
        public_ip = "N/A (disabled for performance)"

        return {
            "hostname": hostname,
            "public_ip": public_ip,
            "uptime_seconds": uptime_seconds,
            "cpu_percent": cpu_percent,
            "per_cpu_percent": per_cpu_percent,
            "cpu_temp": cpu_temp,
            "mem_percent": mem.percent,
            "mem_used_gb": mem.used / (1024**3),
            "mem_total_gb": mem.total / (1024**3),
            "swap_percent": swap.percent,
            "swap_used_gb": swap.used / (1024**3),
            "swap_total_gb": swap.total / (1024**3),
            "disks": disks,
            "net_sent_gb": net_io.bytes_sent / (1024**3),
            "net_recv_gb": net_io.bytes_recv / (1024**3),
            "listening_ports_count": len(listening_ports),
            "docker_count": docker_count,
        }

    def format_stats_embed(self, stats: dict) -> discord.Embed:
        """Format system stats into a Discord embed"""
        # Header section
        header = f"Hostname: {stats['hostname']} | {i18n.t('system.uptime')}: {format_uptime(stats['uptime_seconds'])}"

        # CPU section with temperature
        cpu_line = f"{i18n.t('system.cpu')} ({stats['cpu_temp']}): {get_bar(stats['cpu_percent'])} {stats['cpu_percent']:>5.1f}%"
        core_bars = get_core_bars(stats['per_cpu_percent'])
        if core_bars:
            cpu_section = f"{cpu_line}\n{core_bars}"
        else:
            cpu_section = cpu_line

        # Memory section
        mem_section = (
            f"{i18n.t('system.memory')}: {get_bar(stats['mem_percent'])} {stats['mem_percent']:>5.1f}%\n"
            f"        [{stats['mem_used_gb']:>11.3f} / {stats['mem_total_gb']:>11.3f} GB]"
        )

        # Swap section (only if exists)
        swap_section = ""
        if stats['swap_total_gb'] > 0:
            swap_section = (
                f"{i18n.t('system.swap')}: {get_bar(stats['swap_percent'])} {stats['swap_percent']:>5.1f}%\n"
                f"        [{stats['swap_used_gb']:>11.3f} / {stats['swap_total_gb']:>11.3f} GB]"
            )

        # Disk section - improved formatting
        disk_sections = []
        if stats['disks']:
            disk_sections.append("Disk:")
            for i, disk in enumerate(stats['disks']):
                # Create friendly disk names
                mount = disk['mountpoint']
                if mount == '/':
                    disk_name = "Root"
                elif mount == '/boot/efi':
                    disk_name = "EFI Boot"
                elif mount.startswith('/mnt/'):
                    # Extract meaningful name from mount point
                    name_part = mount[5:]  # Remove '/mnt/'
                    if 'data_pool' in name_part:
                        disk_name = name_part.replace('data_pool_', 'Data Pool ').title()
                    elif 'backup' in name_part:
                        disk_name = "Backup"
                    else:
                        disk_name = name_part.title()
                else:
                    disk_name = mount.replace('/', '').title() or "Unknown"

                disk_line = (
                    f"  {disk_name:<12}: {get_bar(disk['percent'])} {disk['percent']:>5.1f}%\n"
                    f"                [{disk['used_gb']:>10.3f} / {disk['total_gb']:>10.3f} GB    ]\n"
                    f"                [Read: {format_bytes(disk['read_gb'] * 1024**3):>7} / Write: {format_bytes(disk['write_gb'] * 1024**3):>7}]"
                )
                disk_sections.append(disk_line)
        else:
            disk_sections.append(f"{i18n.t('system.disk')}: {i18n.t('system.no_physical_disks')}")

        # Network section
        net_section = (
            f"{i18n.t('system.network')}: Up {format_bytes(stats['sent_speed'])}/s | Down {format_bytes(stats['recv_speed'])}/s\n"
            f"         {i18n.t('system.total_sent')}: {format_bytes(stats['net_sent_gb'] * 1024**3)} | {i18n.t('system.total_recv')}: {format_bytes(stats['net_recv_gb'] * 1024**3)}"
        )

        # Services section
        services_section = f"{i18n.t('system.services')}: {stats['listening_ports_count']} {i18n.t('system.listening_ports')} | {stats['docker_count']} {i18n.t('system.docker_containers')}"

        # Combine all sections with proper spacing
        sections = [
            header,
            "=" * 60,
            cpu_section,
            "",
            mem_section,
        ]

        if swap_section:
            sections.extend(["", swap_section])

        sections.extend([
            "",
            *disk_sections,
            "",
            net_section,
            "",
            services_section
        ])

        content = "```\n" + "\n".join(sections) + "\n```"

        embed = create_standard_embed(
            title=i18n.t('system.status'),
            description=content,
            command_name="monitor",
            bot=self.bot
        )

        # Override footer for auto-refresh info
        lang = self.bot.config.get("language", "en")
        if lang == 'zh':
            footer_text = f"由 Serelix Studio 提供支援 • {i18n.t('system.auto_refresh', interval=self.bot.config.get('update_interval'))}"
        else:
            footer_text = f"Powered by Serelix Studio • {i18n.t('system.auto_refresh', interval=self.bot.config.get('update_interval'))}"
        embed.set_footer(text=footer_text)
        return embed

    async def _monitor_loop(self):
        """Main monitoring loop that updates all active monitors"""
        while True:
            try:
                await asyncio.sleep(self.bot.config.get("update_interval"))

                # Check if there are any active monitoring tasks
                if not self.monitoring_tasks:
                    break

                # Update each active monitor
                for channel_id, task_data in list(self.monitoring_tasks.items()):
                    try:
                        message = task_data['message']
                        last_net_io, last_time = task_data['last_net_io'], task_data['last_time']
                        current_net_io, current_time = psutil.net_io_counters(), time.time()
                        time_diff = current_time - last_time or self.bot.config.get("update_interval")

                        sent_speed = (current_net_io.bytes_sent - last_net_io.bytes_sent) / time_diff
                        recv_speed = (current_net_io.bytes_recv - last_net_io.bytes_recv) / time_diff

                        task_data['last_net_io'], task_data['last_time'] = current_net_io, current_time

                        stats = self.get_system_stats()
                        stats['sent_speed'], stats['recv_speed'] = sent_speed, recv_speed
                        await message.edit(embed=self.format_stats_embed(stats))

                    except discord.NotFound:
                        print(f"Message in channel {channel_id} not found. Removing monitor.")
                        del self.monitoring_tasks[channel_id]
                    except discord.Forbidden as e:
                        print(f"No permission to update message in channel {channel_id}: {e}")
                        del self.monitoring_tasks[channel_id]
                    except discord.HTTPException as e:
                        if e.code == 50027:  # Invalid Webhook Token
                            print(f"Invalid webhook token for channel {channel_id}. Removing monitor.")
                            del self.monitoring_tasks[channel_id]
                        elif e.code == 10008:  # Unknown Message
                            print(f"Message deleted in channel {channel_id}. Removing monitor.")
                            del self.monitoring_tasks[channel_id]
                        else:
                            print(f"HTTP error updating monitor in channel {channel_id}: {e}")
                            # Don't delete for temporary HTTP errors, just skip this update
                    except Exception as e:
                        print(f"Unexpected error updating monitor in channel {channel_id}: {e}")
                        # Only delete on repeated failures
                        task_data['error_count'] = task_data.get('error_count', 0) + 1
                        if task_data['error_count'] >= 3:
                            print(f"Too many errors for monitor in channel {channel_id}. Removing.")
                            del self.monitoring_tasks[channel_id]

            except asyncio.CancelledError:
                print("Monitor loop cancelled")
                break
            except Exception as e:
                print(f"Unexpected error in monitor loop: {e}")
                await asyncio.sleep(5)  # Wait before retrying

    @discord.app_commands.command(name="monitor", description="Control the system monitoring panel.")
    @discord.app_commands.describe(action="Choose to start or stop the monitoring.")
    @discord.app_commands.choices(action=[
        discord.app_commands.Choice(name="start", value="start"),
        discord.app_commands.Choice(name="stop", value="stop"),
    ])
    async def monitor(self, interaction: discord.Interaction, action: discord.app_commands.Choice[str]):
        """Start or stop system monitoring in current channel"""
        channel_id = interaction.channel.id

        if action.value == "start":
            if channel_id in self.monitoring_tasks:
                await interaction.response.send_message(
                    "Monitor already active.",
                    ephemeral=True
                )
                return

            initial_embed = EmbedFormatter.info_embed(
                title="System Monitor",
                description="Initializing system monitor...",
                command_name="monitor"
            )
            await interaction.response.send_message(embed=initial_embed)
            message = await interaction.original_response()

            # Get initial stats and update message immediately
            try:
                stats = self.get_system_stats()
                stats['sent_speed'], stats['recv_speed'] = 0, 0  # Initial values
                await message.edit(embed=self.format_stats_embed(stats))
            except Exception as e:
                await message.edit(content=f"Error initializing monitor: {str(e)}")
                return

            # Create monitoring task data
            self.monitoring_tasks[channel_id] = {
                "message": message,
                "last_net_io": psutil.net_io_counters(),
                "last_time": time.time(),
                "error_count": 0  # Reset error count for new monitor
            }

            # Start the update loop if not already running
            if not hasattr(self, '_monitor_update_task') or self._monitor_update_task.done():
                self._monitor_update_task = asyncio.create_task(self._monitor_loop())

            print(f"Started monitoring in channel {channel_id}")

        elif action.value == "stop":
            if channel_id not in self.monitoring_tasks:
                await interaction.response.send_message(
                    "No monitor active.",
                    ephemeral=True
                )
                return

            message = self.monitoring_tasks[channel_id]["message"]

            stopped_embed = EmbedFormatter.info_embed(
                title="System Monitor Stopped",
                description="```\nSYSTEM STATUS\nMonitoring has been stopped.\n```",
                command_name="monitor stop"
            )

            try:
                await message.edit(embed=stopped_embed)
            except discord.NotFound:
                pass

            del self.monitoring_tasks[channel_id]

            # If no more monitors, the loop will stop automatically
            await interaction.response.send_message("Monitoring stopped.", ephemeral=True)
            print(f"Stopped monitoring in channel {channel_id}")

    @discord.app_commands.command(name="monitor_cleanup", description="Clean up failed monitoring tasks.")
    async def monitor_cleanup(self, interaction: discord.Interaction):
        """Clean up failed monitoring tasks"""
        await interaction.response.defer(ephemeral=True)

        try:
            # Test all monitoring tasks
            failed_tasks = []
            for channel_id, task_data in list(self.monitoring_tasks.items()):
                try:
                    message = task_data["message"]
                    # Try to fetch the message to check if it's still valid
                    await message.fetch()
                except (discord.NotFound, discord.HTTPException, discord.Forbidden):
                    failed_tasks.append(channel_id)
                    del self.monitoring_tasks[channel_id]

            if failed_tasks:
                embed = EmbedFormatter.success_embed(
                    title="🧹 Monitor Cleanup",
                    description=f"Cleaned up {len(failed_tasks)} failed monitoring tasks",
                    command_name="monitor cleanup"
                )
                embed.add_field(
                    name="Affected Channels",
                    value=", ".join([f"<#{cid}>" for cid in failed_tasks]),
                    inline=False
                )
            else:
                embed = EmbedFormatter.success_embed(
                    title="✅ Monitor Status",
                    description="All monitoring tasks are working properly",
                    command_name="monitor cleanup"
                )

            embed.add_field(
                name="Active Monitors",
                value=f"{len(self.monitoring_tasks)} channels",
                inline=True
            )

            await interaction.followup.send(embed=embed, ephemeral=True)

        except Exception as e:
            await interaction.followup.send(
                f"Error during cleanup: {str(e)}",
                ephemeral=True
            )

    @discord.app_commands.command(name="ports", description="Show listening network ports.")
    async def ports(self, interaction: discord.Interaction):
        """Display all listening network ports"""
        await interaction.response.defer(ephemeral=True)

        try:
            # 1) Collect Docker host port mappings
            docker_mappings = []
            try:
                proc = subprocess.run(
                    ["docker", "ps", "--format", "{{.Names}}\t{{.ID}}\t{{.Ports}}"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if proc.returncode == 0 and proc.stdout.strip():
                    for line in proc.stdout.strip().split("\n"):
                        try:
                            name, cid, ports_str = line.split("\t", 2)
                        except ValueError:
                            # If no ports field present
                            parts = line.split("\t")
                            if len(parts) >= 2:
                                name, cid = parts[0], parts[1]
                                ports_str = ""
                            else:
                                continue
                        if not ports_str or ports_str.lower() == "<none>":
                            continue
                        # ports_str example: "0.0.0.0:8080->80/tcp, :::8080->80/tcp, 127.0.0.1:6379->6379/tcp"
                        for seg in [s.strip() for s in ports_str.split(',') if s.strip()]:
                            if '->' not in seg:
                                continue
                            left, right = seg.split('->', 1)
                            host = left.strip()
                            cont = right.strip()  # e.g. 80/tcp OR 80-81/tcp
                            # Extract host port
                            host_port = host.split(':')[-1] if ':' in host else host
                            proto = cont.split('/')[-1] if '/' in cont else 'tcp'
                            docker_mappings.append({
                                'host': host,
                                'host_port': host_port,
                                'proto': proto[:5].upper(),
                                'container': name,
                                'target': cont.split('/')[0]
                            })
            except (subprocess.TimeoutExpired, FileNotFoundError):
                pass

            # 2) Collect system port listeners (host occupancy by processes)
            connections = psutil.net_connections(kind='inet')
            listening_ports = [conn for conn in connections if conn.status == 'LISTEN']

            sys_rows = []
            for conn in listening_ports:
                try:
                    proto = 'TCP' if conn.type == socket.SOCK_STREAM else 'UDP'
                    pid = conn.pid or 0
                    pname = 'Unknown'
                    if pid:
                        try:
                            pname = psutil.Process(pid).name()
                        except (psutil.NoSuchProcess, psutil.AccessDenied):
                            pname = 'N/A'
                    sys_rows.append({
                        'host': (conn.laddr.ip or '')[:15],
                        'port': conn.laddr.port,
                        'proto': proto,
                        'pid': pid,
                        'process': (pname or 'N/A')[:19]
                    })
                except Exception:
                    continue

            # Aggregate duplicates (IPv4/IPv6) for Docker mappings
            agg = {}
            for m in docker_mappings:
                key = (str(m['host_port']), m['proto'], m['container'], m['target'])
                entry = agg.setdefault(key, {'ipv4': False, 'ipv6': False})
                h = m['host']
                if '::' in h or h.startswith('['):
                    entry['ipv6'] = True
                else:
                    entry['ipv4'] = True
            docker_agg = []
            for (port, proto, container, target), flags in agg.items():
                ipver = '*' if (flags['ipv4'] and flags['ipv6']) else ('v6' if flags['ipv6'] else 'v4')
                docker_agg.append({'port': port, 'ipver': ipver, 'proto': proto, 'container': container, 'target': target})
            docker_agg.sort(key=lambda x: (x['proto'], int(str(x['port']).split('-')[0]) if str(x['port']).split('-')[0].isdigit() else 0, x['container']))

            # Aggregate duplicates for system listeners by (port, proto, pid, process)
            sys_rows.sort(key=lambda x: (x['proto'], x['port']))
            sys_agg_map = {}
            for r in sys_rows:
                k = (r['port'], r['proto'], r['pid'], r['process'])
                e = sys_agg_map.setdefault(k, {'ipv4': False, 'ipv6': False})
                # psutil doesn't directly expose IP version, infer from address
                ip = r.get('host') or ''
                if ':' in ip and not ip.count('.'):
                    e['ipv6'] = True
                else:
                    e['ipv4'] = True
            sys_agg = []
            for (port, proto, pid, process), flags in sys_agg_map.items():
                ipver = '*' if (flags['ipv4'] and flags['ipv6']) else ('v6' if flags['ipv6'] else 'v4')
                sys_agg.append({'port': port, 'proto': proto, 'pid': pid, 'process': process, 'ipver': ipver})
            sys_agg.sort(key=lambda x: (x['proto'], x['port'], x['pid']))

            # Build paginated content
            def build_pages(title_prefix: str, header: str, rows: List[str], max_chars: int = 1900):
                pages = []
                page = header
                for r in rows:
                    if len(page) + len(r) + 6 > max_chars:  # 6 for code block fences and slack
                        pages.append(page)
                        page = header
                    page += r + "\n"
                if page.strip():
                    pages.append(page)
                # Wrap in code blocks and make embeds
                embeds = []
                for idx, content in enumerate(pages, start=1):
                    desc = f"```\n{content}```"
                    emb = create_standard_embed(
                        title=f"📡 {title_prefix} ({idx}/{len(pages)})",
                        description=desc,
                        command_name="ports",
                        bot=self.bot
                    )
                    embeds.append(emb)
                return embeds

            # Docker pages (merged IPv4/IPv6)
            docker_rows = [
                "{:<8} {:<3} {:<5} {:<18} {:<12}".format(str(m['port'])[:8], m['ipver'], m['proto'], m['container'][:18], m['target'][:12])
                for m in docker_agg
            ]
            docker_header = "{:<8} {:<3} {:<5} {:<18} {:<12}\n{}\n".format("PORT", "IP", "PROTO", "CONTAINER", "TARGET", "-" * 60)
            docker_pages = build_pages("Ports — Docker Mappings", docker_header, docker_rows) if docker_rows else []

            # System pages (merged IPv4/IPv6)
            system_rows = [
                "{:<8} {:<3} {:<5} {:<8} {:<20}".format(r['port'], r['ipver'], r['proto'], str(r['pid'])[:8], r['process'])
                for r in sys_agg
            ]
            system_header = "{:<8} {:<3} {:<5} {:<8} {:<20}\n{}\n".format("PORT", "IP", "PROTO", "PID", "PROCESS", "-" * 60)
            system_pages = build_pages("Ports — System Listeners", system_header, system_rows) if system_rows else []

            all_pages = docker_pages + system_pages

            if not all_pages:
                embed = create_standard_embed(
                    title="📡 Network Ports",
                    description="No host port usage detected (Docker mappings and system listeners are empty).",
                    command_name="ports",
                    bot=self.bot
                )
                await interaction.followup.send(embed=embed, ephemeral=True)
                return

            # Add a footer with totals to each page
            total_text = f"Docker mappings: {len(docker_rows)} | System listeners: {len(system_rows)}"
            for emb in all_pages:
                emb.set_footer(text=total_text)

            # If only one page, just send it
            if len(all_pages) <= 1:
                await interaction.followup.send(embed=all_pages[0], ephemeral=True)
                return

            # Paginated view with buttons
            class PaginatorView(discord.ui.View):
                def __init__(self, pages: List[discord.Embed], timeout: float = 180):
                    super().__init__(timeout=timeout)
                    self.pages = pages
                    self.index = 0
                    self.message = None

                async def on_timeout(self):
                    for child in self.children:
                        if isinstance(child, discord.ui.Button):
                            child.disabled = True
                    if self.message:
                        try:
                            await self.message.edit(view=self)
                        except Exception:
                            pass

                async def update(self, interaction: discord.Interaction):
                    # Update button states
                    self.first.disabled = self.prev.disabled = (self.index == 0)
                    self.next.disabled = self.last.disabled = (self.index >= len(self.pages) - 1)
                    await interaction.response.edit_message(embed=self.pages[self.index], view=self)

                @discord.ui.button(label="⏮", style=discord.ButtonStyle.secondary)
                async def first(self, interaction: discord.Interaction, button: discord.ui.Button):
                    self.index = 0
                    await self.update(interaction)

                @discord.ui.button(label="◀", style=discord.ButtonStyle.secondary)
                async def prev(self, interaction: discord.Interaction, button: discord.ui.Button):
                    if self.index > 0:
                        self.index -= 1
                    await self.update(interaction)

                @discord.ui.button(label="▶", style=discord.ButtonStyle.secondary)
                async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
                    if self.index < len(self.pages) - 1:
                        self.index += 1
                    await self.update(interaction)

                @discord.ui.button(label="⏭", style=discord.ButtonStyle.secondary)
                async def last(self, interaction: discord.Interaction, button: discord.ui.Button):
                    self.index = len(self.pages) - 1
                    await self.update(interaction)

            view = PaginatorView(all_pages)
            try:
                msg = await interaction.followup.send(embed=all_pages[0], view=view, ephemeral=True)
                view.message = msg
            except discord.HTTPException as send_err:
                # Fallback: send as file if embed fails validation
                try:
                    import io
                    docker_header = "DOCKER MAPPINGS\n{:<21} {:<5} {:<18} {:<12}\n{}\n".format(
                        "HOST", "PROTO", "CONTAINER", "TARGET", "-" * 60
                    )
                    docker_lines = [
                        "{:<21} {:<5} {:<18} {:<12}".format(m['host'], m['proto'], m['container'], m['target'])
                        for m in docker_mappings
                    ]
                    system_header = "\n\nSYSTEM LISTENERS\n{:<8} {:<5} {:<8} {:<20}\n{}\n".format(
                        "PORT", "PROTO", "PID", "PROCESS", "-" * 60
                    )
                    system_lines = [
                        "{:<8} {:<5} {:<8} {:<20}".format(r['port'], r['proto'], str(r['pid'])[:8], r['process'])
                        for r in sys_rows
                    ]
                    full_text = docker_header + "\n".join(docker_lines) + system_header + "\n".join(system_lines)
                    bio = io.BytesIO(full_text.encode("utf-8"))
                    file = discord.File(bio, filename="ports.txt")
                    fallback = create_standard_embed(
                        title="📡 Network Ports",
                        description=(
                            "Output too long for an embed. Attached full list as ports.txt.\n"
                            f"Docker mappings: {len(docker_lines)} | System listeners: {len(system_lines)}"
                        ),
                        command_name="ports",
                        bot=self.bot
                    )
                    await interaction.followup.send(embed=fallback, file=file, ephemeral=True)
                except Exception:
                    # If even fallback fails, raise original
                    raise send_err

        except Exception as e:
            await interaction.followup.send(
                f"Error retrieving port information: {str(e)}",
                ephemeral=True
            )

    @discord.app_commands.command(name="top", description="Show top processes by CPU and memory usage.")
    @discord.app_commands.describe(count="Number of processes to show (default: 10)")
    async def top(self, interaction: discord.Interaction, count: int = 10):
        """Display top processes by resource usage"""
        await interaction.response.defer(ephemeral=True)

        try:
            if count < 1 or count > 20:
                count = 10

            # Get all processes with their CPU and memory usage
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'username']):
                try:
                    pinfo = proc.info
                    if pinfo['cpu_percent'] is None:
                        pinfo['cpu_percent'] = 0.0
                    if pinfo['memory_percent'] is None:
                        pinfo['memory_percent'] = 0.0
                    processes.append(pinfo)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

            # Sort by CPU usage first, then by memory
            processes.sort(key=lambda x: (x['cpu_percent'], x['memory_percent']), reverse=True)

            embed = create_standard_embed(
                title="📊 Top Processes",
                command_name="processes",
                bot=self.bot
            )

            if not processes:
                embed.description = "No process information available."
                await interaction.followup.send(embed=embed, ephemeral=True)
                return

            # Format process list
            content = "```\n{:<8} {:<20} {:<8} {:<8} {:<15}\n".format("PID", "NAME", "CPU%", "MEM%", "USER")
            content += "-" * 65 + "\n"

            for proc in processes[:count]:
                content += "{:<8} {:<20} {:<8.1f} {:<8.1f} {:<15}\n".format(
                    proc['pid'],
                    (proc['name'] or 'Unknown')[:19],
                    proc['cpu_percent'],
                    proc['memory_percent'],
                    (proc['username'] or 'Unknown')[:14]
                )

            content += "```"
            embed.description = content

            # Add system summary
            cpu_count = psutil.cpu_count()
            mem = psutil.virtual_memory()

            embed.add_field(
                name="System Summary",
                value=(
                    f"• CPU Cores: {cpu_count}\n"
                    f"• Total Memory: {mem.total / 1024**3:.1f} GB\n"
                    f"• Available Memory: {mem.available / 1024**3:.1f} GB\n"
                    f"• Total Processes: {len(processes)}"
                ),
                inline=False
            )

            await interaction.followup.send(embed=embed, ephemeral=True)

        except Exception as e:
            await interaction.followup.send(
                f"Error retrieving process information: {str(e)}",
                ephemeral=True
            )

    @discord.app_commands.command(name="smart", description="Show disk health information (SMART data).")
    async def smart(self, interaction: discord.Interaction):
        """Display SMART disk health information"""
        await interaction.response.defer(ephemeral=True)

        try:
            # Try to get disk information using smartctl
            disks = []

            # Get list of physical disks
            partitions = psutil.disk_partitions(all=False)
            disk_devices = set()

            for partition in partitions:
                # Extract device name (e.g., /dev/sda1 -> sda)
                device = partition.device
                if device.startswith('/dev/'):
                    # Remove partition numbers to get base device
                    base_device = re.sub(r'\d+$', '', device.split('/')[-1])
                    if base_device and len(base_device) >= 3:
                        disk_devices.add(base_device)

            embed = create_standard_embed(
                title="🔍 Disk Health (SMART)",
                command_name="health",
                bot=self.bot
            )

            if not disk_devices:
                embed.description = "No physical disks found for SMART monitoring."
                await interaction.followup.send(embed=embed, ephemeral=True)
                return

            disk_info = []

            for device in sorted(disk_devices):
                try:
                    # Try to get SMART data using smartctl
                    result = subprocess.run(
                        ['smartctl', '-H', f'/dev/{device}'],
                        capture_output=True,
                        text=True,
                        timeout=10
                    )

                    if result.returncode == 0:
                        output = result.stdout.lower()
                        if 'passed' in output:
                            health = "✅ PASSED"
                        elif 'failed' in output:
                            health = "❌ FAILED"
                        else:
                            health = "⚠️ UNKNOWN"
                    else:
                        health = "❓ NOT AVAILABLE"

                    # Get basic disk info
                    try:
                        usage = psutil.disk_usage(f'/dev/{device}')
                        size_gb = usage.total / (1024**3)
                    except:
                        size_gb = "Unknown"

                    disk_info.append({
                        'device': device,
                        'health': health,
                        'size': f"{size_gb:.1f} GB" if isinstance(size_gb, float) else size_gb
                    })

                except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
                    disk_info.append({
                        'device': device,
                        'health': "❓ SMARTCTL NOT AVAILABLE",
                        'size': "Unknown"
                    })

            if disk_info:
                content = "```\n{:<10} {:<25} {:<15}\n".format("DEVICE", "HEALTH", "SIZE")
                content += "-" * 50 + "\n"

                for disk in disk_info:
                    content += "{:<10} {:<25} {:<15}\n".format(
                        disk['device'],
                        disk['health'][:24],
                        disk['size']
                    )

                content += "```"
                embed.description = content

                # Add note about SMART requirements
                embed.add_field(
                    name="Note",
                    value=(
                        "SMART monitoring requires `smartmontools` package.\n"
                        "Install with: `sudo apt install smartmontools`\n"
                        "Some virtual environments may not support SMART."
                    ),
                    inline=False
                )
            else:
                embed.description = "No disk information available."

            await interaction.followup.send(embed=embed, ephemeral=True)

        except Exception as e:
            await interaction.followup.send(
                f"Error retrieving SMART information: {str(e)}",
                ephemeral=True
            )

async def setup(bot):
    """Setup function for loading the cog"""
    await bot.add_cog(SystemMonitoringCog(bot))
