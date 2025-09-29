# Befehlsreferenz (Logivore)

Sprachen: [Deutsch](commands.md) | [English](../commands.md) | [繁體中文](../zh-tw/commands.md) | [简体中文](../zh-cn/commands.md) | [日本語](../ja/commands.md) | [한국어](../ko/commands.md)

Diese Referenz listet alle Slash‑Befehle, Parameter und Beispiele auf.

## Inhalt
- Systemüberwachung
- Docker‑Verwaltung
- Alarmverwaltung
- SSL‑Zertifikate
- Konfiguration
- Bot‑Verwaltung
- Hilfe
- Kategorien & Berechtigungen
- Tipps & Fehlerbehandlung

---

## Systemüberwachung

### /monitor
Echtzeit‑Dashboard (CPU/RAM/Platten/Netzwerk), auto‑refresh ~10s.
- Nutzung: `/monitor`

### /ports
Host‑Ports (Docker‑Mappings + System‑Listener), Paginierung, Fallback Anhang.
- Nutzung: `/ports`

### /top
Top‑Prozesse (CPU/RAM).
- Nutzung: `/top [count]` (Standard 10, 1–20)

### /smart
SMART‑Gesundheit (Linux, smartmontools erforderlich).
- Nutzung: `/smart`

---

## Docker‑Verwaltung

### /docker status (/docker ps)
Status/Images/Ports/Ressourcen.
- Nutzung: `/docker status`

### /docker start / stop / restart
- Nutzung: `/docker start <container>` / `stop` / `restart`

### /docker logs
Container‑Logs anzeigen.
- Nutzung: `/docker logs <container> [lines]` (Standard 50)

### /docker stats
Ressourcenstatistiken anzeigen.
- Nutzung: `/docker stats [container]`

---

## Alarmverwaltung (alerts)

### /alerts list
- Nutzung: `/alerts list`

### /alerts add
CPU/RAM/Platte/Prozess.
- Nutzung: `/alerts add <type> <threshold> [channel]`
- type: `cpu` `memory` `disk` `process`

### /alerts remove
- Nutzung: `/alerts remove <alert_id>`

### /alerts test
- Nutzung: `/alerts test [type]`

---

## SSL‑Zertifikate (ssl)

### /ssl list / check / renew / auto-renew
- Nutzung: `list`, `check <domain>`, `renew <domain>`, `auto-renew <enable|disable> [days_before]`

---

## Konfiguration (config)

### /config show
- Nutzung: `/config show [section]` (system/alerts/docker/ssl)

### /config set
- Nutzung: `/config set <key> <value>` (z. B. `update_interval 15`)

### /config reload
- Nutzung: `/config reload`

### /language (/config language)
- Nutzung: `/language [language_code]` (`en`/`zh-tw`/`zh-cn`/`ko`/`ja`/`de`/`ru`)

---

## Bot‑Verwaltung (nur Owner)
- `/restart` neu starten
- `/shutdown` sauber beenden
- `/reload <cog>` Modul neu laden
- `/sync` Slash‑Befehle synchronisieren
- `/status` Status/Serveranzahl/Ressourcen

---

## Hilfe

### /help
Kategorien anzeigen.
- Nutzung: `/help [category]` (`monitoring`/`docker`/`alerts`/`ssl`/`config`/`admin`)

---

## Kategorien & Berechtigungen
- Öffentlich: `/monitor` `/ports` `/top` `/smart` `/docker status|logs|stats` `/ssl list|check` `/config show` `/language` `/status` `/help`
- Owner: `/docker start|stop|restart` `/alerts add|remove` `/ssl renew|auto-renew` `/config set|reload` `/restart|/shutdown|/reload|/sync`
- Discord Rechte: Send Messages / Embed Links / Use Slash Commands / ggf. Manage Messages

---

## Tipps & Fehlerbehandlung
- Monitoring: `/monitor`, proaktive Alarme via `/alerts add`
- Docker: `/docker status` → `logs` → `stats`
- SSL: `/ssl auto-renew enable`, monatlich `/ssl list`
- Konfig: `/config show`/`reload`, Sprache via `/language`

Fehler: Berechtigungen/Parameter/System/Netzwerk mit klaren Meldungen und Fallbacks
