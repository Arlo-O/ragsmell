from pathlib import Path

from ragsmell.detectors import ALL
from ragsmell.scanner import iter_python_files, scan_repo


def test_scanner_excludes_tests_and_keeps_parse_errors(tmp_path: Path):
    (tmp_path / "ok.py").write_text("x = 1\n", encoding="utf-8")
    (tmp_path / "broken.py").write_text("def broken(:\n", encoding="utf-8")
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "ignored.py").write_text("x = 1\n", encoding="utf-8")
    result = scan_repo(tmp_path, ALL)
    assert result.n_files == 2
    assert len(result.parse_errors) == 1
    assert [p.name for p in iter_python_files(tmp_path)] == ["broken.py", "ok.py"]
