# Modern Python開発環境 構築計画

## 🎯 プロジェクト概要
**目的**: OS非依存のモダンPython開発環境をDocker + VSCode DevContainerで構築し、Rust製ツールによる高速CI/CDを実現する

**対象**: 個人〜10人規模の開発チーム

**技術スタック**:
- Python 3.13
- uv (Rust製パッケージマネージャー)
- Ruff (Rust製リンター/フォーマッター)
- pytest (テストフレームワーク)
- ty (型チェッカー)
- Sphinx (ドキュメント生成)
- Docker + VSCode DevContainer
- GitHub Self-hosted Runner

## 📅 実装スケジュール

### Phase 1: 基盤構築（Day 1-2） ✅ **完了**
**目標**: Docker環境とVSCode DevContainerの基本設定

#### タスクリスト
- [x] 開発計画書作成
- [x] 基本ファイル作成（README, .gitignore, LICENSE）
- [x] .devcontainerディレクトリ構築
  - [x] devcontainer.json
  - [x] Dockerfile
  - [x] docker-compose.yml
- [x] .vscodeディレクトリ構築
  - [x] settings.json
  - [x] extensions.json
  - [x] tasks.json
- [x] 環境変数設定（.env.example）

**完了日**: 2025-08-09

### Phase 2: Python環境構築（Day 3-4） 🔶 **一部完了**
**目標**: Python 3.13 + uvによる高速パッケージ管理環境

#### タスクリスト
- [x] Python基本設定
  - [x] pyproject.toml（Ruff設定統合済み）
  - [ ] .python-version
- [x] 開発ツール設定
  - [x] ruff設定（pyproject.toml内に統合）
  - [x] pytest.ini（テスト設定）
  - [ ] ty設定
- [ ] ドキュメント設定
  - [ ] docs/conf.py（Sphinx設定）
  - [ ] docs/Makefile

### Phase 3: CI/CDパイプライン（Day 5-6）
**目標**: GitHub ActionsとSelf-hosted Runnerの設定

#### タスクリスト
- [ ] GitHub Actions設定
  - [ ] .github/workflows/ci.yml
  - [ ] .github/workflows/cd.yml
  - [ ] .github/workflows/docs.yml
- [ ] Self-hosted Runner設定
  - [ ] runner/Dockerfile
  - [ ] runner/docker-compose.yml
  - [ ] runner/config.sh

### Phase 4: サンプルアプリケーション（Day 7）
**目標**: TDD実践のためのサンプル実装

#### タスクリスト
- [ ] サンプル実装
  - [ ] src/__init__.py
  - [ ] src/calculator.py
- [ ] テストコード
  - [ ] tests/__init__.py
  - [ ] tests/test_calculator.py
- [ ] APIドキュメント
  - [ ] docs/api.rst
  - [ ] docs/index.rst

### Phase 5: 自動化と最適化（Day 8）
**目標**: 開発効率化のための自動化設定

#### タスクリスト
- [ ] 自動化スクリプト
  - [ ] scripts/setup.sh
  - [ ] scripts/test.sh
  - [ ] scripts/build.sh
  - [ ] scripts/lint.sh
- [ ] Makefile作成
- [ ] pre-commitフック設定
- [ ] CLAUDE.mdローカル設定

## 📁 最終的なディレクトリ構造

