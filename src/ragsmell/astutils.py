"""Small AST helpers shared by detectors."""

from __future__ import annotations

import ast
from collections.abc import Iterable


def call_name(node: ast.AST) -> str:
    """Return a dotted name for a call/name/attribute, or an empty string."""
    if isinstance(node, ast.Call):
        node = node.func
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        parent = call_name(node.value)
        return f"{parent}.{node.attr}" if parent else node.attr
    return ""


def endswith_any(name: str, suffixes: Iterable[str]) -> bool:
    """Match dotted names on component boundaries, not arbitrary substrings."""
    return any(name == suffix or name.endswith(f".{suffix}") for suffix in suffixes)


def import_aliases(tree: ast.AST) -> dict[str, str]:
    """Map local import aliases to their fully qualified import names."""
    aliases: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for item in node.names:
                aliases[item.asname or item.name.split(".")[0]] = item.name
        elif isinstance(node, ast.ImportFrom):
            prefix = "." * node.level + (node.module or "")
            for item in node.names:
                aliases[item.asname or item.name] = f"{prefix}.{item.name}".strip(".")
    return aliases
