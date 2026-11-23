import ast
from pathlib import Path

import pytest

from ragsmell.detectors import REGISTRY


def analyse(detector_id: str, source: str):
    detector = REGISTRY[detector_id]
    return detector.analyze(ast.parse(source), source, Path("fixture.py"))


@pytest.mark.parametrize("source", [
    "def f():\n    prompt = '" + "x" * 80 + "'\n    if True:\n        return prompt\n",
])
def test_ap1_positive(source):
    assert len(analyse("AP1", source)) == 1


def test_ap3_literal_vs_configured():
    assert len(analyse("AP3", "from openai import ChatOpenAI\nmodel = ChatOpenAI(model='gpt-4o')\n")) == 1
    assert len(analyse("AP3", "from openai import ChatOpenAI\nmodel = ChatOpenAI(model=settings.model)\n")) == 0


def test_ap5_only_critical_suppression():
    positive = "try:\n    llm.invoke(q)\nexcept Exception:\n    pass\n"
    negative = "try:\n    json.loads(text)\nexcept Exception:\n    pass\n"
    assert len(analyse("AP5", positive)) == 1
    assert len(analyse("AP5", negative)) == 0


@pytest.mark.parametrize("fixture", sorted(Path("tests/fixtures").glob("ap*_*.py")))
def test_registered_detector_fixtures(fixture: Path):
    expected = int(fixture.read_text(encoding="utf-8").splitlines()[0].split(":", 1)[1].strip())
    detector_id = fixture.name[:3].upper()
    assert detector_id in REGISTRY
    source = fixture.read_text(encoding="utf-8")
    assert len(analyse(detector_id, source)) == expected
