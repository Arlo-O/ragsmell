"""AP1: long prompt literal mixed with control logic."""

import ast
from pathlib import Path

from ragsmell.detectors.base import Detector
from ragsmell.knowledge import PROMPT_HINTS
from ragsmell.models import Finding


class PromptInfiltration(Detector):
    id = "AP1"
    name = "Hardcoded Prompt Infiltration"

    def analyze(self, tree: ast.AST, source: str, path: Path) -> list[Finding]:
        findings: list[Finding] = []
        for function in (n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))):
            if not any(isinstance(n, (ast.If, ast.For, ast.While, ast.Try)) for n in ast.walk(function)):
                continue
            for node in ast.walk(function):
                if isinstance(node, ast.Constant) and isinstance(node.value, str) and len(node.value) >= 80 and self._prompt_context(function, node):
                    findings.append(Finding(self.id, path.as_posix(), node.lineno, node.col_offset, "Long hardcoded prompt is embedded in control logic", ast.get_source_segment(source, node) or ""))
                elif isinstance(node, ast.JoinedStr) and self._prompt_context(function, node) and len("".join(x.value for x in node.values if isinstance(x, ast.Constant))) >= 80:
                    findings.append(Finding(self.id, path.as_posix(), node.lineno, node.col_offset, "Long f-string prompt is embedded in control logic", ast.get_source_segment(source, node) or ""))
        return findings

    @staticmethod
    def _prompt_context(function: ast.AST, candidate: ast.AST) -> bool:
        for node in ast.walk(function):
            if isinstance(node, ast.Assign) and node.value is candidate and any(isinstance(t, ast.Name) and any(h in t.id.lower() for h in PROMPT_HINTS) for t in node.targets):
                return True
        return False
