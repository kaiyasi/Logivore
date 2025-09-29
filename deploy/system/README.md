# Logivore – System (systemd) Deployment [Recommended]

This is the recommended deployment for servers to ensure maximum visibility and reliability.

References
- `systemd-examples/` – example unit files and sudoers configuration
  - `logivore-boot-recovery.service` – boot recovery helper
  - `logivore-reboot-helper.service` – reboot helper service
  - `logivore-bot-sudoers` – sudoers example for controlled system operations
- `SETUP-RECOVERY.md` – step-by-step guide for boot recovery and service automation

Quick steps
```bash
sudo cp systemd-examples/logivore-boot-recovery.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable logivore-boot-recovery.service
sudo systemctl start logivore-boot-recovery.service

sudo cp systemd-examples/logivore-bot-sudoers /etc/sudoers.d/logivore
sudo chmod 440 /etc/sudoers.d/logivore
sudo visudo -c
```

Notes
- Adjust `User=` and `ExecStart=` paths in unit files to match your environment.
- Use systemd for host-level control (reboots, service management) instead of doing these from inside a container.
