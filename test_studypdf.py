from core.pdf_processor import extract_text_from_pdf
from core.ai_engine import ask_pdf


PDF_PATH = "sample.pdf"


print("=" * 60)
print("              STUDYPDF AI TEST")
print("=" * 60)


# Step 1: Extract PDF text
print("\n[1] Reading PDF...")

pdf_text = extract_text_from_pdf(PDF_PATH)

print(f"Extracted {len(pdf_text)} characters.")


# Step 2: Ask AI
question = input("\nAsk a question about the PDF: ")

print("\n[2] Asking Gemini...\n")

answer = ask_pdf(question, pdf_text)


# Step 3: Display answer
print("-" * 60)
print("AI ANSWER")
print("-" * 60)

print(answer)

print("-" * 60)