from __future__ import annotations

import logging
from dataclasses import dataclass

from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from devmate.config import Settings

logger = logging.getLogger(__name__)

@dataclass(slots=True)
class ModelRegistry:
    primary_llm: ChatOpenAI
    planner_llm: ChatOpenAI
    embeddings: OpenAIEmbeddings

def build_model_registry(config: Settings) -> ModelRegistry:
    primary_llm = ChatOpenAI(
        model=config.model.model_name,
        api_key=config.model.api_key,
        base_url=config.model.ai_base_url,
        temperature=config.model.temperature,
        max_tokens=config.model.max_tokens,
    )

    planner_llm = ChatOpenAI(
        model=config.model.planner_model_name,
        api_key=config.model.api_key,
        base_url=config.model.ai_base_url,
        temperature=0,
        max_tokens=config.model.max_tokens,
    )

    embeddings = OpenAIEmbeddings(
        model=config.model.embedding_model_name,
        api_key=config.model.api_key,
        base_url=config.model.ai_base_url,
    )

    logger.info(
        "Model registry built. primary=%s planner=%s embedding=%s",
        config.model.model_name,
        config.model.planner_model_name,
        config.model.embedding_model_name,
    )

    return ModelRegistry(
        primary_llm=primary_llm,
        planner_llm=planner_llm,
        embeddings=embeddings,
    )