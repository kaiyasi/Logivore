# 再起動後の自動復旧セットアップガイド

言語: 日本語（本ページ） | [繁體中文](../../SETUP-RECOVERY.md) | [简体中文](../zh-cn/SETUP-RECOVERY.md)

## 🎯 概要

再起動後にサービスを自動復旧：Docker コンテナ、systemd サービス、起動スクリプト、監視と通知。

## 🔧 セットアップ

### 1) sudo 権限
```bash
sudo cp systemd-examples/logivore-bot-sudoers /etc/sudoers.d/logivore
sudo chmod 440 /etc/sudoers.d/logivore
```

### 2) 起動復旧スクリプト
```bash
sudo mkdir -p /opt/logivore/scripts
sudo cp scripts/boot-recovery.sh /opt/logivore/scripts/
sudo chmod +x /opt/logivore/scripts/boot-recovery.sh

sudo cp systemd-examples/logivore-boot-recovery.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable logivore-boot-recovery.service
```

### 3) Docker 再起動ポリシー
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

### 4) systemd 自動起動
```bash
sudo systemctl enable service_name
sudo systemctl is-enabled service_name
```

## 🚀 使い方（Discord）

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

## ⚙️ 応用設定

```bash
# /opt/logivore/scripts/boot-recovery.sh
CUSTOM_SERVICES=("nginx" "mysql" "redis" "your-service")
DOCKER_COMPOSE_DIRS=("/opt/docker-apps" "/home/user/projects")
```

再起動ポリシー: `no` / `always` / `unless-stopped`（推奨）/ `on-failure`

起動遅延：
```bash
sleep 60
# systemd 依存関係
After=network.target docker.service mysql.service
```

## 🔍 トラブルシューティング

```bash
sudo tail -f /var/log/logivore-boot-recovery.log
sudo journalctl -u logivore-boot-recovery.service -f
docker logs <container>
```

## 📊 監視と通知

再起動検知 → 復旧 → Discord 通知 → ログ記録。

