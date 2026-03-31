# from __future__ import annotations
#
# import logging
# from pathlib import Path
#
# from langchain_community.document_loaders import DirectoryLoader
# from langchain_community.vectorstores import Chroma
# from langchain_core.embeddings import Embeddings
# from langchain_text_splitters import RecursiveCharacterTextSplitter
#
# from devmate.config import get_settings
# from devmate.embeddings import get_embedding_model
# from devmate.rag.retriever import KnowledgeBaseRetriever
# from devmate.rag.text_loader import TextLoader
#
# logger = logging.getLogger(__name__)
#
# def build_vectorstore(
#     docs_dir: str | None = None,
#     embedding_model: Embeddings | None = None,
#     persist_dir: str | None = None,
# ) -> Chroma:
#     settings = get_settings()
#
#     resolved_docs_dir = docs_dir or settings.rag.docs_dir
#     resolved_persist_dir = persist_dir or settings.rag.vector_store_dir
#     resolved_embedding_model = embedding_model or get_embedding_model()
#
#     loader = DirectoryLoader(
#         path=resolved_docs_dir,
#         glob="**/*.md",
#         loader_cls=TextLoader,
#         show_progress=True,
#     )
#     raw_docs = loader.load()
#     logger.info("Loaded %s documents from %s", len(raw_docs), resolved_docs_dir)
#
#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size=settings.rag.chunk_size,
#         chunk_overlap=settings.rag.chunk_overlap,
#         separators=["\n\n", "\n", "。", "；", "：", " ", ""],
#     )
#     splits = splitter.split_documents(raw_docs)
#     logger.info("Split documents into %s chunks", len(splits))
#
#     vectorstore = Chroma.from_documents(
#         documents=splits,
#         embedding=resolved_embedding_model,
#         persist_directory=resolved_persist_dir,
#     )
#     logger.info("Vector store built at %s", resolved_persist_dir)
#     return vectorstore
#
# __all__ = ["build_vectorstore", "KnowledgeBaseRetriever"]

from __future__ import annotations

import logging
from pathlib import Path

from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from devmate.config import get_settings
from devmate.embeddings import get_embedding_model
from devmate.rag.retriever import KnowledgeBaseRetriever

logger = logging.getLogger(__name__)

def _load_markdown_documents(docs_dir: str) -> list[Document]:
    """Load all markdown documents from the given directory."""

    documents: list[Document] = []
    docs_path = Path(docs_dir)

    if not docs_path.exists():
        raise FileNotFoundError(
            f"Docs directory does not exist: {docs_dir}"
        )

    for file_path in docs_path.rglob("*.md"):
        text = file_path.read_text(encoding="utf-8")
        documents.append(
            Document(
                page_content=text,
                metadata={"source": str(file_path)},
            )
        )

    logger.info(
        "Loaded %s markdown documents from %s",
        len(documents),
        docs_dir,
    )
    return documents

def build_vectorstore(
    docs_dir: str | None = None,
    embedding_model: Embeddings | None = None,
    persist_dir: str | None = None,
) -> Chroma:
    """Build a Chroma vector store from local markdown documents."""

    settings = get_settings()

    resolved_docs_dir = docs_dir or settings.rag.docs_dir
    resolved_persist_dir = (
        persist_dir or settings.rag.vector_store_dir
    )
    resolved_embedding_model = (
        embedding_model or get_embedding_model()
    )

    raw_docs = _load_markdown_documents(resolved_docs_dir)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.rag.chunk_size,
        chunk_overlap=settings.rag.chunk_overlap,
        separators=["\n\n", "\n", "。", "；", "：", " ", ""],
    )
    split_docs = splitter.split_documents(raw_docs)

    logger.info(
        "Split documents into %s chunks",
        len(split_docs),
    )

    vectorstore = Chroma.from_documents(
        documents=split_docs,
        embedding=resolved_embedding_model,
        persist_directory=resolved_persist_dir,
    )

    logger.info(
        "Vector store built at %s",
        resolved_persist_dir,
    )
    return vectorstore

__all__ = [
    "KnowledgeBaseRetriever",
    "build_vectorstore",
]