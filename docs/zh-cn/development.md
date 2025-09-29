# 开发指南（Logivore）

语言：简体中文 | [English](../development.md) | [繁體中文](../zh-tw/development.md)

本指南帮助开发者快速理解项目结构、设置环境、遵循风格、编写/测试 Cogs、维护 i18n 与日志、提交 PR 与发布。

## 目录
- 项目结构
- 开发环境
- 运行与调试
- 代码风格
- Cogs 开发
- 指令与交互
- i18n 管理
- 日志与诊断
- 测试与验证
- Docker 开发流程
- 提交规范
- 发布与变更日志

---

## 项目结构
```
Logivore/
├─ main.py
├─ cogs/
├─ utils/
├─ languages/
├─ deploy/
└─ docs/
```

## 开发环境
```bash
git clone https://github.com/kaiyasi/Logivore.git
cd Logivore
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python main.py
```

## 运行与调试
- `.env` 设置 `LOG_LEVEL=DEBUG`
- `python main.py 2>&1 | tee logs/startup.log`
- 首次 Slash 同步需数十秒

## 代码风格
- Python 3.8+；类型标注以 3.8 兼容
- 命名：snake_case / PascalCase
- 异常：记录→友好提示→不中断主流程
- 嵌入输出遵守 1024 限制（分页或附件）

## Cogs 开发
- `cogs/my_feature.py`；在 `async def setup(bot)` 注册
- 背景任务 `tasks.loop`；于 `cog_unload()` 取消
- Slash 使用 `discord.app_commands`

## 指令与交互
- `tree.sync()` 全局同步
- 大输出：按钮分页与附件回退
- 统一的错误提示（用法/权限）

## i18n 管理
- 复制 `languages/en.json` → 翻译 → `.env DEFAULT_LANGUAGE`
- `i18n.t(key, lang)` 获取文本

## 日志与诊断
- `utils/logging_config.py`：彩色控制台 + 文件
- 命名空间：`logivore.*`

## 测试与验证
- 建议 pytest 测试 utils 与逻辑
- 手工验证常用指令

## Docker 开发流程
- 使用 `deploy/docker/docker-compose.yml`
- 默认启用 host/pid 模式与只读 docker.sock

## 提交规范
- Commit：feat/fix/docs/refactor
- PR：动机/范围/测试/兼容性
- 变更日志：摘要主要更改

## 发布与变更日志
- Tag：`vX.Y.Z`
- 说明：新增/修复/不兼容变更/升级提示

