from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import tomllib

logger = logging.getLogger(__name__)

@dataclass(slots=True)
class ModelSettings:
    ai_base_url: str
    api_key: str
    model_name: str
    embedding_model_name: str
    planner_model_name: str
    temperature: float = 0.1
    max_tokens: int = 8192

@dataclass(slots=True)
class SearchSettings:
    tavily_api_key: str = ""
    max_results: int = 5

@dataclass(slots=True)
class LangSmithSettings:
    langchain_tracing_v2: bool = True
    langchain_api_key: str = ""
    project: str = "devmate"
    endpoint: str = "https://api.smith.langchain.com"

@dataclass(slots=True)
class SkillsSettings:
    skills_dir: str = ".skills"

@dataclass(slots=True)
class RagSettings:
    docs_dir: str = "docs"
    vector_store_dir: str = ".data/vector_store"
    chunk_size: int = 1000
    chunk_overlap: int = 200
    top_k: int = 4

@dataclass(slots=True)
class Settings:
    model: ModelSettings
    search: SearchSettings
    langsmith: LangSmithSettings
    skills: SkillsSettings
    rag: RagSettings

def _read_toml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")
    with path.open("rb") as file:
        return tomllib.load(file)

def _get_secret(raw_value: str, env_name: str) -> str:

    return os.getenv(env_name, raw_value)

def load_config(path: str = "config.toml") -> Settings:
    config_path = Path(path)
    raw = _read_toml(config_path)

    model_raw = raw.get("model", {})
    search_raw = raw.get("search", {})
    langsmith_raw = raw.get("langsmith", {})
    skills_raw = raw.get("skills", {})
    rag_raw = raw.get("rag", {})

    settings = Settings(
        model=ModelSettings(
            ai_base_url=model_raw["ai_base_url"],
            api_key=_get_secret(model_raw.get("api_key", ""), "DEVMATE_MODEL_API_KEY"),
            model_name=model_raw["model_name"],
            embedding_model_name=model_raw["embedding_model_name"],
            planner_model_name=model_raw["planner_model_name"],
            temperature=float(model_raw.get("temperature", 0.1)),
            max_tokens=int(model_raw.get("max_tokens", 8192)),
        ),
        search=SearchSettings(
            tavily_api_key=_get_secret(
                search_raw.get("tavily_api_key", ""),
                "TAVILY_API_KEY",
            ),
            max_results=int(search_raw.get("max_results", 5)),
        ),
        langsmith=LangSmithSettings(
            langchain_tracing_v2=bool(
                langsmith_raw.get("langchain_tracing_v2", True)
            ),
            langchain_api_key=_get_secret(
                langsmith_raw.get("langchain_api_key", ""),
                "LANGCHAIN_API_KEY",
            ),
            project=langsmith_raw.get("project", "devmate"),
            endpoint=langsmith_raw.get(
                "endpoint",
                "https://api.smith.langchain.com",
            ),
        ),
        skills=SkillsSettings(
            skills_dir=skills_raw.get("skills_dir", ".skills"),
        ),
        rag=RagSettings(
            docs_dir=rag_raw.get("docs_dir", "docs"),
            vector_store_dir=rag_raw.get(
                "vector_store_dir",
                ".data/vector_store",
            ),
            chunk_size=int(rag_raw.get("chunk_size", 1000)),
            chunk_overlap=int(rag_raw.get("chunk_overlap", 200)),
            top_k=int(rag_raw.get("top_k", 4)),
        ),
    )

    logger.info("Configuration loaded from %s", config_path)
    return settings