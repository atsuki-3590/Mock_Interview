# 面接練習サイト（Django + ChatGPT）

就活生向けに、PDF形式の履歴書・エントリーシートを元に、面接で想定される質問と模範解答を生成するサービスです。

## 🔧 使用技術

- Django
- Python-dotenv
- OpenAI GPT API
- PyMuPDF（PDFテキスト抽出）
- Render（ホスティング）

## 🚀 セットアップ手順

```bash
git clone https://github.com/yourname/your-repo.git
cd your-repo
python -m venv venv
.\mock_interview\Scripts\Activate.ps1  
pip install -r requirements.txt
```

## 🚀 仮想環境のアクティベート

.\mock_interview\Scripts\Activate.ps1   



# 面接練習サイト（Django × ChatGPT）

## 💡流れの補足（UI的なイメージ）
```
Step 1：ファイルアップロード＋企業名＋質問タイプ選択
↓
Step 2：質問1の表示＋入力フォーム
↓
Step 3：回答を入力→送信
↓
Step 4：フィードバック（点数・意図・改善点）表示＋「次の質問へ」ボタン
↓
Step 5：次の質問（前の回答内容を加味）
↓
（繰り返し）
```

---

## 📁 ディレクトリ構成と各ファイルの役割

```
Mock_Interview/ 
├── manage.py # Django管理コマンド実行用 
├── .env # OpenAI APIキーを管理（Git管理外） 
├── requirements.txt # 依存ライブラリ一覧 
├── templates/ 
│ └── upload.html # アップロード画面 + 質問結果の表示HTML 
├── media/ # アップロードされたPDFの一時保存先 
├── interview/ 
│ ├── views.py # アップロード処理、ChatGPT連携ロジック 
│ 
├── urls.py # このアプリのルーティング定義 
│ ├── models.py # 未使用（将来、DB保存したいときに使用） 
│ └── ... # その他Djangoアプリの標準ファイル 
└── interview_site/ 
├── settings.py # プロジェクト全体の設定ファイル 
├── urls.py # プロジェクト全体のルーティング設定 
├── wsgi.py / asgi.py # デプロイ用設定 
└── ...
```
---

## ✅ 実装済み機能

- [x] PDFファイルアップロード（匿名＆一時的）
- [x] PDFテキスト抽出（PyMuPDF）
- [x] ChatGPT APIへのプロンプト送信
- [x] 想定質問＋模範解答の自動生成
- [x] 結果の画面表示
- [x] アップロードファイルの自動削除

---

## 🔜 Step 1: 回答入力と送信機能の追加
目的：ユーザーが模擬質問に回答できるようにする
- [ ] 回答入力欄（textarea）を表示
- [ ] 回答送信ボタン追加
- [ ] POSTリクエストでユーザーの回答を受け取る
- [ ] 回答内容をセッション or 一時変数に保存

---

## 🔜 Step 2: 回答に対するフィードバックの生成
目的：ChatGPTにユーザー回答を評価させる
- [ ] ChatGPTへ「質問＋ユーザー回答」を送信
- [ ] 評価指標に基づいたプロンプト作成（例：点数、意図、改善点）
- [ ] ChatGPTの返答から情報を抽出して画面に表示

---

## 🔜 Step 3: 次の質問への遷移処理
目的：前の回答を踏まえた質問を生成・表示
- [ ] 「次の質問へ」ボタン設置
- [ ] 過去の回答内容をプロンプトに追加
- [ ] 新たな質問＆模範解答をChatGPTから取得
- [ ] 画面に再表示（フローのループ構築）

---

## 🔜 Step 4: UI/UX改善（後回しでもOK）
目的：見やすさ・使いやすさ向上
- [ ] Bootstrap等の導入でフォーム整形
- [ ] ファイルアップロード・質問画面を分ける or タブ切替
- [ ] 質問番号 or 進捗表示（例：「3/5問目」など）

---

## 🔜 Step 5: 管理機能・保存（任意・後回しOK）
目的：回答・フィードバックを保存して後から振り返れるように
- [ ] モデル作成（User、Session、回答ログなど）
- [ ] ログイン機能（ユーザー別履歴管理）
- [ ] 回答一覧ページ or ダウンロード機能

---

## 🔜 今後の拡張候補

- [ ] ChatGPTの出力を質問と模範解答に分離表示
- [ ] UIスタイリング（見やすさ向上）
- [ ] モバイル最適化
- [ ] Renderへのデプロイ
- [ ] Google広告導入
- [ ] ユーザー認証・データ保存機能（将来的に）

---



