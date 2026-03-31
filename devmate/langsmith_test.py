from __future__ import annotations

import logging
import time

from langsmith import Client, traceable

from devmate.config import load_config
from devmate.observability import configure_langsmith

logger = logging.getLogger(__name__)

@traceable(name="devmate_langsmith_ping", run_type="chain")
def ping_langsmith(text: str) -> str:
    logger.info("Inside traced function. text=%s", text)
    return f"pong: {text}"

def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

    config = load_config()
    configure_langsmith(config)

    client = Client()
    logger.info("LangSmith client initialized: %s", client)

    result = ping_langsmith("hello langsmith")
    logger.info("Ping result: %s", result)

    # 给后台一点上报时间
    time.sleep(3)
    logger.info("LangSmith smoke test finished.")

if __name__ == "__main__":
    main()