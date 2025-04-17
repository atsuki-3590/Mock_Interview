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

## 📁 ディレクトリ構成と各ファイルの役割

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

---

## ✅ 実装済み機能

- [x] PDFファイルアップロード（匿名＆一時的）
- [x] PDFテキスト抽出（PyMuPDF）
- [x] ChatGPT APIへのプロンプト送信
- [x] 想定質問＋模範解答の自動生成
- [x] 結果の画面表示
- [x] アップロードファイルの自動削除

---

## 🔜 今後の拡張候補

- [ ] ChatGPTの出力を質問と模範解答に分離表示
- [ ] UIスタイリング（見やすさ向上）
- [ ] モバイル最適化
- [ ] Renderへのデプロイ
- [ ] Google広告導入
- [ ] ユーザー認証・データ保存機能（将来的に）

---