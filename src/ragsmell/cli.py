"""Command line interface for the research prototype."""

from __future__ import annotations

import csv
from dataclasses import asdict
from pathlib import Path
from typing import Annotated

import typer

from ragsmell import __version__
from ragsmell.detectors import REGISTRY
from ragsmell.metrics import module_metrics
from ragsmell.scanner import iter_python_files, scan_repo

app = typer.Typer(no_args_is_help=True, add_completion=False)


@app.command()
def version() -> None:
    """Print the package version."""
    typer.echo(__version__)


@app.command()
def scan(path: Path, out: Annotated[Path, typer.Option("--out", "-o")] = Path("findings.csv"), only: Annotated[str | None, typer.Option("--only")] = None) -> None:
    """Scan a directory and write findings as CSV."""
    if not path.is_dir():
        raise typer.BadParameter("la ruta debe existir y ser un directorio", param_hint="path")
    ids = [item.strip().upper() for item in only.split(",")] if only else list(REGISTRY)
    unknown = [item for item in ids if item not in REGISTRY]
    if unknown:
        raise typer.BadParameter(f"IDs desconocidos: {', '.join(unknown)}. Permitidos: {', '.join(REGISTRY)}", param_hint="--only")
    result = scan_repo(path, [REGISTRY[item] for item in ids])
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["file", "ap_id", "line", "col", "message", "snippet"])
        writer.writeheader(); writer.writerows(asdict(f) for f in result.findings)
    typer.echo(f"archivos={result.n_files} no_parseables={len(result.parse_errors)} hallazgos={len(result.findings)}")
    for detector in ids:
        typer.echo(f"{detector}={sum(f.ap_id == detector for f in result.findings)}")


@app.command()
def metrics(path: Path, out: Annotated[Path, typer.Option("--out", "-o")] = Path("metricas.csv")) -> None:
    """Calculate metrics for eligible Python modules."""
    if not path.is_dir():
        raise typer.BadParameter("la ruta debe existir y ser un directorio", param_hint="path")
    root = path.resolve()
    rows = []
    for file in iter_python_files(root):
        try:
            values = module_metrics(file.read_text(encoding="utf-8-sig"))
            rows.append({"file": file.relative_to(root).as_posix(), **values})
        except (OSError, UnicodeError, SyntaxError, ValueError):
            continue
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as handle:
        fields = ["file", "sloc", "cc_media", "cc_max", "mi", "cbo_mod"]
        writer = csv.DictWriter(handle, fieldnames=fields); writer.writeheader(); writer.writerows(rows)
    typer.echo(f"módulos={len(rows)}")


if __name__ == "__main__":
    app()
