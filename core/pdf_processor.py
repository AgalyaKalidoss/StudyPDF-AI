import pymupdf


def extract_pdf_content(uploaded_file):
    """
    Extract text from a Flask uploaded PDF file.
    """

    uploaded_file.seek(0)

    pdf_bytes = uploaded_file.read()

    if not pdf_bytes:
        return []

    document = pymupdf.open(
        stream=pdf_bytes,
        filetype="pdf"
    )

    pages = []

    for page_number, page in enumerate(
        document,
        start=1
    ):

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
    Accept either:
    - Flask uploaded file
    - PDF file path
    """

    if isinstance(source, str):

        with open(
            source,
            "rb"
        ) as file:

            pages = extract_pdf_content(file)

    else:

        pages = extract_pdf_content(source)

    return get_full_text(pages)


def get_full_text(pages):
    """
    Combine all PDF pages into one text string.
    """

    sections = []

    for page in pages:

        text = page.get(
            "text",
            ""
        ).strip()

        if text:

            sections.append(
                f"--- Page {page['page']} ---\n{text}"
            )

    return "\n\n".join(sections)


def get_page_count(pages):

    return len(pages)


def get_word_count(pages):

    text = get_full_text(pages)

    return len(text.split())


def get_character_count(pages):

    text = get_full_text(pages)

    return len(text)


def get_non_empty_pages(pages):

    return [
        page
        for page in pages
        if page.get(
            "text",
            ""
        ).strip()
    ]
