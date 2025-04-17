from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import fitz  # PyMuPDF
from openai import OpenAI
import os
import uuid

# ChatGPTクライアント
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def upload_pdf(request):
    questions = []
    if request.method == 'POST' and request.FILES.get('pdf'):
        pdf_file = request.FILES['pdf']
        
        # 一意なファイル名を生成
        extension = pdf_file.name.split('.')[-1]
        unique_filename = f"{uuid.uuid4()}.{extension}"

        # 一時保存
        fs = FileSystemStorage()
        filename = fs.save(unique_filename, pdf_file)
        file_path = fs.path(filename)

        # PDFからテキストを抽出
        with fitz.open(file_path) as doc:
            text = ""
            for page in doc:
                text += page.get_text()

        # 一時ファイルを削除
        os.remove(file_path)

        # プロンプト作成
        prompt = f"""
以下は就活生の履歴書またはエントリーシートです。この内容をもとに、面接で想定される質問とそれに対する模範解答を5セット出力してください。

フォーマット：
Q1: 質問内容
A1: 模範解答
Q2: ...
...

内容:
{text}
"""

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=1000
            )

            answer = response.choices[0].message.content.strip()

            # 質問・回答をリスト化（簡易）
            questions = answer.split("\n")

        except Exception as e:
            questions = [f"エラーが発生しました: {str(e)}"]

    return render(request, 'upload.html', {'questions': questions})
