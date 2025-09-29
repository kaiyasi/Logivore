# 系統重啟後自動服務恢復設定指南
 
語言：繁體中文（本頁） | [简体中文](zh-cn/SETUP-RECOVERY.md)

## 🎯 功能概述

Logivore 提供完整的系統重啟後服務自動恢復功能，包括：

- **Docker 容器自動啟動**
- **Systemd 服務自動恢復**
- **開機腳本自動執行**
- **狀態監控和通知**

## 🔧 安裝配置

### 1. 設定 sudo 權限

```bash
sudo cp systemd-examples/logivore-bot-sudoers /etc/sudoers.d/logivore
sudo chmod 440 /etc/sudoers.d/logivore
```

### 2. 安裝開機恢復腳本

```bash
# 複製腳本到系統目錄
sudo mkdir -p /opt/logivore/scripts
sudo cp scripts/boot-recovery.sh /opt/logivore/scripts/
sudo chmod +x /opt/logivore/scripts/boot-recovery.sh

# 安裝 systemd 服務
sudo cp systemd-examples/logivore-boot-recovery.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable logivore-boot-recovery.service
```

### 3. 配置 Docker 容器重啟策略

#### 方法一：現有容器設定重啟策略
```bash
# 為所有運行中的容器設定重啟策略
docker ps --format "{{.Names}}" | xargs -I {} docker update --restart=unless-stopped {}

# 為特定容器設定
docker update --restart=unless-stopped container_name
```

#### 方法二：使用 Docker Compose
```yaml
# 在 docker-compose.yml 中加入 restart 策略
services:
  myapp:
    image: myapp:latest
    restart: unless-stopped  # 或 always
```

### 4. 配置 Systemd 服務自動啟動

```bash
# 啟用服務開機自動啟動
sudo systemctl enable service_name

# 檢查服務狀態
sudo systemctl is-enabled service_name
```

## 🚀 使用方法

### Discord 命令

#### 1. 保存當前狀態
```
/recovery save_state
```
- 保存目前運行的 Docker 容器和系統服務狀態

#### 2. 立即恢復服務
```
/recovery recover_now
```
- 手動觸發服務恢復

#### 3. 配置自動恢復
```
/recovery config auto_recovery:True monitored_services:"nginx,mysql,redis"
```

#### 4. 查看恢復狀態
```
/recovery status
```

#### 5. 系統重啟管理
```
/reboot schedule hours:6          # 6小時後重啟
/reboot now delay:5               # 5分鐘後重啟
/reboot status                    # 查看重啟狀態
/reboot cancel                    # 取消重啟
```

## ⚙️ 進階配置

### 1. 自定義監控服務

編輯 `/opt/logivore/scripts/boot-recovery.sh`：

```bash
# 添加要自動啟動的服務
CUSTOM_SERVICES=("nginx" "mysql" "redis" "your-service")

# 添加 docker-compose 目錄
DOCKER_COMPOSE_DIRS=("/opt/docker-apps" "/home/user/projects")
```

### 2. Docker 重啟策略說明

- **`no`**: 不自動重啟 (預設)
- **`always`**: 總是重啟
- **`unless-stopped`**: 除非手動停止，否則總是重啟 (推薦)
- **`on-failure`**: 只在失敗時重啟

### 3. 開機延遲設定

如果某些服務需要等待其他服務啟動：

```bash
# 在 boot-recovery.sh 中增加延遲
sleep 60  # 等待 60 秒

# 或者使用 systemd 依賴
After=network.target docker.service mysql.service
```

## 🔍 故障排除

### 檢查日誌

```bash
# 查看開機恢復腳本日誌
sudo tail -f /var/log/logivore-boot-recovery.log

# 查看 systemd 服務日誌
sudo journalctl -u logivore-boot-recovery.service -f

# 查看 Docker 容器日誌
docker logs container_name
```

### 常見問題

1. **容器無法自動啟動**
   - 檢查重啟策略：`docker inspect container_name | grep RestartPolicy`
   - 確認 Docker 服務已啟動：`systemctl status docker`

2. **權限問題**
   - 檢查 sudoers 配置：`sudo visudo -c`
   - 確認腳本執行權限：`ls -la /opt/logivore/scripts/`

3. **服務依賴問題**
   - 調整開機腳本中的延遲時間
   - 使用 systemd 依賴關係

## 📊 監控和通知

系統會自動：

1. **檢測重啟**: 監控系統開機時間
2. **自動恢復**: 根據保存的狀態恢復服務
3. **發送通知**: 在 Discord 頻道報告恢復結果
4. **記錄日誌**: 詳細記錄所有操作

## 🔄 工作流程

1. **正常運行時**: 定期保存服務狀態
2. **系統重啟前**: 可選擇手動保存狀態
3. **系統重啟後**:
   - 開機腳本自動執行
   - Docker 容器根據重啟策略啟動
   - Systemd 服務自動啟動
   - Logivore 檢測並恢復剩餘服務
   - 發送恢復結果通知

這樣就能確保系統重啟後所有服務都能自動恢復運行！
