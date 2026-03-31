from __future__ import annotations

import logging
from typing import Any

from tavily import TavilyClient

from devmate.config import Settings

logger = logging.getLogger(__name__)

def search_web_with_tavily(
    config: Settings,
    query: str,
    max_results: int | None = None,
) -> dict[str, Any]:
    if not query.strip():
        raise ValueError("query must not be empty")

    client = TavilyClient(api_key=config.search.tavily_api_key)
    limit = max_results or config.search.max_results

    logger.info(
        "Calling Tavily search. query=%s max_results=%s",
        query,
        limit,
    )

    response = client.search(
        query=query,
        max_results=limit,
        include_answer=True,
        include_raw_content=False,
    )

    results = response.get("results", [])
    normalized_results: list[dict[str, str]] = []

    for item in results:
        normalized_results.append(
            {
                "title": str(item.get("title", "")),
                "url": str(item.get("url", "")),
                "content": str(item.get("content", "")),
            }
        )

    payload = {
        "query": query,
        "answer": response.get("answer", ""),
        "results": normalized_results,
    }

    logger.info(
        "Tavily search completed. query=%s result_count=%s",
        query,
        len(normalized_results),
    )
    return payload