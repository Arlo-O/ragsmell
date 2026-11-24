"""Clone selected repositories shallowly and record immutable SHAs."""

from __future__ import annotations

import csv
import subprocess
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(*args: str, cwd: Path | None = None) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True, stderr=subprocess.STDOUT).strip()


def main() -> None:
    source = ROOT / "data" / "repos_seleccionados.csv"; clone_root = ROOT / "data" / "clones"; clone_root.mkdir(parents=True, exist_ok=True)
    if not source.exists():
        print("repos_seleccionados.csv no existe; no se clona nada")
        return
    rows = list(csv.DictReader(source.open(encoding="utf-8"))); errors = []; updated = []
    history_path = ROOT / "data" / "clone_errors.csv"
    if history_path.exists():
        with history_path.open(encoding="utf-8") as handle:
            errors.extend({**row, "attempted_at": row.get("attempted_at", ""), "method": row.get("method", "previous"), "status": row.get("status", "failure")} for row in csv.DictReader(handle))
    attempted_at = datetime.now(UTC).replace(microsecond=0).isoformat()
    for row in rows:
        full_name = row["full_name"]; target = clone_root / full_name.replace("/", "__")
        try:
            if not (target / ".git").exists():
                subprocess.run(["git", "clone", "--depth", "1", row["url"], str(target)], check=True, capture_output=True, text=True)
            else:
                remote = run("git", "config", "--get", "remote.origin.url", cwd=target)
                if remote.rstrip("/").removesuffix(".git") not in {row["url"].rstrip("/").removesuffix(".git"), f"git@github.com:{full_name}"}:
                    raise ValueError("la carpeta existente no corresponde a la URL esperada")
            actual = run("git", "rev-parse", "HEAD", cwd=target)
            if subprocess.run(["git", "diff", "--quiet"], cwd=target, check=False).returncode != 0 or subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=target, check=False).returncode != 0 or run("git", "ls-files", "--deleted", cwd=target):
                raise ValueError("checkout incompleto o con archivos rastreados ausentes")
            row["commit_sha"] = actual; updated.append(row)
            errors.append({"full_name": full_name, "error": "", "attempted_at": attempted_at, "method": "git_clone_or_repair", "status": "success"})
        except (subprocess.CalledProcessError, OSError) as exc:
            errors.append({"full_name": full_name, "error": str(exc), "attempted_at": attempted_at, "method": "git_clone_or_repair", "status": "failure"})
            updated.append(row)
        except ValueError as exc:
            errors.append({"full_name": full_name, "error": str(exc), "attempted_at": attempted_at, "method": "git_clone_or_repair", "status": "failure"})
            updated.append(row)
    extra_fields = [field for field in (rows[0].keys() if rows else []) if field not in {"full_name", "url", "stars", "commit_sha"}]
    fields = ["full_name", "url", "stars", "commit_sha", *extra_fields]
    with source.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields); writer.writeheader(); writer.writerows(updated)
    with (ROOT / "data" / "clone_errors.csv").open("w", newline="", encoding="utf-8") as handle:
        fields = ["full_name", "error", "attempted_at", "method", "status"]; writer = csv.DictWriter(handle, fieldnames=fields); writer.writeheader(); writer.writerows(errors)
    print(f"clonados={len(updated)} errores={len(errors)}")


if __name__ == "__main__":
    main()
