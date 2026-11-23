"""Run core detectors over pinned local clones."""
from __future__ import annotations

import csv
from datetime import UTC, datetime
from pathlib import Path

from ragsmell.detectors import ALL
from ragsmell.scanner import scan_repo

ROOT = Path(__file__).resolve().parents[1]

def main() -> None:
    data = ROOT / "data"; result_dir = data / "resultados"; result_dir.mkdir(parents=True, exist_ok=True)
    selected = data / "repos_seleccionados.csv"
    rows = list(csv.DictReader(selected.open(encoding="utf-8"))) if selected.exists() else []
    findings = []; errors = []; summary = []
    for row in rows:
        repo = row["full_name"]; clone = data / "clones" / repo.replace("/", "__")
        try:
            result = scan_repo(clone, ALL)
            for finding in result.findings:
                findings.append({"repo": repo, **{key: getattr(finding, key) for key in ("ap_id", "file", "line", "col", "message", "snippet")}})
            errors.extend({"repo": repo, **error} for error in result.parse_errors)
            summary.append({"repo": repo, "commit_sha": row.get("commit_sha", ""), "n_files": result.n_files, "n_parse_errors": len(result.parse_errors), "n_findings": len(result.findings), "fecha_ejecucion": datetime.now(UTC).isoformat()})
        except (OSError, ValueError) as exc:
            errors.append({"repo": repo, "file": "", "error": f"{type(exc).__name__}: {exc}"})
    def write(name, fields, values):
        with (result_dir / name).open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields); writer.writeheader(); writer.writerows(values)
    write("findings.csv", ["repo", "ap_id", "file", "line", "col", "message", "snippet"], findings)
    write("parse_errors.csv", ["repo", "file", "error"], errors)
    write("scan_summary.csv", ["repo", "commit_sha", "n_files", "n_parse_errors", "n_findings", "fecha_ejecucion"], summary)
    ap_ids = ["AP1", "AP3", "AP4", "AP5"]
    pivot = []
    for repo in [row["full_name"] for row in rows]:
        pivot.append({"repo": repo, **{ap: sum(item["repo"] == repo and item["ap_id"] == ap for item in findings) for ap in ap_ids}, "tiene_ap": any(item["repo"] == repo for item in findings)})
    write("tabla_repo_ap.csv", ["repo", *ap_ids, "tiene_ap"], pivot)
    print(f"repos={len(rows)} hallazgos={len(findings)} errores={len(errors)}")

if __name__ == "__main__": main()
