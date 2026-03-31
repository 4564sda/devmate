from __future__ import annotations

from langchain_core.embeddings import Embeddings

from devmate.llm import get_model_registry

def get_embedding_model() -> Embeddings:
    registry = get_model_registry()
    return registry.embeddings