Modern Python Development Environment
======================================

.. image:: https://img.shields.io/badge/Python-3.13-blue.svg
   :target: https://www.python.org
   :alt: Python 3.13

.. image:: https://img.shields.io/badge/Docker-DevContainer-blue.svg
   :target: https://code.visualstudio.com/docs/remote/containers
   :alt: Docker DevContainer

.. image:: https://img.shields.io/badge/Code%20Style-Ruff-black.svg
   :target: https://github.com/astral-sh/ruff
   :alt: Code style: Ruff

.. image:: https://img.shields.io/badge/Docs-GitHub%20Pages-brightgreen.svg
   :target: https://taroskee.github.io/modern-python/
   :alt: Documentation

Modern Python開発環境へようこそ！このプロジェクトは、Docker + VSCode DevContainerを使用した
OS非依存のPython開発環境を提供します。

主な特徴
--------

* **OS非依存**: Windows/macOS/Linuxで同一の開発体験
* **高速実行**: Rust製ツール（uv, Ruff）による圧倒的な実行速度
* **即座の開発開始**: VSCode DevContainerで環境構築不要
* **品質保証**: TDD実践とCI/CDパイプラインによる継続的な品質管理

.. toctree::
   :maxdepth: 2
   :caption: ユーザーガイド

   getting_started
   installation
   usage
   configuration

.. toctree::
   :maxdepth: 2
   :caption: 開発者ガイド

   development
   testing
   contributing
   architecture

.. toctree::
   :maxdepth: 2
   :caption: API リファレンス

   api
   modules

.. toctree::
   :maxdepth: 1
   :caption: その他

   changelog
   license

クイックスタート
----------------

1. リポジトリをクローン::

    git clone https://github.com/taroskee/modern-python.git
    cd modern-python

2. VSCodeで開く::

    code .

3. VSCodeで "Reopen in Container" を選択

4. 開発開始！

技術スタック
------------

**Core Technologies:**

* Python 3.13
* Docker + DevContainer
* VSCode

**Development Tools:**

* **uv**: Rust製の超高速パッケージマネージャー
* **Ruff**: Rust製の高速リンター/フォーマッター
* **pytest**: Pythonのデファクトスタンダードテストフレームワーク
* **Sphinx**: ドキュメント生成ツール

プロジェクト構造
----------------

.. code-block:: text

    modern-python/
    ├── .devcontainer/    # DevContainer設定
    ├── .github/          # GitHub Actions
    ├── .vscode/          # VSCode設定
    ├── docs/             # ドキュメント
    ├── src/              # ソースコード
    ├── tests/            # テストコード
    └── pyproject.toml    # プロジェクト定義

インデックス
------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`