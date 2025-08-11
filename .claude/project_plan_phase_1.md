# Modern Python 開発環境 - フェーズ1 プロジェクト計画

## 概要
フェーズ1では、Modern Python開発環境の基盤構築から、プロフェッショナルな開発ツールチェーンの確立までを目指します。Docker、VSCode DevContainer、Rust製ツール（uv、Ruff）を活用し、高速で再現可能な開発環境を構築します。

## タスクステータス凡例
- ✅ **完了** - 実装および検証済み
- 🔄 **進行中** - 現在作業中
- ⏳ **保留中** - 未着手
- 🧪 **テスト中** - 実装完了、検証待ち
- ❌ **ブロック** - 問題により停止中

---

## フェーズ1.0: 基盤構築

### タスク1.0.1: Docker環境の構築
**ステータス:** ✅ **完了**

**目的:** OS非依存の統一された開発環境を構築

**実施内容:**
- Docker + VSCode DevContainer環境の構築
- Python 3.13環境のセットアップ
- 必要なシステムパッケージのインストール
- 非rootユーザー（vscode）の設定

**成果:**
- `.devcontainer/Dockerfile` 完成
- `.devcontainer/devcontainer.json` 設定
- Windows/macOS/Linuxで動作確認済み

### タスク1.0.2: Rust製ツールの導入
**ステータス:** ✅ **完了**

**目的:** 高速な開発ツールチェーンの確立

**実施内容:**
- uv（パッケージマネージャー）の導入
- Ruff（リンター/フォーマッター）の設定
- 公式イメージからのバイナリコピー方式を採用

**学んだ教訓:**
- `curl | sh` インストールは環境依存で不安定
- `COPY --from=ghcr.io/astral-sh/uv:0.8.7` が最も確実

### タスク1.0.3: プロジェクト構造の確立
**ステータス:** ✅ **完了**

**目的:** 標準的なPythonプロジェクト構造の構築

**実施内容:**
- `pyproject.toml` による依存関係管理
- `src/` と `tests/` ディレクトリ構造
- Makefile によるタスク自動化
- 基本的なテストとサンプルコード作成

---

## フェーズ1.1: CI/CDパイプライン

### タスク1.1.1: GitHub Actions基本設定
**ステータス:** ✅ **完了**

**目的:** 自動化されたCI/CDパイプラインの構築

**実施内容:**
- `.github/workflows/ci.yml` の作成
- Lint、Test、Build、Docker、Securityジョブの設定
- GitHub Container Registry (GHCR) へのプッシュ設定

**最適化:**
- マトリックステストから単一環境に変更（リソース削減）
- キャッシュ戦略の実装

### タスク1.1.2: GHCR権限問題の解決
**ステータス:** ✅ **完了**

**問題:** Docker imageのpush時に権限エラー

**解決策:**
1. GitHubパッケージ設定をPublicに変更
2. workflow に `packages: write` 権限を追加

**成果:**
- Docker image が `ghcr.io/taroskee/modern-python:main` で公開

### タスク1.1.3: CI品質チェックの問題発見
**ステータス:** ✅ **完了**

**発見した問題:**
- `continue-on-error: true` により品質チェックが形骸化
- mainブランチへの直接pushが可能
- Pre-commitフックが未設定

**文書化:**
- `technical_considerations.md` に問題と対策を記載
- `TODO.md` に改善タスクを整理

---

## フェーズ1.2: ドキュメント整備

### タスク1.2.1: README.md作成
**ステータス:** ✅ **完了**

**内容:**
- プロジェクト概要
- インストール手順
- 使用方法
- コントリビューションガイド

### タスク1.2.2: technical_considerations.md作成
**ステータス:** ✅ **完了**

**内容:**
- 技術的決定事項
- 遭遇した問題と解決策
- トラブルシューティングガイド
- ベストプラクティス

### タスク1.2.3: C4アーキテクチャ図作成
**ステータス:** ✅ **完了**

**内容:**
- System Context図
- Container図
- Component図
- 技術選定理由

### タスク1.2.4: .claudeディレクトリ整備
**ステータス:** ✅ **完了**

**内容:**
- `CLAUDE.md` - Claude Code用ガイドライン
- `pair_programming.md` - ペアプログラミングワークフロー
- `project_plan_phase_1.md` - プロジェクト計画（本ファイル）

