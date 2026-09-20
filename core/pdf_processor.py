import os
import pymupdf


def extract_text_from_pdf(source):
    """
    Extract complete text from a PDF.

    source can be:
    - a file path string
    - a Flask uploaded file object
    """

    try:

        # If source is a file path
        if isinstance(source, (str, os.PathLike)):

            document = pymupdf.open(str(source))

        # If source is an uploaded file object
        else:

            source.seek(0)

            pdf_bytes = source.read()

            document = pymupdf.open(
                stream=pdf_bytes,
                filetype="pdf"
            )

        pages = []

        for page in document:

            text = page.get_text("text").strip()

            if text:
                pages.append(text)

        document.close()

        return "\n\n".join(pages)

    except Exception as e:

        raise Exception(
            f"Could not extract PDF text: {str(e)}"
        )


def extract_pdf_content(source):
    """
    Extract PDF content page by page.
    """

    if isinstance(source, (str, os.PathLike)):

        document = pymupdf.open(str(source))

    else:

        source.seek(0)

        pdf_bytes = source.read()

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

        pages.append({
            "page": page_number,
            "text": text
        })

    document.close()

    return pages


def get_full_text(pages):

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
        if page.get("text", "").strip()
    ]
