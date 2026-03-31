import logging
from devmate.tools.knowledge_base import search_knowledge_base

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    logger.info("Testing search_knowledge_base with query: 'project guidelines'")
    result = search_knowledge_base.invoke({"query": "project guidelines"})
    logger.info("RAG result:\n%s", result)

if __name__ == "__main__":
    main()