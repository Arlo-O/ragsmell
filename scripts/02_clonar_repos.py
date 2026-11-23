"""Clone selected repositories shallowly and record immutable SHAs."""

from __future__ import annotations

import csv
import subprocess
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
    for row in rows:
        full_name = row["full_name"]; target = clone_root / full_name.replace("/", "__")
        try:
            if not (target / ".git").exists():
                subprocess.run(["git", "clone", "--depth", "1", row["url"], str(target)], check=True, capture_output=True, text=True)
            actual = run("git", "rev-parse", "HEAD", cwd=target)
            row["commit_sha"] = actual; updated.append(row)
        except (subprocess.CalledProcessError, OSError) as exc:
            errors.append({"full_name": full_name, "error": str(exc)})
    fields = ["full_name", "url", "stars", "commit_sha"]
    with source.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields); writer.writeheader(); writer.writerows(updated)
    with (ROOT / "data" / "clone_errors.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["full_name", "error"]); writer.writeheader(); writer.writerows(errors)
    print(f"clonados={len(updated)} errores={len(errors)}")


if __name__ == "__main__":
    main()
