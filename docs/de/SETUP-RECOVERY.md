# Auto-Wiederherstellung nach Reboot – Leitfaden

Sprachen: Deutsch (diese Seite) | [繁體中文](../../SETUP-RECOVERY.md) | [简体中文](../zh-cn/SETUP-RECOVERY.md)

## 🎯 Überblick

Nach Systemneustart Dienste automatisch wiederherstellen:
- Docker-Container
- systemd-Services
- Boot-Skripte
- Monitoring & Benachrichtigungen

## 🔧 Installation & Konfiguration

### 1) sudo-Rechte setzen
```bash
sudo cp systemd-examples/logivore-bot-sudoers /etc/sudoers.d/logivore
sudo chmod 440 /etc/sudoers.d/logivore
```

### 2) Boot-Recovery-Skript installieren
```bash
sudo mkdir -p /opt/logivore/scripts
sudo cp scripts/boot-recovery.sh /opt/logivore/scripts/
sudo chmod +x /opt/logivore/scripts/boot-recovery.sh

sudo cp systemd-examples/logivore-boot-recovery.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable logivore-boot-recovery.service
```

### 3) Docker-Restart-Policy
```bash
docker update --restart=unless-stopped <container>
```
oder in `docker-compose.yml`:
```yaml
services:
  myapp:
    image: myapp:latest
    restart: unless-stopped
```

### 4) systemd-Autostart
```bash
sudo systemctl enable service_name
sudo systemctl is-enabled service_name
```

## 🚀 Verwendung (Discord)

```
/recovery save_state    # aktuellen Zustand sichern
/recovery recover_now   # sofortige Wiederherstellung
/recovery config auto_recovery:True monitored_services:"nginx,mysql,redis"
/recovery status

/reboot schedule hours:6
/reboot now delay:5
/reboot status
/reboot cancel
```

## ⚙️ Erweiterte Einstellungen

```bash
# /opt/logivore/scripts/boot-recovery.sh
CUSTOM_SERVICES=("nginx" "mysql" "redis" "your-service")
DOCKER_COMPOSE_DIRS=("/opt/docker-apps" "/home/user/projects")
```

Restart-Policy: `no` | `always` | `unless-stopped` (empfohlen) | `on-failure`

Startverzögerung:
```bash
sleep 60
# oder systemd-Abhängigkeiten
After=network.target docker.service mysql.service
```

## 🔍 Troubleshooting

Logs prüfen:
```bash
sudo tail -f /var/log/logivore-boot-recovery.log
sudo journalctl -u logivore-boot-recovery.service -f
docker logs <container>
```

Häufige Probleme: RestartPolicy, sudoers/Dateirechte, Abhängigkeiten/Verzögerungen.

## 📊 Monitoring & Benachrichtigungen

Neustart erkennen → Dienste wiederherstellen → in Discord melden → protokollieren.

