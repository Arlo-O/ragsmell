"""Record the researcher's adoption of the AI-assisted preliminary classifications.

This script fills only the researcher fields of
``data/resultados/validacion_investigador.csv``. It does not modify the original
validation sample, the AI assessment file, detectors, taxonomy or D1-D10.

The provenance is explicit: the verdict is an adoption of an AI-assisted
proposal without independent source-level verification. UNCERTAIN is preserved
as unresolved and is never recoded to TP or FP.
"""
from __future__ import annotations

import csv
from collections import Counter
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "data/resultados"
WORKING = RESULTS / "validacion_investigador.csv"
ORIGINAL = RESULTS / "validacion_manual.csv"
AI = RESULTS / "revision_ia_preliminar.csv"

REVIEWER = "Investigador (adopción de evaluación asistida por IA)"
REVIEW_STATUS = "accepted_ai_assisted"
ADJUDICATION_METHOD = "adopcion_asistida_por_ia"
ADJUDICATION_DATE = date.today().isoformat()
NOTE = (
    "Adopción de la clasificación preliminar asistida por IA sin verificación "
    "independiente a nivel de fuente. El veredicto es condicional y no "
    "constituye validación humana independiente."
)
NOTE_UNCERTAIN = (
    NOTE + " El caso permanece no resuelto y se conserva como UNCERTAIN; no se "
    "recodifica como TP ni FP."
)
PROVENANCE_COLUMNS = [
    "ai_source_file",
    "adjudication_method",
    "independent_human_verification",
]


def identifier(row: dict[str, str]) -> str:
    return "|".join(row[key] for key in ("repo", "ap_id", "file", "line", "col"))


def read_csv(path: Path) -> list[dict[str, str]]:
    csv.field_size_limit(10_000_000)
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    original = read_csv(ORIGINAL)
    assessments = {row["finding_id"]: row for row in read_csv(AI)}
    working = read_csv(WORKING)
    fields = list(working[0])
    for column in PROVENANCE_COLUMNS:
        if column not in fields:
            fields.append(column)

    original_ids = [identifier(row) for row in original]
    working_ids = [row["original_id"] for row in working]
    if not (len(original) == len(assessments) == len(working) == 60):
        raise SystemExit("Unexpected row count: expected 60 in all three files")
    if set(original_ids) != set(assessments):
        raise SystemExit("AI assessment identifiers do not match the original sample")
    if working_ids != original_ids:
        raise SystemExit("Working-copy identifiers or order do not match the original sample")
    if len(set(working_ids)) != 60:
        raise SystemExit("Duplicate identifiers in the working copy")

    allowed = {"TP", "FP", "UNCERTAIN"}
    for row in working:
        assessment = assessments[row["original_id"]]
        proposal = assessment["proposed_classification"].strip().upper()
        if proposal not in allowed:
            raise SystemExit(f"Unexpected AI proposal: {proposal!r}")
        row["ai_proposal"] = proposal
        row["ai_confidence"] = assessment["confidence"].strip().upper()
        row["researcher_verdict"] = proposal
        row["researcher_note"] = NOTE_UNCERTAIN if proposal == "UNCERTAIN" else NOTE
        row["reviewer"] = REVIEWER
        row["review_date"] = ADJUDICATION_DATE
        row["review_status"] = REVIEW_STATUS
        row["ai_source_file"] = "data/resultados/revision_ia_preliminar.csv"
        row["adjudication_method"] = ADJUDICATION_METHOD
        row["independent_human_verification"] = "no"

    with WORKING.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(working)

    verdicts = Counter(row["researcher_verdict"] for row in working)
    statuses = Counter(row["review_status"] for row in working)
    independent = Counter(row["independent_human_verification"] for row in working)
    resolved = verdicts["TP"] + verdicts["FP"]
    conditional = f"{verdicts['TP']}/{resolved}" if resolved else "no calculable"

    progress = [
        "# Progreso de validación del investigador",
        "",
        "Este resumen se calcula exclusivamente desde los campos del investigador",
        "en `validacion_investigador.csv`. Las columnas `ai_proposal` y",
        "`ai_confidence` son informativas y no cuentan como verificación",
        "independiente.",
        "",
        "## Adjudicación registrada",
        "",
        "Los 60 casos fueron adoptados mediante **adjudicación asistida por IA**:",
        "el investigador aceptó las propuestas preliminares sin inspección",
        "independiente del código fuente.",
        "",
        "| Estado | Casos |",
        "|---|---:|",
        f"| Total | {len(working)} |",
        f"| Revisados (`researcher_verdict` no vacío) | {sum(bool(row['researcher_verdict']) for row in working)} |",
        f"| Pendientes (`researcher_verdict` vacío) | {sum(not row['researcher_verdict'] for row in working)} |",
        f"| Adoptados con `review_status=accepted_ai_assisted` | {statuses[REVIEW_STATUS]} |",
        f"| No resueltos (`UNCERTAIN`) | {verdicts['UNCERTAIN']} |",
        "",
        "## Distribución adoptada (condicional a la adjudicación asistida)",
        "",
        "| Veredicto | Casos |",
        "|---|---:|",
        f"| TP | {verdicts['TP']} |",
        f"| FP | {verdicts['FP']} |",
        f"| UNCERTAIN | {verdicts['UNCERTAIN']} |",
        "",
        f"- Cociente TP/(TP+FP) condicional: **{conditional}**.",
        "- Esta cifra **no es una precisión confirmada** porque no hubo",
        "  verificación humana independiente y 10 casos permanecen sin resolver.",
        "",
        "## Verificación independiente",
        "",
        f"- `independent_human_verification=si`: **{independent['si']}**.",
        f"- `independent_human_verification=no`: **{independent['no']}**.",
        "- No se registró inspección independiente a nivel de fuente.",
        "",
        "## Limitaciones",
        "",
        "- La distribución TP/FP es condicional a la evaluación asistida por IA.",
        "- Los 10 casos UNCERTAIN no están resueltos y no deben usarse como TP o FP.",
        "- No existe una estimación de precisión independientemente verificada.",
        "- Esta limitación metodológica debe declararse en el artículo final.",
        "",
    ]
    (RESULTS / "progreso_validacion.md").write_text("\n".join(progress), encoding="utf-8")

    print(
        f"adjudicated={len(working)} tp={verdicts['TP']} fp={verdicts['FP']} "
        f"uncertain={verdicts['UNCERTAIN']} independent={independent['si']}"
    )


if __name__ == "__main__":
    main()