---

## フェーズ1.3: 品質管理強化（進行中）

### タスク1.3.0: 型チェッカーをmypyからPyrightへ移行
**ステータス:** ✅ **完了**

**目的:** より高速で高機能な型チェッカーへの移行

**計画:**
- **pyproject.toml更新**
  - [tool.mypy]セクション削除
  - [tool.pyright]セクション追加（strict mode設定）
- **CI/CD設定更新**
  - .github/workflows/ci.ymlでmypy→pyright変更
  - Node.js/npmインストール追加
  - pyrightインストールと実行
- **Makefile更新**
  - `make type`コマンドをpyright使用に変更
- **Dockerfile更新**
  - Node.js LTSインストール追加
  - npm install -g pyright追加
- **ドキュメント更新**
  - README.md: ty→Pyright
  - c4-architecture.md: ty→Pyright、技術選定理由更新
  - .claude/CLAUDE.md: 型チェッカーをPyrightに統一
  - technical_considerations.md: 移行理由追記
- **VSCode設定**
  - .vscode/settings.jsonにPylance設定追加
  - python.analysis.typeCheckingMode: strict

**移行理由:**
- 3-5倍高速（大規模コードベースで顕著）
- VSCode/Pylanceとの優れた統合
- より多くのエラー検出と優れた型推論
- Python 3.13新機能への即座対応

### タスク1.3.1: Docker CIワークフローの分離
**ステータス:** 🧪 **テスト中**（修正適用済み、動作確認待ち）

**目的:** CI/CDリソースの最適化

**実施内容:**
- ✅ `.github/workflows/docker.yml`を新規作成
- ✅ Docker関連ファイル変更時のみ実行するpathsフィルター設定
- ✅ ci.ymlからdockerジョブを削除
- ✅ 週次スケジュール実行の設定

**発見した問題（2025-08-11）:**
- **エラー:** Trivyスキャンでイメージ名のパースエラー
  ```
  failed to parse the image name: could not parse reference: ghcr.io/taroskee/modern-python:main
  ```
- **原因:** `${{ github.repository }}` が `taroskee/modern-python` となり、ユーザー名に大文字を含む場合に問題が発生
- **影響:** GitHub Container Registry (GHCR) では全て小文字である必要がある

**適用した修正（2025-08-11）:**
- ✅ docker.ymlに小文字変換ステップを追加
  ```yaml
  - name: Set lowercase image name
    id: image
    run: |
      echo "name=${GITHUB_REPOSITORY,,}" >> $GITHUB_OUTPUT
  ```
- ✅ 全てのイメージ参照を `${{ steps.image.outputs.name }}` に変更
- ✅ Trivy、テスト、SBOM生成の全ステップで修正を適用

**期待効果（修正後）:**
- CI実行時間: 通常のコード変更で約2分短縮
- GitHub Actions無料枠: Docker実行を約80%削減
- 開発速度: フィードバックループの高速化

### タスク1.3.2: Pre-commitフックの導入
**ステータス:** ✅ **完了**

**目的:** ローカルでの品質チェック自動化

**計画:**
- `.pre-commit-config.yaml` の作成
- Ruff（linting/formatting）
- pyright（型チェック）
- bandit（セキュリティ）
- pytest（テスト - pushフック）
- ファイルサイズチェック
- コミットメッセージ検証
- インストール手順の文書化
- チーム向けセットアップガイドの作成

**期待効果:**
- 問題の早期発見（Shift Left）
- CI失敗の削減
- Pre-commitフックは段階的に導入可能（最初はformat/lintのみ等）

### タスク1.3.3: CI設定の改善
**ステータス:** ✅ **完了**

**目的:** 品質チェックの厳格化

**計画:**
- `continue-on-error: true` の削除または見直し
  - mypy（line 59）→ pyrightに変更
  - bandit（line 131）
  - safety（line 141）
- 失敗時の適切なエラーハンドリング
- PR専用のワークフロー作成検討

### タスク1.3.4: ブランチ保護ルールの設定
**ステータス:** ⏳ **保留中**（優先度：中）

**目的:** mainブランチの品質保証

**計画:**
- mainブランチへの直接push禁止
- PR必須化
- ステータスチェック（lint, test）必須化
- レビュー承認必須化
- developブランチの保護（オプション）

