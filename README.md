# 面接練習サイト 

## 概要

本サイトは、新卒就活生を対象にした**面接練習支援Webサービス**です。ユーザーがアップロードした履歴書・エントリーシート（PDF形式）をもとに、ChatGPT APIを利用して**想定質問と模範解答**を自動生成します。また、回答に対するフィードバックも生成することが可能です。

---

## 利用技術

- **フレームワーク**: Django（Python）
- **フロントエンド**: HTML / CSS（テンプレートエンジン使用）
- **バックエンド**:
  - ChatGPT API（OpenAI）
  - PyMuPDF（PDFテキスト抽出）
  - UUID（ファイル名生成）
- **デプロイ**: Render（無料プランを初期利用）
- **静的ファイルの管理**: `static/` ディレクトリに配置（例: `static/css/interview_chat.css`）

---

## 起動方法
```bash
# 仮想環境の立ち上げ
.\mock_interview\Scripts\Activate.ps1  

# reactの起動（react変更時）
cd frontend
npm run dev

# djangoの起動
cd ../
python backend\manage.py runserver

```

---

## 主な機能

### 1. PDFアップロードと解析

- PDFファイル（履歴書・ES）をユーザーがアップロード
- PyMuPDFを用いてテキスト抽出
- 抽出されたテキストをもとにChatGPT APIを呼び出し、以下を生成：
  - 想定質問（5〜10問程度）
  - それぞれの模範解答

### 2. 回答入力とフィードバック生成

- ユーザーが質問ごとに回答を入力
- 回答はセッションで保持
- ChatGPT APIにより回答に対するフィードバックを生成し、表示

### 3. UIの構成

- 質問と回答をチャット形式で表示
- 色分けされたバブル（質問=青、回答=緑、フィードバック=黄）
- アップロード・送信後のページ内表示（リロード不要）

### 4. ファイル構成

```plaintext
Mock_Interview/
│
├── backend/                        ← Djangoプロジェクトルート
│   ├── manage.py                   ← Django管理コマンド起点
│   ├── db.sqlite3                  ← SQLite DB（開発用）
│   │
│   ├── frontend_build/            ← ✅ Reactビルド成果物（自動生成）
│   │   ├── index.html             ← Reactのトップページ
│   │   └── static/                ← ReactのCSS/JS類（staticfiles）
│   │       ├── js/
│   │       └── css/
│   │
│   ├── interview/                 ← Djangoアプリ（ビュー・APIなど）
│   │   ├── views.py              ← Reactのindex.htmlを返すビュー
│   │   ├── urls.py               ← ルーティング（"/" + "/api/*"）
│   │   └── api_views.py          ← ChatGPTとのやりとり（PDF/回答/質問）
│   │
│   └── interview_site/           ← Djangoプロジェクト設定
│       ├── __init__.py
│       ├── settings.py           ← Reactのパス、CORS設定など
│       ├── urls.py               ← URLルートで interview.urls を include
│       └── wsgi.py
│
├── frontend/                      ← Reactプロジェクト
│   ├── public/                    ← favicon, index.html のテンプレートなど
│   ├── src/                       ← ソースコード
│   │   ├── App.jsx               ← メイン画面（チャットなど）
│   │   ├── components/           ← UI部品
│   │   │   └── ChatBubble.jsx
│   │   └── services/             ← API通信
│   │       └── api.js
│   ├── .env                       ← ビルド先設定（例：BUILD_PATH）
│   ├── package.json              ← React依存とビルドコマンド
│   └── node_modules/             ← npm installされたパッケージ群
│
├── .env                            ← 環境変数（OpenAIのAPIキーなど）
├── .gitignore                      ← .env や __pycache__ などを除外
├── requirements.txt                ← Django, django-cors-headers など
└── render.yaml                     ← （任意）Renderの自動設定用

```

---

### 現在の制約
- 入力ファイルはPDF形式に限定
- 企業情報のURL入力機能は未実装（今後拡張予定）
- 質問・模範解答はセッション内での保持に留まる


### 今後の拡張案
- 企業名・業界名入力 → ChatGPTのプロンプトに組み込み
- 質問の保存と一覧表示（ユーザー管理機能の追加）
- 回答の評価システム（ユーザーからの★評価など）
- スマートフォン対応レイアウトの調整
- Web検索による企業情報の自動取得


