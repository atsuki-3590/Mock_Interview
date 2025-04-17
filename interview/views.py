from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import fitz  # PyMuPDF
from openai import OpenAI
import os
import uuid

# ChatGPTクライアント
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# interview/views.py
def upload_pdf(request):
    questions = request.session.get("questions", [])
    answers = []
    feedbacks = []


    if request.method == 'POST':
        # ① 新規PDFアップロード → 初回質問生成
        if request.FILES.get('pdf'):
            pdf_file = request.FILES['pdf']
            extension = pdf_file.name.split('.')[-1]
            unique_filename = f"{uuid.uuid4()}.{extension}"

            fs = FileSystemStorage()
            filename = fs.save(unique_filename, pdf_file)
            file_path = fs.path(filename)

            with fitz.open(file_path) as doc:
                text = ""
                for page in doc:
                    text += page.get_text()

            os.remove(file_path)

            prompt = f"""
以下は就活生の履歴書またはエントリーシートです。この内容をもとに、面接で想定される質問を"1つ"出力してください。

フォーマット：
Q: 質問内容
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
                questions = answer.split("\n")

                # セッションに保存（フォーム再描画時用）
                request.session["questions"] = questions

            except Exception as e:
                questions = [f"エラーが発生しました: {str(e)}"]
                
            request.session["questions"] = questions
            request.session["answers"] = []
            request.session["feedbacks"] = []

        # ② 回答送信 → フィードバック生成
        elif request.POST.get("skip_upload") == "1":
            idx = len(answers)
            user_answer = request.POST.get(f"answer_{idx + 1}", "")
            if user_answer:
                answers.append(user_answer)
                fb = generate_feedback(questions[idx], user_answer)
                feedbacks.append(fb)

                request.session["answers"] = answers
                request.session["feedbacks"] = feedbacks


        # ③ 次の質問へ進む
        elif request.POST.get("next_question") == "1":
            prev_qa = ""
            for i, (q, a) in enumerate(zip(questions, answers), start=1):
                prev_qa += f"Q{i}: {q}\nA{i}: {a}\n"

            prompt = f"""
以下は就活面接でのこれまでのやりとりです。

{prev_qa}

この内容を踏まえて、新たに次の質問を1つ生成してください。

フォーマット：
Q: 質問内容
"""

            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=300
                )

                new_question = response.choices[0].message.content.strip()
                questions.append(new_question)
                request.session["questions"] = questions

            except Exception as e:
                feedbacks.append(f"エラーが発生しました: {str(e)}")

    return render(request, 'upload.html', {
        'questions': questions,
        'answers': answers,
        'feedbacks': feedbacks,
    })

    qa_pairs = list(zip(questions, answers))

    return render(request, 'upload.html', {
        'questions': questions,
        'answers': answers,
        'feedbacks': feedbacks,
        'qa_pairs': qa_pairs,
        'show_answer_form': len(answers) == 0  # ← 回答フォームを出すか
    })


def generate_feedback(question, answer):
    """
    ChatGPTを使って、1つの質問・回答に対するフィードバックを生成する関数
    """
    prompt = f"""
以下は就活面接の想定質問とそれに対する学生の回答です。

【質問】
{question}

【回答】
{answer}

この回答に対して以下の3点を出力してください。
1. 点数（100点満点中で整数）
2. 質問の意図（企業がこの質問で見ようとしている力）
3. 改善点（より良くするためのアドバイス）

出力フォーマット:
点数: ○点
意図: ○○○
改善点: ○○○
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=600
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"エラーが発生しました: {str(e)}"

