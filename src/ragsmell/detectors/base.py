"""Detector protocol."""

import ast
from abc import ABC, abstractmethod
from pathlib import Path

from ragsmell.models import Finding


class Detector(ABC):
    """Base class for an AST detector."""

    id: str
    name: str

    @abstractmethod
    def analyze(self, tree: ast.AST, source: str, path: Path) -> list[Finding]:
        """Analyze one parsed module."""
