# Справочник команд (Logivore)

Языки: [Русский](commands.md) | [English](../commands.md) | [繁體中文](../zh-tw/commands.md) | [简体中文](../zh-cn/commands.md) | [日本語](../ja/commands.md) | [한국어](../ko/commands.md)

Полный список Slash‑команд с параметрами и примерами.

## Содержание
- Системный мониторинг
- Управление Docker
- Оповещения
- SSL‑сертификаты
- Конфигурация
- Управление ботом
- Справка
- Категории и права
- Советы и обработка ошибок

---

## Системный мониторинг

### /monitor
Панель мониторинга в реальном времени (CPU/RAM/диск/сеть), автообновление ~10с.
- Использование: `/monitor`

### /ports
Занятые порты хоста (Docker‑маппинг + системные слушатели), постраничный вывод, при больших объёмах — вложение.
- Использование: `/ports`

### /top
Топ процессов по CPU/RAM.
- Использование: `/top [count]` (по умолчанию 10, 1–20)

### /smart
SMART‑состояние дисков (Linux, требуется smartmontools).
- Использование: `/smart`

---

## Управление Docker

### /docker status (/docker ps)
Статус/образы/порты/ресурсы контейнеров.
- Использование: `/docker status`

### /docker start / stop / restart
- Использование: `/docker start <container>` / `stop` / `restart`

### /docker logs
Логи контейнера.
- Использование: `/docker logs <container> [lines]` (по умолчанию 50)

### /docker stats
Ресурсы контейнера.
- Использование: `/docker stats [container]`

---

## Оповещения (alerts)

### /alerts list
- Использование: `/alerts list`

### /alerts add
CPU/RAM/диск/процесс.
- Использование: `/alerts add <type> <threshold> [channel]`
- type: `cpu` `memory` `disk` `process`

### /alerts remove
- Использование: `/alerts remove <alert_id>`

### /alerts test
- Использование: `/alerts test [type]`

---

## SSL‑сертификаты (ssl)

### /ssl list / check / renew / auto-renew
- Использование: `list`, `check <domain>`, `renew <domain>`, `auto-renew <enable|disable> [days_before]`

---

## Конфигурация (config)

### /config show
- Использование: `/config show [section]` (system/alerts/docker/ssl)

### /config set
- Использование: `/config set <key> <value>` (пример: `update_interval 15`)

### /config reload
- Использование: `/config reload`

### /language (/config language)
- Использование: `/language [language_code]` (`en`/`zh-tw`/`zh-cn`/`ko`/`ja`/`de`/`ru`)

---

## Управление ботом (только Owner)
- `/restart` перезапуск
- `/shutdown` корректное завершение
- `/reload <cog>` перезагрузка модуля
- `/sync` синхронизация команд
- `/status` статус/количество серверов/ресурсы

---

## Справка

### /help
Категории команд.
- Использование: `/help [category]` (`monitoring`/`docker`/`alerts`/`ssl`/`config`/`admin`)

---

## Категории и права
- Общедоступные: `/monitor` `/ports` `/top` `/smart` `/docker status|logs|stats` `/ssl list|check` `/config show` `/language` `/status` `/help`
- Owner: `/docker start|stop|restart` `/alerts add|remove` `/ssl renew|auto-renew` `/config set|reload` `/restart|/shutdown|/reload|/sync`
- Права Discord: Send Messages / Embed Links / Use Slash Commands / при необходимости Manage Messages

---

## Советы и обработка ошибок
- Мониторинг: `/monitor`, оповещения `/alerts add`
- Docker: `/docker status` → `logs` → `stats`
- SSL: `/ssl auto-renew enable`, ежемесячно `/ssl list`
- Конфигурация: `/config show`/`reload`, язык через `/language`

Ошибки: понятные сообщения по правам/параметрам/системе/сети и защитные откаты
