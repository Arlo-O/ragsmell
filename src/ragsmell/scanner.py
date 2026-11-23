"""Filesystem traversal and AST scanning."""

from __future__ import annotations

import ast
from collections.abc import Iterable
from pathlib import Path

from ragsmell.detectors.base import Detector
from ragsmell.models import Finding, ScanResult

EXCLUDED_DIRS = {".git", "venv", ".venv", "node_modules", "tests", "test", "docs", "examples", "example", "migrations", "scripts", "build", "dist", "__pycache__", "site-packages"}
EXCLUDED_FILES = {"conftest.py"}


def iter_python_files(root: Path) -> Iterable[Path]:
    """Yield eligible Python files, deterministically and below 1 MiB."""
    root = root.resolve()
    for path in sorted(root.rglob("*.py")):
        if any(part in EXCLUDED_DIRS for part in path.relative_to(root).parts[:-1]) or path.name in EXCLUDED_FILES or path.name.startswith("test_") or path.name.endswith("_test.py"):
            continue
        try:
            if path.stat().st_size <= 1_000_000:
                yield path
        except OSError:
            continue


def scan_repo(root: Path, detectors: Iterable[Detector]) -> ScanResult:
    """Scan eligible modules, retaining parse/read errors and continuing."""
    root = root.resolve(); findings: list[Finding] = []; errors: list[dict[str, str]] = []; count = 0
    for path in iter_python_files(root):
        rel = path.relative_to(root).as_posix(); count += 1
        try:
            source = path.read_text(encoding="utf-8-sig")
            tree = ast.parse(source, filename=rel)
        except (OSError, UnicodeError, SyntaxError, ValueError) as exc:
            errors.append({"file": rel, "error": f"{type(exc).__name__}: {exc}"}); continue
        for detector in detectors:
            findings.extend(detector.analyze(tree, source, Path(rel)))
    return ScanResult(findings, errors, count)
