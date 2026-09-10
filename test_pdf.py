import fitz

from core.pdf_processor import (
    extract_pdf_content,
    get_full_text,
    get_page_count,
    get_word_count,
)

PDF_PATH = "sample.pdf"

with open(PDF_PATH, "rb") as file:

    class FakeUpload:

        def __init__(self, data):
            self.data = data

        def seek(self, position):
            pass

        def read(self):
            return self.data

    uploaded_file = FakeUpload(file.read())

pages = extract_pdf_content(uploaded_file)

print("\n========== PDF TEST ==========")
print("Pages:", get_page_count(pages))
print("Words:", get_word_count(pages))

print("\nFirst page preview:\n")
if pages:
    print(pages[0]["text"][:1000])

print("\n========== TEST COMPLETE ==========")