from __future__ import annotations

import logging

from devmate.observability import setup_observability
from devmate.rag.vector_store import search_knowledge_base

logger = logging.getLogger(__name__)

def main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        force=True,
    )

    setup_observability()

    query = "project guidelines"
    logger.info("Testing knowledge base search. query=%s", query)

    results = search_knowledge_base(query, k=4)
    logger.info("Knowledge base search returned %s results", len(results))

    for index, doc in enumerate(results, start=1):
        logger.info(
            "Result #%s source=%s content_preview=%s",
            index,
            doc.metadata.get("source", "unknown"),
            doc.page_content[:200].replace("\n", " "),
        )

    return 0