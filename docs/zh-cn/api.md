# API 文档（Logivore）

语言：简体中文 | [English](../api.md) | [繁體中文](../zh-tw/api.md)

本文介绍 Logivore 的核心模块、初始化流程、指令注册、i18n、日志、Docker 与 SSL 集成，以及错误处理模式。

## 架构概览
```
Logivore/
├─ main.py                # 启动与初始化
├─ utils/                 # 日志、i18n、Embed、指令工具
├─ cogs/                  # 功能模块（系统监控/警报/Docker/配置/管理/重启/恢复/SSL）
└─ languages/             # 多语言文本
```

## 启动与初始化
入口 `python main.py`：
1) 加载 .env → 2) 初始化日志 → 3) 打印系统信息 → 4) 实例化 `Logivore()` → 5) 加载 Cogs 并同步 Slash 指令

## 配置管理（ConfigManager）
- 文件 `config.json`；缺失/损坏时写入默认
- 通过 `.get/.set` 在运行时读写，供各 Cog 调用

## 模块（Cogs）
- `setup(bot)` 注册；`cog_unload()` 清理
- 可用 `tasks.loop` 创建后台任务

## i18n（国际化）
- `utils/i18n.py` + `languages/*.json`
- `i18n.t(key, lang)` 或设置 `i18n.default_language`

## 指令系统（Slash）
- 使用 `discord.app_commands` 声明；在 `setup_hook()` 全局同步 `tree.sync()`
- 描述与输出支持多语言

## 动态/本地化指令工具
- `utils/localized_commands.py`、`utils/command_registry.py` 提供按语言动态生成描述与分组的能力

## 日志（utils/logging_config.py）
- `setup_bot_logging("logs/logivore.log")`：彩色控制台 + 文件输出
- 命名空间：`logivore`、`logivore.cogs`、`logivore.discord` 等

## 系统监控
- `/monitor`：嵌入面板（CPU/内存/磁盘/网络）
- `/ports`：主机端口（合并 v4/v6），按钮翻页；过长改为附件
- `/top`、`/smart`：进程/磁盘健康

## 警报
- `alerts[]`（`config.json`）或指令维护；支持 CPU/内存/磁盘/进程，可指定频道

## Docker 集成
- `/docker status|logs|start|stop|restart|stats`
- 推荐 Compose 启用 `network_mode: host`、`pid: host`，只读挂载 `/var/run/docker.sock`

## SSL/NPM 集成
- `/ssl list|check|renew|auto-renew`；通过 `docker exec` + openssl 解析证书

## 错误处理
- Slash 同步/API 调用失败：记录并降级
- 400 长度限制：分页或附件回退
- Owner/权限不足：清晰提示所需权限

