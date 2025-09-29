# 🤖 Logivore

Sprachen: [English](README.md) | [繁體中文](README.zh-tw.md) | [简体中文](README.zh-cn.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | Deutsch | [Русский](README.ru.md)

<div align="center">

**Erweiterte Systemüberwachung & Management Discord Bot**

*Umfassende Echtzeitüberwachung, intelligente Alarme und automatisierte Systemverwaltung*

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Discord.py](https://img.shields.io/badge/discord.py-2.0+-green.svg)](https://discordpy.readthedocs.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Made by](https://img.shields.io/badge/Made%20by-Serelix%20Studio-purple.svg)](https://serelix.xyz)

[🚀 Schnellstart](#-schnellstart) • [✨ Funktionen](#-funktionen) • [🌍 Sprachen](#-unterstützte-sprachen) • [📖 Dokumentation](#-dokumentation) • [💬 Support](#-support)

</div>

## 📋 Übersicht

Logivore ist ein leistungsstarker Discord Bot, der für umfassende Systemüberwachung und -verwaltung entwickelt wurde. Mit erweiterten Automatisierungsfunktionen bietet er Echtzeiteinblicke in Ihre Serverinfrastruktur und gewährleistet dabei Unternehmensqualität in Bezug auf Zuverlässigkeit und Sicherheit.

### 🎯 Kernfunktionen

- **🔍 Echtzeit-Systemüberwachung** - CPU-, Speicher-, Festplatten-, Netzwerkstatistiken
- **🚨 Intelligentes Alarmsystem** - Proaktive Benachrichtigungen bei Systemproblemen
- **🐳 Docker-Management** - Vollständige Container-Lebenszyklus-Verwaltung
- **🔄 Service-Wiederherstellung** - Automatische Service-Wiederherstellung nach Systemereignissen
- **⚡ SSL-Zertifikatverwaltung** - Automatisierte Zertifikatüberwachung und -erneuerung
- **🌐 Mehrsprachige Unterstützung** - 8 Sprachen mit lokalisierten Benutzeroberflächen

## ✨ Funktionen

### 🖥️ Systemüberwachung
```
Echtzeit-Dashboard mit Live-Updates
Netzwerk-Port-Überwachung
Festplatten-Gesundheitsprüfung (SMART)
Prozessverwaltung und -überwachung
```

### 🚨 Alarm-Management
```
CPU/Speicher/Festplatten-Nutzungsalarme
Prozess-Watchdog-Überwachung
Benutzerdefinierte Schwellenwert-Konfiguration
Multi-Kanal-Benachrichtigungsunterstützung
```

### 🐳 Docker-Integration
```
Container-Status-Überwachung
Start/Stopp/Neustart-Operationen
Ressourcenverbrauch-Verfolgung
Log-Management
```

### 🛡️ Systemverwaltung
```
Geplante System-Neustarts
Service-Wiederherstellungs-Automatisierung
SSL-Zertifikat-Überwachung
Nginx Proxy Manager Integration
```

## 🌍 Unterstützte Sprachen

<div align="center">

| Sprache | Code | Status |
|----------|------|--------|
| 🇺🇸 English | `en` | ✅ Vollständig |
| 🇹🇼 繁體中文 | `zh`/`zh-tw` | ✅ Vollständig |
| 🇨🇳 简体中文 | `zh-cn` | ✅ Vollständig |
| 🇰🇷 한국어 | `ko` | ✅ Vollständig |
| 🇯🇵 日本語 | `ja` | ✅ Vollständig |
| 🇩🇪 Deutsch | `de` | ✅ Vollständig |
| 🇷🇺 Русский | `ru` | ✅ Vollständig |

</div>

## 🚀 Schnellstart

### Voraussetzungen
- Python 3.8+
- Discord Bot Token
- Linux/Windows/macOS System

### Installation
```bash
# Repository klonen
git clone https://github.com/kaiyasi/Logivore.git
cd Logivore

# Abhängigkeiten installieren
pip install -r requirements.txt

# Umgebung konfigurieren
cp .env.example .env
# .env mit Ihrem Discord Bot Token und Einstellungen bearbeiten

# Bot ausführen
python main.py
```

### Docker-Bereitstellung
```bash
cd deploy/docker
docker compose up -d --build
```

## 🏗️ Architektur

### 🔧 Technologie-Stack
- **Backend-Framework**: Python 3.8+ mit discord.py 2.0+
- **Systemüberwachung**: psutil, subprocess Integration
- **Container-Management**: Docker API Integration
- **SSL-Management**: Let's Encrypt mit Nginx Proxy Manager
- **Internationalisierung**: JSON-basiertes Mehrsprachensystem
- **Konfiguration**: JSON mit Hot-Reload-Funktionen

### 📦 Kernmodule
```
├── 🔍 Systemüberwachung    - Echtzeit-Systemstatistiken
├── 🚨 Alarmsystem         - Proaktive Überwachungsalarme
├── 🐳 Docker-Management   - Container-Lebenszyklus-Kontrolle
├── 🔄 Service-Wiederherstellung - Automatische Service-Wiederherstellung
├── 🛡️ SSL-Management     - Zertifikatüberwachung und -erneuerung
├── ⚙️ Konfiguration      - Dynamische Einstellungsverwaltung
├── 🤖 Bot-Management      - Verwaltungskontrollen
└── 📚 Hilfesystem        - Interaktive Dokumentation
```

## 📖 Dokumentation

- **[Installationsanleitung](../installation.md)** - Schritt-für-Schritt-Einrichtungsanweisungen
- **[Konfigurationsreferenz](../configuration.md)** - Vollständige Einstellungsdokumentation
- **[Befehlsreferenz](../commands.md)** - Alle verfügbaren Bot-Befehle
- **[API-Dokumentation](../api.md)** - Integrations- und Erweiterungsanleitungen
- **[Fehlerbehebung](../troubleshooting.md)** - Häufige Probleme und Lösungen
- Weitere Anleitungen:
  - **[Embed-Formatierungsleitfaden](EMBED_FORMAT_GUIDE.md)**
  - **[Management-Leitfaden](MANAGEMENT_GUIDE.md)**
  - **[Auto-Wiederherstellung nach Reboot](SETUP-RECOVERY.md)**

## 🤝 Mitwirken

Beiträge sind willkommen! Bitte lesen Sie unsere [Beitragsrichtlinien](CONTRIBUTING.md) für Details.

### Entwicklungsumgebung einrichten
```bash
# Entwicklungsumgebung klonen und einrichten
git clone https://github.com/kaiyasi/Logivore.git
cd Logivore

# Entwicklungsabhängigkeiten installieren
pip install -r requirements-dev.txt

# Tests ausführen
python -m pytest tests/
```

## 📝 Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert - siehe die [LICENSE](LICENSE)-Datei für Details.

## 💬 Support

<div align="center">

### 🔗 Community & Support

[![GitHub Issues](https://img.shields.io/badge/GitHub-Issues-red.svg)](https://github.com/kaiyasi/Logivore/issues)
[![GitHub Discussions](https://img.shields.io/badge/GitHub-Discussions-blue.svg)](https://github.com/kaiyasi/Logivore/discussions)
[![Discord](https://img.shields.io/badge/Discord-Community-purple.svg)](https://discord.gg/serelix)
[![Email](https://img.shields.io/badge/Email-Support-green.svg)](mailto:serelixstudio@gmail.com)

</div>

### 📞 Kontaktinformationen

- **Offizielle Website**: [https://serelix.xyz](https://serelix.xyz)
- **GitHub Repository**: [https://github.com/kaiyasi/Logivore](https://github.com/kaiyasi/Logivore)
- **E-Mail**: serelixstudio@gmail.com
- **Instagram**: [@serelix.studio](https://instagram.com/serelix.studio)

---

<div align="center">

**Mit ❤️ erstellt von [Serelix Studio](https://serelix.xyz)**

*Serververwaltung durch intelligente Automatisierung stärken*

</div>
