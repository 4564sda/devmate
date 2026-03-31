from __future__ import annotations

import logging
import os

from devmate.config import Settings

logger = logging.getLogger(__name__)

def configure_langsmith(config: Settings) -> None:
    tracing_enabled = (
        "true" if config.langsmith.langchain_tracing_v2 else "false"
    )

    os.environ["LANGCHAIN_TRACING_V2"] = tracing_enabled
    os.environ["LANGCHAIN_API_KEY"] = config.langsmith.langchain_api_key
    os.environ["LANGCHAIN_PROJECT"] = config.langsmith.project
    os.environ["LANGCHAIN_ENDPOINT"] = config.langsmith.endpoint

    os.environ["LANGSMITH_TRACING"] = tracing_enabled
    os.environ["LANGSMITH_API_KEY"] = config.langsmith.langchain_api_key
    os.environ["LANGSMITH_PROJECT"] = config.langsmith.project
    os.environ["LANGSMITH_ENDPOINT"] = config.langsmith.endpoint

    logger.info(
        "LangSmith configured. project=%s endpoint=%s tracing=%s",
        config.langsmith.project,
        config.langsmith.endpoint,
        tracing_enabled,
    )