"""Verify local README/source evidence for the acquired sample.

This is a conservative evidence pass, not an AST analysis. It prevents a
technology declaration alone from being treated as proof of a GenAI/RAG
application.
"""

from __future__ import annotations

import csv
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
LLM_HINTS = ("openai", "anthropic", "llama", "langchain", "llm", "generative", "chatgpt", "mistral", "huggingface")
RETRIEVAL_HINTS = ("retriev", "vector", "chroma", "qdrant", "weaviate", "pinecone", "haystack", "embedding", "knowledge base")
EXCLUDED = {".git", ".venv", "venv", "node_modules", "tests", "docs", "examples", "build", "dist"}


def git_sha(path: Path) -> str:
    return subprocess.check_output(["git", "-C", str(path), "rev-parse", "HEAD"], text=True, stderr=subprocess.STDOUT).strip()


def main() -> None:
    selected = list(csv.DictReader((DATA / "repos_seleccionados.csv").open(encoding="utf-8")))
    results = []
    for row in selected:
        clone = DATA / "clones" / row["full_name"].replace("/", "__")
        evidence: list[str] = []
        if not clone.is_dir():
            results.append({"full_name": row["full_name"], "status": "PENDIENTE_DE_VERIFICACIÓN", "sha_match": "false", "readme_evidence": "", "llm_evidence": "", "retrieval_evidence": "", "reason": "clone_missing"})
            continue
        actual = git_sha(clone)
        sha_match = actual == row["commit_sha"]
        readme_text = ""
        for name in ("README.md", "README.rst", "README"):
            path = clone / name
            if path.exists():
                readme_text += path.read_text(encoding="utf-8", errors="ignore").lower()
        llm_hits: set[str] = set()
        retrieval_hits: set[str] = set()
        for path in clone.rglob("*.py"):
            if any(part.lower() in EXCLUDED for part in path.relative_to(clone).parts[:-1]):
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="ignore").lower()
            except OSError:
                continue
            llm_hits.update(hint for hint in LLM_HINTS if hint in text)
            retrieval_hits.update(hint for hint in RETRIEVAL_HINTS if hint in text)
            if len(llm_hits) >= 2 and len(retrieval_hits) >= 2:
                break
        if any(hint in readme_text for hint in LLM_HINTS):
            evidence.append("README:LLM")
        if any(hint in readme_text for hint in RETRIEVAL_HINTS):
            evidence.append("README:retrieval")
        status = "CUMPLE" if sha_match and llm_hits and retrieval_hits else "NO_CUMPLE" if sha_match else "PENDIENTE_DE_VERIFICACIÓN"
        reason = "" if status == "CUMPLE" else "sha_mismatch" if not sha_match else "no_evidencia_conjunta_LLM_RAG"
        results.append({"full_name": row["full_name"], "status": status, "sha_match": str(sha_match).lower(), "readme_evidence": ";".join(evidence), "llm_evidence": ";".join(sorted(llm_hits)), "retrieval_evidence": ";".join(sorted(retrieval_hits)), "reason": reason})
    with (DATA / "evidencia_relevancia.csv").open("w", newline="", encoding="utf-8") as handle:
        fields = ["full_name", "status", "sha_match", "readme_evidence", "llm_evidence", "retrieval_evidence", "reason"]; writer = csv.DictWriter(handle, fieldnames=fields); writer.writeheader(); writer.writerows(results)
    print(f"verificados={len(results)} cumple={sum(item['status'] == 'CUMPLE' for item in results)} pendientes={sum(item['status'] == 'PENDIENTE_DE_VERIFICACIÓN' for item in results)} no_cumple={sum(item['status'] == 'NO_CUMPLE' for item in results)}")


if __name__ == "__main__":
    main()
