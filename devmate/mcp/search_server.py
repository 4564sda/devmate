from __future__ import annotations

import logging
from typing import Any

import httpx
from mcp.server.fastmcp import FastMCP

from devmate.config import get_settings

logger = logging.getLogger(__name__)

settings = get_settings()
mcp = FastMCP(settings.mcp.server_name)

def _build_tavily_payload(
    query: str,
    max_results: int | None = None,
) -> dict[str, Any]:
    search_config = settings.search
    return {
        "query": query,
        "max_results": max_results or search_config.max_results,
        "search_depth": search_config.search_depth,
        "include_answer": search_config.include_answer,
        "include_raw_content": search_config.include_raw_content,
        "topic": search_config.topic,
    }

async def _call_tavily_search(
    query: str,
    max_results: int | None = None,
) -> dict[str, Any]:
    payload = _build_tavily_payload(query=query, max_results=max_results)

    headers = {
        "Authorization": f"Bearer {settings.search.tavily_api_key}",
        "Content-Type": "application/json",
    }

    logger.info(
        "Calling Tavily search API. query=%s max_results=%s",
        query,
        payload["max_results"],
    )

    async with httpx.AsyncClient(timeout=float(settings.mcp.timeout_seconds)) as client:
        response = await client.post(
            "https://api.tavily.com/search",
            headers=headers,
            json=payload,
        )
        response.raise_for_status()
        data = response.json()

    logger.info(
        "Tavily search completed. query=%s result_count=%s",
        query,
        len(data.get("results", [])),
    )
    return data

def _format_tavily_result(data: dict[str, Any]) -> str:
    answer = data.get("answer")
    results = data.get("results", [])

    sections: list[str] = []

    if answer:
        sections.append(f"## Tavily Answer\n{answer}")

    if results:
        formatted_items: list[str] = []
        for index, item in enumerate(results, start=1):
            title = item.get("title", "Untitled")
            url = item.get("url", "")
            content = item.get("content", "")
            formatted_items.append(
                f"### Result {index}\n"
                f"- title: {title}\n"
                f"- url: {url}\n"
                f"- content: {content}"
            )
        sections.append("## Search Results\n" + "\n\n".join(formatted_items))
    else:
        sections.append("## Search Results\nNo results returned.")

    return "\n\n".join(sections)

@mcp.tool()
async def search_web(query: str, max_results: int = 5) -> str:
    """Search the web using Tavily and return a markdown summary."""
    logger.info(
        "MCP tool invoked: search_web query=%s max_results=%s",
        query,
        max_results,
    )
    data = await _call_tavily_search(query=query, max_results=max_results)
    return _format_tavily_result(data)

def run_server() -> None:
    logger.info(
        "Starting MCP search server. host=%s port=%s path=%s transport=streamable-http",
        settings.mcp.host,
        settings.mcp.port,
        settings.mcp.path,
    )
    mcp.run(transport="streamable-http")