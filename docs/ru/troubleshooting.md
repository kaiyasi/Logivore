# Устранение неполадок (Logivore)

Языки: [Русский](troubleshooting.md) | [English](../troubleshooting.md) | [繁體中文](../zh-tw/troubleshooting.md) | [简体中文](../zh-cn/troubleshooting.md) | [日本語](../ja/troubleshooting.md) | [한국어](../ko/troubleshooting.md)

Частые проблемы, диагностика и решения для systemd и Docker.

## Содержание
- Быстрый чек‑лист
- Логи/статус
- Проблемы запуска
- Команды/права
- Docker
- Сервис systemd
- SSL/сертификаты
- Оповещения
- Производительность
- Коды ошибок
- Восстановление
- FAQ

---

## Быстрый чек‑лист
1) `.env`: `DISCORD_TOKEN` / `OWNER_ID`
2) `pip install -r requirements.txt`
3) Права: Send Messages / Embed Links / Use Slash Commands
4) Пути: `logs/` `config/`, монтирование томов в Docker
5) Язык: `DEFAULT_LANGUAGE` имеется в `languages/`

## Логи/статус
```bash
tail -f logs/logivore.log
python main.py 2>&1 | tee logs/startup.log
cd deploy/docker && docker compose logs -f logivore
```
Синхронизация Slash‑команд может занять десятки секунд.

## Проблемы запуска
- Неверный токен: пересоздать в Developer Portal, обновить `.env`
- Зависимости: `pip install -r requirements.txt`
- Python 3.8+
- Нет команд: права `applications.commands`, бот на сервере?

## Команды/права
- Нет отправки/встраиваний: права канала
- Команды Owner: `OWNER_ID` — ваш Discord ID
- 400 Bad Request (длина): реализована пагинация/вложение

## Docker
- Контейнер завершается: `docker compose logs -f logivore`
- Низкая видимость: `network_mode: host` / `pid: host`
- `/ports` дублирует v4/v6: объединено, IP‑колонка v4/v6/*

## Сервис systemd
```bash
sudo systemctl status logivore
sudo journalctl -u logivore -f
```
Проверьте `ExecStart`/`WorkingDirectory`/`User`; см. `systemd-examples/`, `SETUP-RECOVERY.md`.

## SSL/сертификаты
Контейнер NPM, `SSL_CERT_PATH`, OpenSSL; DNS A/AAAA; лимиты Let’s Encrypt.

## Оповещения
Порог 0–100, `alert_interval`, `alert_channel`; рекомендации: CPU/RAM 80–90%, диск 85–95%.

## Производительность
Увеличить интервалы, отключить лишние функции, проверять нагрузку top/htop.

## Коды ошибок
- 50035 Invalid Form Body — превышение длины поля
- LoginFailure — неверный токен
- Missing Permissions — недостаточно прав
- JSONDecodeError — неверный формат config.json

## Восстановление
Резерв: `cp -r config logs backups/$(date +%F_%T)` → при необходимости восстановить → перезапустить

## FAQ
- Команды не появились? Подождите синхронизацию/перезапустите/проверьте права
- `/ports` слишком длинный? Пагинация/вложение включены; пришлите пример
- Безопасность в Docker? read_only/no‑new‑privileges/tmpfs/docker.sock:ro; адаптируйте под политику

