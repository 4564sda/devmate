from __future__ import annotations

from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever

from devmate.config import get_settings

class KnowledgeBaseRetriever(BaseRetriever):
    vectorstore: Chroma

    def _get_relevant_documents(self, query: str) -> list[Document]:
        settings = get_settings()
        return self.vectorstore.similarity_search(query, k=settings.rag.top_k)

    async def _aget_relevant_documents(self, query: str) -> list[Document]:
        settings = get_settings()
        return await self.vectorstore.asimilarity_search(query, k=settings.rag.top_k)