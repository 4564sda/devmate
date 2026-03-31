# from __future__ import annotations
# #二阶段
# import logging
#
# from devmate.mcp.server import run_mcp_server
#
# def main() -> None:
#     logging.basicConfig(
#         level=logging.INFO,
#         format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
#     )
#     run_mcp_server()
#
# if __name__ == "__main__":
#     main()

from __future__ import annotations

import logging

from devmate.mcp.search_server import run_server
from devmate.observability import setup_observability

def main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        force=True,
    )
    setup_observability()
    run_server()
    return 0
