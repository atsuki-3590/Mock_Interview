# interview/views.py
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.views.decorators.http import require_http_methods
import fitz           # PyMuPDF
from openai import OpenAI
import os, uuid, tempfile

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@require_http_methods(["GET", "POST"])
def upload_pdf(request):
    """
    1. PDFアップロード → 初回質問生成
    2. 回答送信        → フィードバック生成
    3. すべて回答済み  → 次の質問生成
    ================================
    セッションに保持するキー
      - questions : list[str]
      - answers   : list[str]
      - feedbacks : list[str]
    """
    # --- セッション読み込み（なければ空リスト） --------------------------
    questions  = request.session.get("questions",  [])
    answers    = request.session.get("answers",    [])
    feedbacks  = request.session.get("feedbacks",  [])

    # --- POST 処理 --------------------------------------------------------
    if request.method == "POST":

        # ① PDFアップロード
        if 'pdf' in request.FILES:
            pdf_text = _extract_text(request.FILES['pdf'])
            questions = [_generate_first_question(pdf_text)]
            answers, feedbacks = [], []

        # ② 回答送信
        elif request.POST.get("action") == "answer":
            idx = int(request.POST["q_idx"])
            user_answer = request.POST.get("answer", "").strip()

            if user_answer:
                # list が短い場合に備え延長
                while len(answers) <= idx:
                    answers.append("")
                answers[idx] = user_answer

                fb = generate_feedback(questions[idx], user_answer)

                while len(feedbacks) <= idx:
                    feedbacks.append("")
                feedbacks[idx] = fb

        # ③ 次の質問生成
        elif request.POST.get("action") == "next":
            prev_qa = "\n".join(
                f"Q{i+1}: {q}\nA{i+1}: {a}"
                for i, (q, a) in enumerate(zip(questions, answers))
            )
            questions.append(_generate_followup_question(prev_qa))

        # --- セッションへ保存 -------------------------------------------
        request.session.update({
            "questions": questions,
            "answers":   answers,
            "feedbacks": feedbacks,
        })
        request.session.modified = True
        return redirect("upload_pdf")   # PRG パターン

    # --- GET / 描画 ------------------------------------------------------
    all_answered = len(answers) == len(questions) and questions
    context = {
        "questions":        questions,
        "answers":          answers,
        "feedbacks":        feedbacks,
        "show_answer_form": not all_answered,
    }
    return render(request, "upload.html", context)


# -----------------------------------------------------------------------
# 補助関数
# -----------------------------------------------------------------------
def _extract_text(django_file):
    """PDF → 一時ファイル → テキスト抽出 → 削除"""
    extension = django_file.name.split(".")[-1]
    with tempfile.NamedTemporaryFile(suffix=f".{extension}", delete=False) as tmp:
        for chunk in django_file.chunks():
            tmp.write(chunk)
        tmp_path = tmp.name

    text = ""
    with fitz.open(tmp_path) as doc:
        for page in doc:
            text += page.get_text()
    os.remove(tmp_path)
    return text


def _generate_first_question(pdf_text: str) -> str:
    prompt = f"""
以下は就活生の履歴書またはエントリーシートです。
この内容をもとに面接で想定される質問を **1つだけ** 出力してください。

フォーマット:
Q: 質問内容

内容:
{pdf_text}
"""
    return _ask_gpt(prompt).lstrip("Q:").strip()


def _generate_followup_question(prev_qa: str) -> str:
    prompt = f"""
以下は就活面接でのこれまでのやり取りです。

{prev_qa}

この内容を踏まえて、新たに次の質問を **1つだけ** 生成してください。

フォーマット:
Q: 質問内容
"""
    return _ask_gpt(prompt).lstrip("Q:").strip()


def _ask_gpt(prompt: str) -> str:
    res = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=300,
    )
    return res.choices[0].message.content.strip()


def generate_feedback(question: str, answer: str) -> str:
    prompt = f"""
以下は就活面接の想定質問と学生の回答です。

【質問】
{question}

【回答】
{answer}

この回答について以下の3点を出力してください。
1. 点数（100点満点の整数）
2. 質問の意図
3. 改善点

フォーマット:
点数: ○点
意図: ○○○
改善点: ○○○
"""
    return _ask_gpt(prompt)
