
import re

from langchain_core.documents import Document


def normalize_text(text: str) -> str:

    # Normalize Windows and old Mac line endings
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Remove null characters
    text = text.replace("\x00", "")

    # Remove excessive spaces and tabs
    text = re.sub(
        r"[ \t]+",
        " ",
        text,
    )

    # Limit excessive blank lines
    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text,
    )

    return text.strip()


def normalize_documents(
    documents: list[Document],
) -> list[Document]:

    normalized_documents = []

    for document in documents:

        normalized_content = normalize_text(
            document.page_content
        )

        if not normalized_content:
            continue

        normalized_documents.append(
            Document(
                page_content=normalized_content,
                metadata=document.metadata.copy(),
            )
        )

    return normalized_documents
