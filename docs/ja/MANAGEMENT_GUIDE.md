# 🛠️ 管理ガイド

言語: 日本語（本ページ） | [繁體中文](../../MANAGEMENT_GUIDE.md) | [简体中文](../zh-cn/MANAGEMENT_GUIDE.md)

## 概要

Bot を再起動せずに、Cog/機能を動的に管理します。

## 🔧 コマンド

- `/manage reload` — 単一モジュールのリロード
- `/manage reload_all` — すべてのモジュールをリロード
- `/manage sync` — Slash コマンドを同期
- `/manage status` — Bot/システム状態、ロード済みモジュール
- `/manage logs` — 直近ログ表示
- `/manage restart` — Bot を再起動（systemd）
- `/manage shutdown` — Bot を安全に停止
- `/manage eval` — コード実行（所有者のみ、要注意）

## 🔒 権限

管理コマンドは Bot 所有者のみに制限。

## 🚀 例

機能追加: 変更 → `/manage reload` → 必要なら `/manage sync` → テスト → `/manage status`

大規模変更: `/manage reload_all` → `/manage sync` → `/manage logs`

## ⚠️ 注意

- リロードでモジュール内部状態がリセットされる場合あり
- 失敗時は詳細なエラーを返す
- `/manage eval` は高権限

## 🔄 ホットリロードの利点

無停止、迅速な検証、他モジュールへの影響最小化、障害の局所化。

