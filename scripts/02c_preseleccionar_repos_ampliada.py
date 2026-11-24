"""Create a separate, auditable preselection from expanded candidates."""

from __future__ import annotations

import csv
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
BLOCK_WORDS = {"tutorial", "course", "workshop", "awesome", "example", "demo", "cookbook", "notebook", "template"}
FIELDS = ["full_name", "stars", "pushed_at", "size_kb", "topics", "description", "url", "star_band"]


def main() -> None:
    source = DATA / "repos_candidatos_ampliados.csv"
    rows = list(csv.DictReader(source.open(encoding="utf-8"))) if source.exists() else []
    rows.sort(key=lambda item: (-int(item.get("stars", 0)), item["full_name"]))
    candidates: list[dict[str, str]] = []
    excluded: list[dict[str, str]] = []
    for item in rows:
        text = f"{item['full_name']} {item.get('description', '')}".lower()
        blocked = next((word for word in BLOCK_WORDS if word in text), None)
        if blocked:
            excluded.append({"full_name": item["full_name"], "reason": f"NO_CUMPLE:blocked_word:{blocked}", "evidence": text, "checked_at": datetime.now(UTC).isoformat()})
        elif int(item.get("size_kb", 0)) < 500:
            excluded.append({"full_name": item["full_name"], "reason": "NO_CUMPLE:size_lt_500_kb", "evidence": item.get("size_kb", ""), "checked_at": datetime.now(UTC).isoformat()})
        else:
            candidates.append(item)
    by_band = {band: [item for item in candidates if item.get("star_band") == band][:40] for band in ("11..100", "101..1000", ">1000")}
    stratified = [item for band in ("11..100", "101..1000", ">1000") for item in by_band[band]]
    with (DATA / "repos_preseleccion_ampliada.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS); writer.writeheader(); writer.writerows(stratified)
    with (DATA / "repos_excluidos_ampliada.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["full_name", "reason", "evidence", "checked_at"]); writer.writeheader(); writer.writerows(excluded)
    print(f"candidatos={len(rows)} preseleccionados={len(stratified)} excluidos={len(excluded)}")


if __name__ == "__main__":
    main()
