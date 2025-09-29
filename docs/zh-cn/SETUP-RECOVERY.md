# 系统重启后自动服务恢复设置指南

语言：简体中文（本页） | [繁體中文](../../SETUP-RECOVERY.md)

## 🎯 功能概述

提供完整的重启后服务自动恢复方案：
- Docker 容器自动启动
- systemd 服务自动恢复
- 开机脚本自动执行
- 状态监控与通知

## 🔧 安装配置

### 1. 配置 sudo 权限
```bash
sudo cp systemd-examples/logivore-bot-sudoers /etc/sudoers.d/logivore
sudo chmod 440 /etc/sudoers.d/logivore
```

### 2. 安装开机恢复脚本
```bash
sudo mkdir -p /opt/logivore/scripts
sudo cp scripts/boot-recovery.sh /opt/logivore/scripts/
sudo chmod +x /opt/logivore/scripts/boot-recovery.sh

sudo cp systemd-examples/logivore-boot-recovery.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable logivore-boot-recovery.service
```

### 3. 配置 Docker 重启策略

方法一：为现有容器设置重启策略
```bash
# 为所有运行中容器设置
docker ps --format "{{.Names}}" | xargs -I {} docker update --restart=unless-stopped {}

# 为特定容器设置
docker update --restart=unless-stopped container_name
```

方法二：Docker Compose
```yaml
services:
  myapp:
    image: myapp:latest
    restart: unless-stopped
```

### 4. 配置 systemd 开机自启
```bash
sudo systemctl enable service_name
sudo systemctl is-enabled service_name
```

## 🚀 使用方法（Discord 指令）

保存当前状态
```
/recovery save_state
```

立即恢复
```
/recovery recover_now
```

配置自动恢复
```
/recovery config auto_recovery:True monitored_services:"nginx,mysql,redis"
```

查看状态
```
/recovery status
```

重启管理
```
/reboot schedule hours:6
/reboot now delay:5
/reboot status
/reboot cancel
```

## ⚙️ 进阶配置

自定义监控服务（编辑 `/opt/logivore/scripts/boot-recovery.sh`）
```bash
CUSTOM_SERVICES=("nginx" "mysql" "redis" "your-service")
DOCKER_COMPOSE_DIRS=("/opt/docker-apps" "/home/user/projects")
```

Docker 重启策略说明：
- `no`：不自动重启（默认）
- `always`：总是重启
- `unless-stopped`：除非手动停止，否则重启（推荐）
- `on-failure`：仅失败时重启

开机延迟：
```bash
sleep 60
# 或使用 systemd 依赖
After=network.target docker.service mysql.service
```

## 🔍 故障排除

查看日志：
```bash
sudo tail -f /var/log/logivore-boot-recovery.log
sudo journalctl -u logivore-boot-recovery.service -f
docker logs container_name
```

常见问题：
1) 容器未自动启动：检查 RestartPolicy、确认 docker 运行
2) 权限问题：校验 sudoers，检查脚本权限
3) 依赖问题：增加延迟、设置 systemd 依赖

## 📊 监控与通知

系统将：检测重启 → 恢复服务 → 通知频道 → 记录日志

## 🔄 工作流程

正常运行：定期保存状态 → 重启后脚本/策略生效 → Logivore 校验并补齐 → 通知结果

