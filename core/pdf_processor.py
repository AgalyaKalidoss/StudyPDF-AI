import pymupdf


def extract_pdf_content(uploaded_file):
    """
    Extract text from a Flask uploaded PDF file.
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

        if text:
            pages.append({
                "page": page_number,
                "text": text
            })

    document.close()

    return pages


def extract_text_from_pdf(source):
    """
    Extract complete text from either:
    - Flask uploaded file object
    - PDF file path
    """

    if isinstance(source, str):

        with open(source, "rb") as file:

            pages = extract_pdf_content(file)

    else:

        pages = extract_pdf_content(source)

    return get_full_text(pages)


def get_full_text(pages):
    """
    Combine all page text into one string.
    """

    sections = []

    for page in pages:

        text = page.get("text", "").strip()

        if text:

            sections.append(
                f"--- Page {page['page']} ---\n{text}"
            )

    return "\n\n".join(sections)


def get_page_count(pages):
    return len(pages)


def get_word_count(pages):
    return len(get_full_text(pages).split())


def get_character_count(pages):
    return len(get_full_text(pages))


def get_non_empty_pages(pages):

    return [
        page
        for page in pages
        if page.get("text", "").strip()
    ]
