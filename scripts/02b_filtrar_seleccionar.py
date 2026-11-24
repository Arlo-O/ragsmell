"""Verify the preselected GitHub repositories with authenticated, serial API calls.

The verifier deliberately distinguishes evidence of exclusion from an inability
to inspect a resource.  It defaults to three repositories; pass ``--all`` only
after inspecting that controlled run.
"""

from __future__ import annotations

import argparse
import csv
import json
import time
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from github import Auth, Github
from github.GithubException import GithubException, RateLimitExceededException

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
TECHNOLOGIES = ("langchain", "llama-index", "llama_index", "chromadb", "qdrant")
MANIFESTS = ("requirements.txt", "pyproject.toml", "setup.py")
BLOCK_WORDS = {"tutorial", "course", "workshop", "awesome", "example", "demo", "cookbook", "notebook", "template"}
FIELDS = ["full_name", "stars", "pushed_at", "size_kb", "topics", "description", "url", "star_band"]
VERIFICATION_FIELDS = ["full_name", "included", "status", "repo_status", "manifest_status", "technology_status", "commits_status", "recent_activity_status", "evidence", "reason", "checked_at"]


class VerificationPending(RuntimeError):
    """Raised when the API did not provide enough evidence."""


def now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


def load_cache() -> dict[str, dict[str, Any]]:
    path = DATA / ".github_verification_cache.json"
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def save_cache(cache: dict[str, dict[str, Any]]) -> None:
    (DATA / ".github_verification_cache.json").write_text(json.dumps(cache, indent=2, ensure_ascii=False), encoding="utf-8")


def retry_after(exc: GithubException) -> float:
    headers = getattr(exc, "headers", {}) or {}
    value = headers.get("retry-after") or headers.get("Retry-After")
    if value:
        try:
            return max(1.0, float(value))
        except ValueError:
            pass
    reset = headers.get("x-ratelimit-reset") or headers.get("X-RateLimit-Reset")
    if reset:
        try:
            return max(1.0, float(reset) - time.time() + 1)
        except ValueError:
            pass
    return 2.0


def call_api(operation: str, function: Any, attempts: int = 3) -> Any:
    """Call one PyGithub operation with bounded, serial retries."""
    for attempt in range(attempts):
        try:
            return function()
        except RateLimitExceededException as exc:
            if attempt == attempts - 1:
                raise VerificationPending(f"{operation}: rate limit") from None
            time.sleep(retry_after(exc))
        except GithubException as exc:
            if exc.status in {401, 403, 429}:
                if attempt == attempts - 1:
                    raise VerificationPending(f"{operation}: HTTP {exc.status}") from None
                time.sleep(max(retry_after(exc), 2**attempt))
            else:
                raise
        except (OSError, TimeoutError) as exc:
            if attempt == attempts - 1:
                raise VerificationPending(f"{operation}: {type(exc).__name__}") from None
            time.sleep(2**attempt)
    raise VerificationPending(f"{operation}: exhausted retries")


def rate_limits(client: Github) -> dict[str, Any]:
    """Return only non-secret rate-limit metadata."""
    limit = call_api("rate_limit", client.get_rate_limit)
    result: dict[str, Any] = {"consulted_at": now()}
    for name in ("core", "search"):
        resource = getattr(limit.resources, name)
        result[name] = {"limit": resource.limit, "remaining": resource.remaining, "reset_at": resource.reset.isoformat()}
    return result


def manifest_evidence(repo: Any) -> tuple[str, str, list[str]]:
    """Inspect root manifests; a missing file is not an API access failure."""
    names: set[str] = set()
    try:
        contents = call_api("root_contents", lambda: repo.get_contents(""))
    except GithubException as exc:
        if exc.status == 404:
            return "PENDIENTE_DE_VERIFICACIÓN", "PENDIENTE_DE_VERIFICACIÓN:root_contents_404", []
        raise
    for item in contents:
        if item.name.lower() in MANIFESTS:
            names.add(item.name)
    if not names:
        return "NO_CUMPLE", "NO_CUMPLE:sin_manifesto_raiz", []
    matching: list[str] = []
    for name in sorted(names):
        try:
            content = call_api(f"manifest:{name}", lambda name=name: repo.get_contents(name))
            text = content.decoded_content.decode("utf-8", errors="replace").lower()
            if any(technology in text for technology in TECHNOLOGIES):
                matching.append(name)
        except GithubException as exc:
            if exc.status == 404:
                return "PENDIENTE_DE_VERIFICACIÓN", f"PENDIENTE_DE_VERIFICACIÓN:manifest_access_404:{name}", sorted(names)
            raise
    if matching:
        return "CUMPLE", f"CUMPLE:manifestos={','.join(matching)}", matching
    return "NO_CUMPLE", "NO_CUMPLE:sin_tecnologia_RAG_en_manifestos", sorted(names)


