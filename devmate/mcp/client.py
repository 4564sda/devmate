from __future__ import annotations

import logging
from collections.abc import Sequence

from langchain_core.tools import BaseTool
from langchain_mcp_adapters.client import MultiServerMCPClient

from devmate.config import Settings, load_settings

logger = logging.getLogger(__name__)

async def get_mcp_tools(
    config: Settings | None = None,
) -> Sequence[BaseTool]:
    settings = config or load_settings()

    logger.info(
        "Connecting MCP client via Streamable HTTP. url=%s",
        settings.mcp.server_url,
    )

    client = MultiServerMCPClient(
        {
            settings.mcp.server_name: {
                "transport": "streamable_http",
                "url": settings.mcp.server_url,
            }
        }
    )

    tools = await client.get_tools()
    logger.info("Loaded MCP tools. count=%s", len(tools))
    return tools