```
modern-python/
├── .devcontainer/
│   ├── devcontainer.json      # VSCode DevContainer設定
│   ├── Dockerfile              # 開発環境用Dockerイメージ
│   └── docker-compose.yml      # マルチコンテナ構成
├── .github/
│   └── workflows/
│       ├── ci.yml              # 継続的インテグレーション
│       ├── cd.yml              # 継続的デプロイメント
│       └── docs.yml            # ドキュメント自動生成
├── .vscode/
│   ├── settings.json           # VSCode設定
│   ├── extensions.json         # 推奨拡張機能
│   └── tasks.json              # タスク定義
├── docs/
│   ├── conf.py                 # Sphinx設定
│   ├── index.rst               # ドキュメントトップ
│   ├── api.rst                 # API仕様書
│   └── Makefile                # ドキュメントビルド
├── runner/
│   ├── Dockerfile              # Self-hosted Runner用イメージ
│   ├── docker-compose.yml      # Runner構成
│   └── config.sh               # Runner設定スクリプト
├── scripts/
│   ├── setup.sh                # 初期セットアップ
│   ├── test.sh                 # テスト実行
│   ├── build.sh                # ビルド処理
│   └── lint.sh                 # リント実行
├── src/
│   ├── __init__.py             # パッケージ初期化
│   └── calculator.py           # サンプル実装
├── tests/
│   ├── __init__.py             # テストパッケージ初期化
│   └── test_calculator.py      # テストコード
├── .env.example                # 環境変数テンプレート
├── .gitignore                  # Git除外設定
├── .pre-commit-config.yaml     # pre-commitフック設定
├── .python-version             # Pythonバージョン指定
├── CLAUDE.md                   # Claude Code設定
├── LICENSE                     # ライセンスファイル
├── Makefile                    # タスク自動化
├── README.md                   # プロジェクト説明
├── c4-architecture.md          # C4アーキテクチャ図
├── development-plan.md         # 本開発計画書
├── pyproject.toml              # Pythonプロジェクト定義
├── pytest.ini                  # pytest設定
├── ruff.toml                   # Ruff設定
└── uv.lock                     # 依存関係ロック
```

## 🎯 成功指標とKPI

### 開発環境
- ✅ **起動時間**: `devcontainer open`で30秒以内に開発開始可能
- ✅ **依存関係**: `uv sync`で10秒以内にインストール完了
- ✅ **互換性**: Windows/macOS/Linuxで同一の動作

### パフォーマンス
- ✅ **リント**: `ruff check`が0.5秒以内に完了
- ✅ **テスト**: `pytest`が3秒以内に完了（100テストケース想定）
- ✅ **ビルド**: CI/CDが5分以内に完了

### 品質
- ✅ **テストカバレッジ**: 80%以上
- ✅ **型チェック**: 100%の型ヒント適用
- ✅ **ドキュメント**: 全公開APIにdocstring

## 🚀 クイックスタート（完成後）

```bash
# 1. リポジトリをクローン
git clone https://github.com/your-org/modern-python.git
cd modern-python

# 2. VSCode DevContainerで開く
code .
# VSCodeで "Reopen in Container" を選択

# 3. 依存関係インストール（コンテナ内で自動実行）
uv sync

# 4. テスト実行
make test

# 5. 開発開始！
```

## 📝 進捗管理

### 現在の進捗状況
- **Phase 1**: ✅ 完了（2025-08-09）
  - 全基本ファイル作成完了
  - Docker/DevContainer設定完了
  - VSCode統合設定完了
- **Phase 2**: 🔶 進行中（50%完了）
  - pyproject.toml作成（Ruff設定統合）
  - pytest.ini更新
- **Phase 3-5**: ⏳ 未着手

### 完了したファイル
✅ development-plan.md
✅ README.md
✅ .gitignore
✅ LICENSE
✅ .env.example
✅ .devcontainer/devcontainer.json
✅ .devcontainer/Dockerfile
✅ .devcontainer/docker-compose.yml
✅ .vscode/settings.json
✅ .vscode/extensions.json
✅ .vscode/tasks.json
✅ pyproject.toml
✅ pytest.ini（更新）
✅ c4-architecture.md

各フェーズの完了時に以下を確認：
1. 全タスクがチェック済み
2. テストが全てパス
3. ドキュメントが更新済み
4. git commitが完了

## 🔄 継続的改善

月次でのレビューと改善：
- パフォーマンスメトリクスの測定
- 開発者フィードバックの収集
- ツールのアップデート確認
- セキュリティ脆弱性のチェック