# 🛠️ 机器人管理工具使用指南

语言：简体中文（本页） | [繁體中文](../../MANAGEMENT_GUIDE.md)

## 功能概述

管理工具允许在不重启机器人的情况下动态管理模块与系统功能。

## 🔧 可用指令

### `/manage reload` — 重新加载单个模块
重新加载指定 Cog 模块，适用于单模块更新。

选项示例：
- System Monitoring（系统监控）
- Alerting（告警系统）
- Docker Management（Docker 管理）
- Config Management（配置管理）
- Bot Management（机器人管理）

使用场景：
```
开发者修改了告警系统 → 使用 /manage reload Alerting
```

### `/manage reload_all` — 重新加载全部模块
一次性重新加载全部 Cogs，适合大范围更新。

### `/manage sync` — 同步指令
手动同步 Slash Commands，适用于新增指令后。

### `/manage status` — 机器人状态
显示机器人与系统状态、已加载模块、配置摘要等。

### `/manage logs` — 查看日志
显示最近日志（默认 20 行）。

### `/manage restart` — 重启机器人
若以 systemd 运行，可重启服务。

### `/manage shutdown` — 关闭机器人
优雅关闭机器人。

### `/manage eval` — 执行代码（危险）
仅限机器人拥有者用于调试。

## 🔒 权限控制

仅机器人拥有者可使用管理指令，确保安全。

## 🚀 开发流程示例

场景：新增功能后测试
1. 修改代码
2. `/manage reload [模块]`
3. 若新增指令，执行 `/manage sync`
4. 测试功能
5. `/manage status` 检查状态

场景：大范围更新
1. 完成所有修改
2. `/manage reload_all`
3. `/manage sync`
4. `/manage logs` 检查无错误

## ⚠️ 注意事项

1. 权限：仅拥有者可用
2. 状态：重新加载可能重置模块内运行状态
3. 错误：失败时会返回详细错误信息
4. 安全：`/manage eval` 拥有高权限，谨慎使用

## 🔄 热重载优势

- 零停机：无需重启整个机器人
- 快速验证：改完立即测
- 状态保持：其他模块不受影响
- 故障隔离：单模块异常不影响全局

