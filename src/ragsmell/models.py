"""Immutable data structures emitted by the scanner."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Finding:
    """One detector finding, using paths relative to the scanned root."""

    ap_id: str
    file: str
    line: int
    col: int
    message: str
    snippet: str


@dataclass(frozen=True, slots=True)
class ScanResult:
    """Aggregate scan output."""

    findings: list[Finding]
    parse_errors: list[dict[str, str]]
    n_files: int
