from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

import httpx
from langchain_core.embeddings import Embeddings

logger = logging.getLogger(__name__)

@dataclass(slots=True)
class HttpEmbeddings(Embeddings):
    base_url: str
    api_key: str
    model: str
    timeout_seconds: int = 60

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def _endpoint(self) -> str:
        return f"{self.base_url.rstrip('/')}/embeddings"

    def _payload(self, input_texts: list[str]) -> dict[str, Any]:
        return {
            "model": self.model,
            "input": input_texts,
        }

    def _extract_embeddings(self, data: Any) -> list[list[float]]:
        if not isinstance(data, dict):
            raise ValueError("Embedding response is not a JSON object")

        if "data" in data and isinstance(data["data"], list):
            items = data["data"]
            vectors: list[list[float]] = []
            for item in items:
                if isinstance(item, dict) and "embedding" in item:
                    embedding = item["embedding"]
                    if isinstance(embedding, list):
                        vectors.append([float(x) for x in embedding])
            if vectors:
                return vectors

        if "embeddings" in data and isinstance(data["embeddings"], list):
            items = data["embeddings"]
            if items and isinstance(items[0], list):
                return [[float(x) for x in item] for item in items]
            if items and isinstance(items[0], dict) and "embedding" in items[0]:
                return [
                    [float(x) for x in item["embedding"]]
                    for item in items
                    if isinstance(item, dict) and isinstance(item.get("embedding"), list)
                ]

        if "vectors" in data and isinstance(data["vectors"], list):
            items = data["vectors"]
            if items and isinstance(items[0], list):
                return [[float(x) for x in item] for item in items]
            if items and isinstance(items[0], dict) and "embedding" in items[0]:
                return [
                    [float(x) for x in item["embedding"]]
                    for item in items
                    if isinstance(item, dict) and isinstance(item.get("embedding"), list)
                ]
            if items and isinstance(items[0], dict) and "vector" in items[0]:
                return [
                    [float(x) for x in item["vector"]]
                    for item in items
                    if isinstance(item, dict) and isinstance(item.get("vector"), list)
                ]

        if "embedding" in data and isinstance(data["embedding"], list):
            return [[float(x) for x in data["embedding"]]]

        if "vector" in data and isinstance(data["vector"], list):
            return [[float(x) for x in data["vector"]]]

        logger.error("Unsupported embedding response keys: %s", list(data.keys()))
        raise ValueError("No embedding data received")

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []

        payload = self._payload(texts)
        endpoint = self._endpoint()

        logger.info(
            "Requesting embeddings. endpoint=%s model=%s text_count=%s",
            endpoint,
            self.model,
            len(texts),
        )

        with httpx.Client(timeout=self.timeout_seconds) as client:
            response = client.post(
                endpoint,
                headers=self._headers(),
                json=payload,
            )

        response.raise_for_status()

        json_data = response.json()
        logger.info(
            "Embedding response received. top_level_keys=%s",
            list(json_data.keys()) if isinstance(json_data, dict) else type(json_data).__name__,
        )

        vectors = self._extract_embeddings(json_data)
        logger.info(
            "Parsed embeddings successfully. vector_count=%s vector_dim=%s",
            len(vectors),
            len(vectors[0]) if vectors else 0,
        )
        return vectors

    def embed_query(self, text: str) -> list[float]:
        vectors = self.embed_documents([text])
        if not vectors:
            raise ValueError("No query embedding returned")
        return vectors[0]