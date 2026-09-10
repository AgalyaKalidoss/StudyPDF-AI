import fitz


def extract_text_from_pdf(pdf_path):
    """
    Extract all text from a PDF file.
    """

    try:
        doc = fitz.open(pdf_path)

        text = ""

        for page in doc:
            text += page.get_text()

        doc.close()

        return text.strip()

    except Exception as e:
        raise Exception(f"PDF extraction failed: {e}")


def get_pdf_page_count(pdf_path):
    """
    Return the number of pages in a PDF.
    """

    try:
        doc = fitz.open(pdf_path)
        page_count = len(doc)
        doc.close()

        return page_count

    except Exception as e:
        raise Exception(f"Could not read PDF: {e}")