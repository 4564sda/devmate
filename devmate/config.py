from __future__ import annotations

from dataclasses import dataclass
import logging
from pathlib import Path
import tomllib

logger = logging.getLogger(__name__)

DEFAULT_CONFIG_PATH = Path("config.toml")

@dataclass(slots=True)
class ModelConfig:
    ai_base_url: str
    api_key: str
    model_name: str
    embedding_model_name: str
    planner_model_name: str
    temperature: float
    max_tokens: int

@dataclass(slots=True)
class SearchConfig:
    tavily_api_key: str
    max_results: int

@dataclass(slots=True)
class LangSmithConfig:
    langchain_tracing_v2: bool
    langchain_api_key: str
    project: str
    endpoint: str

@dataclass(slots=True)
class SkillsConfig:
    skills_dir: str = ".skills"

@dataclass(slots=True)
class RagConfig:
    docs_dir: str
    vector_store_dir: str
    chunk_size: int
    chunk_overlap: int
    top_k: int

@dataclass(slots=True)
class Settings:
    model: ModelConfig
    search: SearchConfig
    langsmith: LangSmithConfig
    skills: SkillsConfig
    rag: RagConfig

class ConfigError(Exception):
    """Raised when the configuration file is missing or invalid."""

def _require_section(data: dict, section_name: str) -> dict:
    section = data.get(section_name)
    if not isinstance(section, dict):
        raise ConfigError(f"Missing or invalid section: [{section_name}]")
    return section

def _require_value(section: dict, key: str, section_name: str):
    value = section.get(key)
    if value is None:
        raise ConfigError(f"Missing required key '{key}' in section [{section_name}]")
    return value

def load_settings(config_path: str | Path = DEFAULT_CONFIG_PATH) -> Settings:
    path = Path(config_path)

    if not path.exists():
        raise ConfigError(
            f"Config file not found: {path}. "
            "Please copy config.toml.example to config.toml and update values."
        )

    with path.open("rb") as file:
        raw_data = tomllib.load(file)

    model_section = _require_section(raw_data, "model")
    search_section = _require_section(raw_data, "search")
    langsmith_section = _require_section(raw_data, "langsmith")
    skills_section = _require_section(raw_data, "skills")
    rag_section = _require_section(raw_data, "rag")

    settings = Settings(
        model=ModelConfig(
            ai_base_url=str(_require_value(model_section, "ai_base_url", "model")),
            api_key=str(_require_value(model_section, "api_key", "model")),
            model_name=str(_require_value(model_section, "model_name", "model")),
            embedding_model_name=str(
                _require_value(model_section, "embedding_model_name", "model")
            ),
            planner_model_name=str(
                _require_value(model_section, "planner_model_name", "model")
            ),
            temperature=float(_require_value(model_section, "temperature", "model")),
            max_tokens=int(_require_value(model_section, "max_tokens", "model")),
        ),
        search=SearchConfig(
            tavily_api_key=str(
                _require_value(search_section, "tavily_api_key", "search")
            ),
            max_results=int(_require_value(search_section, "max_results", "search")),
        ),
        langsmith=LangSmithConfig(
            langchain_tracing_v2=bool(
                _require_value(
                    langsmith_section,
                    "langchain_tracing_v2",
                    "langsmith",
                )
            ),
            langchain_api_key=str(
                _require_value(langsmith_section, "langchain_api_key", "langsmith")
            ),
            project=str(_require_value(langsmith_section, "project", "langsmith")),
            endpoint=str(_require_value(langsmith_section, "endpoint", "langsmith")),
        ),
        skills=SkillsConfig(
            skills_dir=str(_require_value(skills_section, "skills_dir", "skills"))
        ),
        rag=RagConfig(
            docs_dir=str(_require_value(rag_section, "docs_dir", "rag")),
            vector_store_dir=str(
                _require_value(rag_section, "vector_store_dir", "rag")
            ),
            chunk_size=int(_require_value(rag_section, "chunk_size", "rag")),
            chunk_overlap=int(_require_value(rag_section, "chunk_overlap", "rag")),
            top_k=int(_require_value(rag_section, "top_k", "rag")),
        ),
    )

    logger.info("Configuration loaded from %s", path)
    return settings