# 指令参考（Logivore）

语言：[简体中文](commands.md) | [English](../commands.md) | [繁體中文](../zh-tw/commands.md)

本指南完整列出 Logivore 的所有斜杠指令、用途、参数与示例。

## 目录
- 系统监控指令
- Docker 管理指令
- 警报管理指令
- SSL 证书指令
- 配置指令
- 机器人管理指令
- 帮助指令
- 指令分类与权限
- 使用建议与错误处理

---

## 系统监控指令

### /monitor
显示实时系统监控面板（CPU、内存、磁盘、网络），每 10 秒自动更新。
- 用法：`/monitor`
- 参数：无

### /ports
显示主机端口占用概况（Docker 映射 + 系统监听），支持分页与附件回退。
- 用法：`/ports`
- 参数：无（结果分页展示，完整清单过长时会附加文件）

### /top
列出资源占用高的进程（CPU/内存）。
- 用法：`/top [count]`
- 参数：`count`（可选，默认 10，1–20）

### /smart
显示磁盘 SMART 健康信息（Linux，需 smartmontools）。
- 用法：`/smart`

---

## Docker 管理指令

### /docker status（或 /docker ps）
显示所有容器状态、镜像、端口映射、资源使用等。
- 用法：`/docker status`

### /docker start
启动指定容器。
- 用法：`/docker start <container_name>`
- 参数：`container_name`（必填）

### /docker stop
停止指定容器。
- 用法：`/docker stop <container_name>`
- 参数：`container_name`（必填）

### /docker restart
重启指定容器。
- 用法：`/docker restart <container_name>`

### /docker logs
查看指定容器日志（可指定返回行数）。
- 用法：`/docker logs <container_name> [lines]`
- 参数：`lines`（可选，默认 50）

### /docker stats
显示容器实时资源使用统计。
- 用法：`/docker stats [container_name]`

---

## 警报管理指令（alerts）

### /alerts list
列出已设置的警报及状态。
- 用法：`/alerts list`

### /alerts add
新增系统警报（CPU/内存/磁盘/进程）。
- 用法：`/alerts add <type> <threshold> [channel]`
- 参数：
  - `type`：cpu、memory、disk、process
  - `threshold`：阈值（% 或类型所需值）
  - `channel`：通知频道（可选）
- 示例：
  - `/alerts add cpu 90`
  - `/alerts add memory 85 #alerts`
  - `/alerts add disk 95`

### /alerts remove
移除既有警报。
- 用法：`/alerts remove <alert_id>`

### /alerts test
测试警报通知（可指定类型）。
- 用法：`/alerts test [type]`

---

## SSL 证书指令（ssl）

### /ssl list
列出证书清单、到期日、状态等。
- 用法：`/ssl list`

### /ssl check
查询特定域名证书状态。
- 用法：`/ssl check <domain>`

### /ssl renew
为指定域名续期证书（需整合 NPM 与正确 DNS）。
- 用法：`/ssl renew <domain>`

### /ssl auto-renew
设置自动续期。
- 用法：`/ssl auto-renew <enable|disable> [days_before]`
- 示例：`/ssl auto-renew enable 15`

---

## 配置指令（config）

### /config show
显示当前配置（可指定区段：system、alerts、docker、ssl）。
- 用法：`/config show [section]`

### /config set
更新配置键值。
- 用法：`/config set <key> <value>`
- 示例：`/config set update_interval 15`

### /config reload
重新加载配置文件。
- 用法：`/config reload`

### /language（或 /config language）
更改显示语言或查看可用语言。
- 用法：`/language [language_code]`
- 支持：`en`、`zh`/`zh-tw`、`zh-cn`、`ko`、`ja`、`de`、`ru`

---

## 机器人管理指令（管理权限）

### /restart
重启机器人（仅 Owner）。

### /shutdown
优雅关闭机器人（仅 Owner）。

### /reload
重载指定模块（cog）。
- 用法：`/reload <cog_name>`

### /sync
同步斜杠指令至 Discord。

### /status
显示机器人状态与统计（在线时间、服务器数、资源使用等）。

---

## 帮助指令

### /help
显示说明与分类；可指定分类查看详细指令。
- 用法：`/help [category]`
- 分类：`monitoring`、`docker`、`alerts`、`ssl`、`config`、`admin`

---

## 指令分类与权限

### 公开指令
`/monitor`、`/ports`、`/top`、`/smart`、`/docker status|logs|stats`、`/ssl list|check`、`/config show`、`/language`、`/status`、`/help`

### Owner 指令
`/docker start|stop|restart`、`/alerts add|remove`、`/ssl renew|auto-renew`、`/config set|reload`、`/restart|/shutdown|/reload|/sync`

### 服务器权限（Discord）
- 发送消息：所有指令
- 嵌入链接：带富文本输出的指令
- 使用斜杠指令：所有斜杠指令
- 管理消息：需要编辑/删除消息的功能

---

## 使用建议
- 用 `/monitor` 快速总览系统；配合 `/alerts add` 建立主动警示
- Docker 管理先看 `/docker status`，排错用 `/docker logs`，资源看 `/docker stats`
- 证书建议启用 `/ssl auto-renew enable` 并定期 `/ssl list`
- 配置变更后可 `/config reload`，语言用 `/language` 切换

## 错误处理
- 权限错误：提示所需权限
- 参数错误：提供正确用法建议
- 系统错误：友好信息与保护性降级
- 网络错误：超时处理与重试机制
