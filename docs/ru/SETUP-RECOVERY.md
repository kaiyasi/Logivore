# Автовосстановление после перезагрузки — руководство

Языки: Русский (эта страница) | [繁體中文](../../SETUP-RECOVERY.md) | [简体中文](../zh-cn/SETUP-RECOVERY.md)

## 🎯 Обзор

Автовосстановление служб после перезагрузки: контейнеры Docker, сервисы systemd, скрипты запуска, мониторинг и уведомления.

## 🔧 Установка и настройка

### 1) Права sudo
```bash
sudo cp systemd-examples/logivore-bot-sudoers /etc/sudoers.d/logivore
sudo chmod 440 /etc/sudoers.d/logivore
```

### 2) Скрипт восстановления при загрузке
```bash
sudo mkdir -p /opt/logivore/scripts
sudo cp scripts/boot-recovery.sh /opt/logivore/scripts/
sudo chmod +x /opt/logivore/scripts/boot-recovery.sh

sudo cp systemd-examples/logivore-boot-recovery.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable logivore-boot-recovery.service
```

### 3) Политика перезапуска Docker
```bash
docker update --restart=unless-stopped <container>
```
Docker Compose:
```yaml
services:
  myapp:
    image: myapp:latest
    restart: unless-stopped
```

### 4) Автозапуск systemd
```bash
sudo systemctl enable service_name
sudo systemctl is-enabled service_name
```

## 🚀 Использование (Discord)

```
/recovery save_state
/recovery recover_now
/recovery config auto_recovery:True monitored_services:"nginx,mysql,redis"
/recovery status

/reboot schedule hours:6
/reboot now delay:5
/reboot status
/reboot cancel
```

## ⚙️ Расширенные настройки

```bash
# /opt/logivore/scripts/boot-recovery.sh
CUSTOM_SERVICES=("nginx" "mysql" "redis" "your-service")
DOCKER_COMPOSE_DIRS=("/opt/docker-apps" "/home/user/projects")
```

Политики: `no` / `always` / `unless-stopped` (рекомендуется) / `on-failure`

Задержка запуска:
```bash
sleep 60
After=network.target docker.service mysql.service
```

## 🔍 Устранение неполадок

```bash
sudo tail -f /var/log/logivore-boot-recovery.log
sudo journalctl -u logivore-boot-recovery.service -f
docker logs <container>
```

## 📊 Мониторинг и уведомления

Обнаружение перезагрузки → восстановление → уведомление в Discord → журналирование.