def commit_evidence(repo: Any, since: datetime) -> tuple[str, str]:
    """Use the first page of 20 commits as a conservative >=20 test."""
    commits = call_api("commits", lambda: repo.get_commits(since=since).get_page(0))
    count = len(commits)
    if count >= 20:
        return "CUMPLE", "CUMPLE:>=20_commits_en_primer_pagina"
    return "NO_CUMPLE", f"NO_CUMPLE:solo_{count}_commits_en_periodo"


def verify(repo_row: dict[str, str], client: Github, since: datetime, cache: dict[str, dict[str, Any]]) -> dict[str, Any]:
    full_name = repo_row["full_name"]
    checked_at = now()
    cached = cache.get(full_name)
    if cached and cached.get("since") == since.isoformat():
        return cached["result"]
    result: dict[str, Any] = {"full_name": full_name, "checked_at": checked_at, "status": "PENDIENTE_DE_VERIFICACIÓN", "included": False, "repo_status": "PENDIENTE_DE_VERIFICACIÓN", "manifest_status": "PENDIENTE_DE_VERIFICACIÓN", "technology_status": "PENDIENTE_DE_VERIFICACIÓN", "commits_status": "PENDIENTE_DE_VERIFICACIÓN", "recent_activity_status": "PENDIENTE_DE_VERIFICACIÓN", "evidence": [], "reason": ""}
    try:
        owner, name = full_name.split("/", 1)
        repo = call_api("repository", lambda: client.get_repo(f"{owner}/{name}"))
        result["repo_status"] = "CUMPLE" if not repo.fork and not repo.archived and (repo.language or "").lower() == "python" and repo.stargazers_count > 10 else "NO_CUMPLE"
        result["evidence"].extend([f"url={repo.html_url}", f"language={repo.language}", f"stars={repo.stargazers_count}", f"fork={repo.fork}", f"archived={repo.archived}"])
        if result["repo_status"] == "NO_CUMPLE":
            result["reason"] = "No cumple metadatos de Python/estrellas/fork/archivo"
        else:
            manifest_status, manifest_reason, manifests = manifest_evidence(repo)
            result["manifest_status"] = manifest_status
            result["technology_status"] = "CUMPLE" if manifest_status == "CUMPLE" else manifest_status
            result["evidence"].extend([manifest_reason, *manifests])
            result["commits_status"], commit_reason = commit_evidence(repo, since)
            result["evidence"].append(commit_reason)
            pushed_at = repo.pushed_at
            result["recent_activity_status"] = "CUMPLE" if pushed_at and pushed_at >= since else "NO_CUMPLE"
            result["evidence"].append(f"pushed_at={pushed_at.isoformat() if pushed_at else ''}")
            statuses = [result["manifest_status"], result["commits_status"], result["recent_activity_status"]]
            result["status"] = "CUMPLE" if all(status == "CUMPLE" for status in statuses) else "NO_CUMPLE" if "NO_CUMPLE" in statuses else "PENDIENTE_DE_VERIFICACIÓN"
            result["included"] = result["status"] == "CUMPLE"
            result["reason"] = "" if result["included"] else ";".join(status for status in statuses if status != "CUMPLE")
    except VerificationPending as exc:
        result["status"] = "PENDIENTE_DE_VERIFICACIÓN"
        result["reason"] = str(exc)
    except GithubException as exc:
        if exc.status == 404:
            result["status"] = "NO_CUMPLE"
            result["repo_status"] = "NO_CUMPLE"
            result["reason"] = "NO_CUMPLE:repositorio_inexistente_o_no_accesible"
        else:
            result["reason"] = f"PENDIENTE_DE_VERIFICACIÓN:HTTP_{exc.status}"
    cache[full_name] = {"since": since.isoformat(), "result": result}
    return result


