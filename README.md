# Modern Python Development Environment

[![Documentation](https://img.shields.io/badge/Docs-GitHub%20Pages-brightgreen.svg)](https://taroskee.github.io/modern-python/)
[![Python 3.13](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org)
[![Code style: Ruff](https://img.shields.io/badge/Code%20Style-Ruff-black.svg)](https://github.com/astral-sh/ruff)

モダンPythonフレームワークとGitHubセルフホストランナーをDockerで構築する開発環境

## 📚 ドキュメント

- 📖 **[オンラインドキュメント](https://taroskee.github.io/modern-python/)** - 最新のAPIドキュメントとガイド
- 🏗️ **[アーキテクチャ](c4-architecture.md)** - システム設計と技術選定
- 🔧 **[技術的考察](technical_considerations.md)** - 実装の詳細と解決策

## 🚀 特徴

- **高速実行**: Rust製ツール（uv, Ruff）による圧倒的な実行速度
- **即座の開発開始**: VSCode DevContainerで環境構築不要
- **品質保証**: TDD実践とCI/CDパイプラインによる継続的な品質管理

## 📋 技術スタック

### Core
- **Python 3.13**: 最新の言語機能とパフォーマンス
- **Docker + DevContainer**: 再現可能な開発環境
- **VSCode**: 統合開発環境

### Development Tools
- **uv**: Rust製の超高速パッケージマネージャー
- **Ruff**: Rust製の高速リンター/フォーマッター
- **pytest**: Pythonのデファクトスタンダードテストフレームワーク
- **Pyright**: Microsoftの高速型チェッカー（Pylance基盤）
- **Sphinx**: 公式ドキュメント生成ツール

### CI/CD
- **GitHub Actions**: 自動化されたワークフロー
- **Self-hosted Runner**: ローカル実行による高速ビルド

## 📦 インストール

### 前提条件
- Docker Desktop (Windows/macOS) または Docker Engine (Linux)
- Visual Studio Code
- VSCode拡張機能: Dev Containers

### セットアップ手順

```bash
# 1. リポジトリをクローン
git clone https://github.com/taroskee/modern-python.git
cd modern-python

# 2. VSCodeで開く
code .

# 3. コマンドパレット（Cmd/Ctrl+Shift+P）から
# "Dev Containers: Reopen in Container" を選択

# 4. コンテナが起動したら開発開始！
```

### Pre-commitフックの設定（推奨）

```bash
# pre-commitをインストール
pip install pre-commit

# フックをインストール
pre-commit install

# 手動で全ファイルをチェック（初回のみ）
pre-commit run --all-files
```

Pre-commitフックにより、コミット時に自動的に以下がチェックされます：
- コードフォーマット (Ruff)
- リント (Ruff)
- 型チェック (Pyright)
- セキュリティチェック (Bandit)
- シークレット検出
- その他の品質チェック

## 🎯 使い方

### 基本コマンド

```bash
# 依存関係のインストール
uv sync

# テスト実行
make test

# リント実行
make lint

# フォーマット実行
make format

# ドキュメント生成
make docs

# 全チェック実行
make all
```

### ライブラリ管理

このプロジェクトでは、3つの方法でPythonライブラリを管理できます：

#### 1. プロジェクト依存関係（pyproject.toml）
プロジェクトのコア機能に必要なライブラリは `pyproject.toml` で管理されています。

#### 2. チーム共通ライブラリ（requirements-common.txt）
チーム全体で使用する共通ライブラリ：

```bash
# チーム共通ライブラリの確認
cat requirements-common.txt

# 新しいライブラリを追加（チーム全体に影響）
echo "新しいライブラリ>=バージョン" >> requirements-common.txt
git add requirements-common.txt
git commit -m "feat: add 新しいライブラリ to common requirements"
```

#### 3. 個人用ライブラリ（requirements-dev.txt）
個人の開発環境に必要なライブラリ：

```bash
# テンプレートから個人用ファイルを作成
cp requirements-dev.txt.example requirements-dev.txt

# 個人用ライブラリを追加
echo "jupyter>=1.0.0" >> requirements-dev.txt

# インストール（DevContainer起動時に自動実行）
uv pip install -r requirements-dev.txt
```

**注意**: `requirements-dev.txt` は `.gitignore` に含まれているため、個人の設定はGitに保存されません。

#### 自動インストール
DevContainer起動時またはセットアップスクリプト実行時に、すべてのライブラリが自動的にインストールされます：

```bash
# 手動でセットアップスクリプトを実行
bash scripts/setup.sh
```

### 開発フロー

**注意**: mainブランチは保護されており、直接pushはできません。必ずPR経由で変更を行ってください。

1. **最新のmainを取得**
   ```bash
   git checkout main
   git pull --rebase origin main
   ```

2. **機能ブランチを作成**
   ```bash
   git checkout -b feature/your-feature
   ```

3. **TDDサイクルで開発**
   - RED: 失敗するテストを書く
   - GREEN: テストを通す最小限の実装
   - REFACTOR: コードを改善

4. **品質チェック**
   ```bash
   make all
   ```

5. **コミット**
   ```bash
   git add .
   git commit -m "feat: your feature description"
   ```

6. **mainの最新を取り込み（リベース）**
   ```bash
   git fetch origin main
   git rebase origin/main
   ```

7. **プルリクエスト作成**
   - featureブランチをpush
   - GitHub UIでPRを作成
   - 全てのステータスチェック（CI）が成功するまで待つ
   - マージ（リニアヒストリーを保つため、Squash and mergeまたはRebase and mergeを使用）

## 📁 プロジェクト構造

```
modern-python/
├── .devcontainer/      # DevContainer設定
├── .github/            # GitHub Actions設定
├── .vscode/            # VSCode設定
├── docs/               # ドキュメント
├── runner/             # Self-hosted Runner設定
├── scripts/            # ユーティリティスクリプト
├── src/                # ソースコード
├── tests/              # テストコード
├── pyproject.toml      # Pythonプロジェクト定義
├── ruff.toml           # Ruff設定
└── Makefile            # タスク自動化
```

## 🧪 テスト

```bash
# 全テスト実行
pytest

# カバレッジ付きテスト
pytest --cov=src --cov-report=html

# 特定のテストのみ実行
pytest tests/test_example_calculator.py -v

# マーカー付きテスト実行
pytest -m "not slow"
```

## 📚 ドキュメント

```bash
# ドキュメント生成
make docs

# ローカルでドキュメントを確認
python -m http.server --directory docs/_build/html 8000
# ブラウザで http://localhost:8000 を開く
```

## 🔧 設定

### 環境変数
`.env.example`をコピーして`.env`を作成し、必要な環境変数を設定：

```bash
cp .env.example .env
```

### VSCode設定
`.vscode/settings.json`でプロジェクト固有の設定を管理

### Python設定
`pyproject.toml`でプロジェクトの依存関係とメタデータを管理

## 🤝 コントリビューション

1. このリポジトリをフォーク
2. フィーチャーブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'feat: add amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

### コミットメッセージ規約

[Conventional Commits](https://www.conventionalcommits.org/)に従います：

- `feat:` 新機能
- `fix:` バグ修正
- `docs:` ドキュメントのみの変更
- `style:` コードの意味に影響しない変更
- `refactor:` バグ修正や機能追加を含まないコード変更
- `test:` テストの追加や修正
- `chore:` ビルドプロセスやツールの変更

## 📈 パフォーマンス指標

| 操作 | 目標時間 | 実測時間 |
|-----|---------|---------|
| 環境起動 | < 30秒 | - |
| 依存関係インストール | < 10秒 | - |
| リント実行（1000行） | < 0.5秒 | - |
| テスト実行（100件） | < 3秒 | - |
| CI/CD完了 | < 5分 | - |

## 📄 ライセンス

MITライセンス - 詳細は[LICENSE](LICENSE)を参照してください。

## 🙏 謝辞

このプロジェクトは以下の素晴らしいツールを使用しています：

- [Python](https://www.python.org/)
- [uv](https://github.com/astral-sh/uv)
- [Ruff](https://github.com/astral-sh/ruff)
- [pytest](https://pytest.org/)
- [Docker](https://www.docker.com/)
- [Visual Studio Code](https://code.visualstudio.com/)

## 📞 サポート

問題が発生した場合は、[Issues](https://github.com/taroskee/modern-python/issues)で報告してください。

---

Built with ❤️ using Modern Python Stack
