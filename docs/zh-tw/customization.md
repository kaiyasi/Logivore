# 自訂化指南（Logivore）

語言：繁體中文 | [English](../customization.md) | [简体中文](../zh-cn/customization.md)

本指南說明如何依需求自訂與擴充 Logivore：包含新增功能、修改既有行為、擴展指令與模組、擴充 Docker/SSL 整合、加入語言、建立外掛/控制台等。內容對齊英文版章節，提供可直接套用的程式片段。

## 目錄
- 瞭解架構
- 設定自訂（config/.env）
- 新增自訂指令
- 建立自訂 Cog 模組
- 自訂 Embed 與 UI
- 新增語言
- 自訂監控功能
- 警報系統擴充
- Docker 整合擴充
- SSL 管理擴充
- 資料庫整合（選用）
- 建立 Web 控制台（選用）
- 外掛系統設計（選用）

---

## 瞭解架構
- `main.py`：啟動、設定、載入 Cogs、同步 Slash 指令
- `cogs/`：功能模組（系統監控、Docker、警報、設定、管理、重啟/恢復、SSL）
- `utils/`：通用工具（i18n、Embed、日誌、指令工具）
- `languages/`：多語 JSON 檔
- `config/`：自訂設定（如需）

關鍵模式：
1) Cog 分層（discord.py cogs）
2) 設定驅動（JSON 與 .env）
3) 非阻塞（async/await）
4) 多語支援（i18n）
5) 模組化易擴充

---

## 設定自訂（config/.env）

### `config.json` 擴充範例
```json
{
  "custom_features": {
    "weather_monitoring": {
      "enabled": true,
      "api_key": "your_api_key",
      "locations": ["Taipei", "Tokyo"],
      "update_interval": 3600
    },
    "backup_system": {
      "enabled": true,
      "backup_path": "/backups",
      "schedule": "0 2 * * *",
      "retention_days": 30
    }
  }
}
```

### `.env` 擴充
```bash
WEATHER_API_KEY=your_weather_api_key
BACKUP_API_TOKEN=your_backup_token
CUSTOM_WEBHOOK_URL=https://your-webhook.com
ENABLE_WEATHER_MONITORING=true
```

### 於程式取用設定
```python
class CustomFeatureCog(commands.Cog):
    def __init__(self, bot):
        self.config = bot.config
        self.weather_enabled = self.config.get('custom_features.weather_monitoring.enabled', False)
        self.backup_path = self.config.get('custom_features.backup_system.backup_path', '/backups')
        self.weather_api_key = os.getenv('WEATHER_API_KEY')
```

---

## 新增自訂指令

### 簡單指令
```python
@app_commands.command(name="serverinfo", description="顯示伺服器資訊")
async def server_info(self, interaction: discord.Interaction):
    guild = interaction.guild
    embed = EmbedFormatter.create_embed(title=f"📊 {guild.name} 伺服器資訊", command_name="serverinfo")
    embed.add_field(name="👥 成員", value=str(guild.member_count))
    await interaction.response.send_message(embed=embed)
```

### 進階：帶參數與驗證
```python
@app_commands.command(name="weather", description="查詢城市天氣")
@app_commands.describe(city="城市名稱")
async def weather(self, interaction: discord.Interaction, city: str):
    if not self.config.get('custom_features.weather_monitoring.enabled', False):
        return await interaction.response.send_message("❌ 功能已停用", ephemeral=True)
    api_key = os.getenv('WEATHER_API_KEY')
    if not api_key:
        return await interaction.response.send_message("❌ 未設定 API KEY", ephemeral=True)
    # 呼叫外部 API 取得資料...
```

---

## 建立自訂 Cog 模組

### 最小 Cog 範本
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

### 背景任務與清理
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

## 自訂 Embed 與 UI

- 使用 `utils/embed_formatter.py` 統一風格
- 大量列表請使用「按鈕分頁」與「附件退回」避免 1024 限制

分頁範例：
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

## 新增語言
1) 複製 `languages/en.json` → `languages/xx.json`
2) 翻譯所有鍵值；避免刪除既有鍵
3) `.env` 或 `config.json` 設定 `DEFAULT_LANGUAGE=xx`
4) 在 `config_management.py` 的語言選單加入對應項目

---

## 自訂監控功能
- 以 Cog 新增 `/netcheck`、`/netscan` 等專用功能
- 與既有 `/monitor`、`/ports` 輸出一致
- 依需求引入 `nmap` 等外部工具

---

## 警報系統擴充
- 新增自訂 alert type 與處理流程
- 支援自訂頻道、門檻與冷卻時間

---

## Docker 整合擴充
- 依需求新增容器操作（如 prune/inspect）
- 建議唯讀掛載 `/var/run/docker.sock` 並審視安全

---

## SSL 管理擴充
- 透過 `docker exec <npm>` 搭配 openssl 解析與續期
- 增加自動續期策略與提醒天數

---

## 資料庫整合（選用）
- 可引入 SQLite/PostgreSQL 儲存歷史統計與警報紀錄
- 建議使用 async driver（asyncpg/aiosqlite）

---

## Web 控制台（選用）
- 以 FastAPI/Flask + SocketIO 建立即時面板
- 以 bot 內部事件或佇列與 Web 同步

---

## 外掛系統設計（選用）
- 定義 plugin 介面（metadata、hooks、路由註冊）
- sandbox/授權控管，避免任意碼風險

---

最佳實踐：版本控制與代碼審查、分環境設定（dev/prod）、輸出長度保護、錯誤處理與回退、權限最小化、敏感資訊置於 .env。

