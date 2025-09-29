# Installationsanleitung (Logivore)

Sprachen: Deutsch | [English](../installation.md) | [繁體中文](../zh-tw/installation.md) | [简体中文](../zh-cn/installation.md) | [日本語](../ja/installation.md) | [한국어](../ko/installation.md)

Diese Anleitung führt dich durch die Einrichtung von Logivore – lokal, via Docker und als systemd‑Dienst.

## Inhalte
- Voraussetzungen
- Systemanforderungen
- Discord‑Bot erstellen
- Lokale Installation (ohne Container)
- Docker‑Bereitstellung (optional)
- Umgebungsvariablen (.env)
- Erster Start
- Als systemd‑Dienst (Linux)
- Fehlerbehebung

## Voraussetzungen
- Python 3.8+
- Git / pip
- Optional: Docker, Docker Compose, systemd (Linux), smartmontools (SMART)

## Systemanforderungen
- Minimum: 512MB RAM, 1GB Speicher, 1 CPU‑Kern, stabile Verbindung
- Empfohlen: 1GB+ RAM, 2GB+ Speicher, 2+ Kerne, Ubuntu 20.04+ / Windows 10+ / macOS 10.15+

## Discord‑Bot erstellen
1) [Developer Portal](https://discord.com/developers/applications) → New Application → Name „Logivore“
2) Tab „Bot“ → Add Bot
3) Intents aktivieren: Server Members, Message Content
4) Token regenerieren und sicher notieren (für `.env`)
5) OAuth2 → URL Generator: `bot` + `applications.commands`, Rechte wählen (Send Messages, Embed Links, Use Slash Commands, Read Message History, View Channels) und einladen

## Lokale Installation
```bash
git clone https://github.com/kaiyasi/Logivore.git
cd Logivore
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # DISCORD_TOKEN/OWNER_ID eintragen
python main.py
```

## Docker‑Bereitstellung (optional)
Hinweis: Docker kann Host‑Sichtbarkeit (Ports/Metriken) und Host‑Kontrollfunktionen einschränken. Für maximale Funktionen systemd nutzen.
```bash
cd deploy/docker
# .env im Projektwurzelordner vorbereiten: cp .env.example .env
docker compose up -d --build
```
Die Compose‑Datei nutzt `network_mode: host`, `pid: host` und bindet `/var/run/docker.sock:ro` für Containerverwaltung ein.

## Umgebungsvariablen (.env)
```bash
DISCORD_TOKEN=dein_bot_token
OWNER_ID=deine_discord_user_id
LOG_LEVEL=INFO
LOG_FILE=logs/logivore.log
```
Weitere Optionen: `docs/configuration.md`.

## Erster Start
Erwarte in der Konsole u. a. „✅ Bot is ready!“. Teste in Discord: `/help`, `/config show`, `/monitor`.

## Als systemd‑Dienst (Linux)
```bash
sudo nano /etc/systemd/system/logivore.service
```
```ini
[Unit]
Description=Logivore - System Monitoring Discord Bot
After=network.target

[Service]
Type=simple
User=logivore
WorkingDirectory=/home/logivore/Logivore
ExecStart=/home/logivore/Logivore/venv/bin/python main.py
Restart=always
RestartSec=10

Environment=PYTHONPATH=/home/logivore/Logivore
Environment=DISCORD_TOKEN=your_token_here
Environment=OWNER_ID=your_user_id

[Install]
WantedBy=multi-user.target
```
Aktivieren:
```bash
sudo systemctl daemon-reload
sudo systemctl enable logivore
sudo systemctl start logivore
sudo systemctl status logivore
```
Boot‑Recovery & sudoers: `systemd-examples/`, `SETUP-RECOVERY.md`.

## Fehlerbehebung
- Abhängigkeiten: `pip install -r requirements.txt`
- Token ungültig: `DISCORD_TOKEN` in `.env` prüfen
- Slash Commands fehlen: auf Sync warten, Rechte prüfen
- Docker‑Container beendet sofort: `docker compose logs -f logivore`
Debug: `LOG_LEVEL=DEBUG` oder `python main.py 2>&1 | tee logs/startup.log`
