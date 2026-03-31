# from __future__ import annotations
#
# from dataclasses import dataclass
# from functools import lru_cache
# import logging
# import os
# from pathlib import Path
# from typing import Any
#
# try:
#     import tomllib
# except ModuleNotFoundError:  # pragma: no cover
#     import tomli as tomllib  # type: ignore
#
# logger = logging.getLogger(__name__)
#
# @dataclass(slots=True)
# class ModelSettings:
#     ai_base_url: str
#     api_key: str
#     model_name: str
#     embedding_model_name: str
#     planner_model_name: str
#     temperature: float
#     max_tokens: int
#     embedding_base_url: str | None = None
#     embedding_api_key: str | None = None
#
# @dataclass(slots=True)
# class SearchSettings:
#     tavily_api_key: str
#     max_results: int
#     search_depth: str
#     include_answer: bool
#     include_raw_content: bool
#     topic: str = str
#
# @dataclass(slots=True)
# class LangSmithSettings:
#     langchain_tracing_v2: bool
#     langchain_api_key: str
#     project: str
#     endpoint: str
#
# @dataclass(slots=True)
# class SkillsSettings:
#     skills_dir: str = ".skills"
#
# @dataclass(slots=True)
# class RagSettings:
#     docs_dir: str = str
#     vector_store_dir: str = str
#     chunk_size: int = int
#     chunk_overlap: int = int
#     top_k: int = str
#
# @dataclass(slots=True)
# class McpSettings:
#     host: str
#     port: int
#     path: str
#     server_name: str
#     timeout_seconds: int
#
#     @property
#     def server_url(self) -> str:
#         return f"http://{self.host}:{self.port}{self.path}"
#
# @dataclass(slots=True)
# class Settings:
#     model: ModelSettings
#     search: SearchSettings
#     langsmith: LangSmithSettings
#     skills: SkillsSettings
#     rag: RagSettings
#     mcp: McpSettings
#
# def _get_section(raw: dict[str, Any], name: str) -> dict[str, Any]:
#     value = raw.get(name)
#     if not isinstance(value, dict):
#         raise ValueError(f"Missing or invalid section: [{name}]")
#     return value
#
# def _get_bool_env(name: str, default: bool) -> bool:
#     raw = os.getenv(name)
#     if raw is None:
#         return default
#     return raw.lower() in {"1", "true", "yes", "on"}
#
# def load_settings(config_path: str = "config.toml") -> Settings:
#     path = Path(config_path)
#     if not path.exists():
#         raise FileNotFoundError(f"Config file not found: {config_path}")
#
#     with path.open("rb") as f:
#         raw = tomllib.load(f)
#
#     model_data = _get_section(raw, "model")
#     search_data = _get_section(raw, "search")
#     langsmith_data = _get_section(raw, "langsmith")
#     skills_data = _get_section(raw, "skills")
#     rag_data = _get_section(raw, "rag")
#     mcp_data = _get_section(raw, "mcp")
#
#     model = ModelSettings(
#         ai_base_url=os.getenv("DEVMATE_MODEL_AI_BASE_URL", model_data["ai_base_url"]),
#         api_key=os.getenv("DEVMATE_MODEL_API_KEY", model_data["api_key"]),
#         model_name=os.getenv("DEVMATE_MODEL_NAME", model_data["model_name"]),
#         embedding_model_name=os.getenv(
#             "DEVMATE_EMBEDDING_MODEL_NAME",
#             model_data["embedding_model_name"],
#         ),
#         planner_model_name=os.getenv(
#             "DEVMATE_PLANNER_MODEL_NAME",
#             model_data["planner_model_name"],
#         ),
#         temperature=float(
#             os.getenv(
#                 "DEVMATE_MODEL_TEMPERATURE",
#                 str(model_data.get("temperature", 0.1)),
#             )
#         ),
#         max_tokens=int(
#             os.getenv(
#                 "DEVMATE_MODEL_MAX_TOKENS",
#                 str(model_data.get("max_tokens", 8192)),
#             )
#         ),
#         embedding_base_url=os.getenv(
#             "DEVMATE_EMBEDDING_BASE_URL",
#             model_data.get("embedding_base_url", model_data["ai_base_url"]),
#         ),
#         embedding_api_key=os.getenv(
#             "DEVMATE_EMBEDDING_API_KEY",
#             model_data.get("embedding_api_key", model_data["api_key"]),
#         ),
#     )
#
#     search = SearchSettings(
#         tavily_api_key=os.getenv("TAVILY_API_KEY", search_data["tavily_api_key"]),
#         max_results=int(
#             os.getenv(
#                 "DEVMATE_SEARCH_MAX_RESULTS",
#                 str(search_data.get("max_results", 5)),
#             )
#         ),
#         search_depth=os.getenv(
#             "DEVMATE_SEARCH_DEPTH",
#             search_data.get("search_depth", "basic"),
#         ),
#         topic=os.getenv(
#             "DEVMATE_SEARCH_TOPIC",
#             search_data.get("topic", "general"),
#         ),
#     )
#
#     langsmith = LangSmithSettings(
#         langchain_tracing_v2=_get_bool_env(
#             "LANGCHAIN_TRACING_V2",
#             bool(langsmith_data.get("langchain_tracing_v2", True)),
#         ),
#         langchain_api_key=os.getenv(
#             "LANGCHAIN_API_KEY",
#             langsmith_data["langchain_api_key"],
#         ),
#         project=os.getenv("LANGCHAIN_PROJECT", langsmith_data["project"]),
#         endpoint=os.getenv("LANGCHAIN_ENDPOINT", langsmith_data["endpoint"]),
#     )
#
#     skills = SkillsSettings(
#         skills_dir=os.getenv(
#             "DEVMATE_SKILLS_DIR",
#             skills_data.get("skills_dir", ".skills"),
#         )
#     )
#
#     rag = RagSettings(
#         docs_dir=os.getenv("DEVMATE_DOCS_DIR", rag_data.get("docs_dir", "docs")),
#         vector_store_dir=os.getenv(
#             "DEVMATE_VECTOR_STORE_DIR",
#             rag_data.get("vector_store_dir", ".data/vector_store"),
#         ),
#         chunk_size=int(
#             os.getenv(
#                 "DEVMATE_RAG_CHUNK_SIZE",
#                 str(rag_data.get("chunk_size", 1000)),
#             )
#         ),
#         chunk_overlap=int(
#             os.getenv(
#                 "DEVMATE_RAG_CHUNK_OVERLAP",
#                 str(rag_data.get("chunk_overlap", 200)),
#             )
#         ),
#         top_k=int(
#             os.getenv(
#                 "DEVMATE_RAG_TOP_K",
#                 str(rag_data.get("top_k", 4)),
#             )
#         ),
#     )
#
#     mcp = McpSettings(
#         host=os.getenv("DEVMATE_MCP_HOST", mcp_data.get("host", "127.0.0.1")),
#         port=int(os.getenv("DEVMATE_MCP_PORT", str(mcp_data.get("port", 8001)))),
#         path=os.getenv("DEVMATE_MCP_PATH", mcp_data.get("path", "/mcp")),
#         server_name=os.getenv(
#             "DEVMATE_MCP_SERVER_NAME",
#             mcp_data.get("server_name", "devmate-search"),
#         ),
#         timeout_seconds=int(
#             os.getenv(
#                 "DEVMATE_MCP_TIMEOUT_SECONDS",
#                 str(mcp_data.get("timeout_seconds", 30)),
#             )
#         ),
#     )
#
#     settings = Settings(
#         model=model,
#         search=search,
#         langsmith=langsmith,
#         skills=skills,
#         rag=rag,
#         mcp=mcp,
#     )
#
#     logger.info("Configuration loaded from %s", config_path)
#     return settings
#
# @lru_cache(maxsize=1)
# def get_settings() -> Settings:
#     return load_settings()
#
# def load_config(config_path: str = "config.toml") -> Settings:
#     return load_settings(config_path)

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import logging
import os
from pathlib import Path
from typing import Any

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib  # type: ignore

