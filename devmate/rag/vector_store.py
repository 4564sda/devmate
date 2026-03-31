from __future__ import annotations

import logging
from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from devmate.config import get_settings
from devmate.llm import get_embeddings

logger = logging.getLogger(__name__)

def _load_documents(docs_dir: Path) -> list[Document]:
    documents: list[Document] = []

    if not docs_dir.exists():
        logger.warning("Docs directory does not exist: %s", docs_dir)
        return documents

    for path in docs_dir.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in {".md", ".txt"}:
            continue

        content = path.read_text(encoding="utf-8")
        documents.append(
            Document(
                page_content=content,
                metadata={"source": str(path)},
            )
        )

    logger.info("Loaded %s source documents from %s", len(documents), docs_dir)
    return documents

def _split_documents(documents: list[Document]) -> list[Document]:
    settings = get_settings()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.rag.chunk_size,
        chunk_overlap=settings.rag.chunk_overlap,
    )
    chunks = splitter.split_documents(documents)
    logger.info("Split documents into %s chunks", len(chunks))
    return chunks

def _get_vector_store() -> Chroma:
    settings = get_settings()
    persist_dir = Path(settings.rag.vector_store_dir)
    persist_dir.mkdir(parents=True, exist_ok=True)

    embeddings = get_embeddings()
    logger.info("Using embedding implementation: %s", type(embeddings).__name__)

    return Chroma(
        collection_name="devmate_kb",
        persist_directory=str(persist_dir),
        embedding_function=embeddings,
    )

def build_knowledge_base() -> int:
    settings = get_settings()
    docs_dir = Path(settings.rag.docs_dir)

    documents = _load_documents(docs_dir)
    if not documents:
        logger.warning("No documents found. Knowledge base build skipped.")
        return 0

    chunks = _split_documents(documents)
    if not chunks:
        logger.warning("No chunks generated. Knowledge base build skipped.")
        return 0

    vector_store = _get_vector_store()

    try:
        existing = vector_store.get()
        ids = existing.get("ids", []) if isinstance(existing, dict) else []
        if ids:
            logger.info("Clearing existing Chroma collection. id_count=%s", len(ids))
            vector_store.delete(ids=ids)
    except Exception as exc:
        logger.warning("Failed to clear existing collection safely: %s", exc)

    vector_store.add_documents(chunks)
    logger.info("Knowledge base build finished. chunk_count=%s", len(chunks))
    return len(chunks)

def search_knowledge_base(query: str, k: int = 4) -> list[Document]:
    vector_store = _get_vector_store()
    results = vector_store.similarity_search(query, k=k)
    logger.info(
        "Knowledge base search finished. query=%s result_count=%s",
        query,
        len(results),
    )
    return results