# 疑难排除（Logivore）

语言：[简体中文](troubleshooting.md) | [English](../troubleshooting.md) | [繁體中文](../zh-tw/troubleshooting.md)

本指南汇总常见问题、诊断流程与修复步骤，帮助你在原生 systemd 或 Docker 环境下快速定位并解决问题。

## 目录

- 快速检查清单
- 获取诊断信息（日志/状态）
- 常见启动问题
- 指令与权限问题
- Docker 相关问题
- systemd 服务问题
- SSL / 证书问题
- 警报（Alerts）相关
- 性能与资源使用
- 错误码与常见信息
- 恢复与回滚
- 常见问答（FAQ）

---

## 快速检查清单

1) `.env` 是否正确：`DISCORD_TOKEN`、`OWNER_ID` 无多余空格/引号且有效。
2) 版本与依赖：`python --version`（3.8+）与 `pip install -r requirements.txt` 成功。
3) 网络与权限：能连 Discord API，Bot 已进服务器并具备最小权限（Send Messages / Embed Links / Use Slash Commands）。
4) 文件与路径：`logs/`、`config/` 可读写；Docker 下对应卷已挂载。
5) 语言与配置：`config.json` 语法正确，`DEFAULT_LANGUAGE` 存在于 `languages/`。

---

## 获取诊断信息（日志/状态）

### 应用日志
```bash
tail -f logs/logivore.log
```

### 保留启动日志
```bash
python main.py 2>&1 | tee logs/startup.log
```

### Docker 日志
```bash
cd deploy/docker
docker compose logs -f logivore
```

### 斜杠指令同步
- 首次同步可能需要数十秒；若指令未出现，可重启或使用管理指令进行同步。

---

## 常见启动问题

### Token 无效或未设置
- 现象：LoginFailure 或 “DISCORD_TOKEN is not set”。
- 检查：`.env` 的 `DISCORD_TOKEN` 是否正确、无多余空格/引号。
- 修复：在 Developer Portal 重置 Token，更新 `.env` 后重启。

### 依赖缺失
- 现象：ImportError / ModuleNotFoundError。
- 修复：`pip install -r requirements.txt`；确保在 venv 内执行。

### Python/系统版本问题
- 现象：语法错误、类型标注错误、系统 API 缺少。
- 修复：升级至 Python 3.8+；容器内使用 deploy/docker 的镜像构建。

### 斜杠指令没有出现
- 现象：/help /monitor 等不可见。
- 检查：等待同步、重启、确认 Bot 已在服务器且勾选 `applications.commands` 权限。

---

## 指令与权限问题

### 无法发消息/嵌入
- 现象：无输出或嵌入被过滤。
- 修复：检查频道/服务器权限：Send Messages、Embed Links、Read Message History。

### Owner 限制的指令
- 现象：/restart /shutdown /config set 等提示无权限。
- 检查：`.env` 的 `OWNER_ID` 是否为你的 Discord 用户 ID。

### 长度限制导致 400 Bad Request
- 现象：Invalid Form Body，embeds.*.value 超过 1024。
- 修复：已内置分页与附件回退；若仍触发，请反馈使用场景与列表规模。

---

## Docker 相关问题

### 容器立即退出
- 查看日志：`docker compose logs -f logivore`
- 检查：环境变量（DISCORD_TOKEN / OWNER_ID）、卷挂载（config/logs）、Docker Socket 是否以只读挂载（若需容器管理）。

### 监控数据不足（主机可视性不够）
- 原因：未启用 `network_mode: host` / `pid: host`。
- 修复：使用 deploy/docker/docker-compose.yml 的默认配置，或按需开启 host/pid 模式。

### `/ports` 列表与 Docker 映射不一致
- 现象：同端口出现 IPv4/IPv6 重复。
- 修复：已合并显示为单列（IP 标记 v4/v6/*）。若仍异常，请提供 docker ps 的 Ports 与系统 ss/netstat 参考。

---

## systemd 服务问题（Linux）

### 服务无法启动
```bash
sudo systemctl status logivore
sudo journalctl -u logivore -f
```
- 检查服务文件 `ExecStart`、`WorkingDirectory`、`User` 是否正确；venv 路径是否存在。

### 开机自动恢复
- 参考 `systemd-examples/`（`logivore-boot-recovery.service`）与 `SETUP-RECOVERY.md`，确认 `/opt/logivore/scripts/boot-recovery.sh` 可执行。

---

## SSL / 证书问题

### 列表或续期失败
- 检查：NPM 容器名（`NPM_CONTAINER`）、证书路径（`SSL_CERT_PATH`）、OpenSSL 是否可用。
- 权限：Docker exec 需容器存在且允许跑 openssl。
- 域名：DNS A/AAAA 正确；未触发 Let’s Encrypt 频率限制。

---

## 警报（Alerts）相关

### 未触发或过于频繁
- 检查：`alerts` 阈值（0–100）、`alert_interval`、`alert_channel`。
- 建议：CPU 80–90%、内存 80–90%、磁盘 85–95%。

---

## 性能与资源使用

### 资源占用高
- 降低频率：`UPDATE_INTERVAL`、`ALERT_INTERVAL`
- 关闭不必要功能：禁用 Docker 监控或减少监控面板
- 系统侧检查：top/htop 观察进程

---

## 错误码与常见信息

- 50035 Invalid Form Body：字段长度超限（已加入保护）。
- LoginFailure：Token 无效。
- Missing Permissions：频道/服务器权限不足。
- JSONDecodeError：config.json 语法错误。

---

## 恢复与回滚

1) 备份设置与日志：`cp -r config logs backups/$(date +%F_%T)`
2) 如需回滚，将备份覆盖回 `config/` 与 `logs/`
3) 重启服务或容器

---

## 常见问答（FAQ）

Q: 指令没有出现？
- A: 首次同步需要时间；确认 Bot 在服务器且权限完整，重启后再试。

Q: `/ports` 过长报错？
- A: 已支持分页与附件回退；若仍错误，请提供截图与输出内容。

Q: Docker 部署是否安全？
- A: 默认 read_only / no-new-privileges / tmpfs 与只读 Docker Socket；请依安全策略调整。

---

需要更多帮助？
- 应用日志：`tail -f logs/logivore.log`
- Docker：`docker compose logs -f logivore`
- Issues：<https://github.com/kaiyasi/Logivore/issues>
