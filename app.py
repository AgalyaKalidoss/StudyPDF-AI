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


# =========================
# PDF UPLOAD
# =========================

@app.route("/upload", methods=["POST"])
def upload_pdf():

    global pdf_text

    try:

        if "pdf" not in request.files:

            return jsonify({
                "success": False,
                "message": "No PDF selected."
            }), 400

        file = request.files["pdf"]

        if file.filename == "":

            return jsonify({
                "success": False,
                "message": "Please select a PDF."
            }), 400

        if not file.filename.lower().endswith(".pdf"):

            return jsonify({
                "success": False,
                "message": "Only PDF files are allowed."
            }), 400

        # Extract directly from uploaded file
        pdf_text = extract_text_from_pdf(file)

        if not pdf_text.strip():

            return jsonify({
                "success": False,
                "message": "No readable text found in this PDF."
            }), 400

        return jsonify({
            "success": True,
            "message": "PDF uploaded successfully.",
            "filename": file.filename,
            "characters": len(pdf_text),
            "words": len(pdf_text.split())
        })

    except Exception as e:

        print("UPLOAD ERROR:", e)

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# =========================
# ASK QUESTION
# =========================

@app.route("/ask", methods=["POST"])
def ask():

    global pdf_text

    try:

        if not pdf_text:

            return jsonify({
                "success": False,
                "answer": "Please upload a PDF first."
            })

        data = request.get_json(silent=True) or {}

        question = data.get("question", "").strip()

        if not question:

            return jsonify({
                "success": False,
                "answer": "Please enter a question."
            })

        answer = ask_pdf(
            question,
            pdf_text
        )

        return jsonify({
            "success": True,
            "answer": answer
        })

    except Exception as e:

        print("ASK ERROR:", e)

        return jsonify({
            "success": False,
            "answer": str(e)
        }), 500


# =========================
# SUMMARY
# =========================

@app.route("/summary", methods=["POST"])
def summary():

    global pdf_text

    try:

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

    except Exception as e:

        print("SUMMARY ERROR:", e)

        return jsonify({
            "success": False,
            "answer": str(e)
        }), 500


# =========================
# 2 MARK QUESTIONS
# =========================

@app.route("/two-mark", methods=["POST"])
def two_mark():

    global pdf_text

    try:

        if not pdf_text:

            return jsonify({
                "success": False,
                "answer": "Please upload a PDF first."
            })

        result = generate_two_mark_questions(
            pdf_text,
            10
        )

        return jsonify({
            "success": True,
            "answer": result
        })

    except Exception as e:

        print("2-MARK ERROR:", e)

        return jsonify({
            "success": False,
            "answer": str(e)
        }), 500


# =========================
# 16 MARK QUESTIONS
# =========================

@app.route("/sixteen-mark", methods=["POST"])
def sixteen_mark():

    global pdf_text

    try:

        if not pdf_text:

            return jsonify({
                "success": False,
                "answer": "Please upload a PDF first."
            })

        result = generate_sixteen_mark_questions(
            pdf_text,
            5
        )

        return jsonify({
            "success": True,
            "answer": result
        })

    except Exception as e:

        print("16-MARK ERROR:", e)

        return jsonify({
            "success": False,
            "answer": str(e)
        }), 500


# =========================
# IMPORTANT QUESTIONS
# =========================

@app.route("/important-questions", methods=["POST"])
def important_questions():

    global pdf_text

    try:

        if not pdf_text:

            return jsonify({
                "success": False,
                "answer": "Please upload a PDF first."
            })

        result = generate_important_questions(
            pdf_text,
            15
        )

        return jsonify({
            "success": True,
            "answer": result
        })

    except Exception as e:

        print("IMPORTANT QUESTIONS ERROR:", e)

        return jsonify({
            "success": False,
            "answer": str(e)
        }), 500


# =========================
# RUN
# =========================

if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
