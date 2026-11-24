"""Generate the researcher-facing validation workspace without human labels."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

csv.field_size_limit(10_000_000)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/resultados"


def identifier(row: dict[str, str]) -> str:
    return "|".join(row[key] for key in ("repo", "ap_id", "file", "line", "col"))


def duplicate_note(row: dict[str, str]) -> str:
    repo, file_name, ap = row["repo"], row["file"], row["ap_id"]
    if ap == "AP1" and repo == "verygoodplugins/automem":
        return "Grupo lógico relacionado: consultas system_query de automem en dos archivos."
    if ap == "AP1" and repo == "multimindlab/multimind-sdk" and file_name.endswith("memory/procedural.py"):
        return "Grupo lógico relacionado: dos prompts de procedimiento en el mismo módulo."
    if ap == "AP3" and repo == "bojieli/ai-agent-book" and file_name.endswith("agent/service.py"):
        return "Grupo lógico repetido: dos defaults ChatOpenAI en el mismo servicio."
    if ap == "AP3" and repo == "bojieli/ai-agent-book" and file_name.endswith("browser_use/cli.py"):
        return "Grupo lógico repetido: dos ramas de autodetección en el mismo CLI."
    if ap == "AP5" and repo == "BerriAI/litellm" and "router_rust" in file_name:
        return "Grupo lógico relacionado: dos fallbacks best-effort de capacidades."
    if ap == "AP5" and repo == "run-llama/llama_index" and "code_interpreter/base.py" in file_name:
        return "Grupo lógico repetido: métodos síncrono y asíncrono del code interpreter."
    return "Sin duplicación lógica evidente en esta revisión."


def source_excerpt(row: dict[str, str]) -> tuple[bool, str, int, int]:
    path = ROOT / "data/clones" / row["repo"].replace("/", "__") / row["file"]
    if not path.exists():
        return False, "", 0, 0
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    line = int(row["line"])
    start = max(1, line - 6)
    end = min(len(lines), line + 7)
    excerpt = "\n".join(f"{number}: {lines[number - 1]}" for number in range(start, end + 1))
    return True, excerpt, start, end


def command(row: dict[str, str], start: int) -> str:
    path = f'data/clones/{row["repo"].replace("/", "__")}/{row["file"]}'
    return f'Get-Content "{path}" | Select-Object -Skip {start - 1} -First 18'


def main() -> None:
    original = list(csv.DictReader((OUT / "validacion_manual.csv").open(encoding="utf-8")))
    assessments = {row["finding_id"]: row for row in csv.DictReader((OUT / "revision_ia_preliminar.csv").open(encoding="utf-8"))}
    ids = [identifier(row) for row in original]
    assert len(original) == 60 and len(assessments) == 60 and set(ids) == set(assessments)
    text = [
        "# Validación asistida de los 60 hallazgos", "",
        "> Las clasificaciones y confianzas son propuestas de IA; no son etiquetas confirmadas. La decisión final debe registrarse en `validacion_manual.csv` después de la inspección humana.", "",
        "## Control de integridad", "", "- Filas originales: 60.", "- Evaluaciones IA coincidentes: 60.", "- Duplicados de identificador: 0.", "- Semilla: 42.", "- Todas las filas requieren revisión humana.", "",
        "Distinga evidencia TP, evidencia FP, insuficiencia de evidencia y juicio arquitectónico. Compare siempre con `docs/taxonomia.md`.", "",
    ]
    for batch_start in range(0, 60, 10):
        batch = original[batch_start : batch_start + 10]
        text += [f"## Lote {batch_start // 10 + 1} — hallazgos {batch_start + 1}–{batch_start + 10}", "", f"Casos en este lote: **{len(batch)}**.", ""]
        for index, row in enumerate(batch, batch_start + 1):
            assessment = assessments[identifier(row)]
            exists, excerpt, start, end = source_excerpt(row)
            text += [
                f"### {index}. `{identifier(row)}`", "", f"- **Repositorio:** `{row['repo']}`", f"- **Archivo:** `{row['file']}`", f"- **Detector:** `{row['ap_id']}`", f"- **Línea/columna:** `{row['line']}:{row['col']}`; contexto `{start}–{end}`", f"- **Regla que activó el hallazgo:** {row['message']}", f"- **Propuesta IA:** **{assessment['proposed_classification']}**", f"- **Confianza IA:** **{assessment['confidence']}**", f"- **Evidencia de apoyo:** {assessment['supporting_evidence']}", f"- **Evidencia contradictoria o limitación:** {assessment['contradicting_evidence']}", f"- **Explicación preliminar:** {assessment['proposed_explanation']}", f"- **Archivo fuente existe:** `{exists}`", "- **Contexto fuente:**", "```python", excerpt[:1800], "```", f"- **Comando sugerido:** `{command(row, start)}`", f"- **Duplicación lógica:** {duplicate_note(row)}", "", "- **Decisión final del investigador:** `[ ] TP   [ ] FP   [ ] UNCERTAIN`", "- **Nota del investigador:**", "", "---", "",
            ]
    (OUT / "validacion_asistida.md").write_text("\n".join(text), encoding="utf-8")
    counts = Counter(assessments[item]["proposed_classification"] for item in ids)
    confidence = Counter(assessments[item]["confidence"] for item in ids)
    summary = ["# Resumen de validación asistida", "", "## Integridad", "", "- Filas originales: **60**.", "- Evaluaciones IA: **60**.", "- Identificadores faltantes o extra: **0**.", "- Duplicados: **0**.", "- Lotes: **6**, con **10 filas cada uno**.", "- La muestra original y semilla 42 se conservaron.", "", "## Propuestas IA (no confirmadas)", "", "| Propuesta | Total |", "|---|---:|"]
    summary += [f"| {key} | {counts[key]} |" for key in ("TP", "FP", "UNCERTAIN")]
    summary += ["", "| Confianza | Total |", "|---|---:|"] + [f"| {key} | {confidence[key]} |" for key in ("HIGH", "MEDIUM", "LOW")]
    summary += ["", "## Duplicaciones lógicas identificadas", "", "- AP1: dos consultas `system_query` en automem; dos prompts de procedimiento en `multimind-sdk`; dos prompts GUI de Khoj.", "- AP3: dos defaults en `browser_use/agent/service.py`; dos ramas en `browser_use/cli.py`; varias familias de adapters/defaults en LlamaIndex.", "- AP5: dos fallbacks de capacidades en LiteLLM; métodos síncrono/asíncrono del code interpreter de LlamaIndex.", "", "Las filas relacionadas no se eliminaron ni fusionaron.", "", "## Estado metodológico", "", "No se modificaron campos humanos, conclusiones, detectores, taxonomía, decisiones D1–D10 ni el muestreo. No se ejecutó inferencia."]
    (OUT / "validacion_asistida_resumen.md").write_text("\n".join(summary) + "\n", encoding="utf-8")
    print(f"batches=6 rows=60 counts={dict(counts)} confidence={dict(confidence)}")


if __name__ == "__main__":
    main()
