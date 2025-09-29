# 재부팅 후 자동 복구 설정 가이드

언어: 한국어(본 문서) | [繁體中文](../../SETUP-RECOVERY.md) | [简体中文](../zh-cn/SETUP-RECOVERY.md)

## 🎯 개요

재부팅 이후 서비스 자동 복구: Docker 컨테이너, systemd 서비스, 부팅 스크립트, 모니터링/알림.

## 🔧 설치/설정

### 1) sudo 권한
```bash
sudo cp systemd-examples/logivore-bot-sudoers /etc/sudoers.d/logivore
sudo chmod 440 /etc/sudoers.d/logivore
```

### 2) 부팅 복구 스크립트
```bash
sudo mkdir -p /opt/logivore/scripts
sudo cp scripts/boot-recovery.sh /opt/logivore/scripts/
sudo chmod +x /opt/logivore/scripts/boot-recovery.sh

sudo cp systemd-examples/logivore-boot-recovery.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable logivore-boot-recovery.service
```

### 3) Docker 재시작 정책
```bash
docker update --restart=unless-stopped <container>
```
docker-compose:
```yaml
services:
  myapp:
    image: myapp:latest
    restart: unless-stopped
```

### 4) systemd 자동 시작
```bash
sudo systemctl enable service_name
sudo systemctl is-enabled service_name
```

## 🚀 사용법(Discord)

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

## ⚙️ 고급 설정

```bash
# /opt/logivore/scripts/boot-recovery.sh
CUSTOM_SERVICES=("nginx" "mysql" "redis" "your-service")
DOCKER_COMPOSE_DIRS=("/opt/docker-apps" "/home/user/projects")
```

정책: `no` / `always` / `unless-stopped`(권장) / `on-failure`

지연:
```bash
sleep 60
After=network.target docker.service mysql.service
```

## 🔍 문제 해결

```bash
sudo tail -f /var/log/logivore-boot-recovery.log
sudo journalctl -u logivore-boot-recovery.service -f
docker logs <container>
```

## 📊 모니터링/알림

재부팅 감지 → 복구 → Discord 알림 → 로그 기록.

