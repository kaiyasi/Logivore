# 🛠️ Management-Leitfaden

Sprachen: Deutsch (diese Seite) | [繁體中文](../../MANAGEMENT_GUIDE.md) | [简体中文](../zh-cn/MANAGEMENT_GUIDE.md)

## Überblick

Verwalten Sie Cogs und Bot-Funktionen dynamisch, ohne den Bot neu zu starten.

## 🔧 Befehle

- `/manage reload` — einzelnes Modul neu laden (z. B. Alerting)
- `/manage reload_all` — alle Module neu laden
- `/manage sync` — Slash-Commands synchronisieren
- `/manage status` — Bot/Systemstatus, geladene Module, Konfig-Überblick
- `/manage logs` — letzte Logs anzeigen
- `/manage restart` — Bot neustarten (als systemd-Service)
- `/manage shutdown` — Bot sauber beenden
- `/manage eval` — Code ausführen (nur Owner, vorsichtig!)

## 🔒 Berechtigungen

Nur Bot-Eigentümer:in darf Management-Befehle ausführen.

## 🚀 Beispielabläufe

- Feature-Update: Code ändern → `/manage reload` → ggf. `/manage sync` → testen → `/manage status`
- Großer Umbau: Änderungen abschließen → `/manage reload_all` → `/manage sync` → `/manage logs`

## ⚠️ Hinweise

- Reload kann Modulzustände zurücksetzen
- Detaillierte Fehlermeldungen bei Problemen
- `/manage eval` hat hohe Rechte

## 🔄 Vorteile von Hot-Reload

Kein Downtime, schnelle Verifikation, Zustand der übrigen Module bleibt erhalten, Fehlerisolation.

