from __future__ import annotations

import logging

from langchain_core.tools import tool

from devmate.rag import KnowledgeBaseRetriever, build_vectorstore

logger = logging.getLogger(__name__)

_vectorstore = None
_retriever = None

def get_retriever() -> KnowledgeBaseRetriever:
    global _vectorstore, _retriever

    if _retriever is None:
        _vectorstore = build_vectorstore()
        _retriever = KnowledgeBaseRetriever(vectorstore=_vectorstore)
        logger.info("Knowledge base retriever initialized")

    return _retriever

@tool
def search_knowledge_base(query: str) -> str:
    """Search the local knowledge base (docs/) for relevant information."""
    retriever = get_retriever()
    docs = retriever.invoke(query)

    if not docs:
        return "No relevant documents found."

    result = "\n\n".join(
        f"### {index + 1}. {doc.metadata.get('source', 'unknown')}\n{doc.page_content}"
        for index, doc in enumerate(docs)
    )
    logger.info(
        "Knowledge base search completed. query=%s result_count=%s",
        query,
        len(docs),
    )
    return result