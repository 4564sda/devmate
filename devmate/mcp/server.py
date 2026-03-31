from __future__ import annotations

import logging
from typing import Any

from mcp.server.fastmcp import FastMCP
from tavily import TavilyClient

from devmate.config import load_settings

logger = logging.getLogger(__name__)

mcp = FastMCP("devmate-search-server")

@mcp.tool()
def search_web(query: str, max_results: int = 5) -> dict[str, Any]:
    config = load_settings()

    logger.info(
        "search_web called with query=%s, max_results=%s",
        query,
        max_results,
    )

    effective_max_results = max_results or config.search.max_results

    client = TavilyClient(api_key=config.search.tavily_api_key)

    response = client.search(
        query=query,
        max_results=effective_max_results,
        search_depth=config.search.search_depth,
        topic=config.search.topic,
    )

    results: list[dict[str, Any]] = []
    for item in response.get("results", []):
        results.append(
            {
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "content": item.get("content", ""),
                "score": item.get("score"),
            }
        )

    return {
        "query": query,
        "max_results": effective_max_results,
        "results": results,
        "answer": response.get("answer"),
        "follow_up_questions": response.get("follow_up_questions"),
    }

def run_mcp_server() -> None:
    config = load_settings()
    logger.info(
        "Starting MCP server with Streamable HTTP at %s",
        config.mcp.server_url,
    )
    mcp.run(transport="streamable-http")