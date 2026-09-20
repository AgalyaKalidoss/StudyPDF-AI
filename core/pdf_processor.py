import pymupdf


def extract_pdf_content(uploaded_file):
    """
    Extract text from an uploaded PDF.

    Returns:
        A list of dictionaries containing page number and text.
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


def extract_text_from_pdf(uploaded_file):
    """
    Compatibility function for the Flask application.

    Returns the complete extracted PDF text.
    """

    pages = extract_pdf_content(uploaded_file)

    return get_full_text(pages)


def get_full_text(pages):
    """
    Combine all extracted pages into one text string.
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
    """
    Return the number of pages.
    """

    return len(pages)


def get_word_count(pages):
    """
    Return the number of words.
    """

    full_text = get_full_text(pages)

    return len(full_text.split())


def get_character_count(pages):
    """
    Return the number of characters.
    """

    full_text = get_full_text(pages)

    return len(full_text)


def get_non_empty_pages(pages):
    """
    Return only pages containing text.
    """

    return [
        page
        for page in pages
        if page.get("text", "").strip()
    ]
