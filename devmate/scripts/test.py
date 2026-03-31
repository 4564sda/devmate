from __future__ import annotations

import argparse
import logging

from langchain_core.messages import HumanMessage
from langsmith import traceable

from devmate.config import load_settings
from devmate.llm import build_model_registry
from devmate.observability import configure_langsmith

logger = logging.getLogger(__name__)

@traceable(name="devmate_llm_smoke_test", run_type="chain")
def run_llm_smoke_test(user_prompt: str) -> str:
    config = load_settings()
    registry = build_model_registry(config)
    model = registry.primary_llm

    logger.info("Running real LLM invocation for smoke test...")
    response = model.invoke([HumanMessage(content=user_prompt)])

    content = response.content if hasattr(response, "content") else str(response)
    if isinstance(content, list):
        content = " ".join(str(item) for item in content)

    logger.info("LLM invocation completed successfully.")
    logger.info("Smoke test response: %s", content)
    return str(content)

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--prompt",
        default="请用一句话介绍 DevMate 项目当前状态。",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

    config = load_settings()
    configure_langsmith(config)

    logger.info("Starting LangSmith-enabled LLM smoke test...")
    result = run_llm_smoke_test(args.prompt)
    logger.info("Final result: %s", result)

if __name__ == "__main__":
    main()