"""AP3: literal provider/model lock-in."""

import ast
from pathlib import Path

from ragsmell.detectors.base import Detector
from ragsmell.knowledge import LLM_CLASSES, MODEL_NAME_REGEX
from ragsmell.models import Finding


class ProviderLockin(Detector):
    id = "AP3"
    name = "Hardcoded Provider Lock-in"

    def analyze(self, tree: ast.AST, source: str, path: Path) -> list[Finding]:
        findings: list[Finding] = []
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            name = node.func.attr if isinstance(node.func, ast.Attribute) else getattr(node.func, "id", "")
            if name not in LLM_CLASSES and not any(part in name.lower() for part in ("openai", "anthropic", "mistral")):
                continue
            for keyword in node.keywords:
                if keyword.arg in {"model", "model_name"} and isinstance(keyword.value, ast.Constant) and isinstance(keyword.value.value, str) and MODEL_NAME_REGEX.fullmatch(keyword.value.value):
                    findings.append(Finding(self.id, path.as_posix(), node.lineno, node.col_offset, "Literal model name creates provider lock-in", ast.get_source_segment(source, node) or ""))
                    break
        return findings
