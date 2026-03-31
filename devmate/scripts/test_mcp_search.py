from __future__ import annotations

import asyncio
import logging

from devmate.mcp.search_client import build_mcp_client
from devmate.observability import setup_observability

logger = logging.getLogger(__name__)

async def _run() -> int:
    client = build_mcp_client()

    logger.info("Connecting to MCP server and loading tools")
    tools = await client.get_tools()
    logger.info("Loaded MCP tools: %s", [tool.name for tool in tools])

    target_tool = None
    for tool in tools:
        if tool.name == "search_web":
            target_tool = tool
            break

    if target_tool is None:
        raise RuntimeError("search_web tool not found from MCP server")

    query = "FastAPI best practices 2025"
    logger.info("Invoking MCP tool search_web. query=%s", query)

    result = await target_tool.ainvoke(
        {
            "query": query,
            "max_results": 3,
        }
    )

    logger.info("MCP tool result:\n%s", result)
    return 0

def main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        force=True,
    )
    setup_observability()
    return asyncio.run(_run())