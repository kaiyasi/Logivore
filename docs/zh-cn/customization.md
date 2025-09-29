# 自定义指南（Logivore）

语言：简体中文 | [English](../customization.md) | [繁體中文](../zh-tw/customization.md)

本指南说明如何按需自定义与扩展 Logivore：包括新增功能、修改行为、扩展指令与模块、扩展 Docker/SSL 集成、添加语言、构建插件/控制台等。与英文版对齐，提供可直接使用的代码片段。

## 目录
- 了解架构
- 配置自定义（config/.env）
- 新增自定义指令
- 创建自定义 Cog 模块
- 自定义 Embed 与 UI
- 新增语言
- 自定义监控功能
- 警报系统扩展
- Docker 集成扩展
- SSL 管理扩展
- 数据库集成（可选）
- 构建 Web 控制台（可选）
- 插件系统设计（可选）

---

## 了解架构
- `main.py`：启动、配置、加载 Cogs、同步 Slash 指令
- `cogs/`：功能模块（系统监控、Docker、警报、配置、管理、重启/恢复、SSL）
- `utils/`：通用工具（i18n、Embed、日志、指令工具）
- `languages/`：多语言 JSON
- `config/`：自定义配置（如需）

关键模式：Cog 分层 / 配置驱动 / async/await / 多语言 / 模块化

---

## 配置自定义（config/.env）

### `config.json` 扩展示例
```json
{
  "custom_features": {
    "weather_monitoring": {"enabled": true, "api_key": "your_api_key", "locations": ["Shanghai", "Tokyo"], "update_interval": 3600},
    "backup_system": {"enabled": true, "backup_path": "/backups", "schedule": "0 2 * * *", "retention_days": 30}
  }
}
```

### `.env` 扩充
```bash
WEATHER_API_KEY=your_weather_api_key
BACKUP_API_TOKEN=your_backup_token
CUSTOM_WEBHOOK_URL=https://your-webhook.com
ENABLE_WEATHER_MONITORING=true
```

### 在代码中读取配置
```python
class CustomFeatureCog(commands.Cog):
    def __init__(self, bot):
        self.config = bot.config
        self.weather_enabled = self.config.get('custom_features.weather_monitoring.enabled', False)
        self.backup_path = self.config.get('custom_features.backup_system.backup_path', '/backups')
        self.weather_api_key = os.getenv('WEATHER_API_KEY')
```

---

## 新增自定义指令

### 简单指令
```python
@app_commands.command(name="serverinfo", description="显示服务器信息")
async def server_info(self, interaction: discord.Interaction):
    guild = interaction.guild
    embed = EmbedFormatter.create_embed(title=f"📊 {guild.name} 服务器信息", command_name="serverinfo")
    embed.add_field(name="👥 成员", value=str(guild.member_count))
    await interaction.response.send_message(embed=embed)
```

### 进阶：带参数与校验
```python
@app_commands.command(name="weather", description="查询城市天气")
@app_commands.describe(city="城市名称")
async def weather(self, interaction: discord.Interaction, city: str):
    if not self.config.get('custom_features.weather_monitoring.enabled', False):
        return await interaction.response.send_message("❌ 功能已停用", ephemeral=True)
    api_key = os.getenv('WEATHER_API_KEY')
    if not api_key:
        return await interaction.response.send_message("❌ 未设置 API KEY", ephemeral=True)
    # 调用外部 API 获取数据...
```

---

## 创建自定义 Cog 模块

### 最小 Cog 模板
```python
# cogs/my_feature.py
class MyFeature(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.Cog.listener()
    async def on_ready(self):
        print("MyFeature ready")
async def setup(bot):
    await bot.add_cog(MyFeature(bot))
```

### 后台任务与清理
```python
from discord.ext import tasks
class MyFeature(commands.Cog):
    def __init__(self, bot):
        self.task.start()
    def cog_unload(self):
        self.task.cancel()
    @tasks.loop(seconds=60)
    async def task(self):
        ...
```

---

## 自定义 Embed 与 UI
- 使用 `utils/embed_formatter.py` 统一风格
- 长列表使用按钮分页与附件退回避免 1024 限制

分页示例：
```python
class Paginator(discord.ui.View):
    def __init__(self, pages):
        super().__init__(timeout=180)
        self.pages = pages; self.idx = 0
    @discord.ui.button(label="◀")
    async def prev(self, i, b):
        if self.idx>0: self.idx-=1; await i.response.edit_message(embed=self.pages[self.idx], view=self)
    @discord.ui.button(label="▶")
    async def nxt(self, i, b):
        if self.idx<len(self.pages)-1: self.idx+=1; await i.response.edit_message(embed=self.pages[self.idx], view=self)
```

---

## 新增语言
1) 复制 `languages/en.json` → `languages/xx.json`
2) 翻译所有键值；避免删除现有键
3) `.env` 或 `config.json` 设置 `DEFAULT_LANGUAGE=xx`
4) 在 `config_management.py` 的语言菜单添加选项

---

## 自定义监控功能
- 以 Cog 新增 `/netcheck`、`/netscan` 等功能
- 与现有 `/monitor`、`/ports` 输出一致
- 需要 `nmap` 等外部工具时请检查目标环境

---

## 警报系统扩展
- 新增自定义 alert type 与处理流程
- 支持自定义频道、阈值与冷却

---

## Docker 集成扩展
- 视需要新增容器操作（如 prune/inspect）
- 建议只读挂载 `/var/run/docker.sock` 并审视安全

---

## SSL 管理扩展
- 通过 `docker exec <npm>` + openssl 解析/续期
- 增加自动续期策略与提醒天数

---

## 数据库集成（可选）
- 可引入 SQLite/PostgreSQL 存储历史统计/警报记录
- 建议使用 async driver（asyncpg/aiosqlite）

---

## Web 控制台（可选）
- FastAPI/Flask + SocketIO 实时面板
- 通过内部事件/队列与 Web 同步

---

## 插件系统设计（可选）
- 定义 plugin 接口（metadata、hooks、路由注册）
- sandbox/授权管控，避免任意代码执行风险

---

最佳实践：版本控制与 Code Review、分环境配置（dev/prod）、输出长度保护、错误处理与回退、最小权限、敏感信息放入 .env。

