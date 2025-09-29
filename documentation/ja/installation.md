# インストールガイド（Logivore）

言語：[日本語](installation.md) | [English](../installation.md) | [繁體中文](../zh-tw/installation.md) | [简体中文](../zh-cn/installation.md)

本ガイドは、Logivore をゼロからセットアップする手順（Docker と systemd 推奨手順を含む）と、初期トラブルシューティングを解説します。

## 目次

- 前提条件
- システム要件
- Discord Bot の作成
- ローカルインストール（非コンテナ）
- Docker デプロイ（任意）
- 環境変数（.env）
- 初回起動
- システムサービスとして実行（Linux, systemd）
- トラブルシューティング

## 前提条件

- Python 3.8 以上
- Git / pip
（任意）Docker / Docker Compose、systemd（Linux）、smartmontools（SMART 検査）

## システム要件

- 最小：RAM 512MB、Disk 1GB、CPU 1 コア、安定したネットワーク
- 推奨：RAM 1GB+、Disk 2GB+、CPU 2 コア以上、Ubuntu 20.04+ / Windows 10+ / macOS 10.15+

## Discord Bot の作成

1) [Discord Developer Portal](https://discord.com/developers/applications)
2) New Application → 名前（例：Logivore）
3) Bot タブで Add Bot
4) Intents：Server Members / Message Content を有効化
5) Token を再生成して安全に保存（.env に設定）
6) OAuth2 → URL Generator：`bot` と `applications.commands` を選択、必要権限（Send Messages / Embed Links / Use Slash Commands / Read Message History / View Channels）でサーバーに招待

## ローカルインストール（非コンテナ）

```bash
git clone https://github.com/kaiyasi/Logivore.git
cd Logivore

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env  # DISCORD_TOKEN / OWNER_ID などを設定
python main.py
```

## Docker デプロイ（任意）

Docker で容易に実行できますが、ホスト可視性（/ports や詳細メトリクス）やホスト制御の一部が制限される場合があります。最大機能が必要なら systemd を推奨します。

```bash
cd deploy/docker
# 事前にプロジェクトルートで .env を用意：cp .env.example .env
docker compose up -d --build
```

デフォルト compose は `network_mode: host` / `pid: host` を使用し、`/var/run/docker.sock:ro` をマウントしてコンテナ情報取得と管理を可能にしています。

## 環境変数（.env）

```bash
DISCORD_TOKEN=あなたのBotトークン
OWNER_ID=あなたのDiscordユーザーID
LOG_LEVEL=INFO
LOG_FILE=logs/logivore.log
```

詳細設定は `docs/configuration.md` を参照。

## 初回起動

コンソールに以下のような出力が表示されます：

```
✅ Bot is ready!
✅ Logged in as: <YourBot>#1234
✅ Connected to X guilds
```

Discord でテスト：`/help`、`/config show`、`/monitor`

## システムサービスとして実行（Linux, systemd）

最大の安定性と可視性が必要な場合は systemd を推奨します。

```bash
sudo nano /etc/systemd/system/logivore.service
```

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

有効化：

```bash
sudo systemctl daemon-reload
sudo systemctl enable logivore
sudo systemctl start logivore
sudo systemctl status logivore
```

起動時の自動復旧や sudoers 設定は `systemd-examples/` と `SETUP-RECOVERY.md` を参照。

## トラブルシューティング

- 依存関係：`pip install -r requirements.txt`
- Token エラー：`.env` の `DISCORD_TOKEN` を再確認
- Slash Commands が出ない：同期に数十秒、権限 `applications.commands` を確認
- Docker コンテナが即終了：`docker compose logs -f logivore` でログ確認、環境変数やボリューム設定を確認

デバッグ：`.env` の `LOG_LEVEL=DEBUG`、または `python main.py 2>&1 | tee logs/startup.log`