logger = logging.getLogger(__name__)

@dataclass(slots=True)
class ModelSettings:
    ai_base_url: str
    api_key: str
    model_name: str
    embedding_model_name: str
    planner_model_name: str
    temperature: float
    max_tokens: int
    embedding_base_url: str | None = None
    embedding_api_key: str | None = None

@dataclass(slots=True)
class SearchSettings:
    tavily_api_key: str
    max_results: int
    search_depth: str
    include_answer: bool
    include_raw_content: bool
    topic: str = str

@dataclass(slots=True)
class LangSmithSettings:
    langchain_tracing_v2: bool
    langchain_api_key: str
    project: str
    endpoint: str

@dataclass(slots=True)
class SkillsSettings:
    skills_dir: str = ".skills"

@dataclass(slots=True)
class RagSettings:
    docs_dir: str = str
    vector_store_dir: str = str
    chunk_size: int = int
    chunk_overlap: int = int
    top_k: int = str

@dataclass(slots=True)
class McpSettings:
    host: str
    port: int
    path: str
    server_name: str
    timeout_seconds: int

    @property
    def server_url(self) -> str:
        return f"http://{self.host}:{self.port}{self.path}"

@dataclass(slots=True)
class Settings:
    model: ModelSettings
    search: SearchSettings
    langsmith: LangSmithSettings
    skills: SkillsSettings
    rag: RagSettings
    mcp: McpSettings

def _get_section(raw: dict[str, Any], name: str) -> dict[str, Any]:
    value = raw.get(name)
    if not isinstance(value, dict):
        raise ValueError(f"Missing or invalid section: [{name}]")
    return value

