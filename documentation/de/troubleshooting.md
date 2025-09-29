# Fehlerbehebung (Logivore)

Sprachen: [Deutsch](troubleshooting.md) | [English](../troubleshooting.md) | [繁體中文](../zh-tw/troubleshooting.md) | [简体中文](../zh-cn/troubleshooting.md) | [日本語](../ja/troubleshooting.md) | [한국어](../ko/troubleshooting.md)

Häufige Probleme, Diagnose und Lösungen für systemd‑ und Docker‑Umgebungen.

## Inhalte
- Schnellcheck
- Logs/Status
- Startprobleme
- Befehle/Berechtigungen
- Docker‑Themen
- systemd‑Dienst
- SSL/Zertifikate
- Alarme
- Performance
- Fehlercodes
- Recovery
- FAQ

---

## Schnellcheck
1) `.env`: `DISCORD_TOKEN` / `OWNER_ID`
2) `pip install -r requirements.txt`
3) Rechte: Send Messages / Embed Links / Use Slash Commands
4) Pfade: `logs/` `config/`, Docker Volumes
5) Sprache: `DEFAULT_LANGUAGE` vorhanden

## Logs/Status
```bash
tail -f logs/logivore.log
python main.py 2>&1 | tee logs/startup.log
cd deploy/docker && docker compose logs -f logivore
```
Slash‑Befehls‑Sync kann einige Sekunden dauern.

## Startprobleme
- Ungültiger Token: im Developer Portal neu erzeugen, `.env` aktualisieren
- Abhängigkeiten: `pip install -r requirements.txt`
- Python: 3.8+
- Slash‑Befehle fehlen: `applications.commands` Rechte, Bot auf dem Server?

## Befehle/Berechtigungen
- Keine Ausgabe/Embeds: Channel‑Rechte prüfen
- Owner‑Befehle: `OWNER_ID` korrekt?
- 400 Bad Request (Längenlimit): Ausgabe wird paginiert/als Datei angehängt

## Docker‑Themen
- Container beendet sofort: `docker compose logs -f logivore`
- Geringe Host‑Sichtbarkeit: `network_mode: host` / `pid: host`
- `/ports` doppelt (v4/v6): zusammengeführt, IP‑Spalte v4/v6/*

## systemd‑Dienst
```bash
sudo systemctl status logivore
sudo journalctl -u logivore -f
```
`ExecStart`/`WorkingDirectory`/`User` prüfen; Boot‑Recovery siehe `systemd-examples/` & `SETUP-RECOVERY.md`.

## SSL/Zertifikate
NPM‑Container, `SSL_CERT_PATH`, OpenSSL; DNS A/AAAA; Let’s Encrypt Limits.

## Alarme
Schwellen 0–100, `alert_interval`, `alert_channel`; Empfehlungen: CPU/RAM 80–90%, Platte 85–95%.

## Performance
Intervalle erhöhen, nicht benötigte Features deaktivieren, OS‑Last mit top/htop prüfen.

## Fehlercodes
- 50035 Invalid Form Body – Längenlimit (Schutz eingebaut)
- LoginFailure – Token ungültig
- Missing Permissions – Rechte fehlen
- JSONDecodeError – config.json fehlerhaft

## Recovery
Backups: `cp -r config logs backups/$(date +%F_%T)` → bei Bedarf zurückspielen → Dienst/Container neu starten

## FAQ
- Sync dauert? Warten/Neustart/Rechte prüfen
- `/ports` zu lang? Paginierung/Anhang aktiv; ggf. Beispiel teilen
- Docker‑Sicherheit? read_only/no‑new‑privileges/tmpfs/docker.sock:ro; an Umgebung anpassen
