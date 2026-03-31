from __future__ import annotations

import logging

from devmate.config import  load_config
from devmate.llm import build_model_registry
from devmate.observability import configure_langsmith

logger = logging.getLogger(__name__)

def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

def main() -> None:
    setup_logging()

    try:
        settings = load_config()
        configure_langsmith(settings.langsmith)
        registry = build_model_registry(settings.model)

    except Exception:
        logger.exception("Failed during DevMate bootstrap.")
        raise

    logger.info("DevMate bootstrap started.")
    logger.info("Primary model ready: %s", settings.model.model_name)
    logger.info("Planner model ready: %s", settings.model.planner_model_name)
    logger.info("Embedding model ready: %s", settings.model.embedding_model_name)
    logger.info("Skills dir configured: %s", settings.skills.skills_dir)
    logger.info("RAG docs dir configured: %s", settings.rag.docs_dir)
    logger.info(
        "Model clients initialized successfully: primary=%s planner=%s embeddings=%s",
        type(registry.primary_llm).__name__,
        type(registry.planner_llm).__name__,
        type(registry.embeddings).__name__,
    )