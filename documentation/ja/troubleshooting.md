# トラブルシューティング（Logivore）

言語：[日本語](troubleshooting.md) | [English](../troubleshooting.md) | [繁體中文](../zh-tw/troubleshooting.md) | [简体中文](../zh-cn/troubleshooting.md)

一般的な問題、診断手順、修正方法をまとめています（systemd / Docker 両対応）。

## 目次
- クイックチェック
- ログ/ステータス取得
- 起動時の問題
- コマンド/権限の問題
- Docker 関連
- systemd サービス
- SSL/証明書
- アラート
- パフォーマンス
- エラーコード
- リカバリー
- FAQ

---

## クイックチェック
1) `.env`：`DISCORD_TOKEN` / `OWNER_ID` 正しいか
2) 依存関係：`pip install -r requirements.txt`
3) 権限：Send Messages / Embed Links / Use Slash Commands
4) パス：`logs/` `config/` 書込可、Docker のボリューム
5) 言語：`DEFAULT_LANGUAGE` が `languages/` に存在

## ログ/ステータス取得
```bash
tail -f logs/logivore.log
python main.py 2>&1 | tee logs/startup.log
cd deploy/docker && docker compose logs -f logivore
```

Slash Commands の同期は数十秒かかる場合があります。

## 起動時の問題
- Token 無効：Developer Portal で再発行し `.env` 更新
- 依存不足：`pip install -r requirements.txt`
- Python 版：3.8+ を使用
- Slash Commands が出ない：`applications.commands` 権限、Bot がサーバーに参加しているか

## コマンド/権限
- 送信/埋め込み不可：チャンネル権限を確認
- Owner 限定：`.env` の `OWNER_ID` が自分の ID か
- 400 Bad Request（フィールド長超過）：出力は分割/添付にフォールバック済み（再発時は状況共有）

## Docker 関連
- 即終了：`docker compose logs -f logivore`、環境変数/ボリュームを確認
- 可視性不足：`network_mode: host` / `pid: host` を有効化
- `/ports` 重複表示：IPv4/IPv6 を統合表示（IP 列は v4/v6/*）

## systemd サービス
```bash
sudo systemctl status logivore
sudo journalctl -u logivore -f
```
- `ExecStart` / `WorkingDirectory` / `User` を確認
- 起動時復旧：`systemd-examples/` と `SETUP-RECOVERY.md`

## SSL/証明書
- NPM コンテナ名、`SSL_CERT_PATH`、OpenSSL 利用可否
- DNS（A/AAAA）と Let’s Encrypt の制限

## アラート
- 閾値 0–100、`alert_interval`、`alert_channel` 設定
- 目安：CPU/メモリ 80–90%、ディスク 85–95%

## パフォーマンス
- 間隔：`UPDATE_INTERVAL` / `ALERT_INTERVAL` を長く
- 機能：不要なら Docker 監視やパネル数を削減
- OS 側：top/htop で調査

## エラーコード
- 50035 Invalid Form Body：長さ制限超過（保護あり）
- LoginFailure：Token 無効
- Missing Permissions：権限不足
- JSONDecodeError：config.json 構文

## リカバリー
- バックアップ：`cp -r config logs backups/$(date +%F_%T)`
- 復元：必要に応じて戻す
- 再起動：サービス/コンテナ

## FAQ
- 初回同期？ → 数十秒待機、再起動、権限確認
- `/ports` が長い → 分割/添付対応。再発時は出力を共有
- Docker 安全性 → read_only / no-new-privileges / tmpfs / docker.sock:ro の前提。要件に応じ調整
