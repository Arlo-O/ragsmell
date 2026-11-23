"""Calculate metrics over exactly the scanned eligible modules."""
from __future__ import annotations

import csv
from pathlib import Path

from ragsmell.metrics import module_metrics
from ragsmell.scanner import iter_python_files

ROOT = Path(__file__).resolve().parents[1]

def main() -> None:
    data = ROOT / "data"; output = data / "resultados"; output.mkdir(parents=True, exist_ok=True)
    selected = data / "repos_seleccionados.csv"; rows = list(csv.DictReader(selected.open(encoding="utf-8"))) if selected.exists() else []
    metrics=[]; errors=[]
    for row in rows:
        repo=row["full_name"]; root=data / "clones" / repo.replace("/", "__")
        for file in iter_python_files(root):
            rel=file.relative_to(root).as_posix()
            try: metrics.append({"repo":repo,"file":rel,**module_metrics(file.read_text(encoding="utf-8-sig"))})
            except (OSError, UnicodeError, SyntaxError, ValueError) as exc: errors.append({"repo":repo,"file":rel,"error":f"{type(exc).__name__}: {exc}"})
    def write(name, fields, values):
        with (output/name).open("w",newline="",encoding="utf-8") as handle:
            writer=csv.DictWriter(handle,fieldnames=fields); writer.writeheader(); writer.writerows(values)
    write("metricas.csv",["repo","file","sloc","cc_media","cc_max","mi","cbo_mod"],metrics); write("metricas_errors.csv",["repo","file","error"],errors)
    print(f"metricas={len(metrics)} errores={len(errors)}")
if __name__ == "__main__": main()
