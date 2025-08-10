# Modern Python Development Environment

モダンPythonフレームワークとGitHubセルフホストランナーをDockerで構築する開発環境

## 🚀 特徴

- **OS非依存**: Docker ContainerによりWindows/macOS/Linuxで統一された開発体験
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

## 🏗️ アーキテクチャ

詳細は[C4アーキテクチャ図](c4-architecture.md)を参照してください。

## 📦 インストール

### 前提条件
- Docker Desktop (Windows/macOS) または Docker Engine (Linux)
- Visual Studio Code
- VSCode拡張機能: Dev Containers

### セットアップ手順

```bash
# 1. リポジトリをクローン
git clone https://github.com/your-org/modern-python.git
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

### 開発フロー

1. **機能ブランチを作成**
   ```bash
   git checkout -b feature/your-feature
   ```

2. **TDDサイクルで開発**
   - RED: 失敗するテストを書く
   - GREEN: テストを通す最小限の実装
   - REFACTOR: コードを改善

3. **品質チェック**
   ```bash
   make all
   ```

4. **コミット**
   ```bash
   git add .
   git commit -m "feat: your feature description"
   ```

5. **プルリクエスト作成**
   - GitHub ActionsでCI/CDが自動実行

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
pytest tests/test_calculator.py -v

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

問題が発生した場合は、[Issues](https://github.com/your-org/modern-python/issues)で報告してください。

---

Built with ❤️ using Modern Python Stack