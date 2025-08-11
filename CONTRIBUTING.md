# Contributing to Modern Python Development Environment

このプロジェクトへの貢献を歓迎します！このガイドは、効率的かつ品質の高い貢献を行うための手順を説明します。

## 📋 目次

- [貢献の種類](#貢献の種類)
- [開発環境のセットアップ](#開発環境のセットアップ)
- [開発ワークフロー](#開発ワークフロー)
- [コーディング規約](#コーディング規約)
- [テスト](#テスト)
- [プルリクエスト](#プルリクエスト)
- [問題の報告](#問題の報告)
- [コミュニティガイドライン](#コミュニティガイドライン)

## 貢献の種類

以下のような貢献を歓迎します：

- 🐛 **バグ報告**: 問題を発見したらIssueで報告してください
- 💡 **機能提案**: 新機能のアイデアを共有してください
- 📝 **ドキュメント改善**: typoの修正から構造の改善まで
- 🔧 **コード貢献**: バグ修正、新機能、リファクタリング
- 🧪 **テスト追加**: テストカバレッジの向上
- 🌐 **翻訳**: ドキュメントの多言語化

## 開発環境のセットアップ

### 前提条件

- Docker Desktop (Windows/macOS) または Docker Engine (Linux)
- Visual Studio Code
- Git
- GitHub CLI (`gh`)

### 環境構築手順

```bash
# 1. リポジトリをフォーク
# GitHubのUIから「Fork」ボタンをクリック

# 2. フォークしたリポジトリをクローン
git clone https://github.com/taroskee/modern-python.git
cd modern-python

# 3. upstreamリモートを追加
git remote add upstream https://github.com/taroskee/modern-python.git

# 4. VSCodeで開く
code .

# 5. DevContainerで開発開始
# コマンドパレット（Cmd/Ctrl+Shift+P）から
# "Dev Containers: Reopen in Container" を選択

# 6. Pre-commitフックをインストール（推奨）
make pre-commit
```

### 依存関係のインストール

DevContainer起動時に自動的にインストールされますが、手動でインストールする場合：

```bash
# すべての依存関係をインストール
make setup

# または個別にインストール
uv sync                                    # pyproject.tomlから
uv pip install -r requirements-common.txt # チーム共通ライブラリ
cp requirements-dev.txt.example requirements-dev.txt
uv pip install -r requirements-dev.txt    # 個人用ライブラリ
```

## 開発ワークフロー

### ブランチ戦略

mainブランチは保護されており、直接のpushはできません。すべての変更はプルリクエスト経由で行います。

```bash
# 1. mainブランチを最新に更新
git checkout main
git pull upstream main

# 2. 機能ブランチを作成
git checkout -b feature/your-feature-name
# または
git checkout -b fix/bug-description

# 3. 変更を実装（TDDサイクルを使用）

# 4. コミット
git add .
git commit -m "feat: add awesome feature"

# 5. フォークにプッシュ
git push origin feature/your-feature-name
```

### TDD（テスト駆動開発）サイクル

#### 1. RED フェーズ - 失敗するテストを書く

```python
# tests/test_feature.py
def test_new_feature():
    result = new_feature()
    assert result == expected_value
```

```bash
# テストが失敗することを確認
make test
```

#### 2. GREEN フェーズ - テストを通す最小限の実装

```python
# src/feature.py
def new_feature():
    return expected_value
```

```bash
# テストが成功することを確認
make test
```

#### 3. REFACTOR フェーズ - コードを改善

```bash
# コードの品質を改善
make format  # コードフォーマット
make lint    # リントチェック
make type    # 型チェック
```

### 品質チェック

コミット前に必ず実行：

```bash
# すべての品質チェックを実行
make all

# 個別に実行
make test         # テスト実行
make lint         # Ruffでリント
make format       # コードフォーマット
make type         # Pyrightで型チェック
make security     # セキュリティチェック
```

## コーディング規約

### Pythonコードスタイル

[Ruff](https://github.com/astral-sh/ruff)の設定（`pyproject.toml`）に従います：

- 行長: 88文字
- インデント: スペース4つ
- 引用符: ダブルクォート
- Python 3.13の機能を活用

### 型ヒント

すべての公開関数・メソッドに型ヒントを付ける：

```python
from typing import Optional

def calculate_sum(numbers: list[int], initial: int = 0) -> int:
    """
    数値のリストの合計を計算する。

    Args:
        numbers: 合計する数値のリスト
        initial: 初期値（デフォルト: 0）

    Returns:
        計算された合計値
    """
    return sum(numbers, initial)
```

### docstring

Google styleのdocstringを使用：

```python
def function_name(param1: str, param2: int) -> bool:
    """
    関数の簡潔な説明。

    詳細な説明（必要に応じて）。

    Args:
        param1: パラメータ1の説明
        param2: パラメータ2の説明

    Returns:
        戻り値の説明

    Raises:
        ValueError: エラー条件の説明

    Examples:
        >>> function_name("test", 42)
        True
    """
    pass
```

### コミットメッセージ

[Conventional Commits](https://www.conventionalcommits.org/)規約に従う：

```bash
# 形式
<type>(<scope>): <subject>

<body>

<footer>
```

**タイプ**:
- `feat`: 新機能
- `fix`: バグ修正
- `docs`: ドキュメントのみの変更
- `style`: コードフォーマット（セミコロン不足など）
- `refactor`: リファクタリング
- `test`: テストの追加・修正
- `chore`: ビルドプロセスやツールの変更
- `ci`: CI/CD設定の変更

**例**:
```bash
feat: add user authentication system

Implement JWT-based authentication with refresh tokens.
Includes login, logout, and token refresh endpoints.

Closes #123
```

## テスト

### テスト要件

- すべての新機能にテストを追加
- テストカバレッジ80%以上を維持
- 既存のテストを壊さない

### テストの実行

```bash
# すべてのテストを実行
make test

# カバレッジ付きで実行
make test-coverage

# 特定のテストのみ実行
pytest tests/test_specific.py -v

# マーカー付きテスト
pytest -m "not slow"
```

### テストの書き方

```python
import pytest
from src.module import function_to_test

class TestFeature:
    """機能のテストクラス"""

    def test_normal_case(self):
        """正常系のテスト"""
        result = function_to_test("input")
        assert result == "expected"

    def test_edge_case(self):
        """エッジケースのテスト"""
        with pytest.raises(ValueError):
            function_to_test(None)

    @pytest.mark.slow
    def test_performance(self):
        """パフォーマンステスト"""
        # 時間のかかるテスト
        pass
```

## プルリクエスト

### PRを作成する前に

1. **最新のmainを取り込む**:
   ```bash
   git fetch upstream main
   git rebase upstream/main
   ```

2. **ローカルで品質チェック**:
   ```bash
   make all
   ```

3. **ドキュメントを更新**:
   - 新機能の場合はREADME.mdを更新
   - 技術的な決定事項は`technical_considerations.md`に記録
   - APIの変更は`docs/`内のドキュメントを更新

### PRの作成

1. GitHubでPRを作成
2. PRテンプレートに従って記入：

```markdown
## 概要
変更内容の簡潔な説明

## 変更の種類
- [ ] バグ修正
- [ ] 新機能
- [ ] 破壊的変更
- [ ] ドキュメント更新

## 関連Issue
Closes #(issue番号)

## 変更内容
- 変更点1
- 変更点2

## テスト
- [ ] ユニットテストを追加/更新
- [ ] すべてのテストがパス
- [ ] カバレッジ80%以上を維持

## チェックリスト
- [ ] コードがプロジェクトのスタイルガイドに従っている
- [ ] セルフレビューを実施
- [ ] コメントを追加（特に複雑な箇所）
- [ ] ドキュメントを更新
- [ ] 破壊的変更がない（ある場合は説明を追加）
```

### CIチェック

PRを作成すると自動的に以下のチェックが実行されます：

- **Lint Code**: コードスタイルチェック
- **Test Python**: テスト実行
- **Security Scan**: セキュリティチェック
- **Build Distribution**: パッケージビルド
- **Test Documentation**: ドキュメントビルド

すべてのチェックが成功するまでマージできません。

### レビュープロセス

1. 自動CIチェックがすべて成功
2. コードレビューを受ける
3. フィードバックに対応
4. 承認後、メンテナーがマージ

## 問題の報告

### バグ報告

[Issue](https://github.com/taroskee/modern-python/issues)を作成し、以下を含めてください：

1. **環境情報**:
   - OS (Windows/macOS/Linux)
   - Pythonバージョン
   - 関連パッケージのバージョン

2. **再現手順**:
   - 問題を再現する最小限のコード
   - 実行したコマンド
   - 期待した結果
   - 実際の結果

3. **エラーログ**:
   ```
   完全なトレースバック
   ```

### 機能リクエスト

新機能の提案は大歓迎です！以下を含めてください：

1. **ユースケース**: なぜこの機能が必要か
2. **提案する解決策**: どのように実装するか
3. **代替案**: 検討した他の方法
4. **追加コンテキスト**: スクリーンショットや参考リンク

## コミュニティガイドライン

### 行動規範

- 建設的で敬意のあるコミュニケーション
- 多様性を尊重し、包括的な環境を維持
- フィードバックは具体的かつ建設的に
- 他者の時間と努力を尊重

### サポート

質問やサポートが必要な場合：

1. まず[ドキュメント](https://taroskee.github.io/modern-python/)を確認
2. 既存の[Issue](https://github.com/taroskee/modern-python/issues)を検索
3. それでも解決しない場合は新しいIssueを作成

### 貢献者の認識

すべての貢献者に感謝します！貢献者はREADME.mdのContributorsセクションに記載されます。

## よくある質問

### Q: 小さな変更（typo修正など）でもPRが必要ですか？
A: はい、すべての変更はPR経由で行います。これにより変更履歴が明確になり、CIチェックが実行されます。

### Q: 複数の問題を1つのPRで修正してもよいですか？
A: 関連する変更であれば問題ありませんが、レビューしやすいように1つのPRは1つの目的に集中することを推奨します。

### Q: CIが失敗した場合はどうすればよいですか？
A: GitHub ActionsのログでエラーCUIの詳細を確認し、ローカルで`make all`を実行して問題を特定してください。

### Q: どのくらいでPRがマージされますか？
A: 通常2-3営業日以内にレビューされます。複雑な変更の場合はより時間がかかることがあります。

---

🙏 **Thank you for contributing to Modern Python Development Environment!**

あなたの貢献がこのプロジェクトをより良いものにします。
