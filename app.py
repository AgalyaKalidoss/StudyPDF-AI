import os
import uuid

from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    session
)

from werkzeug.utils import secure_filename

from core.pdf_processor import extract_text_from_pdf

from core.ai_engine import (
    ask_pdf,
    summarize_pdf,
    generate_two_mark_questions,
    generate_sixteen_mark_questions,
    generate_important_questions,
)


app = Flask(__name__)

# Secret key for Flask sessions
app.secret_key = os.environ.get(
    "SECRET_KEY",
    "studypdf-ai-secret-key"
)

# Upload settings
UPLOAD_FOLDER = "uploads"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

app.config["MAX_CONTENT_LENGTH"] = (
    20 * 1024 * 1024
)


# =====================================================
# HOME
# =====================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# =====================================================
# GET CURRENT PDF TEXT
# =====================================================

def get_current_pdf_text():

    filename = session.get(
        "pdf_filename"
    )

    if not filename:

        return None

    file_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    if not os.path.exists(file_path):

        session.pop(
            "pdf_filename",
            None
        )

        return None

    try:

        text = extract_text_from_pdf(
            file_path
        )

        return text

    except Exception:

        return None


# =====================================================
# UPLOAD PDF
# =====================================================

@app.route(
    "/upload",
    methods=["POST"]
)
def upload_pdf():

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


    # Remove previous PDF belonging to this session
    old_filename = session.get(
        "pdf_filename"
    )

    if old_filename:

        old_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            old_filename
        )

        if os.path.exists(old_path):

            try:
                os.remove(old_path)

            except Exception:
                pass


    # Create unique filename
    original_name = secure_filename(
        file.filename
    )

    unique_filename = (
        f"{uuid.uuid4().hex}_{original_name}"
    )


    file_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        unique_filename
    )


    try:

        # Save PDF
        file.save(file_path)


        # Extract text to verify PDF
        text = extract_text_from_pdf(
            file_path
        )


        if not text.strip():

            os.remove(file_path)

            return jsonify({
                "success": False,
                "message":
                    "No readable text found in this PDF."
            }), 400


        # Store filename in session
        session["pdf_filename"] = (
            unique_filename
        )

        session.modified = True


        return jsonify({

            "success": True,

            "message":
                "PDF uploaded successfully.",

            "filename":
                original_name,

            "characters":
                len(text),

            "words":
                len(text.split())

        })


    except Exception as e:

        if os.path.exists(file_path):

            try:
                os.remove(file_path)

            except Exception:
                pass


        return jsonify({

            "success": False,

            "message":
                f"PDF processing failed: {str(e)}"

        }), 500


# =====================================================
# ASK PDF
# =====================================================

@app.route(
    "/ask",
    methods=["POST"]
)
def ask():

    pdf_text = get_current_pdf_text()


    if not pdf_text:

        return jsonify({

            "success": False,

            "answer":
                "Please upload a PDF first."

        }), 400


    data = request.get_json(
        silent=True
    ) or {}


    question = data.get(
        "question",
        ""
    ).strip()


    if not question:

        return jsonify({

            "success": False,

            "answer":
                "Please enter a question."

        }), 400


    try:

        answer = ask_pdf(
            question,
            pdf_text
        )


        return jsonify({

            "success": True,

            "answer": answer

        })


    except Exception as e:

        return jsonify({

            "success": False,

            "answer":
                f"AI Error: {str(e)}"

        }), 500


# =====================================================
# SUMMARY
# =====================================================

@app.route(
    "/summary",
    methods=["POST"]
)
def summary():

    pdf_text = get_current_pdf_text()


    if not pdf_text:

        return jsonify({

            "success": False,

            "answer":
                "Please upload a PDF first."

        }), 400


    try:

        result = summarize_pdf(
            pdf_text
        )


        return jsonify({

            "success": True,

            "answer": result

        })


    except Exception as e:

        return jsonify({

            "success": False,

            "answer":
                f"AI Error: {str(e)}"

        }), 500


# =====================================================
# 2-MARK QUESTIONS
# =====================================================

@app.route(
    "/two-mark",
    methods=["POST"]
)
def two_mark():

    pdf_text = get_current_pdf_text()


    if not pdf_text:

        return jsonify({

            "success": False,

            "answer":
                "Please upload a PDF first."

        }), 400


    try:

        result = generate_two_mark_questions(
            pdf_text,
            count=10
        )


        return jsonify({

            "success": True,

            "answer": result

        })


    except Exception as e:

        return jsonify({

            "success": False,

            "answer":
                f"AI Error: {str(e)}"

        }), 500


# =====================================================
# 16-MARK QUESTIONS
# =====================================================

@app.route(
    "/sixteen-mark",
    methods=["POST"]
)
def sixteen_mark():

    pdf_text = get_current_pdf_text()


    if not pdf_text:

        return jsonify({

            "success": False,

            "answer":
                "Please upload a PDF first."

        }), 400


    try:

        result = generate_sixteen_mark_questions(
            pdf_text,
            count=5
        )


        return jsonify({

            "success": True,

            "answer": result

        })


    except Exception as e:

        return jsonify({

            "success": False,

            "answer":
                f"AI Error: {str(e)}"

        }), 500


# =====================================================
# IMPORTANT QUESTIONS
# =====================================================

@app.route(
    "/important-questions",
    methods=["POST"]
)
def important_questions():

    pdf_text = get_current_pdf_text()


    if not pdf_text:

        return jsonify({

            "success": False,

            "answer":
                "Please upload a PDF first."

        }), 400


    try:

        result = generate_important_questions(
            pdf_text,
            count=15
        )


        return jsonify({

            "success": True,

            "answer": result

        })


    except Exception as e:

        return jsonify({

            "success": False,

            "answer":
                f"AI Error: {str(e)}"

        }), 500


# =====================================================
# RUN
# =====================================================

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
