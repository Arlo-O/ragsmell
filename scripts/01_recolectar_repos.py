"""Collect GitHub candidates without embedding an obsolete extraction date."""

from __future__ import annotations

import csv
import json
import os
import time
from datetime import UTC, datetime, timedelta
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
TOPICS = ["rag", "retrieval-augmented-generation", "langchain", "llamaindex", "chatbot"]
EXTRA_TOPICS = ["llm", "vector-database", "chromadb", "qdrant"]
FIELDS = ["full_name", "stars", "pushed_at", "size_kb", "topics", "description", "url", "star_band"]


def github_get(url: str) -> dict:
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "ragsmell-research"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = Request(url, headers=headers)
    with urlopen(request, timeout=30) as response:
        return json.load(response)


def main() -> None:
    extracted = datetime.now(UTC).replace(microsecond=0)
    since = extracted - timedelta(days=365)
    queries = []
    topics = TOPICS
    for topic in topics:
        for band in ("11..100", "101..1000", ">1000"):
            queries.append(f"topic:{topic} language:python fork:false archived:false pushed:>{since.date()} stars:{band}")
    rows: dict[str, dict] = {}; diagnostics = []
    for query in queries:
        try:
            result = github_get(f"https://api.github.com/search/repositories?q={quote(query)}&per_page=100")
            diagnostics.append({"query": query, "count": result.get("total_count", 0)})
            for item in result.get("items", []):
                stars = int(item.get("stargazers_count", 0))
                band = "11..100" if stars <= 100 else "101..1000" if stars <= 1000 else ">1000"
                rows[item["full_name"]] = {"full_name": item["full_name"], "stars": stars, "pushed_at": item.get("pushed_at", ""), "size_kb": item.get("size", 0), "topics": ";".join(item.get("topics", [])), "description": item.get("description") or "", "url": item["html_url"], "star_band": band}
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
            diagnostics.append({"query": query, "error": f"{type(exc).__name__}: {exc}"})
        time.sleep(0.2)
    data = ROOT / "data"; data.mkdir(exist_ok=True)
    with (data / "repos_candidatos.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS); writer.writeheader(); writer.writerows(sorted(rows.values(), key=lambda row: row["full_name"]))
    metadata = {"fecha_extraccion": extracted.isoformat(), "fecha_corte": since.isoformat(), "queries": diagnostics, "autenticado": bool(os.environ.get("GITHUB_TOKEN")), "topics_iniciales": TOPICS, "topics_ampliacion": EXTRA_TOPICS, "nota": "La elegibilidad RAG se verifica posteriormente; una búsqueda por topic no es prueba definitiva."}
    (data / "metadata_muestra.json").write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"candidatos={len(rows)} consultas={len(queries)} autenticado={metadata['autenticado']}")


if __name__ == "__main__":
    main()
