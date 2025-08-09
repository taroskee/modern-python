# Modern Python開発環境 C4アーキテクチャ図

## System Context図（レベル1）
システムの全体的な位置づけと外部アクターとの関係

```mermaid
graph TB
    subgraph "System Context"
        style PythonDev fill:#1168bd,stroke:#0b4884,color:#ffffff
        
        Developer["👤 開発者<br/>【役割】<br/>・コード開発<br/>・テスト実行<br/>・ドキュメント作成"]
        GitHub["🌐 GitHub<br/>【外部システム】<br/>・ソースコード管理<br/>・CI/CD連携<br/>・Issue管理"]
        OnPremise["🏢 オンプレミスサーバー<br/>【運用環境】<br/>・本番環境<br/>・ステージング環境"]
        PythonDev["🐍 Modern Python開発システム<br/>【ソフトウェアシステム】<br/>・OS非依存の開発環境<br/>・高速CI/CD実行<br/>・統一された開発ツールチェーン"]
        
        Developer -->|"VSCode DevContainerで<br/>開発作業"| PythonDev
        PythonDev -->|"セルフホストランナーで<br/>CI/CD実行"| GitHub
        PythonDev -->|"コンテナイメージを<br/>デプロイ"| OnPremise
        GitHub -->|"Webhook通知"| PythonDev
    end
```

## Container図（レベル2）
システム内のコンテナ（実行単位）とその関係

```mermaid
graph TB
    subgraph "Python開発システム - Containers"
        style Docker fill:#2e7eea,stroke:#1168bd,color:#ffffff
        style VSCode fill:#007acc,stroke:#005a9e,color:#ffffff
        
        VSCode["📝 VSCode DevContainer<br/>【IDE統合】<br/>・開発環境UI<br/>・拡張機能管理<br/>・デバッグ機能"]
        Docker["🐳 Docker環境<br/>【コンテナ基盤】<br/>・Linux/Windows/macOS対応<br/>・隔離された実行環境<br/>・再現可能な環境"]
        Runner["🏃 GitHub Self-hosted Runner<br/>【CI/CD実行】<br/>・ローカル実行<br/>・高速ビルド<br/>・キャッシュ活用"]
        Python["🐍 Python 3.13 + uv<br/>【実行環境】<br/>・最新Python<br/>・高速パッケージ管理<br/>・仮想環境管理"]
        CICD["⚡ CI/CDパイプライン<br/>【ビルドツール】<br/>・Rust製高速ツール<br/>・並列実行<br/>・インクリメンタルビルド"]
        ClaudeNode["🤖 Claude Code + Node.js<br/>【開発支援】<br/>・コード生成支援<br/>・自動化スクリプト<br/>・開発効率化"]
        
        VSCode -->|"コンテナ内で実行"| Docker
        Docker -->|"包含"| Python
        Docker -->|"包含"| Runner
        Docker -->|"包含"| ClaudeNode
        Runner -->|"トリガー"| CICD
        CICD -->|"使用"| Python
        ClaudeNode -->|"支援"| Python
    end
```

## Component図（レベル3）
Python実行環境内のコンポーネント詳細

```mermaid
graph TB
    subgraph "Python実行環境 - Components"
        style uv fill:#5e4fa2,stroke:#4a3c7e,color:#ffffff
        
        uv["📦 uv<br/>【パッケージマネージャー】<br/>・Rust製高速実装<br/>・pip互換<br/>・ロックファイル管理"]
        pytest["🧪 pytest<br/>【テストフレームワーク】<br/>・単体テスト<br/>・統合テスト<br/>・カバレッジ測定"]
        Ruff["🔍 Ruff<br/>【リンター/フォーマッター】<br/>・Rust製高速実行<br/>・Black互換フォーマット<br/>・Flake8互換チェック"]
        ty["✅ ty<br/>【型チェッカー】<br/>・静的型検査<br/>・型ヒント検証<br/>・エラー早期発見"]
        Sphinx["📚 Sphinx<br/>【ドキュメント生成】<br/>・API文書自動生成<br/>・Markdown/reSTサポート<br/>・多言語対応"]
        
        uv -->|"パッケージ管理"| pytest
        uv -->|"パッケージ管理"| Ruff
        uv -->|"パッケージ管理"| ty
        uv -->|"パッケージ管理"| Sphinx
        pytest -->|"コード品質保証"| Ruff
        Ruff -->|"フォーマット済みコード"| ty
        ty -->|"型安全なコード"| Sphinx
    end
```

## アーキテクチャの特徴

### 1. **OS非依存性**
- Docker Containerによる完全な環境分離
- Windows/macOS/Linux全てで同一の開発体験

### 2. **高速化**
- Rust製ツール（uv, Ruff）による高速実行
- GitHub Self-hosted Runnerによるローカルビルド
- キャッシュを活用した効率的なビルド

### 3. **開発効率**
- VSCode DevContainerによる即座の開発開始
- Claude Codeによる開発支援
- 統一されたツールチェーン

### 4. **品質保証**
- pytest による包括的なテスト
- Ruff による一貫したコードスタイル
- ty による型安全性の確保
- Sphinx による最新ドキュメントの維持

## 技術選定理由

| コンポーネント | 選定理由 |
|------------|---------|
| Python 3.13 | 最新の言語機能とパフォーマンス改善 |
| uv | pip/pip-tools/pipenvより高速、Rust実装 |
| Ruff | Black+Flake8+isortを統合、超高速 |
| pytest | デファクトスタンダード、豊富なプラグイン |
| ty | 軽量な型チェッカー |
| Sphinx | Python公式ドキュメントツール |
| Docker | 環境の再現性と隔離性 |
| GitHub Runner | CI/CDのローカル実行による高速化 |