**必要な権限:**
- リポジトリ管理者権限

### タスク1.3.5: CONTRIBUTING.md作成
**ステータス:** ⏳ **保留中**（優先度：中）

**目的:** 開発フローの標準化

**計画:**
- ブランチ戦略（feature → develop → main）
- コミットメッセージ規約
- PR作成ガイドライン
- コードレビュープロセス
- 環境セットアップ手順
- テスト実行方法
- トラブルシューティング

### タスク1.3.6: README.md更新
**ステータス:** ⏳ **保留中**（優先度：低）

**目的:** プロジェクト情報の充実

**計画:**
- 開発フローの概要追加
- Pre-commitフック使用方法
- CI/CDパイプラインの説明
- 品質管理プロセスの説明

---

## フェーズ1.4: パフォーマンス最適化（計画中）

### タスク1.4.1: Self-hosted Runner導入
**ステータス:** ⏳ **保留中**

**目的:** CI/CD実行の高速化とコスト削減

**計画:**
- ローカルランナーのセットアップ
- runner/ディレクトリの活用
- セキュリティ設定

### タスク1.4.2: キャッシュ戦略の最適化
**ステータス:** ⏳ **保留中**

**目的:** ビルド時間の短縮

**計画:**
- uvキャッシュの最適化
- Dockerレイヤーキャッシュ
- GitHub Actionsキャッシュの改善

### タスク1.4.3: Dockerイメージサイズ最適化
**ステータス:** ⏳ **保留中**

**現状:** 約1.2GB

**計画:**
- マルチステージビルドの検討
- 不要パッケージの削除
- Alpine Linuxベースイメージの検討

---

## 進捗状況サマリー

### 完了済みタスク
- ✅ Docker環境構築
- ✅ Rust製ツール導入
- ✅ プロジェクト構造確立
- ✅ GitHub Actions基本設定
- ✅ GHCR権限問題解決
- ✅ ドキュメント整備（README、technical_considerations、C4図）
- ✅ .claudeディレクトリ整備

### 進行中/保留中タスク
- ❌ Docker CIワークフロー分離（レジストリ名大文字問題の修正が必要）
- ⏳ ブランチ保護ルール設定
- ⏳ CONTRIBUTING.md作成
- ⏳ Self-hosted Runner導入
- ⏳ キャッシュ戦略最適化
- ⏳ Dockerイメージサイズ最適化

### 達成指標
- **基盤構築**: 100% 完了
- **CI/CDパイプライン**: 80% 完了（品質ゲート改善が必要）
- **ドキュメント**: 85% 完了（CONTRIBUTING.md が未作成）
- **品質管理**: 40% 完了（Pre-commit、ブランチ保護が未実装）
- **パフォーマンス**: 0% 完了（計画段階）

## 次のステップ

### 優先度：緊急
1. Docker CIワークフローの修正（レジストリ名の小文字化）

### 優先度：高
2. ブランチ保護ルールの設定

### 優先度：中
4. CONTRIBUTING.md作成
5. Self-hosted Runner導入検討

### 優先度：低
6. キャッシュ戦略最適化
7. Dockerイメージサイズ最適化

## リスクと課題

### 技術的リスク
- Python 3.13の互換性問題（一部パッケージ）
- GitHub Actions無料枠の制限

### 組織的課題
- ブランチ保護には管理者権限が必要
- チーム全体での開発フロー合意が必要

### 緩和策
- 互換性問題は個別に対処し、technical_considerations.mdに記録
- CI/CDリソースはSelf-hosted Runnerで対応予定
- 段階的な導入により、チームの適応を促進

---

## 成功指標

フェーズ1の完了は以下で評価されます：

- **開発効率**: DevContainerで5分以内に開発開始可能
- **ビルド速度**: CI/CDパイプラインが5分以内に完了
- **コード品質**: リントエラー0、テストカバレッジ80%以上
- **ドキュメント**: 新規開発者が30分以内に環境構築可能
- **再現性**: 3つのOS（Windows/macOS/Linux）で同一動作

現在、基盤構築は完了し、品質管理強化フェーズに移行中です。残りのタスクを完了することで、プロフェッショナルなPython開発環境が確立されます。
