# コマンドリファレンス（Logivore）

言語：[日本語](commands.md) | [English](../commands.md) | [繁體中文](../zh-tw/commands.md) | [简体中文](../zh-cn/commands.md)

本ガイドは、Logivore のすべてのスラッシュコマンドを用途・引数・例とともに解説します。

## 目次
- システム監視
- Docker 管理
- アラート管理
- SSL 証明書
- 設定
- ボット管理
- ヘルプ
- カテゴリと権限
- 使い方のヒント / エラー処理

---

## システム監視

### /monitor
リアルタイムの監視ダッシュボード（CPU/メモリ/ディスク/ネットワーク）。10 秒ごとに自動更新。
- 使い方：`/monitor`

### /ports
ホストのポート占有状況（Docker マッピング + システム LISTEN）を表示。ページネーション対応、長文は添付へフォールバック。
- 使い方：`/ports`

### /top
CPU/メモリの上位プロセス。
- 使い方：`/top [count]`（デフォルト 10、1–20）

### /smart
ディスクの SMART 健康情報（Linux、smartmontools 必要）。
- 使い方：`/smart`

---

## Docker 管理

### /docker status（/docker ps）
全コンテナの状態・画像・ポート・リソース。
- 使い方：`/docker status`

### /docker start / stop / restart
- 使い方：`/docker start <container>` / `stop` / `restart`

### /docker logs
コンテナのログを表示。
- 使い方：`/docker logs <container> [lines]`（デフォルト 50）

### /docker stats
コンテナのリソース統計。
- 使い方：`/docker stats [container]`

---

## アラート管理（alerts）

### /alerts list
設定済みアラート一覧。
- 使い方：`/alerts list`

### /alerts add
アラート作成（CPU/メモリ/ディスク/プロセス）。
- 使い方：`/alerts add <type> <threshold> [channel]`
- type：`cpu` `memory` `disk` `process`

### /alerts remove
- 使い方：`/alerts remove <alert_id>`

### /alerts test
- 使い方：`/alerts test [type]`

---

## SSL 証明書（ssl）

### /ssl list / check / renew / auto-renew
- 使い方：`/ssl list`、`/ssl check <domain>`、`/ssl renew <domain>`、`/ssl auto-renew <enable|disable> [days_before]`

---

## 設定（config）

### /config show
- 使い方：`/config show [section]`（system / alerts / docker / ssl）

### /config set
- 使い方：`/config set <key> <value>`（例：`/config set update_interval 15`）

### /config reload
- 使い方：`/config reload`

### /language（/config language）
- 使い方：`/language [language_code]`（`en`/`zh-tw`/`zh-cn`/`ko`/`ja`/`de`/`ru`）

---

## ボット管理（要 Owner）

- `/restart`：再起動
- `/shutdown`：正常停止
- `/reload <cog>`：モジュール再読み込み
- `/sync`：スラッシュコマンド同期
- `/status`：稼働状況、サーバー数、リソース等

---

## ヘルプ

### /help
カテゴリ別の説明を表示。
- 使い方：`/help [category]`（`monitoring` / `docker` / `alerts` / `ssl` / `config` / `admin`）

---

## カテゴリと権限

- 一般ユーザー：`/monitor` `/ports` `/top` `/smart` `/docker status|logs|stats` `/ssl list|check` `/config show` `/language` `/status` `/help`
- Owner 限定：`/docker start|stop|restart` `/alerts add|remove` `/ssl renew|auto-renew` `/config set|reload` `/restart|/shutdown|/reload|/sync`
- Discord 権限：Send Messages / Embed Links / Use Slash Commands /（必要に応じて）Manage Messages

---

## 使い方のヒント / エラー処理

- 監視：`/monitor` で概観、`/alerts add` で能動的通知
- Docker：`/docker status` → `logs` → `stats` の順で確認
- SSL：`/ssl auto-renew enable` を有効化し、定期的に `/ssl list`
- 設定：`/config show` / `reload`、言語は `/language`

エラー処理：
- 権限不足 → 必要権限を案内
- 引数不正 → 正しい使い方を提案
- システム例外 → わかりやすいメッセージとフォールバック
- ネットワーク → タイムアウトとリトライ
