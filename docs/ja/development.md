# 開発ガイド

言語: 日本語 | [English](../development.md) | [繁體中文](../zh-tw/development.md) | [简体中文](../zh-cn/development.md)

本ガイドは、Logivore に貢献する開発者のための実務手順・規約をまとめたものです。

## 目次

- [開発環境のセットアップ](#開発環境のセットアップ)
- [プロジェクト構成](#プロジェクト構成)
- [開発ワークフロー](#開発ワークフロー)
- [コードスタイルと規約](#コードスタイルと規約)
- [テストフレームワーク](#テストフレームワーク)
- [アーキテクチャパターン](#アーキテクチャパターン)
- [コントリビューションガイドライン](#コントリビューションガイドライン)
- [リリースプロセス](#リリースプロセス)
- [開発ツール](#開発ツール)
- [デバッグとプロファイリング](#デバッグとプロファイリング)

## 開発環境のセットアップ

### 前提

- Python 3.8 以上、Git、（任意）Docker
- 仮想環境（venv/virtualenv/conda）

### 初期セットアップ

```bash
# 1) リポジトリをクローン
git clone https://github.com/kaiyasi/Logivore.git
cd Logivore

# 2) 仮想環境の作成と有効化
python -m venv venv
source venv/bin/activate      # Linux/Mac
# または
venv\Scripts\activate        # Windows

# 3) 依存関係のインストール
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 4) pre-commit のセットアップ
pre-commit install

# 5) 設定ファイルの準備
cp .env.example .env
cp config/bot_config.example.json config/bot_config.json

# 6) ディレクトリの作成
mkdir -p logs data/backups
```

## プロジェクト構成

- エントリポイント: `main.py`
- 機能: `cogs/`
- 共通: `utils/`
- 言語: `languages/`
- テスト: `tests/`
- ドキュメント: `docs/`

英語版の詳細ガイドに、より完全な構成図や関係図があります。

## 開発ワークフロー

### Git Flow

```bash
main        # 本番安定
develop     # 統合ブランチ
feature/*   # 新機能
hotfix/*    # 重大バグ修正
release/*   # リリース準備
```

### 作業フロー例

```bash
git checkout develop && git pull
git checkout -b feature/new-monitoring
# 実装
git add . && git commit -m "feat(monitoring): add GPU temperature"
git push -u origin feature/new-monitoring
# PR → レビュー → develop へマージ
```

### コミット規約

Conventional Commits（feat/fix/docs/style/refactor/perf/test/chore/ci）に従います。

## コードスタイルと規約

- 型ヒント（type hints）を徹底
- Lint/Format：Black, isort, flake8, mypy
- Docstring：Google スタイル

```python
from typing import Any, Dict, List, Optional, Union

async def process_data(
    data: List[Dict[str, Any]],
    config: Dict[str, str],
    timeout: Optional[float] = None
) -> Union[str, None]:
    pass
```

## テストフレームワーク

- Pytest 構成、非同期テスト、モック/フィクスチャ
- 変更箇所の単体テストから開始し、徐々に広げる

```bash
pytest -q
pytest tests/test_utils -q
```

## アーキテクチャパターン

- Cog ベースのモジュール化
- Async-first
- 設定駆動（JSON）

## コントリビューションガイドライン

- 小さく焦点の定まった PR
- 新規/変更ロジックにはテストを同梱
- 無関連の変更を単一 PR に混在させない

## リリースプロセス

- `develop` から release ブランチ
- CI/CD：テスト、Lint、ビルド/配布
- バージョニングと CHANGELOG の更新

## 開発ツール

### VS Code 設定例

```json
{
  "python.defaultInterpreterPath": "./venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "python.linting.mypyEnabled": true,
  "python.formatting.provider": "black",
  "python.formatting.blackArgs": ["--line-length", "100"],
  "python.sortImports.args": ["--profile", "black"],
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {"source.organizeImports": true}
}
```

## デバッグとプロファイリング

- 構造化ログと例外時の十分な文脈
- バックグラウンドタスクのトレーシング
- メトリクス収集とボトルネックの特定