def _get_bool_env(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.lower() in {"1", "true", "yes", "on"}

def load_settings(config_path: str = "config.toml") -> Settings:
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with path.open("rb") as f:
        raw = tomllib.load(f)

    model_data = _get_section(raw, "model")
    search_data = _get_section(raw, "search")
    langsmith_data = _get_section(raw, "langsmith")
    skills_data = _get_section(raw, "skills")
    rag_data = _get_section(raw, "rag")
    mcp_data = _get_section(raw, "mcp")

    model = ModelSettings(
        ai_base_url=os.getenv("DEVMATE_MODEL_AI_BASE_URL", model_data["ai_base_url"]),
        api_key=os.getenv("DEVMATE_MODEL_API_KEY", model_data["api_key"]),
        model_name=os.getenv("DEVMATE_MODEL_NAME", model_data["model_name"]),
        embedding_model_name=os.getenv(
            "DEVMATE_EMBEDDING_MODEL_NAME",
            model_data["embedding_model_name"],
        ),
        planner_model_name=os.getenv(
            "DEVMATE_PLANNER_MODEL_NAME",
            model_data["planner_model_name"],
        ),
        temperature=float(
            os.getenv(
                "DEVMATE_MODEL_TEMPERATURE",
                str(model_data.get("temperature", 0.1)),
            )
        ),
        max_tokens=int(
            os.getenv(
                "DEVMATE_MODEL_MAX_TOKENS",
                str(model_data.get("max_tokens", 8192)),
            )
        ),
        embedding_base_url=os.getenv(
            "DEVMATE_EMBEDDING_BASE_URL",
            model_data.get("embedding_base_url", model_data["ai_base_url"]),
        ),
        embedding_api_key=os.getenv(
            "DEVMATE_EMBEDDING_API_KEY",
            model_data.get("embedding_api_key", model_data["api_key"]),
        ),
    )

    search = SearchSettings(
        tavily_api_key=os.getenv("TAVILY_API_KEY", search_data["tavily_api_key"]),
        max_results=int(
            os.getenv(
                "DEVMATE_SEARCH_MAX_RESULTS",
                str(search_data.get("max_results", 5)),
            )
        ),
        search_depth=os.getenv(
            "DEVMATE_SEARCH_DEPTH",
            search_data.get("search_depth", "basic"),
        ),
        include_answer=_get_bool_env(
            "DEVMATE_SEARCH_INCLUDE_ANSWER",
            bool(search_data.get("include_answer", True)),
        ),
        include_raw_content=_get_bool_env(
            "DEVMATE_SEARCH_INCLUDE_RAW_CONTENT",
            bool(search_data.get("include_raw_content", False)),
        ),
        topic=os.getenv(
            "DEVMATE_SEARCH_TOPIC",
            search_data.get("topic", "general"),
        ),
    )

    langsmith = LangSmithSettings(
        langchain_tracing_v2=_get_bool_env(
            "LANGCHAIN_TRACING_V2",
            bool(langsmith_data.get("langchain_tracing_v2", True)),
        ),
        langchain_api_key=os.getenv(
            "LANGCHAIN_API_KEY",
            langsmith_data["langchain_api_key"],
        ),
        project=os.getenv("LANGCHAIN_PROJECT", langsmith_data["project"]),
        endpoint=os.getenv("LANGCHAIN_ENDPOINT", langsmith_data["endpoint"]),
    )

    skills = SkillsSettings(
        skills_dir=os.getenv(
            "DEVMATE_SKILLS_DIR",
            skills_data.get("skills_dir", ".skills"),
        )
    )

    rag = RagSettings(
        docs_dir=os.getenv("DEVMATE_DOCS_DIR", rag_data.get("docs_dir", "docs")),
        vector_store_dir=os.getenv(
            "DEVMATE_VECTOR_STORE_DIR",
            rag_data.get("vector_store_dir", ".data/vector_store"),
        ),
        chunk_size=int(
            os.getenv(
                "DEVMATE_RAG_CHUNK_SIZE",
                str(rag_data.get("chunk_size", 1000)),
            )
        ),
        chunk_overlap=int(
            os.getenv(
                "DEVMATE_RAG_CHUNK_OVERLAP",
                str(rag_data.get("chunk_overlap", 200)),
            )
        ),
        top_k=int(
            os.getenv(
                "DEVMATE_RAG_TOP_K",
                str(rag_data.get("top_k", 4)),
            )
        ),
    )

    mcp = McpSettings(
        host=os.getenv("DEVMATE_MCP_HOST", mcp_data.get("host", "127.0.0.1")),
        port=int(os.getenv("DEVMATE_MCP_PORT", str(mcp_data.get("port", 8001)))),
        path=os.getenv("DEVMATE_MCP_PATH", mcp_data.get("path", "/mcp")),
        server_name=os.getenv(
            "DEVMATE_MCP_SERVER_NAME",
            mcp_data.get("server_name", "devmate-search"),
        ),
        timeout_seconds=int(
            os.getenv(
                "DEVMATE_MCP_TIMEOUT_SECONDS",
                str(mcp_data.get("timeout_seconds", 30)),
            )
        ),
    )

    settings = Settings(
        model=model,
        search=search,
        langsmith=langsmith,
        skills=skills,
        rag=rag,
        mcp=mcp,
    )

    logger.info("Configuration loaded from %s", config_path)
    return settings

@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return load_settings()

def load_config(config_path: str = "config.toml") -> Settings:
    return load_settings(config_path)