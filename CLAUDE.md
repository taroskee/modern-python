# Modern Python

このファイルは、Claude Code（claude.ai/code）がこのリポジトリ内のコードを扱う際のガイドラインを提供します。

## 新しいセッションのクイックスタート

**作業を始める前に、以下のファイルをこの順番で読んでください：**

1. **`README.md`** - プロジェクト概要と基本的な使い方
2. **`technical_considerations.md`** - 学んだ教訓と技術的決定事項
3. **`c4-architecture.md`** - システムアーキテクチャと設計判断
4. **`pair_programming.md`** - 開発ワークフローとベストプラクティス
5. **`project_plan_phase_1.md`** - 現在の進捗状況と次のタスク

**CI/CD品質管理の作業を行う場合は、以下も読んでください：**
6. **`TODO.md`** - 未完了タスクの詳細リスト

**ワークフローに関する重要な注意事項：**
- タスクの進行状況を追跡するために常にTodoWriteツールを使用すること
- `make test` でテストを実行してから変更をコミット
- `make lint` と `make format` でコード品質を保証
- 各タスクの完了後には、学んだことを `technical_considerations.md` に追記すること

## 概要

Modern Python開発環境は、Docker と VSCode DevContainer を使用した、OS非依存で高速な Python 開発環境です。Rust製ツール（uv, Ruff）により圧倒的な実行速度を実現し、TDD実践とCI/CDパイプラインによる継続的な品質管理を提供します。

## 開発コマンド

### 基本的な開発コマンド
- `make test` - pytestでテストを実行
- `make lint` - Ruffでコードをチェック
- `make format` - Ruffでコードをフォーマット
- `make type` - Pyrightで型チェック
- `make all` - すべての品質チェックを実行

### パッケージ管理

#### 3つのライブラリ管理方法
1. **pyproject.toml** - プロジェクトのコア依存関係
2. **requirements-common.txt** - チーム共通ライブラリ（Gitで管理）
3. **requirements-dev.txt** - 個人用ライブラリ（.gitignoreで除外）

#### 基本コマンド
- `uv sync` - pyproject.tomlの依存関係を同期
- `uv pip install -r requirements-common.txt` - チーム共通ライブラリをインストール
- `uv pip install -r requirements-dev.txt` - 個人用ライブラリをインストール
- `uv pip install [package]` - 単一パッケージをインストール
- `uv venv` - 仮想環境を作成
- `source .venv/bin/activate` - 仮想環境を有効化

#### 自動インストール
- DevContainer起動時に `scripts/setup.sh` が自動実行
- すべてのライブラリ（pyproject.toml、requirements-common.txt、requirements-dev.txt）が自動インストール

#### 個人用ライブラリの追加方法
```bash
# テンプレートからコピー（初回のみ）
cp requirements-dev.txt.example requirements-dev.txt

# ライブラリを追加
echo "jupyter>=1.0.0" >> requirements-dev.txt

# インストール
uv pip install -r requirements-dev.txt
```

### Docker開発
- `docker build -f .devcontainer/Dockerfile .` - Dockerイメージをビルド
- VSCode: "Dev Containers: Reopen in Container" - DevContainerで開発開始

### CI/CD関連
- `gh run list` - 最近のCI実行を確認
- `gh run view [RUN_ID]` - 特定の実行の詳細を確認
- `make ci-status` - CI状況を確認（Makefileに定義されている場合）


## 開発のベストプラクティス

### コード品質

- **Ruffを使用**: `make lint` と `make format` で一貫したコードスタイル
- **型ヒントを活用**: Python 3.13の型機能を最大限に活用
- **テストファースト**: 機能実装前にテストを書く（TDD）
- **小さなコミット**: 機能単位で頻繁にコミット

### 問題解決アプローチ

1. **最小限の変更で検証**: 一度に複数の変更を加えない
2. **ローカルテスト**: `make all` でCI前に問題を発見
3. **ドキュメント化**: `technical_considerations.md` に学びを記録
4. **段階的解決**: 複雑な問題も一つずつ解決

### よくある落とし穴と対策

- **Docker権限エラー**: USER切り替え前にroot権限でシステムパッケージをインストール
- **Python 3.13互換性**: 一部のパッケージが非互換の可能性あり
- **CIリソース消費**: マトリックステストは最小限に
- **大容量ファイル**: コミット前にファイルサイズを確認

詳細は `technical_considerations.md` を参照してください。

詳細なプロジェクト状況は `project_plan_phase_1.md` を参照してください。

## 重要な注意事項

### 必ず守るべきルール

1. **テスト実行**: `make test` を必ず実行してからコミット
2. **コード品質**: `make lint` でエラーがないことを確認
3. **ドキュメント更新**: 重要な変更は `technical_considerations.md` に記録
4. **TodoWrite使用**: タスク管理には必ずTodoWriteツールを使用

### エラー調査方法

```bash
# CI失敗時の調査
gh run list --limit 5
gh run view [RUN_ID]
gh run view [RUN_ID] --log-failed

# ローカルでの検証
make all
docker build -f .devcontainer/Dockerfile .
```

## コミットメッセージ規約

[Conventional Commits](https://www.conventionalcommits.org/)に従います：

- `feat:` 新機能
- `fix:` バグ修正
- `docs:` ドキュメントのみの変更
- `style:` コードフォーマット
- `refactor:` リファクタリング
- `test:` テストの追加・修正
- `chore:` ビルドプロセスやツールの変更
- `ci:` CI/CD設定の変更

## まとめ

このプロジェクトは「動くコード」から「持続可能なシステム」への進化を目指しています。シンプルさを保ちながら、早期の検証、適切なドキュメント化、自動化を通じて、堅牢で保守しやすい開発環境を構築していきます。
