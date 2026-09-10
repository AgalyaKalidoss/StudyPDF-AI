from flask import Flask, render_template, request, jsonify
import os

from core.pdf_processor import extract_text_from_pdf
from core.ai_engine import (
    ask_pdf,
    summarize_pdf,
    generate_two_mark_questions,
    generate_sixteen_mark_questions,
    generate_important_questions,
)


app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# Store extracted PDF text temporarily
pdf_text = ""


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_pdf():

    global pdf_text

    if "pdf" not in request.files:
        return jsonify({
            "success": False,
            "message": "No PDF selected."
        })

    file = request.files["pdf"]

    if file.filename == "":
        return jsonify({
            "success": False,
            "message": "Please select a PDF."
        })

    if not file.filename.lower().endswith(".pdf"):
        return jsonify({
            "success": False,
            "message": "Only PDF files are allowed."
        })

    file_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        file.filename
    )

    file.save(file_path)

    try:

        pdf_text = extract_text_from_pdf(file_path)

        return jsonify({
            "success": True,
            "message": "PDF uploaded successfully.",
            "characters": len(pdf_text),
            "filename": file.filename
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        })


@app.route("/ask", methods=["POST"])
def ask():

    global pdf_text

    if not pdf_text:
        return jsonify({
            "success": False,
            "answer": "Please upload a PDF first."
        })

    data = request.get_json()

    question = data.get("question", "").strip()

    if not question:
        return jsonify({
            "success": False,
            "answer": "Please enter a question."
        })

    answer = ask_pdf(question, pdf_text)

    return jsonify({
        "success": True,
        "answer": answer
    })


@app.route("/summary", methods=["POST"])
def summary():

    global pdf_text

    if not pdf_text:
        return jsonify({
            "success": False,
            "answer": "Please upload a PDF first."
        })

    result = summarize_pdf(pdf_text)

    return jsonify({
        "success": True,
        "answer": result
    })


@app.route("/two-mark", methods=["POST"])
def two_mark():

    global pdf_text

    if not pdf_text:
        return jsonify({
            "success": False,
            "answer": "Please upload a PDF first."
        })

    result = generate_two_mark_questions(pdf_text)

    return jsonify({
        "success": True,
        "answer": result
    })


@app.route("/sixteen-mark", methods=["POST"])
def sixteen_mark():

    global pdf_text

    if not pdf_text:
        return jsonify({
            "success": False,
            "answer": "Please upload a PDF first."
        })

    result = generate_sixteen_mark_questions(pdf_text)

    return jsonify({
        "success": True,
        "answer": result
    })


@app.route("/important-questions", methods=["POST"])
def important_questions():

    global pdf_text

    if not pdf_text:
        return jsonify({
            "success": False,
            "answer": "Please upload a PDF first."
        })

    result = generate_important_questions(pdf_text)

    return jsonify({
        "success": True,
        "answer": result
    })


if __name__ == "__main__":
    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )