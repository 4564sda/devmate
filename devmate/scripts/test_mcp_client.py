from __future__ import annotations

import asyncio
import logging

from devmate.config import load_settings
from devmate.mcp.client import get_mcp_tools

logger = logging.getLogger(__name__)

async def main_async() -> None:
    config = load_settings()
    tools = await get_mcp_tools(config)

    tool_map = {tool.name: tool for tool in tools}
    if "search_web" not in tool_map:
        raise RuntimeError("search_web tool not found from MCP server")

    search_tool = tool_map["search_web"]
    logger.info("Invoking MCP tool: %s", search_tool.name)

    result = await search_tool.ainvoke(
        {
            "query": "LangChain MCP adapters streamable http example",
            "max_results": 3,
        }
    )

    logger.info("MCP tool result: %s", result)

def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
    asyncio.run(main_async())

if __name__ == "__main__":
    main()