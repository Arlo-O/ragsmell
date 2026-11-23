"""Apply auditable preselection criteria to collected candidates.

This script deliberately records unknown API evidence as pending instead of
classifying a repository as eligible by assumption.
"""
from __future__ import annotations

import csv
import json
import os
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
BLOCK_WORDS = {"tutorial", "course", "workshop", "awesome", "example", "demo", "cookbook", "notebook", "template"}
TECHNOLOGIES = {"langchain", "llama-index", "llama_index", "chromadb", "qdrant"}


def get(url: str) -> dict:
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "ragsmell-research"}
    if token := os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = f"Bearer {token}"
    with urlopen(Request(url, headers=headers), timeout=30) as response:
        return json.load(response)


def main() -> None:
    data = ROOT / "data"; candidates = list(csv.DictReader((data / "repos_candidatos.csv").open(encoding="utf-8"))) if (data / "repos_candidatos.csv").exists() else []
    candidates.sort(key=lambda row: (-int(row["stars"]), row["full_name"]))
    preselected = []; excluded = []
    for row in candidates:
        now = datetime.now(UTC).isoformat(); text = f"{row['full_name']} {row['description']}".lower()
        blocked = next((word for word in BLOCK_WORDS if word in text), None)
        if blocked:
            excluded.append({"full_name": row["full_name"], "reason": f"blocked_word:{blocked}", "evidence": text, "checked_at": now}); continue
        if int(row.get("size_kb", 0)) < 500:
            excluded.append({"full_name": row["full_name"], "reason": "size_lt_500_kb", "evidence": row.get("size_kb", ""), "checked_at": now}); continue
        preselected.append(row)
    fields = list(candidates[0]) if candidates else ["full_name", "stars", "pushed_at", "size_kb", "topics", "description", "url", "star_band"]
    with (data / "repos_preseleccion.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields); writer.writeheader(); writer.writerows(preselected[:40])
    with (data / "repos_excluidos.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["full_name", "reason", "evidence", "checked_at"]); writer.writeheader(); writer.writerows(excluded)
    # Selection is intentionally conservative: API-manifest evidence is required.
    selected = []; decisions = []
    for row in preselected[:40]:
        owner, repo = row["full_name"].split("/", 1); evidence = []; dependency_ok = False
        try:
            tree = get(f"https://api.github.com/repos/{quote(owner)}/{quote(repo)}/git/trees/HEAD?recursive=1")
            names = [item.get("path", "") for item in tree.get("tree", [])]
            for name in names:
                if Path(name).name.lower().startswith(("requirements", "pyproject.toml", "setup.py")) and "/" not in name:
                    try:
                        blob = get(f"https://api.github.com/repos/{owner}/{repo}/contents/{quote(name)}")
                        content = json.dumps(blob).lower()
                        if any(tech in content for tech in TECHNOLOGIES): dependency_ok = True; evidence.append(name)
                    except (OSError, ValueError, KeyError) as exc: evidence.append(f"PENDIENTE_DE_VERIFICACIÓN:{name}:{type(exc).__name__}")
        except (OSError, ValueError, KeyError) as exc: evidence.append(f"PENDIENTE_DE_VERIFICACIÓN:tree:{type(exc).__name__}")
        included = dependency_ok
        decision = {"full_name": row["full_name"], "incluido": str(included).lower(), "criterios_cumplidos": "manifest_relevant" if included else "PENDIENTE_DE_VERIFICACIÓN", "evidencia": ";".join(evidence), "motivo": "" if included else "No se verificó manifiesto relevante accesible", "star_band": row["star_band"]}
        decisions.append(decision)
        if included: selected.append({"full_name": row["full_name"], "url": row["url"], "stars": row["stars"], "commit_sha": ""})
    with (data / "decision_muestra.csv").open("w", newline="", encoding="utf-8") as handle:
        fields = ["full_name", "incluido", "criterios_cumplidos", "evidencia", "motivo", "star_band"]; writer = csv.DictWriter(handle, fieldnames=fields); writer.writeheader(); writer.writerows(decisions)
    with (data / "repos_seleccionados.csv").open("w", newline="", encoding="utf-8") as handle:
        fields = ["full_name", "url", "stars", "commit_sha"]; writer = csv.DictWriter(handle, fieldnames=fields); writer.writeheader(); writer.writerows(selected)
    print(f"candidatos={len(candidates)} preseleccionados={len(preselected[:40])} incluidos={len(selected)}")


if __name__ == "__main__":
    main()
