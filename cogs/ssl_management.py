"""
SSL Certificate Management Cog for Logivore
Manages SSL certificates through Nginx Proxy Manager integration
"""
import discord
from discord.ext import commands
import subprocess
import asyncio
import datetime
import json
import os
from utils.i18n import i18n
from utils.embed_formatter import create_standard_embed

class SSLManagementCog(commands.Cog):
    """Handles SSL certificate management and renewal"""

    def __init__(self, bot):
        self.bot = bot
        self.npm_container = "npm-app-1"  # NPM container name
        self.npm_data_path = "/mnt/data_pool_b/npm/data"

    async def run_npm_command(self, command: list, timeout: int = 60):
        """Execute command in NPM container"""
        try:
            full_command = ["docker", "exec", self.npm_container] + command
            result = subprocess.run(
                full_command,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            return result.returncode == 0, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return False, "", "Command timed out"
        except Exception as e:
            return False, "", str(e)

    async def get_ssl_certificates(self):
        """Get list of SSL certificates"""
        try:
            success, stdout, stderr = await self.run_npm_command([
                "find", "/etc/letsencrypt/live", "-name", "fullchain.pem", "-exec",
                "dirname", "{}", ";"
            ])

            if not success:
                return []

            certificates = []
            for cert_dir in stdout.strip().split('\n'):
                if cert_dir and '/live/' in cert_dir:
                    cert_name = os.path.basename(cert_dir)

                    # Get certificate expiry
                    success, cert_info, _ = await self.run_npm_command([
                        "openssl", "x509", "-in", f"{cert_dir}/fullchain.pem",
                        "-noout", "-enddate"
                    ])

                    expiry_date = None
                    if success and cert_info:
                        try:
                            # Parse notAfter=MMM DD HH:MM:SS YYYY GMT
                            date_str = cert_info.split('notAfter=')[1].strip()
                            expiry_date = datetime.datetime.strptime(
                                date_str, "%b %d %H:%M:%S %Y %Z"
                            )
                        except:
                            pass

                    # Get certificate domains
                    success, domain_info, _ = await self.run_npm_command([
                        "openssl", "x509", "-in", f"{cert_dir}/fullchain.pem",
                        "-noout", "-text"
                    ])

                    domains = []
                    if success and domain_info:
                        for line in domain_info.split('\n'):
                            if 'DNS:' in line:
                                dns_entries = line.split('DNS:')[1:]
                                for entry in dns_entries:
                                    domain = entry.split(',')[0].strip()
                                    if domain:
                                        domains.append(domain)

                    certificates.append({
                        'name': cert_name,
                        'path': cert_dir,
                        'expiry': expiry_date,
                        'domains': domains
                    })

            return certificates

        except Exception as e:
            print(f"Error getting SSL certificates: {e}")
            return []

    async def renew_certificate(self, cert_name: str = None):
        """Renew SSL certificate(s)"""
        try:
            if cert_name:
                # Renew specific certificate
                success, stdout, stderr = await self.run_npm_command([
                    "certbot", "renew", "--cert-name", cert_name, "--force-renewal"
                ], timeout=120)
            else:
                # Renew all certificates
                success, stdout, stderr = await self.run_npm_command([
                    "certbot", "renew"
                ], timeout=300)

            # Reload nginx after renewal
            if success:
                reload_success, _, reload_error = await self.run_npm_command([
                    "nginx", "-s", "reload"
                ])
                if not reload_success:
                    stderr += f"\nNginx reload failed: {reload_error}"

            return success, stdout, stderr

        except Exception as e:
            return False, "", str(e)

    async def get_npm_proxy_hosts(self):
        """Get proxy hosts from NPM"""
        try:
            # Read proxy host configurations
            success, stdout, stderr = await self.run_npm_command([
                "find", "/data/nginx/proxy_host", "-name", "*.conf"
            ])

            if not success:
                return []

            proxy_hosts = []
            for conf_file in stdout.strip().split('\n'):
                if conf_file:
                    # Read configuration file
                    success, conf_content, _ = await self.run_npm_command([
                        "cat", conf_file
                    ])

                    if success and conf_content:
                        # Extract server_name
                        server_names = []
                        for line in conf_content.split('\n'):
                            line = line.strip()
                            if line.startswith('server_name'):
                                name = line.split()[1].rstrip(';')
                                if name != '_':
                                    server_names.append(name)

                        if server_names:
                            proxy_hosts.append({
                                'config_file': conf_file,
                                'domains': server_names
                            })

            return proxy_hosts

        except Exception as e:
            print(f"Error getting proxy hosts: {e}")
            return []

    # SSL command group
    ssl_group = discord.app_commands.Group(name="ssl", description="SSL certificate management")

    @ssl_group.command(name="list", description="List all SSL certificates and their status")
    async def ssl_list(self, interaction: discord.Interaction):
        """List all SSL certificates"""
        await interaction.response.defer(ephemeral=True)

        try:
            certificates = await self.get_ssl_certificates()

            if not certificates:
                embed = EmbedFormatter.warning_embed(
                    title="📜 SSL Certificates",
                    description="No SSL certificates found",
                    command_name="ssl list"
                )
                await interaction.followup.send(embed=embed, ephemeral=True)
                return

            embed = create_standard_embed(
                title="📜 SSL Certificates",
                command_name="ssl list",
                bot=self.bot
            )

            for cert in certificates:
                # Calculate days until expiry
                days_left = "Unknown"
                status_emoji = "⚪"

                if cert['expiry']:
                    days_left = (cert['expiry'] - datetime.datetime.now()).days
                    if days_left > 30:
                        status_emoji = "🟢"
                    elif days_left > 7:
                        status_emoji = "🟡"
                    else:
                        status_emoji = "🔴"

                domains_text = "\n".join([f"• {domain}" for domain in cert['domains'][:5]])
                if len(cert['domains']) > 5:
                    domains_text += f"\n• ... and {len(cert['domains']) - 5} more"

                embed.add_field(
                    name=f"{status_emoji} {cert['name']}",
                    value=f"**Domains:**\n{domains_text}\n**Expires:** {cert['expiry'].strftime('%Y-%m-%d') if cert['expiry'] else 'Unknown'}\n**Days left:** {days_left}",
                    inline=True
                )

            embed.set_footer(text="🟢 Good | 🟡 Renewal soon | 🔴 Urgent renewal")
            await interaction.followup.send(embed=embed, ephemeral=True)

        except Exception as e:
            await interaction.followup.send(
                f"Error retrieving SSL certificates: {str(e)}",
                ephemeral=True
            )

    @ssl_group.command(name="renew", description="Renew SSL certificate(s)")
    @discord.app_commands.describe(
        certificate="Specific certificate name to renew (leave empty for all)",
        force="Force renewal even if not needed"
    )
    async def ssl_renew(self, interaction: discord.Interaction, certificate: str = None, force: bool = False):
        """Renew SSL certificates"""
        await interaction.response.defer(ephemeral=True)

        try:
            embed = EmbedFormatter.warning_embed(
                title="🔄 SSL Certificate Renewal",
                description="Starting certificate renewal...",
                command_name="ssl renew"
            )

            if certificate:
                embed.description += f"\nTarget: `{certificate}`"
            else:
                embed.description += "\nTarget: All certificates"

            if force:
                embed.description += "\nMode: Force renewal"

            await interaction.followup.send(embed=embed, ephemeral=True)

            # Perform renewal
            if certificate:
                success, stdout, stderr = await self.renew_certificate(certificate)
            else:
                success, stdout, stderr = await self.renew_certificate()

            # Update embed with results
            if success:
                embed.title = "✅ Certificate Renewal Successful"
                embed.color = 0x4caf50
                embed.description = "SSL certificate(s) renewed successfully"

                if "renewed" in stdout.lower():
                    embed.add_field(
                        name="Renewal Status",
                        value="✅ Certificate(s) were renewed",
                        inline=False
                    )
                elif "not yet due" in stdout.lower():
                    embed.add_field(
                        name="Renewal Status",
                        value="ℹ️ Certificate(s) not yet due for renewal",
                        inline=False
                    )
                else:
                    embed.add_field(
                        name="Renewal Status",
                        value="✅ Process completed",
                        inline=False
                    )

            else:
                embed.title = "❌ Certificate Renewal Failed"
                embed.color = 0xf44336
                embed.description = "Failed to renew SSL certificate(s)"
                embed.add_field(
                    name="Error",
                    value=f"```\n{stderr[:1000]}\n```",
                    inline=False
                )

            # Show output if available
            if stdout and len(stdout) < 1000:
                embed.add_field(
                    name="Output",
                    value=f"```\n{stdout}\n```",
                    inline=False
                )

            # Edit the original message
            await interaction.edit_original_response(embed=embed)

        except Exception as e:
            error_embed = EmbedFormatter.error_embed(
                title="❌ Renewal Error",
                description=f"Unexpected error: {str(e)}",
                command_name="ssl renew"
            )
            await interaction.edit_original_response(embed=error_embed)

    @ssl_group.command(name="status", description="Check SSL certificate and NPM status")
    async def ssl_status(self, interaction: discord.Interaction):
        """Check overall SSL and NPM status"""
        await interaction.response.defer(ephemeral=True)

        try:
            # Check NPM container status
            npm_running = False
            try:
                result = subprocess.run(
                    ["docker", "ps", "--filter", f"name={self.npm_container}", "--format", "{{.Status}}"],
                    capture_output=True, text=True, timeout=10
                )
                npm_running = "Up" in result.stdout
            except:
                pass

            # Get certificate count and expiry info
            certificates = await self.get_ssl_certificates()

            # Get proxy hosts
            proxy_hosts = await self.get_npm_proxy_hosts()

            if npm_running:
                embed = EmbedFormatter.success_embed(
                    title="🔐 SSL & NPM Status",
                    command_name="ssl status"
                )
            else:
                embed = EmbedFormatter.error_embed(
                    title="🔐 SSL & NPM Status",
                    command_name="ssl status"
                )

            # NPM Status
            embed.add_field(
                name="🐳 Nginx Proxy Manager",
                value=f"{'🟢 Running' if npm_running else '🔴 Stopped'}",
                inline=True
            )

            # Certificate summary
            cert_summary = f"Total: {len(certificates)}\n"

            if certificates:
                expiring_soon = 0
                expired = 0

                for cert in certificates:
                    if cert['expiry']:
                        days_left = (cert['expiry'] - datetime.datetime.now()).days
                        if days_left <= 0:
                            expired += 1
                        elif days_left <= 30:
                            expiring_soon += 1

                cert_summary += f"Expiring soon (≤30d): {expiring_soon}\n"
                cert_summary += f"Expired: {expired}"

            embed.add_field(
                name="📜 SSL Certificates",
                value=cert_summary,
                inline=True
            )

            # Proxy hosts
            embed.add_field(
                name="🌐 Proxy Hosts",
                value=f"Configured: {len(proxy_hosts)}",
                inline=True
            )

            # Quick actions
            embed.add_field(
                name="🚀 Quick Actions",
                value="`/ssl list` - View all certificates\n`/ssl renew` - Renew certificates\n`/docker restart npm-app-1` - Restart NPM",
                inline=False
            )

            await interaction.followup.send(embed=embed, ephemeral=True)

        except Exception as e:
            await interaction.followup.send(
                f"Error checking SSL status: {str(e)}",
                ephemeral=True
            )

    @ssl_group.command(name="check_expiry", description="Check certificates expiring soon")
    @discord.app_commands.describe(days="Number of days to check ahead (default: 30)")
    async def ssl_check_expiry(self, interaction: discord.Interaction, days: int = 30):
        """Check certificates expiring soon"""
        await interaction.response.defer(ephemeral=True)

        try:
            certificates = await self.get_ssl_certificates()

            if not certificates:
                await interaction.followup.send(
                    "No SSL certificates found",
                    ephemeral=True
                )
                return

            expiring_certs = []
            for cert in certificates:
                if cert['expiry']:
                    days_left = (cert['expiry'] - datetime.datetime.now()).days
                    if days_left <= days:
                        expiring_certs.append((cert, days_left))

            if not expiring_certs:
                embed = EmbedFormatter.success_embed(
                    title="✅ Certificate Expiry Check",
                    description=f"No certificates expiring within {days} days",
                    command_name="ssl check"
                )
            else:
                if days <= 30:
                    embed = EmbedFormatter.warning_embed(
                        title="⚠️ Certificates Expiring Soon",
                        description=f"Found {len(expiring_certs)} certificate(s) expiring within {days} days",
                        command_name="ssl check"
                    )
                else:
                    embed = EmbedFormatter.error_embed(
                        title="⚠️ Certificates Expiring Soon",
                        description=f"Found {len(expiring_certs)} certificate(s) expiring within {days} days",
                        command_name="ssl check"
                )

                for cert, days_left in expiring_certs:
                    status = "🔴 EXPIRED" if days_left <= 0 else f"⚠️ {days_left} days left"
                    domains = ", ".join(cert['domains'][:3])
                    if len(cert['domains']) > 3:
                        domains += f" (+{len(cert['domains']) - 3} more)"

                    embed.add_field(
                        name=f"{cert['name']} - {status}",
                        value=f"Domains: {domains}\nExpires: {cert['expiry'].strftime('%Y-%m-%d %H:%M')}",
                        inline=False
                    )

                embed.add_field(
                    name="🔧 Action Required",
                    value="Use `/ssl renew` to renew certificates",
                    inline=False
                )

            await interaction.followup.send(embed=embed, ephemeral=True)

        except Exception as e:
            await interaction.followup.send(
                f"Error checking certificate expiry: {str(e)}",
                ephemeral=True
            )

async def setup(bot):
    """Setup function for loading the cog"""
    await bot.add_cog(SSLManagementCog(bot))