def write_rows(path: Path, fields: list[str], rows: list[dict[str, Any]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields); writer.writeheader(); writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true", help="verify all 40 preselected rows after the controlled run")
    parser.add_argument("--limit", type=int, default=3, help="number of rows to verify; default 3")
    parser.add_argument("--input", default="repos_preseleccion.csv", help="CSV de preselección relativo a data/")
    parser.add_argument("--expanded", action="store_true", help="escribir decisiones y exclusiones ampliadas")
    args = parser.parse_args()
    load_dotenv(ROOT / ".env")
    import os

    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise SystemExit("GITHUB_TOKEN no está disponible; no se ejecutan solicitudes")
    # Auth.Token is intentional: the token itself is never printed, persisted, or included in errors.
    client = Github(auth=Auth.Token(token), per_page=100, retry=0)
    before = rate_limits(client)
    source = DATA / args.input
    rows = list(csv.DictReader(source.open(encoding="utf-8"))) if source.exists() else []
    metadata_path = DATA / "metadata_muestra.json"
    metadata = json.loads(metadata_path.read_text(encoding="utf-8")) if metadata_path.exists() else {}
    extraction = datetime.fromisoformat(metadata.get("fecha_extraccion", now()))
    since = extraction - timedelta(days=365)
    selected_rows = rows if args.all else rows[: args.limit]
    cache = load_cache()
    results = [verify(row, client, since, cache) for row in selected_rows]
    save_cache(cache)
    after = rate_limits(client)
    metadata.update({"verificacion_autenticada": True, "fecha_verificacion": now(), "fecha_corte_verificacion": since.isoformat(), "api_limits_before": before, "api_limits_after": after, "verificacion_modo": "all" if args.all else f"controlled_{len(selected_rows)}", "verificacion_count": len(selected_rows)})
    metadata_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")
    errors = [{"full_name": item["full_name"], "error": item["reason"], "checked_at": item["checked_at"]} for item in results if item["status"] == "PENDIENTE_DE_VERIFICACIÓN"]
    write_rows(DATA / "github_verification_errors.csv", ["full_name", "error", "checked_at"], errors)
    decisions = []
    excluded = []
    for item in results:
        evidence = ";".join(item["evidence"])
        reason = item["reason"]
        if not item["included"]:
            failures = [part for part in item["evidence"] if part.startswith(("NO_CUMPLE:", "PENDIENTE_DE_VERIFICACIÓN:"))]
            reason = ";".join(failures) or reason
        decisions.append({"full_name": item["full_name"], "incluido": str(item["included"]).lower(), "criterios_cumplidos": item["status"], "evidencia": evidence, "motivo": reason, "star_band": next((row.get("star_band", "") for row in rows if row["full_name"] == item["full_name"]), "")})
        if not item["included"]:
            excluded.append({"full_name": item["full_name"], "reason": reason, "evidence": evidence, "checked_at": item["checked_at"]})
    decision_name = "decision_muestra_ampliada.csv" if args.expanded else "decision_muestra.csv"
    exclusion_name = "repos_excluidos_ampliada.csv" if args.expanded else "repos_excluidos.csv"
    write_rows(DATA / decision_name, ["full_name", "incluido", "criterios_cumplidos", "evidencia", "motivo", "star_band"], decisions)
    if args.expanded:
        existing_exclusions = list(csv.DictReader((DATA / "repos_excluidos.csv").open(encoding="utf-8"))) if (DATA / "repos_excluidos.csv").exists() else []
        excluded = existing_exclusions + excluded
    write_rows(DATA / exclusion_name, ["full_name", "reason", "evidence", "checked_at"], excluded)
    included = [row for row in rows if any(item["full_name"] == row["full_name"] and item["included"] for item in results)]
    selected_path = DATA / "repos_seleccionados.csv"
    existing_selected = list(csv.DictReader(selected_path.open(encoding="utf-8"))) if args.expanded and selected_path.exists() else []
    merged = {row["full_name"]: row for row in existing_selected}
    merged.update({row["full_name"]: {"full_name": row["full_name"], "url": row["url"], "stars": row["stars"], "commit_sha": ""} for row in included})
    write_rows(selected_path, ["full_name", "url", "stars", "commit_sha"], list(merged.values()))
    print(f"autenticado=true verificados={len(results)} cumple={len(included)} pendientes={len(errors)}")


if __name__ == "__main__":
    main()
