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


# =========================
# HOME
# =========================

@app.route("/")
def home():
    return render_template("index.html")


# =========================
# UPLOAD PDF
# =========================

@app.route("/upload", methods=["POST"])
def upload_pdf():

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

        # Extract text directly from uploaded PDF
        extracted_text = extract_text_from_pdf(file)

        if not extracted_text.strip():

            return jsonify({
                "success": False,
                "message": "No readable text found in this PDF."
            }), 400

        return jsonify({
            "success": True,
            "message": "PDF uploaded successfully.",
            "filename": file.filename,
            "characters": len(extracted_text),
            "words": len(extracted_text.split()),

            # Send extracted text to browser
            "pdf_text": extracted_text
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

    try:

        data = request.get_json(silent=True) or {}

        question = data.get(
            "question",
            ""
        ).strip()

        pdf_text = data.get(
            "pdf_text",
            ""
        )

        if not pdf_text:

            return jsonify({
                "success": False,
                "answer": "Please upload a PDF first."
            })

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

    try:

        data = request.get_json(silent=True) or {}

        pdf_text = data.get(
            "pdf_text",
            ""
        )

        if not pdf_text:

            return jsonify({
                "success": False,
                "answer": "Please upload a PDF first."
            })

        result = summarize_pdf(
            pdf_text
        )

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

    try:

        data = request.get_json(silent=True) or {}

        pdf_text = data.get(
            "pdf_text",
            ""
        )

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

    try:

        data = request.get_json(silent=True) or {}

        pdf_text = data.get(
            "pdf_text",
            ""
        )

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

    try:

        data = request.get_json(silent=True) or {}

        pdf_text = data.get(
            "pdf_text",
            ""
        )

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
