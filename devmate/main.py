import logging

from devmate.config import ConfigError, load_settings

logger = logging.getLogger(__name__)

def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

def main() -> None:
    setup_logging()

    try:
        settings = load_settings()
    except ConfigError:
        logger.exception("Failed to load application configuration.")
        raise

    logger.info("DevMate bootstrap started.")
    logger.info("Main model: %s", settings.model.model_name)
    logger.info("Embedding model: %s", settings.model.embedding_model_name)
    logger.info("Planner model: %s", settings.model.planner_model_name)
    logger.info("Skills dir: %s", settings.skills.skills_dir)
    logger.info("RAG docs dir: %s", settings.rag.docs_dir)