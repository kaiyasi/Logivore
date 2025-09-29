# Руководство по разработке

Языки: Русский | [English](../development.md) | [繁體中文](../zh-tw/development.md) | [简体中文](../zh-cn/development.md)

Практическое руководство для разработчиков, желающих внести вклад в Logivore:
настройка среды, стиль кода, рабочие процессы и инструменты.

## Содержание

- [Настройка среды разработки](#настройка-среды-разработки)
- [Структура проекта](#структура-проекта)
- [Процесс разработки](#процесс-разработки)
- [Стиль кода и стандарты](#стиль-кода-и-стандарты)
- [Тестовый фреймворк](#тестовый-фреймворк)
- [Архитектурные паттерны](#архитектурные-паттерны)
- [Руководство по вкладу](#руководство-по-вкладу)
- [Процесс релиза](#процесс-релиза)
- [Инструменты разработки](#инструменты-разработки)
- [Отладка и профилирование](#отладка-и-профилирование)

## Настройка среды разработки

### Требования

- Python 3.8+, Git, при необходимости Docker
- Виртуальное окружение (venv/virtualenv/conda)

### Первичная настройка

```bash
# 1) Клонировать репозиторий
git clone https://github.com/kaiyasi/Logivore.git
cd Logivore

# 2) Создать и активировать виртуальное окружение
python -m venv venv
source venv/bin/activate      # Linux/Mac
# или
venv\Scripts\activate        # Windows

# 3) Установить зависимости
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 4) Установить pre-commit
pre-commit install

# 5) Подготовить конфигурацию
cp .env.example .env
cp config/bot_config.example.json config/bot_config.json

# 6) Создать каталоги
mkdir -p logs data/backups
```

## Структура проекта

- Точка входа: `main.py`
- Функции: `cogs/`
- Утилиты: `utils/`
- Языки: `languages/`
- Тесты: `tests/`
- Документация: `docs/`

Расширенная схема и зависимости приведены в английском руководстве.

## Процесс разработки

### Git Flow

```bash
main        # Готово к продакшену
develop     # Интеграция фич
feature/*   # Новые возможности
hotfix/*    # Критические исправления
release/*   # Подготовка релиза
```

### Пример рабочего цикла

```bash
git checkout develop && git pull
git checkout -b feature/new-monitoring
# Реализация изменений
git add . && git commit -m "feat(monitoring): add GPU temperature"
git push -u origin feature/new-monitoring
# PR → Review → merge в develop
```

### Конвенция коммитов

Используйте Conventional Commits (feat/fix/docs/style/refactor/perf/test/chore/ci).

## Стиль кода и стандарты

- Обязательные аннотации типов (type hints)
- Линт/формат: Black, isort, flake8, mypy
- Docstring по стилю Google

```python
from typing import Any, Dict, List, Optional, Union

async def process_data(
    data: List[Dict[str, Any]],
    config: Dict[str, str],
    timeout: Optional[float] = None
) -> Union[str, None]:
    pass
```

## Тестовый фреймворк

- Pytest, асинхронные тесты, моки/фикстуры
- Сначала точечные модульные тесты, затем широкий прогон

```bash
pytest -q
pytest tests/test_utils -q
```

## Архитектурные паттерны

- Модульность по Cog
- Async‑first
- Конфигурационный подход (JSON)

## Руководство по вкладу

- Небольшие, фокусные PR
- Тесты для нового/изменённого кода
- Не смешивайте несвязанные изменения в одном PR

## Процесс релиза

- Ветви релиза от `develop`
- CI/CD: тесты, линтинг, сборка/деплой
- Версионирование и CHANGELOG

## Инструменты разработки

### Пример настроек VS Code

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

## Отладка и профилирование

- Структурированные логи и контекст в исключениях
- Трейсинг фоновых задач
- Метрики/тайминги и анализ узких мест

