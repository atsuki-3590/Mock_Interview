import os
import uuid
import tempfile
import fitz  # PyMuPDF
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.files.storage import default_storage
from openai import OpenAI

print("🔑 OPENAI_API_KEY =", os.getenv("OPENAI_API_KEY"))

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@csrf_exempt
@require_http_methods(["POST"])
def api_upload_pdf(request):
    """PDFをアップロードし、初回質問を生成"""
    if 'pdf' not in request.FILES:
        return JsonResponse({"error": "PDFファイルが必要です"}, status=400)

    pdf_file = request.FILES['pdf']
    text = extract_text_from_pdf(pdf_file)
    question = generate_first_question(text)

    return JsonResponse({"question": question})


@csrf_exempt
@require_http_methods(["POST"])
def api_send_answer(request):
    """質問と回答を受け取り、フィードバックを返す"""
    import json
    try:
        body = json.loads(request.body)
        question = body.get("question", "")
        answer = body.get("answer", "")
    except Exception:
        return JsonResponse({"error": "不正なJSONです"}, status=400)

    if not question or not answer:
        return JsonResponse({"error": "質問と回答は必須です"}, status=400)

    feedback = generate_feedback(question, answer)
    return JsonResponse({"feedback": feedback})


@csrf_exempt
@require_http_methods(["POST"])
def api_next_question(request):
    """過去のQA履歴を受け取り、次の質問を生成"""
    import json
    try:
        body = json.loads(request.body)
        history = body.get("history", [])  # list of {"question": ..., "answer": ...}
    except Exception:
        return JsonResponse({"error": "不正なJSONです"}, status=400)

    prev_qa = "\n".join(
        f"Q{i+1}: {item['question']}\nA{i+1}: {item['answer']}"
        for i, item in enumerate(history)
    )

    next_q = generate_followup_question(prev_qa)
    return JsonResponse({"question": next_q})


# -----------------------------------------------------------------------
# 補助関数
# -----------------------------------------------------------------------

def extract_text_from_pdf(django_file):
    """PDF → 一時ファイルに保存 → テキスト抽出"""
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


def generate_first_question(pdf_text: str) -> str:
    prompt = f"""
以下は就活生の履歴書またはエントリーシートです。
この内容をもとに面接で想定される質問を **1つだけ** 出力してください。

フォーマット:
Q: 質問内容

内容:
{pdf_text}
"""
    return ask_gpt(prompt).lstrip("Q:").strip()


def generate_followup_question(prev_qa: str) -> str:
    prompt = f"""
以下は就活面接でのこれまでのやり取りです。

{prev_qa}

この内容を踏まえて、新たに次の質問を **1つだけ** 生成してください。

フォーマット:
Q: 質問内容
"""
    return ask_gpt(prompt).lstrip("Q:").strip()


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
    return ask_gpt(prompt)


def ask_gpt(prompt: str) -> str:
    res = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=300,
    )
    return res.choices[0].message.content.strip()
