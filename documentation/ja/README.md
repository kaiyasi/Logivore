# 🤖 Logivore

Languages: [English](README.md) | [繁體中文](README.zh-tw.md) | [简体中文](README.zh-cn.md) | 日本語 | [한국어](README.ko.md) | [Deutsch](README.de.md) | [Русский](README.ru.md)

<div align="center">

**高度なシステム監視・管理 Discord ボット**

*包括的なリアルタイム監視、インテリジェントアラート、自動化されたシステム管理*

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Discord.py](https://img.shields.io/badge/discord.py-2.0+-green.svg)](https://discordpy.readthedocs.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Made by](https://img.shields.io/badge/Made%20by-Serelix%20Studio-purple.svg)](https://serelix.xyz)

[🚀 クイックスタート](#-クイックスタート) • [✨ 機能](#-機能) • [🌍 言語](#-対応言語) • [📖 ドキュメント](#-ドキュメント) • [💬 サポート](#-サポート)

</div>

## 📋 概要

Logivore は、包括的なシステム監視と管理のために設計された強力な Discord ボットです。高度な自動化機能で構築され、サーバーインフラストラクチャへのリアルタイムな洞察を提供しながら、エンタープライズグレードの信頼性とセキュリティを維持します。

### 🎯 主要機能

- **🔍 リアルタイムシステム監視** - CPU、メモリ、ディスク、ネットワーク統計
- **🚨 インテリジェントアラートシステム** - システム問題の予防的通知
- **🐳 Docker 管理** - 完全なコンテナライフサイクル管理
- **🔄 サービス復旧** - システムイベント後の自動サービス復元
- **⚡ SSL証明書管理** - 自動化された証明書監視と更新
- **🌐 多言語サポート** - ローカライズされたインターフェースで8言語対応

## ✨ 機能

### 🖥️ システム監視
```
リアルタイム更新のダッシュボード
ネットワークポート監視
ディスクヘルスチェック (SMART)
プロセス管理と監視
```

### 🚨 アラート管理
```
CPU/メモリ/ディスク使用率アラート
プロセス監視モニタリング
カスタム閾値設定
マルチチャンネル通知サポート
```

### 🐳 Docker 統合
```
コンテナ状態監視
開始/停止/再起動操作
リソース使用量追跡
ログ管理
```

### 🛡️ システム管理
```
スケジュールされたシステム再起動
サービス復旧の自動化
SSL証明書監視
Nginx Proxy Manager 統合
```

## 🌍 対応言語

<div align="center">

| 言語 | コード | 状態 |
|----------|------|--------|
| 🇺🇸 English | `en` | ✅ 完了 |
| 🇹🇼 繁體中文 | `zh`/`zh-tw` | ✅ 完了 |
| 🇨🇳 简体中文 | `zh-cn` | ✅ 完了 |
| 🇰🇷 한국어 | `ko` | ✅ 完了 |
| 🇯🇵 日本語 | `ja` | ✅ 完了 |
| 🇩🇪 Deutsch | `de` | ✅ 完了 |
| 🇷🇺 Русский | `ru` | ✅ 完了 |

</div>

## 🚀 クイックスタート

### 前提条件
- Python 3.8+
- Discord Bot Token
- Linux/Windows/macOS システム

### インストール
```bash
# リポジトリのクローン
git clone https://github.com/kaiyasi/Logivore.git
cd Logivore

# 依存関係のインストール
pip install -r requirements.txt

# 環境設定
cp .env.example .env
# Discord ボットトークンと設定で .env を編集

# ボットの実行
python main.py
```

### Docker デプロイメント（オプション）
```bash
cd deploy/docker
docker compose up -d --build
```

## 🏗️ アーキテクチャ

### 🔧 技術スタック
- **バックエンドフレームワーク**: discord.py 2.0+ を使用した Python 3.8+
- **システム監視**: psutil、subprocess 統合
- **コンテナ管理**: Docker API 統合
- **SSL 管理**: Nginx Proxy Manager との Let's Encrypt
- **国際化**: JSON ベースの多言語システム
- **設定**: ホットリロード機能付き JSON

### 📦 コアモジュール
```
├── 🔍 システム監視      - リアルタイムシステム統計
├── 🚨 アラートシステム  - 予防的監視アラート
├── 🐳 Docker 管理      - コンテナライフサイクル制御
├── 🔄 サービス復旧      - 自動サービス復元
├── 🛡️ SSL 管理        - 証明書監視と更新
├── ⚙️ 設定            - 動的設定管理
├── 🤖 ボット管理        - 管理制御
└── 📚 ヘルプシステム    - インタラクティブドキュメント
```

## 📖 ドキュメント

- **[インストールガイド](../installation.md)** - ステップバイステップの設定手順
- **[設定リファレンス](../configuration.md)** - 完全な設定ドキュメント
- **[コマンドリファレンス](../commands.md)** - 利用可能なすべてのボットコマンド
- **[API ドキュメント](../api.md)** - 統合と拡張ガイド
- **[トラブルシューティング](../troubleshooting.md)** - 一般的な問題と解決策
- 追加ガイド:
  - **[Embed フォーマットガイド](../ja/EMBED_FORMAT_GUIDE.md)**
  - **[管理ガイド](../ja/MANAGEMENT_GUIDE.md)**
  - **[再起動後の自動復旧セットアップ](../ja/SETUP-RECOVERY.md)**

## 🤝 貢献

貢献を歓迎します！詳細については、[貢献ガイドライン](CONTRIBUTING.md)をご覧ください。

### 開発環境セットアップ
```bash
# 開発環境のクローンとセットアップ
git clone https://github.com/kaiyasi/Logivore.git
cd Logivore

# 開発依存関係のインストール
pip install -r requirements-dev.txt

# テストの実行
python -m pytest tests/
```

## 📝 ライセンス

このプロジェクトは MIT ライセンスの下でライセンスされています。詳細については [LICENSE](LICENSE) ファイルをご覧ください。

## 💬 サポート

<div align="center">

### 🔗 コミュニティとサポート

[![GitHub Issues](https://img.shields.io/badge/GitHub-Issues-red.svg)](https://github.com/kaiyasi/Logivore/issues)
[![GitHub Discussions](https://img.shields.io/badge/GitHub-Discussions-blue.svg)](https://github.com/kaiyasi/Logivore/discussions)
[![Discord](https://img.shields.io/badge/Discord-Community-purple.svg)](https://discord.gg/serelix)
[![Email](https://img.shields.io/badge/Email-Support-green.svg)](mailto:serelixstudio@gmail.com)

</div>

### 📞 連絡先情報

- **公式ウェブサイト**: [https://serelix.xyz](https://serelix.xyz)
- **GitHub リポジトリ**: [https://github.com/kaiyasi/Logivore](https://github.com/kaiyasi/Logivore)
- **メール**: serelixstudio@gmail.com
- **Instagram**: [@serelix.studio](https://instagram.com/serelix.studio)

---

<div align="center">

**❤️ で作られた [Serelix Studio](https://serelix.xyz)**

*インテリジェントな自動化によるサーバー管理の強化*

</div>
