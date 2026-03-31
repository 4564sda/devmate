from __future__ import annotations

import logging
from dataclasses import dataclass
from functools import lru_cache

from langchain_openai import ChatOpenAI

from devmate.config import Settings, get_settings
from devmate.embeddings.http_embeddings import HttpEmbeddings

logger = logging.getLogger(__name__)

@dataclass(slots=True)
class ModelRegistry:
    primary_llm: ChatOpenAI
    planner_llm: ChatOpenAI
    embeddings: HttpEmbeddings

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

    embeddings = HttpEmbeddings(
        model=config.model.embedding_model_name,
        api_key=config.model.embedding_api_key or config.model.api_key,
        base_url=config.model.embedding_base_url or config.model.ai_base_url,
    )

    logger.info(
        "Model registry built. primary=%s planner=%s embedding=%s embedding_class=%s",
        config.model.model_name,
        config.model.planner_model_name,
        config.model.embedding_model_name,
        type(embeddings).__name__,
    )

    return ModelRegistry(
        primary_llm=primary_llm,
        planner_llm=planner_llm,
        embeddings=embeddings,
    )

@lru_cache(maxsize=1)
def get_model_registry() -> ModelRegistry:
    settings = get_settings()
    return build_model_registry(settings)

def get_primary_llm() -> ChatOpenAI:
    return get_model_registry().primary_llm

def get_planner_llm() -> ChatOpenAI:
    return get_model_registry().planner_llm

def get_embeddings() -> HttpEmbeddings:
    return get_model_registry().embeddings