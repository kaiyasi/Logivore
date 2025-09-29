# 安装指南（Logivore）

语言：[简体中文](installation.md) | [English](../installation.md) | [繁體中文](../zh-tw/installation.md)

本指南将带你从零开始完成 Logivore 的安装与部署（含 Docker 与 systemd 推荐实践），并提供常见问题排查。

## 目录

- 先决条件
- 系统需求
- 创建 Discord Bot
- 本地安装（非容器）
- Docker 安装（可选）
- 环境变量（.env）
- 首次启动
- 作为系统服务（Linux, systemd）
- 故障排除

## 先决条件

开始前请确认：

- Python 3.8 以上
- Git
- pip（通常随 Python 自带）

可选（提升功能）：
- Docker、Docker Compose
- systemd（Linux）
- smartmontools（Linux，用于磁盘 SMART 健康检查）

## 系统需求

最小需求：
- 内存：可用 512MB
- 磁盘：可用 1GB
- CPU：单核（建议双核）
- 网络：稳定网络连接

推荐需求：
- 内存：1GB 以上
- 磁盘：2GB 以上
- CPU：双核或更高
- 系统：Linux（Ubuntu 20.04+）、Windows 10+、macOS 10.15+

## 创建 Discord Bot

1) 进入 [Discord Developer Portal](https://discord.com/developers/applications)
2) 新建应用（New Application），命名「Logivore」或你喜欢的名称
3) Bot 分页添加 Bot（Add Bot）
4) 打开 Intents：Server Members、Message Content
5) 重新生成 Token 并妥善保存（稍后填入 `.env`）
6) 在 OAuth2 → URL Generator 勾选 `bot` 与 `applications.commands`，选择必要权限（Send Messages、Embed Links、Use Slash Commands、Read Message History、View Channels），邀请到你的服务器

## 本地安装（非容器）

```bash
# 获取源码
git clone https://github.com/kaiyasi/Logivore.git
cd Logivore

# 建议：创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 生成环境文件
cp .env.example .env
# 编辑 .env，填写 DISCORD_TOKEN、OWNER_ID、LOG_LEVEL 等

# 启动
python main.py
```

## Docker 安装（可选）

Docker 便于部署，但可能影响主机层级可视性（如 /ports、完整系统指标）与主机控制能力；若需最完整能力，推荐使用 systemd 方案。

```bash
cd deploy/docker
# 建议先在项目根目录复制 .env 并填写 Token：cp .env.example .env
docker compose up -d --build
```

默认 compose 使用 `network_mode: host` 与 `pid: host` 提升可视性，并挂载 `/var/run/docker.sock:ro` 使 Bot 能查询与管理容器。

## 环境变量（.env）

将 `.env.example` 复制为 `.env`，常用变量：

```bash
DISCORD_TOKEN=你的BotToken
OWNER_ID=你的Discord用户ID
LOG_LEVEL=INFO
LOG_FILE=logs/logivore.log
```

更多选项参见 `docs/configuration.md`。

## 首次启动

启动后控制台应看到：

```
✅ Bot is ready!
✅ Logged in as: <你的Bot>#1234
✅ Connected to X guilds
```

在 Discord 测试：

```
/help
/config show
/monitor
```

## 作为系统服务（Linux, systemd）

为了获得最佳可视性与可靠性，推荐使用 systemd 常驻 Logivore，并结合开机恢复示例：

1) 创建服务文件：

```bash
sudo nano /etc/systemd/system/logivore.service
```

2) 内容示例：

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

3) 启用服务：

```bash
sudo systemctl daemon-reload
sudo systemctl enable logivore
sudo systemctl start logivore
sudo systemctl status logivore
```

开机恢复与 sudoers 示例参见：
- `systemd-examples/`（`logivore-boot-recovery.service`、`logivore-bot-sudoers` 等）
- `SETUP-RECOVERY.md`

## 故障排除

常见问题：

- 找不到 discord.py：`pip install -r requirements.txt`
- Token 无效：确认 `.env` 中 `DISCORD_TOKEN` 是否正确
- Bot 无响应：检查是否在线、权限是否充足、重新邀请权限
- 权限问题（Linux）：

```bash
chmod +x main.py
chmod 644 .env
sudo chown -R $USER:$USER .
```

- Docker 容器立即退出：
  1) 查看日志 `docker compose logs -f logivore`
  2) 检查环境变量是否填写正确

启用调试：将 `.env` 设置 `LOG_LEVEL=DEBUG`，或使用 `python main.py 2>&1 | tee logs/startup.log` 启动。
