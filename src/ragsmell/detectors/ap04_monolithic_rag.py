"""AP4: retrieval and generation in one oversized function."""

import ast
from pathlib import Path

from ragsmell.detectors.base import Detector
from ragsmell.knowledge import is_generation_call, is_retrieval_call
from ragsmell.models import Finding


class MonolithicRag(Detector):
    id = "AP4"
    name = "Monolithic RAG Function"

    def analyze(self, tree: ast.AST, source: str, path: Path) -> list[Finding]:
        findings: list[Finding] = []
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) or not node.end_lineno:
                continue
            names = [self._call_name(item) for item in ast.walk(node)]
            if node.end_lineno - node.lineno + 1 > 60 and any(is_retrieval_call(n) for n in names) and any(is_generation_call(n) for n in names):
                findings.append(Finding(self.id, path.as_posix(), node.lineno, node.col_offset, "Function combines retrieval and generation over 60 lines", ast.get_source_segment(source, node) or ""))
        return findings

    @staticmethod
    def _call_name(node: ast.AST) -> str:
        if isinstance(node, ast.Call):
            node = node.func
        if isinstance(node, ast.Attribute):
            parent = MonolithicRag._call_name(node.value)
            return f"{parent}.{node.attr}" if parent else node.attr
        return getattr(node, "id", "")
