# Руководство по установке (Logivore)

Языки: [Русский](installation.md) | [English](../installation.md) | [繁體中文](../zh-tw/installation.md) | [简体中文](../zh-cn/installation.md) | [日本語](../ja/installation.md) | [한국어](../ko/installation.md)

Пошаговая установка Logivore: локально, в Docker и как служба systemd.

## Содержание
- Предварительные требования
- Системные требования
- Создание Discord‑бота
- Локальная установка (без контейнера)
- Развертывание в Docker (опционально)
- Переменные окружения (.env)
- Первый запуск
- Сервис systemd (Linux)
- Устранение неполадок

## Предварительные требования
- Python 3.8+, Git, pip
- По желанию: Docker/Compose, systemd (Linux), smartmontools (SMART)

## Системные требования
- Минимум: 512MB RAM, 1GB диск, 1 ядро, стабильный интернет
- Рекомендуется: 1GB+ RAM, 2GB+ диск, 2+ ядра, Ubuntu 20.04+/Windows 10+/macOS 10.15+

## Создание Discord‑бота
1) [Developer Portal](https://discord.com/developers/applications) → New Application (например, Logivore)
2) Bot → Add Bot
3) Включить Intents: Server Members, Message Content
4) Сгенерировать токен и сохранить (для `.env`)
5) OAuth2 → URL Generator: `bot` + `applications.commands`, выбрать права (Send Messages/Embed Links/Use Slash Commands/Read Message History/View Channels), пригласить на сервер

## Локальная установка
```bash
git clone https://github.com/kaiyasi/Logivore.git
cd Logivore
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python main.py
```

## Развертывание в Docker (опционально)
В Docker проще, но видимость хоста (порты/метрики) и управление хостом могут быть ограничены. Для максимальных возможностей используйте systemd.
```bash
cd deploy/docker
# Подготовьте .env в корне: cp .env.example .env
docker compose up -d --build
```
Compose использует `network_mode: host`, `pid: host` и монтирует `/var/run/docker.sock:ro` для управления контейнерами.

## Переменные окружения (.env)
```bash
DISCORD_TOKEN=ваш_токен
OWNER_ID=ваш_Discord_ID
LOG_LEVEL=INFO
LOG_FILE=logs/logivore.log
```
Больше опций: `docs/configuration.md`.

## Первый запуск
В консоли ожидается „✅ Bot is ready!“. Проверьте `/help`, `/config show`, `/monitor` в Discord.

## Сервис systemd (Linux)
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
Активировать:
```bash
sudo systemctl daemon-reload
sudo systemctl enable logivore
sudo systemctl start logivore
sudo systemctl status logivore
```
Автовосстановление и sudoers: `systemd-examples/`, `SETUP-RECOVERY.md`.

## Устранение неполадок
- Зависимости: `pip install -r requirements.txt`
- Токен: проверьте `DISCORD_TOKEN`
- Нет Slash‑команд: подождать синхронизацию, права `applications.commands`
- Контейнер сразу завершается: `docker compose logs -f logivore`
Отладка: `LOG_LEVEL=DEBUG` или `python main.py 2>&1 | tee logs/startup.log`
