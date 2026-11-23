"""Apply auditable preselection criteria without inventing eligibility evidence."""

from __future__ import annotations

import csv
import json
import os
from datetime import UTC, datetime
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
BLOCK_WORDS = {"tutorial", "course", "workshop", "awesome", "example", "demo", "cookbook", "notebook", "template"}
TECHNOLOGIES = {"langchain", "llama-index", "llama_index", "chromadb", "qdrant"}
FIELDS = ["full_name", "stars", "pushed_at", "size_kb", "topics", "description", "url", "star_band"]


def github_get(url: str) -> dict:
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "ragsmell-research"}
    if token := os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = f"Bearer {token}"
    with urlopen(Request(url, headers=headers), timeout=30) as response:
        return json.load(response)


def main() -> None:
    data = ROOT / "data"
    source = data / "repos_candidatos.csv"
    candidates = list(csv.DictReader(source.open(encoding="utf-8"))) if source.exists() else []
    candidates.sort(key=lambda row: (-int(row.get("stars", 0)), row.get("full_name", "")))
    preselected: list[dict[str, str]] = []
    excluded: list[dict[str, str]] = []
    for row in candidates:
        checked_at = datetime.now(UTC).isoformat()
        text = f"{row.get('full_name', '')} {row.get('description', '')}".lower()
        blocked = next((word for word in BLOCK_WORDS if word in text), None)
        if blocked:
            excluded.append({"full_name": row["full_name"], "reason": f"blocked_word:{blocked}", "evidence": text, "checked_at": checked_at})
        elif int(row.get("size_kb", 0)) < 500:
            excluded.append({"full_name": row["full_name"], "reason": "size_lt_500_kb", "evidence": row.get("size_kb", ""), "checked_at": checked_at})
        else:
            preselected.append(row)

    data.mkdir(parents=True, exist_ok=True)
    with (data / "repos_preseleccion.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS); writer.writeheader(); writer.writerows(preselected[:40])
    with (data / "repos_excluidos.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["full_name", "reason", "evidence", "checked_at"]); writer.writeheader(); writer.writerows(excluded)

    selected: list[dict[str, str]] = []
    decisions: list[dict[str, str]] = []
    for row in preselected[:40]:
        full_name = row["full_name"]
        evidence: list[str] = []
        dependency_ok = False
        commits_ok = False
        try:
            owner, repo = full_name.split("/", 1)
            tree = github_get(f"https://api.github.com/repos/{owner}/{repo}/git/trees/HEAD?recursive=1")
            root_manifests = [item["path"] for item in tree.get("tree", []) if "/" not in item.get("path", "") and Path(item.get("path", "")).name.lower().startswith(("requirements", "pyproject.toml", "setup.py"))]
            for name in root_manifests:
                try:
                    blob = github_get(f"https://api.github.com/repos/{owner}/{repo}/contents/{name}")
                    content = json.dumps(blob).lower()
                    if any(technology in content for technology in TECHNOLOGIES):
                        dependency_ok = True
                        evidence.append(name)
                except (OSError, ValueError, KeyError) as exc:
                        evidence.append(f"PENDIENTE_DE_VERIFICACIÓN:{name}:{type(exc).__name__}")
            metadata_path = data / "metadata_muestra.json"
            since = ""
            if metadata_path.exists():
                since = json.loads(metadata_path.read_text(encoding="utf-8")).get("fecha_corte", "")
            if since:
                commits = github_get(f"https://api.github.com/repos/{owner}/{repo}/commits?since={since}&per_page=20")
                commits_ok = len(commits) >= 20
                evidence.append(f"commits_ultimo_anio>={'20' if commits_ok else len(commits)}")
            else:
                evidence.append("PENDIENTE_DE_VERIFICACIÓN:fecha_corte")
        except (OSError, ValueError, KeyError) as exc:
            evidence.append(f"PENDIENTE_DE_VERIFICACIÓN:manifest:{type(exc).__name__}")
        included = dependency_ok and commits_ok
        reason = "" if included else ";".join(filter(None, ["No se verificó manifiesto relevante accesible" if not dependency_ok else "", "No se verificaron >=20 commits del último año" if not commits_ok else ""]))
        decisions.append({"full_name": full_name, "incluido": str(included).lower(), "criterios_cumplidos": "manifest_relevant;commits_20" if included else "PENDIENTE_DE_VERIFICACIÓN", "evidencia": ";".join(evidence), "motivo": reason, "star_band": row.get("star_band", "")})
        if included:
            selected.append({"full_name": full_name, "url": row["url"], "stars": row["stars"], "commit_sha": ""})

    with (data / "decision_muestra.csv").open("w", newline="", encoding="utf-8") as handle:
        fields = ["full_name", "incluido", "criterios_cumplidos", "evidencia", "motivo", "star_band"]; writer = csv.DictWriter(handle, fieldnames=fields); writer.writeheader(); writer.writerows(decisions)
    with (data / "repos_seleccionados.csv").open("w", newline="", encoding="utf-8") as handle:
        fields = ["full_name", "url", "stars", "commit_sha"]; writer = csv.DictWriter(handle, fieldnames=fields); writer.writeheader(); writer.writerows(selected)
    print(f"candidatos={len(candidates)} preseleccionados={len(preselected[:40])} incluidos={len(selected)}")


if __name__ == "__main__":
    main()
