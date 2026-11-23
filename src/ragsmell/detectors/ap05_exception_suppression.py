"""AP5: broad suppression of critical LLM/retrieval errors."""

import ast
from pathlib import Path

from ragsmell.detectors.base import Detector
from ragsmell.knowledge import is_generation_call, is_retrieval_call
from ragsmell.models import Finding


class ExceptionSuppression(Detector):
    id = "AP5"
    name = "Non-Deterministic Exception Suppression"

    def analyze(self, tree: ast.AST, source: str, path: Path) -> list[Finding]:
        findings: list[Finding] = []
        for node in ast.walk(tree):
            if not isinstance(node, ast.Try) or not any(self._critical(c) for c in ast.walk(node) if isinstance(c, ast.Call)):
                continue
            for handler in node.handlers:
                broad = handler.type is None or (isinstance(handler.type, ast.Name) and handler.type.id in {"Exception", "BaseException"})
                if broad and self._suppresses(handler):
                    findings.append(Finding(self.id, path.as_posix(), handler.lineno, handler.col_offset, "Broad critical exception is suppressed", ast.get_source_segment(source, handler) or ""))
        return findings

    @staticmethod
    def _critical(call: ast.Call) -> bool:
        name = ""
        node: ast.AST = call.func
        while isinstance(node, ast.Attribute):
            name = f"{node.attr}.{name}"; node = node.value
        name = f"{getattr(node, 'id', '')}.{name}".strip(".")
        return is_generation_call(name) or is_retrieval_call(name)

    @staticmethod
    def _suppresses(handler: ast.ExceptHandler) -> bool:
        return not any(isinstance(n, ast.Raise) for n in ast.walk(handler)) and all(isinstance(n, (ast.Pass, ast.Expr, ast.Return, ast.Constant, ast.Name, ast.Call)) for n in handler.body for _ in [0])
