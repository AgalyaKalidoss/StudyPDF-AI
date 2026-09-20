import pymupdf


def extract_pdf_content(uploaded_file):
    """
    Extract text from every page of an uploaded PDF.
    """

    uploaded_file.seek(0)

    pdf_bytes = uploaded_file.read()

    document = pymupdf.open(
        stream=pdf_bytes,
        filetype="pdf"
    )

    pages = []

    for page_number, page in enumerate(document, start=1):

        text = page.get_text("text").strip()

        pages.append({
            "page": page_number,
            "text": text
        })

    document.close()

    return pages


def get_full_text(pages):
    """
    Combine extracted page text into one string.
    """

    sections = []

    for page in pages:

        if page["text"].strip():

            sections.append(
                f"--- Page {page['page']} ---\n"
                f"{page['text']}"
            )

    return "\n\n".join(sections)


def get_page_count(pages):
    return len(pages)


def get_word_count(pages):

    full_text = get_full_text(pages)

    return len(full_text.split())


def get_character_count(pages):

    full_text = get_full_text(pages)

    return len(full_text)


def get_non_empty_pages(pages):

    return [
        page
        for page in pages
        if page["text"].strip()
    ]
