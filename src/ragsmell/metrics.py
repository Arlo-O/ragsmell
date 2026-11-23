"""Module-level source metrics."""

from __future__ import annotations

import ast
import sys
from statistics import mean

from radon.complexity import cc_visit
from radon.metrics import mi_visit


def _import_root(name: str) -> str:
    return name.lstrip(".").split(".", 1)[0]


def module_metrics(source: str) -> dict[str, float | int | None]:
    """Return Radon metrics and approximate module-level coupling.

    `cbo_mod` counts distinct imported roots outside the standard library. It is
    intentionally not presented as the original class-level CK CBO metric.
    """
    tree = ast.parse(source)
    blocks = cc_visit(source)
    complexities = [block.complexity for block in blocks]
    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(_import_root(alias.name) for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imported.add(_import_root("." * node.level + (node.module or "")))
    stdlib = getattr(sys, "stdlib_module_names", set())
    external = {name for name in imported if name and name not in stdlib}
    return {"sloc": sum(1 for line in source.splitlines() if line.strip() and not line.lstrip().startswith("#")), "cc_media": mean(complexities) if complexities else 0.0, "cc_max": max(complexities) if complexities else 0, "mi": mi_visit(source, multi=True), "cbo_mod": len(external)}
