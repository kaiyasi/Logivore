# Logivore – Docker Deployment (Optional)

Warning: Running Logivore in Docker may limit or change some monitoring and management capabilities compared to a native systemd deployment.

What may be affected
- Host visibility: Without `network_mode: host` and `pid: host`, the bot may only see container-level metrics instead of full host metrics.
- Port listing: The `/ports` view relies on host networking/proc data; without host modes, results can be incomplete.
- Reboot/systemctl: Host reboot or service control should be handled outside the container (e.g., via systemd on the host).
- File paths: Log files and configs are inside the container unless volumes are mounted.

Recommended compose settings
- `network_mode: host` and `pid: host` to improve host visibility.
- Mount `/var/run/docker.sock` (read-only) to enable Docker management commands from the bot.
- Mount volumes for `./config` and `./logs`.

Quick start
```bash
cd deploy/docker
cp ../../.env.example ../../.env   # set DISCORD_TOKEN, OWNER_ID, etc.
docker compose up -d --build
```

Files
- `docker-compose.yml` – recommended runtime configuration with host/pid mode, volumes, and security options
- `Dockerfile` – minimal Python image building the app and dependencies

Notes
- For full functionality (including safe host-level operations), prefer the system (systemd) deployment.
- Review the compose file before production, especially security and volume mounts.
