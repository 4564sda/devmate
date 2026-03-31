from __future__ import annotations
from .text_loader import TextLoader

import logging
from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from devmate.config import load_settings

logger = logging.getLogger(__name__)

SUPPORTED_EXTENSIONS = {".md", ".txt"}

def load_source_documents() -> list[Document]:
    config = load_settings()
    docs_dir = Path(config.rag.docs_dir)

    if not docs_dir.exists():
        logger.warning("Docs directory does not exist: %s", docs_dir)
        return []

    documents: list[Document] = []

    for path in docs_dir.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        content = path.read_text(encoding="utf-8")
        documents.append(
            Document(
                page_content=content,
                metadata={
                    "source": str(path),
                    "filename": path.name,
                },
            )
        )

    logger.info("Loaded source documents. count=%s", len(documents))
    return documents

def split_documents(documents: list[Document]) -> list[Document]:
    config = load_settings()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.rag.chunk_size,
        chunk_overlap=config.rag.chunk_overlap,
    )

    chunks = splitter.split_documents(documents)
    logger.info("Split documents into chunks. count=%s", len(chunks))
    return chunks