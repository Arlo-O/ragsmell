"""Expand the candidate universe using authenticated GitHub searches.

The original candidate CSV is read but never overwritten. New search results
are deduplicated by ``full_name`` and written to a separate expanded CSV.
"""

from __future__ import annotations

import csv
import json
import os
import time
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from github import Auth, Github
from github.GithubException import GithubException, RateLimitExceededException

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
FIELDS = ["full_name", "stars", "pushed_at", "size_kb", "topics", "description", "url", "star_band"]
TECHNOLOGY_QUERIES = [
    "langchain OR llamaindex OR chromadb OR qdrant",
    "weaviate OR pinecone OR haystack OR vector database",
    "retrieval-augmented-generation OR RAG application OR LLM application",
]
BANDS = ("11..100", "101..1000", ">1000")


def get_page(client: Github, query: str) -> list[Any]:
    for attempt in range(3):
        try:
            return client.search_repositories(query=query, sort="updated", order="desc").get_page(0)
        except RateLimitExceededException as exc:
            if attempt == 2:
                raise
            reset = getattr(exc, "headers", {}).get("x-ratelimit-reset")
            delay = max(2.0, float(reset) - time.time() + 1) if reset else 2**attempt
            if delay > 30:
                raise
            time.sleep(delay)
        except GithubException as exc:
            if exc.status in {403, 429} and attempt < 2:
                time.sleep(2**attempt)
                continue
            raise
    return []


def row(item: Any) -> dict[str, Any]:
    stars = int(item.stargazers_count)
    band = "11..100" if stars <= 100 else "101..1000" if stars <= 1000 else ">1000"
    topics = item.raw_data.get("topics", []) if hasattr(item, "raw_data") else []
    return {"full_name": item.full_name, "stars": stars, "pushed_at": item.pushed_at.isoformat() if item.pushed_at else "", "size_kb": item.size, "topics": ";".join(topics), "description": item.description or "", "url": item.html_url, "star_band": band}


def main() -> None:
    load_dotenv(ROOT / ".env")
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise SystemExit("GITHUB_TOKEN no disponible")
    client = Github(auth=Auth.Token(token), per_page=100, retry=0, timeout=15)
    extracted = datetime.now(UTC).replace(microsecond=0)
    since = extracted - timedelta(days=365)
    original_path = DATA / "repos_candidatos.csv"
    original = list(csv.DictReader(original_path.open(encoding="utf-8"))) if original_path.exists() else []
    candidates = {item["full_name"]: item for item in original}
    diagnostics = []
    for technology in TECHNOLOGY_QUERIES:
        for band in BANDS:
            query = f"{technology} language:python fork:false archived:false pushed:>{since.date()} stars:{band}"
            try:
                items = get_page(client, query)
                for item in items:
                    candidates[item.full_name] = row(item)
                diagnostics.append({"query": query, "count": len(items), "status": "CUMPLE_API"})
            except (GithubException, OSError, TimeoutError) as exc:
                diagnostics.append({"query": query, "count": 0, "status": "PENDIENTE_DE_VERIFICACIÓN", "error": type(exc).__name__})
    output = DATA / "repos_candidatos_ampliados.csv"
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS); writer.writeheader(); writer.writerows(sorted(candidates.values(), key=lambda item: item["full_name"]))
    metadata_path = DATA / "metadata_muestra.json"
    metadata = json.loads(metadata_path.read_text(encoding="utf-8")) if metadata_path.exists() else {}
    metadata["ampliacion"] = {"fecha_extraccion": extracted.isoformat(), "fecha_corte": since.isoformat(), "tecnologias": TECHNOLOGY_QUERIES, "franjas": BANDS, "consultas": diagnostics, "candidatos_originales": len(original), "candidatos_ampliados": len(candidates), "deduplicacion": "full_name", "autenticado": True}
    metadata_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"originales={len(original)} ampliados={len(candidates)} consultas={len(diagnostics)}")


if __name__ == "__main__":
    main()
