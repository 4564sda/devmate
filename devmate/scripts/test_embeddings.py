# from __future__ import annotations
#
# import json
# import logging
#
# from devmate.config import load_config
# from devmate.llm import get_embeddings
# from devmate.observability import setup_observability
#
# logger = logging.getLogger(__name__)
#
# def main() -> None:
#     setup_observability()
#
#     settings = load_config()
#     embeddings = get_embeddings()
#
#     logger.info(
#         "Testing embeddings with base_url=%s, embedding_model=%s",
#         settings.model.ai_base_url,
#         settings.model.embedding_model_name,
#     )
#
#     vectors = embeddings.embed_documents(
#         [
#             "DevMate is an AI coding assistant.",
#             "RAG uses embeddings and vector search.",
#         ]
#     )
#
#     result = {
#         "vector_count": len(vectors),
#         "vector_dim": len(vectors[0]) if vectors else 0,
#     }
#
#     logger.info("Embedding test succeeded: %s", json.dumps(result))

from __future__ import annotations

import json
import logging

from devmate.config import get_settings
from devmate.llm import get_embeddings
from devmate.observability import setup_observability

logger = logging.getLogger(__name__)

def main() -> None:
    setup_observability()

    settings = get_settings()
    embeddings = get_embeddings()

    logger.info(
        "Testing embeddings with base_url=%s, embedding_model=%s",
        settings.model.embedding_base_url or settings.model.ai_base_url,
        settings.model.embedding_model_name,
    )

    vectors = embeddings.embed_documents(
        [
            "DevMate is an AI coding assistant.",
            "RAG uses embeddings and vector search.",
        ]
    )

    result = {
        "vector_count": len(vectors),
        "vector_dim": len(vectors[0]) if vectors else 0,
    }
    logger.info("Embedding test succeeded: %s", json.dumps(result))