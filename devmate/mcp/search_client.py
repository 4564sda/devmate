from __future__ import annotations

from langchain_mcp_adapters.client import MultiServerMCPClient

from devmate.config import get_settings

def build_mcp_client() -> MultiServerMCPClient:
    settings = get_settings()

    server_url = (
        f"http://{settings.mcp.host}:"
        f"{settings.mcp.port}"
        f"{settings.mcp.path}"
    )

    return MultiServerMCPClient(
        {
            settings.mcp.server_name: {
                "transport": "streamable_http",
                "url": server_url,
            }
        }
    )