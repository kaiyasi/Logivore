# Entwicklungsleitfaden

Sprachen: Deutsch | [English](../development.md) | [繁體中文](../zh-tw/development.md) | [简体中文](../zh-cn/development.md)

Dieser Leitfaden richtet sich an Beitragende, die die Codebasis verstehen,
Entwicklungsstandards einhalten und effizient am Projekt mitarbeiten möchten.

## Inhaltsverzeichnis

- [Einrichtung der Entwicklungsumgebung](#einrichtung-der-entwicklungsumgebung)
- [Projektstruktur](#projektstruktur)
- [Entwicklungs-Workflow](#entwicklungs-workflow)
- [Codestil und Standards](#codestil-und-standards)
- [Testframework](#testframework)
- [Architekturmuster](#architekturmuster)
- [Beitragsrichtlinien](#beitragsrichtlinien)
- [Release-Prozess](#release-prozess)
- [Entwicklungswerkzeuge](#entwicklungswerkzeuge)
- [Debugging und Profiling](#debugging-und-profiling)

## Einrichtung der Entwicklungsumgebung

### Voraussetzungen

- Python 3.8 oder höher
- Git
- Optional: Docker (für Integrations-/E2E‑Tests)

### Initiales Setup

```bash
# 1) Repository klonen
git clone https://github.com/kaiyasi/Logivore.git
cd Logivore

# 2) Virtuelle Umgebung erstellen/aktivieren
python -m venv venv
source venv/bin/activate      # Linux/Mac
# oder
venv\Scripts\activate        # Windows

# 3) Abhängigkeiten installieren
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 4) Pre-commit einrichten
pre-commit install

# 5) Konfiguration vorbereiten
cp .env.example .env
cp config/bot_config.example.json config/bot_config.json

# 6) Verzeichnisse erstellen
mkdir -p logs data/backups
```

## Projektstruktur

- Einstiegspunkt: `main.py`
- Module: `cogs/`
- Hilfsfunktionen: `utils/`
- Sprachdateien: `languages/`
- Tests: `tests/`
- Dokumentation: `docs/`

Siehe zusätzlich die erweiterte Übersicht im englischen Leitfaden (Diagramme, Beziehungen).

## Entwicklungs-Workflow

### Git Flow

```bash
main        # Produktionsreif
develop     # Integration neuer Features
feature/*   # Feature-Zweige
hotfix/*    # Kritische Fehlerbehebungen
release/*   # Release-Vorbereitung
```

### Beispielablauf

```bash
git checkout develop && git pull
git checkout -b feature/neues-monitoring
# Änderungen implementieren
git add . && git commit -m "feat(monitoring): füge GPU-Temperatur hinzu"
git push -u origin feature/neues-monitoring
# PR gegen develop erstellen → Review → Merge
```

### Commit-Konvention

Conventional Commits (feat/fix/docs/style/refactor/perf/test/chore/ci) verwenden.

## Codestil und Standards

- Typisierungen (type hints) verpflichtend
- Lint/Format: Black, isort, flake8, mypy
- Docstrings im Google‑Style

Beispiel‑Signaturen:

```python
from typing import Any, Dict, List, Optional, Union

async def process_data(
    data: List[Dict[str, Any]],
    config: Dict[str, str],
    timeout: Optional[float] = None
) -> Union[str, None]:
    pass
```

## Testframework

- Pytest‑Struktur mit async‑Tests und Mocks/Fixtures
- Start spezifischer Modultests, danach breitere Testläufe

```bash
pytest -q
pytest tests/test_utils -q
```

## Architekturmuster

- Cog‑basierte Modularität
- Async‑First
- Konfigurationsgetrieben (JSON)

## Beitragsrichtlinien

- Kleine, fokussierte PRs
- Tests für neue/angepasste Logik
- Keine unzusammenhängenden Änderungen in einem PR

## Release-Prozess

- Release‑Branches aus `develop`
- CI/CD‑Pipelines: Tests, Linting, Build/Publish
- Versionierung und CHANGELOG pflegen

## Entwicklungswerkzeuge

### VS Code (Beispiel)

```json
{
  "python.defaultInterpreterPath": "./venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "python.linting.mypyEnabled": true,
  "python.formatting.provider": "black",
  "python.formatting.blackArgs": ["--line-length", "100"],
  "python.sortImports.args": ["--profile", "black"],
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {"source.organizeImports": true}
}
```

## Debugging und Profiling

- Strukturierte Logs und Kontext in Ausnahmen
- Tracing für Hintergrund‑Tasks
- Metriken, Timing‑Messungen und Auswertung von Bottlenecks
