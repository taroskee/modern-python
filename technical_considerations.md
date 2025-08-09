# 技術的考慮事項と決定事項

## 概要
このドキュメントは、Modern Python開発環境構築プロジェクトにおける技術的な決定事項、遭遇した問題、解決策、そして得られた教訓をまとめたものです。将来の開発や問題解決の参考資料として活用してください。

## CI/CDパイプライン最適化

### GitHub Actionsリソース消費問題
**問題**: マトリックステスト（3つのOS × 3つのPythonバージョン = 9ジョブ）により、GitHub Actionsの無料枠を急速に消費していた。

**解決策**:
- 日常的なCIは最小構成（Ubuntu + Python 3.13のみ）に変更
- フルマトリックステストは週次実行または手動トリガーに分離
- `.github/workflows/ci.yml`（軽量版）と`.github/workflows/ci-full.yml`（完全版）に分割

**教訓**:
```yaml
# ❌ 避けるべき：毎回のpushで実行
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest, macos-latest]
    python-version: ["3.11", "3.12", "3.13"]

# ✅ 推奨：必要最小限のテスト
runs-on: ubuntu-latest
env:
  PYTHON_VERSION: "3.13"
```

## Docker環境構築の落とし穴

### uvインストール方法の進化
**問題の変遷**:
1. 初期: `curl | sh`でインストール → シェル環境変数の問題で失敗
2. 第2段階: 環境変数設定とmv → exit code 2で失敗
3. 第3段階: cpコマンドに変更 → それでも不安定

**最終解決策**:
```dockerfile
# ✅ 最も確実な方法：公式イメージからバイナリをコピー
COPY --from=ghcr.io/astral-sh/uv:0.8.7 /uv /uvx /bin/

# ❌ 避けるべき方法
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
```

**重要なポイント**:
- バージョンを明示的に固定する（再現性確保）
- インストールスクリプトの実行を避ける（環境依存を排除）
- 公式提供のバイナリを信頼する

## パッケージ管理の教訓

### uv toolインストールのエントリーポイント問題
**問題**: `uv tool install jupyter`が「No executables are provided」エラーで失敗

**原因**: 
- `jupyter`パッケージ自体はメタパッケージで実行可能ファイルを含まない
- 実際の実行ファイルは`jupyter-core`や`jupyterlab`に存在

**解決策**:
```dockerfile
# ❌ 失敗する
RUN uv tool install jupyter

# ✅ 正しい方法
RUN uv tool install jupyterlab  # または jupyter-core
```

### typing-inspectionインストール失敗
**問題**: Dockerビルド中に`typing-inspection==0.4.1`のインストールが失敗

**考えられる原因**:
- Python 3.13との互換性問題
- 依存関係の競合
- パッケージレジストリの問題

**対処方針**:
- 必要最小限のパッケージのみインストール
- バージョン固定による安定性確保
- 開発ツールとランタイム依存の分離

## ファイル管理とGit

### 大容量ファイルの混入問題
**問題**: 446MBのVCDファイルが誤ってコミットされ、push失敗

**防止策**:
```bash
# コミット前の確認手順
git status --porcelain | awk '{print $2}' | xargs -I {} du -h {} | sort -rh | head -20

# .gitignoreに追加すべき項目
*.vcd        # 大容量バイナリファイル
test_app/    # 他プロジェクトのテストファイル
```

**リカバリー方法**:
```bash
git reset --soft HEAD~1  # コミット取り消し（変更は保持）
rm -rf 不要なディレクトリ
git add 必要なファイルのみ
git commit -m "正しいコミットメッセージ"
```

## トラブルシューティングガイド

### CI失敗時の調査フロー
1. **概要確認**
   ```bash
   gh run list --limit 5
   ```

2. **詳細確認**
   ```bash
   gh run view [RUN_ID]
   ```

3. **エラーログ検索**
   ```bash
   gh run view [RUN_ID] --log-failed
   gh run view [RUN_ID] --log | grep -A5 "ERROR:"
   ```

4. **アノテーション確認**
   - GitHub UIでアノテーションタブを確認
   - 具体的なファイル名と行番号を特定

### GitHub CLI活用法
```bash
# インストール（macOS）
brew install gh

# 認証
gh auth login

# Makefileに追加した便利コマンド
make ci-status     # 最近のCI実行状況
make ci-view       # 最新の詳細
make ci-watch      # 実行中のCIを監視
```

## ベストプラクティス

### 段階的問題解決アプローチ
1. **最小限の変更で検証**
   - 一度に複数の変更を加えない
   - 各変更後に必ずテスト

2. **ローカルでの事前検証**
   ```bash
   # Lintチェック
   ruff check .
   
   # テスト実行
   pytest tests/
   
   # Dockerビルドテスト
   docker build -f .devcontainer/Dockerfile .
   ```

3. **コミットメッセージの明確化**
   ```
   fix: Docker build - [具体的な変更内容]
   style: format code with Ruff
   ci: optimize GitHub Actions workflow
   ```

### 開発環境の分離
- **仮想環境の活用**
  ```bash
  uv venv
  source .venv/bin/activate
  ```

- **依存関係の明確化**
  - 本番: `dependencies`
  - 開発: `dev-dependencies`
  - テスト: `test-dependencies`

## 🚨 重要な注意点

### 必ず覚えておくべきこと
- **Docker内でのuvインストール**: 公式イメージからCOPY方式を使用
- **CIマトリックス**: コスト意識を持って最小限に
- **パッケージ選択**: エントリーポイントの有無を事前確認
- **コミット前確認**: ファイルサイズと不要ファイルのチェック
- **エラー調査**: GitHub CLIを活用した効率的なデバッグ

### よくある落とし穴
1. **サイレントエラー**: CIが緑でも実際には問題があることがある
2. **キャッシュ問題**: 古いキャッシュが原因の不可解なエラー
3. **バージョン非互換**: 最新版が常に最良とは限らない
4. **環境差異**: ローカルとCIの環境差による失敗

## 今後の改善点

### 検討事項
- [ ] Self-hosted Runnerの導入（コスト削減）
- [ ] キャッシュ戦略の最適化
- [ ] セキュリティスキャンの強化
- [ ] パフォーマンステストの自動化

### 技術的負債
- mypyのpydanticプラグイン設定エラー
- typing-inspectionパッケージの互換性問題
- Dockerイメージサイズの最適化余地

## まとめ

このプロジェクトを通じて、「動くコード」から「持続可能なシステム」への進化には、継続的な学習と改善が不可欠であることを学びました。特に以下の原則が重要です：

1. **シンプルさを保つ**: 複雑な構成は保守コストを増大させる
2. **早期の検証**: 問題は小さいうちに発見・修正する
3. **ドキュメント化**: 未来の自分や他の開発者への贈り物
4. **自動化**: 繰り返し作業は必ず自動化する

これらの教訓を活かし、より堅牢で保守しやすい開発環境を構築していきましょう。