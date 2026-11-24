"""Generate the final-report LaTeX tables from the audited result CSV files.

Tables are written to ``documentos_latex/anteproyecto/tablas``. Numeric values
are read from the CSV files; only the taxonomy and limitation descriptions are
literal text taken from ``docs/taxonomia.md`` and the execution records.

Usage:
    .\\.venv\\Scripts\\python.exe scripts\\09_generar_tablas_latex.py
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "data" / "resultados"
DATA = ROOT / "data"
OUT = ROOT / "documentos_latex" / "anteproyecto" / "tablas"


# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------
def esc(text: object) -> str:
    """Escape a value for LaTeX text mode."""
    value = str(text)
    value = value.replace("\\", r"\textbackslash{}")
    for char in ("&", "%", "$", "#", "_", "{", "}"):
        value = value.replace(char, "\\" + char)
    return value.replace("~", r"\textasciitilde{}").replace("^", r"\textasciicircum{}")


def num(value: float, decimals: int = 2) -> str:
    """Spanish number with thousands separator and decimal comma."""
    if pd.isna(value):
        return "---"
    text = f"{value:,.{decimals}f}"
    return text.replace(",", "\u00a0").replace(".", ",").replace("\u00a0", r"\,")


def integer(value: float) -> str:
    return num(value, 0)


def pvalue(value: float) -> str:
    if pd.isna(value):
        return "---"
    if value < 0.001:
        mantissa, exponent = f"{value:.2e}".split("e")
        mantissa = mantissa.replace(".", "{,}")
        return f"${mantissa} \\times 10^{{{int(exponent)}}}$"
    return num(value, 5)


def dmath(value: float, decimals: int = 3) -> str:
    if pd.isna(value):
        return "---"
    return "$" + f"{value:+.{decimals}f}".replace(".", "{,}") + "$"


def rho_math(value: float) -> str:
    return "$" + f"{value:+.3f}".replace(".", "{,}") + "$"


MAGNITUDE = {"grande": "Grande", "mediano": "Mediano", "pequeno": "Pequeño", "despreciable": "Despreciable"}
STATUS = {"calculado_significativo": "Significativo", "n_insuficiente": "n insuficiente"}
DIRECTION = {"mayor_en_con_ap": "Mayor en con AP", "menor_en_con_ap": "Menor en con AP"}


def write(name: str, content: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    path.write_text(content, encoding="utf-8")
    print(f"tabla escrita: {path.relative_to(ROOT)}")


def longtable(
    columns: str,
    caption: str,
    label: str,
    header: str,
    body: str,
    n_columns: int,
    size: str = r"\footnotesize",
    tabcolsep: str = "3pt",
) -> str:
    return "\n".join(
        [
            r"% Generado automáticamente por scripts/09_generar_tablas_latex.py",
            r"\begingroup",
            size,
            r"\setlength{\tabcolsep}{" + tabcolsep + "}",
            r"\begin{longtable}{" + columns + "}",
            r"\caption{" + caption + r"}\label{" + label + r"}\\",
            r"\toprule",
            header + r" \\",
            r"\midrule",
            r"\endfirsthead",
            rf"\multicolumn{{{n_columns}}}{{@{{}}l}}{{\small Tabla \thetable\ (continuación)}}\\",
            r"\toprule",
            header + r" \\",
            r"\midrule",
            r"\endhead",
            r"\bottomrule",
            r"\endlastfoot",
            body,
            r"\end{longtable}",
            r"\endgroup",
            "",
        ]
    )


def table(
    columns: str,
    caption: str,
    label: str,
    header: str,
    body: str,
    size: str = r"\small",
    tabcolsep: str = "4pt",
    position: str = "htbp",
) -> str:
    return "\n".join(
        [
            r"% Generado automáticamente por scripts/09_generar_tablas_latex.py",
            r"\begin{table}[" + position + "]",
            r"\centering",
            size,
            r"\setlength{\tabcolsep}{" + tabcolsep + "}",
            r"\caption{" + caption + r"}",
            r"\label{" + label + "}",
            r"\begin{tabular}{" + columns + "}",
            r"\toprule",
            header + r" \\",
            r"\midrule",
            body,
            r"\bottomrule",
            r"\end{tabular}",
            r"\end{table}",
            "",
        ]
    )


# ---------------------------------------------------------------------------
# Table 1. Repository sample
# ---------------------------------------------------------------------------
def tabla_muestra() -> None:
    ap = pd.read_csv(RESULTS / "tabla_repo_ap.csv")
    resumen = pd.read_csv(RESULTS / "resumen_repositorio.csv")
    selected = pd.read_csv(DATA / "repos_seleccionados.csv")
    merged = (
        resumen.merge(ap[["repo", "AP1", "AP3", "AP4", "AP5"]], on="repo", how="left")
        .merge(selected[["full_name", "star_band"]], left_on="repo", right_on="full_name", how="left")
        .sort_values("findings", ascending=False)
    )
    bands = {"11..100": "11--100", "101..1000": "101--1000", ">1000": ">1000"}
    rows = []
    for _, row in merged.iterrows():
        rows.append(
            " & ".join(
                [
                    rf"\texttt{{{esc(row['repo'])}}}",
                    bands.get(row["star_band"], esc(row["star_band"])),
                    integer(row["modules"]),
                    integer(row["modules_with_ap"]),
                    num(100 * row["pct_modules_with_ap"], 2),
                    integer(row["findings"]),
                ]
            )
            + r" \\"
        )
    rows.append(r"\midrule")
    rows.append(
        " & ".join(
            [
                r"\textbf{Total}",
                "---",
                integer(merged["modules"].sum()),
                integer(merged["modules_with_ap"].sum()),
                num(100 * merged["modules_with_ap"].sum() / merged["modules"].sum(), 2),
                integer(merged["findings"].sum()),
            ]
        )
        + r" \\"
    )
    content = longtable(
        r"@{}p{5.3cm}crrrr@{}",
        "Composición de la muestra: módulos y hallazgos por repositorio",
        "tab:muestra",
        r"\textbf{Repositorio} & \textbf{Banda} & \textbf{Módulos} & \textbf{Mód.\ con AP} & \textbf{\% con AP} & \textbf{Hallazgos}",
        "\n".join(rows),
        6,
        size=r"\footnotesize",
        tabcolsep="3pt",
    )
    write("tab01_muestra_repositorios.tex", content)


# ---------------------------------------------------------------------------
# Table 2. Taxonomy and detector status
# ---------------------------------------------------------------------------
def tabla_taxonomia() -> None:
    rows = [
        ("AP1", "Hardcoded Prompt Infiltration", "Prompt extenso incrustado en una función que concentra lógica de control.", "Mantenibilidad, evolvabilidad", "Cadena o f-string $\\geq$ 80 caracteres en función con control, vinculada a pista de prompt o llamada a LLM.", "Implementado"),
        ("AP2", "Vector Store Leakage", "Acceso vectorial desde la presentación o credencial literal.", "Seguridad, separación de capas", "Framework web con cliente vectorial, o credencial literal en el constructor.", "No implementado"),
        ("AP3", "Hardcoded Provider Lock-in", "Proveedor o modelo rígido sin abstracción configurable.", "Portabilidad, mantenibilidad", "Valor literal de \\texttt{model} o \\texttt{model\\_name} reconocible en constructor o SDK documentado.", "Implementado"),
        ("AP4", "Monolithic RAG Function", "Una función concentra recuperación y generación.", "Mantenibilidad, testabilidad", "Función de más de 60 líneas con llamada de recuperación y llamada al LLM.", "Implementado"),
        ("AP5", "Non-Deterministic Exception Suppression", "Error crítico silenciado o convertido en fallback constante.", "Confiabilidad", "\\texttt{try} con llamada crítica y manejador amplio sin \\texttt{raise}; solo \\texttt{pass}, registro o fallback constante.", "Implementado"),
        ("AP6", "Unvalidated Generation Output", "Salida generada llega a un sumidero sensible sin validación reconocible.", "Confiabilidad, seguridad", "Salida del LLM en \\texttt{json.loads}, \\texttt{eval}, \\texttt{exec} o \\texttt{.execute()} sin guardas.", "No implementado"),
    ]
    body = "\n".join(" & ".join([f"\\textbf{{{row[0]}}}", esc(row[1]), row[2], esc(row[3]), row[4], row[5]]) + r" \\" for row in rows)
    content = longtable(
        r"@{}c p{2.7cm} p{3.5cm} p{2.0cm} p{3.8cm} p{1.5cm}@{}",
        "Taxonomía operacional de antipatrones y estado de implementación de los detectores",
        "tab:taxonomia",
        r"\textbf{ID} & \textbf{Nombre} & \textbf{Definición operacional} & \textbf{Atributo afectado} & \textbf{Regla de detección (AST)} & \textbf{Estado}",
        body,
        6,
        size=r"\scriptsize",
        tabcolsep="2.5pt",
    )
    write("tab02_taxonomia.tex", content)


# ---------------------------------------------------------------------------
# Table 3. Distribution of findings
# ---------------------------------------------------------------------------
def tabla_distribucion() -> None:
    findings = pd.read_csv(RESULTS / "findings.csv")
    counts = findings["ap_id"].value_counts()
    repos = findings.groupby("ap_id")["repo"].nunique()
    names = {
        "AP1": "Hardcoded Prompt Infiltration",
        "AP2": "Vector Store Leakage",
        "AP3": "Hardcoded Provider Lock-in",
        "AP4": "Monolithic RAG Function",
        "AP5": "Non-Deterministic Exception Suppression",
        "AP6": "Unvalidated Generation Output",
    }
    rows = []
    for ap_id, name in names.items():
        if ap_id in ("AP2", "AP6"):
            rows.append(f"\\textbf{{{ap_id}}} & {esc(name)} & --- & --- & --- & No evaluado \\\\")
        else:
            value = int(counts[ap_id])
            rows.append(
                f"\\textbf{{{ap_id}}} & {esc(name)} & {value} & {num(100 * value / len(findings), 2)} & {int(repos[ap_id])} & Implementado \\\\"
            )
    rows.append(r"\midrule")
    rows.append(f"\\textbf{{Total}} & & {len(findings)} & 100,00 & {findings['repo'].nunique()} & 4 de 6 implementados \\\\")
    content = table(
        r"@{}l p{5.0cm} r r r l@{}",
        "Distribución de los hallazgos detectados por antipatrón",
        "tab:distribucion",
        r"\textbf{ID} & \textbf{Antipatrón} & \textbf{Hallazgos} & \textbf{\%} & \textbf{Repos.} & \textbf{Estado}",
        "\n".join(rows),
        size=r"\small",
        tabcolsep="4pt",
    )
    write("tab03_distribucion_hallazgos.tex", content)


# ---------------------------------------------------------------------------
# Table 4. Descriptive statistics
# ---------------------------------------------------------------------------
def tabla_descriptivos() -> None:
    frame = pd.read_csv(RESULTS / "resumen_descriptivo.csv")
    labels = {"todos": "Todos", "con_ap": "Con AP", "sin_ap": "Sin AP"}
    metrics = {"cc_max": r"\texttt{cc\_max}", "mi": r"\texttt{mi}", "cbo_mod": r"\texttt{cbo\_mod}", "cc_media": r"\texttt{cc\_media}", "sloc": r"\texttt{sloc}"}
    order = ["cc_max", "mi", "cbo_mod", "cc_media", "sloc"]
    rows = []
    for metric in order:
        for group in ["todos", "con_ap", "sin_ap"]:
            row = frame[(frame["metric"] == metric) & (frame["group"] == group)].iloc[0]
            rows.append(
                " & ".join(
                    [
                        metrics[metric],
                        labels[group],
                        integer(row["n"]),
                        num(row["mean"], 2),
                        num(row["sd"], 2),
                        num(row["median"], 2),
                        num(row["q1"], 2),
                        num(row["q3"], 2),
                        num(row["min"], 2),
                        num(row["max"], 2),
                    ]
                )
                + r" \\"
            )
        if metric != order[-1]:
            rows.append(r"\midrule")
    content = table(
        r"@{}l l r r r r r r r r@{}",
        "Estadística descriptiva de las métricas por grupo",
        "tab:descriptivos",
        r"\textbf{Métrica} & \textbf{Grupo} & \textbf{n} & \textbf{Media} & \textbf{DE} & \textbf{Mediana} & \textbf{Q1} & \textbf{Q3} & \textbf{Mín.} & \textbf{Máx.}",
        "\n".join(rows),
        size=r"\scriptsize",
        tabcolsep="3pt",
    )
    write("tab04_descriptivos.tex", content)


# ---------------------------------------------------------------------------
# Table 5. Primary Mann-Whitney tests
# ---------------------------------------------------------------------------
def tabla_mann_whitney() -> None:
    frame = pd.read_csv(RESULTS / "estadisticas.csv")
    frame = frame[frame["analysis"] == "mann_whitney"]
    rows = []
    for _, row in frame.iterrows():
        rows.append(
            " & ".join(
                [
                    f"\\texttt{{{esc(row['metric'])}}}",
                    integer(row["n_con"]),
                    integer(row["n_sin"]),
                    num(row["mediana_con"], 2),
                    num(row["mediana_sin"], 2),
                    num(row["U"], 1),
                    pvalue(row["p"]),
                    pvalue(row["p_holm"]),
                    dmath(row["delta_cliff"]),
                    MAGNITUDE.get(row["effect_magnitude"], esc(row["effect_magnitude"])),
                ]
            )
            + r" \\"
        )
    content = table(
        r"@{}l r r r r r l l r l@{}",
        "Contraste primario de Mann--Whitney U entre módulos con y sin antipatrones detectados",
        "tab:mann-whitney",
        r"\textbf{Métrica} & \textbf{n con} & \textbf{n sin} & \textbf{Med.\ con} & \textbf{Med.\ sin} & \textbf{U} & \textbf{p} & \textbf{p Holm} & \textbf{$\delta$} & \textbf{Magnitud}",
        "\n".join(rows),
        size=r"\footnotesize",
        tabcolsep="3pt",
    )
    write("tab05_mann_whitney.tex", content)


# ---------------------------------------------------------------------------
# Table 6. Spearman correlations
# ---------------------------------------------------------------------------
def tabla_spearman() -> None:
    frame = pd.read_csv(RESULTS / "spearman.csv")
    interpretation = {
        "cc_max": "Asociación positiva débil",
        "mi": "Asociación negativa débil",
        "cbo_mod": "Asociación positiva muy débil",
    }
    rows = []
    for _, row in frame.iterrows():
        rows.append(
            " & ".join(
                [
                    f"\\texttt{{{esc(row['metric'])}}}",
                    rho_math(row["rho"]),
                    pvalue(row["p"]),
                    pvalue(row["p_holm"]),
                    integer(row["n"]),
                    interpretation.get(row["metric"], ""),
                ]
            )
            + r" \\"
        )
    content = table(
        r"@{}l r l l r p{5.2cm}@{}",
        "Correlaciones de Spearman entre el número de hallazgos por módulo y las métricas",
        "tab:spearman",
        r"\textbf{Métrica} & \textbf{$\rho$} & \textbf{p} & \textbf{p Holm} & \textbf{n} & \textbf{Lectura}",
        "\n".join(rows),
        size=r"\small",
        tabcolsep="4pt",
    )
    write("tab06_spearman.tex", content)


# ---------------------------------------------------------------------------
# Table 7. SLOC tercile analysis
# ---------------------------------------------------------------------------
def tabla_terciles() -> None:
    frame = pd.read_csv(RESULTS / "estadisticas.csv")
    frame = frame[frame["analysis"] == "mann_whitney_tercil_sloc"].copy()
    order = ["(-0.001, 43.0]", "(43.0, 164.0]", "(164.0, 13018.0]"]
    labels = {
        "(-0.001, 43.0]": ("Inferior", r"$\leq 43$"),
        "(43.0, 164.0]": ("Medio", "43--164"),
        "(164.0, 13018.0]": ("Superior", r"$>164$"),
    }
    metric_order = ["cc_max", "mi", "cbo_mod"]
    rows = []
    for stratum in order:
        name, rango = labels[stratum]
        for metric in metric_order:
            row = frame[(frame["stratum"] == stratum) & (frame["metric"] == metric)].iloc[0]
            status = STATUS.get(row["status"], esc(row["status"]))
            if row["status"] == "n_insuficiente":
                status = r"\textit{n insuficiente}"
            rows.append(
                " & ".join(
                    [
                        name if metric == metric_order[0] else "",
                        rango if metric == metric_order[0] else "",
                        f"\\texttt{{{esc(metric)}}}",
                        integer(row["n_con"]),
                        integer(row["n_sin"]),
                        num(row["mediana_con"], 2),
                        num(row["mediana_sin"], 2),
                        pvalue(row["p"]),
                        dmath(row["delta_cliff"]),
                        MAGNITUDE.get(row["effect_magnitude"], esc(row["effect_magnitude"])),
                        status,
                    ]
                )
                + r" \\"
            )
        if stratum != order[-1]:
            rows.append(r"\midrule")
    content = longtable(
        r"@{}p{1.5cm} p{1.5cm} l r r r r l r p{1.5cm} p{1.7cm}@{}",
        "Análisis exploratorio por terciles de líneas de código (SLOC)",
        "tab:terciles",
        r"\textbf{Tercil} & \textbf{SLOC} & \textbf{Métrica} & \textbf{n con} & \textbf{n sin} & \textbf{Med.\ con} & \textbf{Med.\ sin} & \textbf{p} & \textbf{$\delta$} & \textbf{Magnitud} & \textbf{Estado}",
        "\n".join(rows),
        11,
        size=r"\scriptsize",
        tabcolsep="2pt",
    )
    write("tab07_terciles.tex", content)


# ---------------------------------------------------------------------------
# Table 8. Repository-level sensitivity
# ---------------------------------------------------------------------------
def tabla_sensibilidad() -> None:
    frame = pd.read_csv(RESULTS / "estadisticas.csv")
    frame = frame[frame["analysis"] == "sensibilidad_repositorio"]
    rows = []
    for _, row in frame.iterrows():
        matches = "Sí" if bool(row["direction_matches"]) else "No"
        rows.append(
            " & ".join(
                [
                    f"\\texttt{{{esc(row['metric'])}}}",
                    integer(row["n_con"]),
                    integer(row["n_sin"]),
                    num(row["mediana_con"], 2),
                    num(row["mediana_sin"], 2),
                    dmath(row["delta_cliff"]),
                    DIRECTION.get(row["expected_direction"], esc(row["expected_direction"])),
                    matches,
                    r"\textit{n insuficiente}",
                ]
            )
            + r" \\"
        )
    content = table(
        r"@{}l r r r r r l l p{1.8cm}@{}",
        "Análisis de sensibilidad agregado por repositorio (medianas por repositorio)",
        "tab:sensibilidad",
        r"\textbf{Métrica} & \textbf{n con} & \textbf{n sin} & \textbf{Med.\ con} & \textbf{Med.\ sin} & \textbf{$\delta$} & \textbf{Dirección esperada} & \textbf{¿Coincide?} & \textbf{Estado}",
        "\n".join(rows),
        size=r"\footnotesize",
        tabcolsep="3pt",
    )
    write("tab08_sensibilidad_repositorio.tex", content)


# ---------------------------------------------------------------------------
# Table 9. Hypothesis verification
# ---------------------------------------------------------------------------
def tabla_hipotesis() -> None:
    decisions = pd.read_csv(RESULTS / "decisiones_hipotesis.csv").set_index("regla")
    rows = [
        (
            "H1",
            "Los antipatrones de la taxonomía están presentes en aplicaciones open source GenAI/RAG.",
            "D9",
            f"21 de 23 repositorios (91,3~\\%) con al menos un hallazgo; AP1 en 20, AP5 en 14, AP3 en 6 y AP4 en 3 repositorios.",
            "Apoyada en el piloto",
            "Descriptiva; no cubre AP2 ni AP6.",
        ),
        (
            "H2",
            "La presencia de antipatrones se asocia con mayor deterioro de mantenibilidad y calidad estructural.",
            "D10",
            "3 de 3 métricas primarias con $p_{Holm}<0{,}001$ y magnitud $\\geq$ 0,403 en la dirección esperada (\\texttt{cc\\_max}, \\texttt{mi}, \\texttt{cbo\\_mod}).",
            "Apoyada en el piloto",
            "Asociación correlacional; no causalidad.",
        ),
    ]
    body = "\n".join(" & ".join(row) + r" \\" for row in rows)
    content = table(
        r"@{}c p{3.5cm} c p{4.2cm} p{2.0cm} p{1.9cm}@{}",
        "Correspondencia entre las hipótesis de trabajo y las decisiones estadísticas del piloto",
        "tab:hipotesis",
        r"\textbf{Hip.} & \textbf{Enunciado abreviado} & \textbf{Regla} & \textbf{Evidencia principal} & \textbf{Decisión} & \textbf{Alcance}",
        body,
        size=r"\scriptsize",
        tabcolsep="3pt",
    )
    write("tab09_hipotesis.tex", content)
    _ = decisions


# ---------------------------------------------------------------------------
# Table 10. AI-assisted adjudication
# ---------------------------------------------------------------------------
def tabla_adjudicacion() -> None:
    frame = pd.read_csv(RESULTS / "validacion_investigador.csv")
    detectors = ["AP1", "AP3", "AP4", "AP5"]
    rows = []
    for detector in detectors:
        subset = frame[frame["detector"] == detector]
        verdicts = subset["researcher_verdict"].value_counts()
        confidence = subset["ai_confidence"].value_counts()
        rows.append(
            " & ".join(
                [
                    detector,
                    str(int(verdicts.get("TP", 0))),
                    str(int(verdicts.get("FP", 0))),
                    str(int(verdicts.get("UNCERTAIN", 0))),
                    str(len(subset)),
                    str(int(confidence.get("HIGH", 0))),
                    str(int(confidence.get("MEDIUM", 0))),
                    str(int(confidence.get("LOW", 0))),
                ]
            )
            + r" \\"
        )
    verdicts = frame["researcher_verdict"].value_counts()
    confidence = frame["ai_confidence"].value_counts()
    rows.append(r"\midrule")
    rows.append(
        " & ".join(
            [
                r"\textbf{Total}",
                f"\\textbf{{{int(verdicts.get('TP', 0))}}}",
                f"\\textbf{{{int(verdicts.get('FP', 0))}}}",
                f"\\textbf{{{int(verdicts.get('UNCERTAIN', 0))}}}",
                f"\\textbf{{{len(frame)}}}",
                f"\\textbf{{{int(confidence.get('HIGH', 0))}}}",
                f"\\textbf{{{int(confidence.get('MEDIUM', 0))}}}",
                f"\\textbf{{{int(confidence.get('LOW', 0))}}}",
            ]
        )
        + r" \\"
    )
    content = table(
        r"@{}l r r r r r r r@{}",
        "Propuestas de adjudicación asistida por IA y confianza declarada para los 60 hallazgos muestreados",
        "tab:adjudicacion",
        r"\textbf{Detector} & \textbf{TP} & \textbf{FP} & \textbf{Indet.} & \textbf{Total} & \textbf{Conf.\ alta} & \textbf{Conf.\ media} & \textbf{Conf.\ baja}",
        "\n".join(rows),
        size=r"\small",
        tabcolsep="5pt",
    )
    write("tab10_adjudicacion.tex", content)


# ---------------------------------------------------------------------------
# Table 11. Limitations
# ---------------------------------------------------------------------------
def tabla_limitaciones() -> None:
    rows = [
        ("Ausencia de validación humana independiente", "Validez de constructo", "Las etiquetas de los 60 casos son propuestas de IA; no existe estándar de referencia humano.", "Se declara la procedencia en cada registro."),
        ("Adjudicación asistida por IA con 10 casos inciertos", "Validez de constructo", "La proporción de aciertos no puede interpretarse como precisión confirmada.", "Los casos inciertos se conservan como tales."),
        ("Riesgo de falsos positivos", "Validez interna", "La prevalencia observada puede estar sobreestimada si los detectores aceptan construcciones legítimas.", "Reglas conservadoras y revisión de 60 casos."),
        ("Diseño observacional transversal", "Validez interna", "No permite establecer relaciones causales ni evolución temporal.", "Se reportan asociaciones, no efectos."),
        ("Confusión por tamaño del código", "Validez interna", "Parte de la asociación puede explicarse por el mayor tamaño de los módulos con hallazgos.", "Terciles de SLOC como control parcial."),
        ("Dependencia por anidamiento en repositorios", "Validez externa", "Los módulos de un mismo repositorio no son observaciones independientes.", "Sensibilidad agregada por repositorio, no concluyente."),
        ("Concentración en dos repositorios", "Validez externa", "280 de 445 hallazgos (62,9~\\%) provienen de dos repositorios.", "Se describe la concentración de forma explícita."),
        ("Sensibilidad por repositorio no concluyente", "Validez interna", "Solo dos repositorios carecen de hallazgos; el grupo de comparación es insuficiente.", "Se reporta como limitación de robustez."),
        ("Comparaciones múltiples exploratorias sin Holm", "Validez estadística", "Los nueve contrastes por tercil no están corregidos por multiplicidad.", "Se etiquetan como exploratorios."),
        ("Ausencia de intervalos de confianza y potencia", "Validez estadística", "No se cuantifica la incertidumbre de los tamaños de efecto ni la potencia.", "Se informan tamaños de efecto y n."),
        ("AP2 y AP6 no implementados", "Cobertura de la taxonomía", "La ausencia de estos antipatrones no es evidencia de ausencia empírica.", "Se excluyen de toda inferencia de prevalencia."),
        ("Conclusiones específicas por detector limitadas", "Validez de constructo", "Solo AP1 y AP5 cuentan con 20 casos revisados; AP3 y AP4 tienen 17 y 3.", "No se comparan precisiones entre detectores."),
        ("Sin estimación de exhaustividad (recall)", "Validez de constructo", "No se conoce qué proporción de antipatrones reales detecta el instrumento.", "Se evita toda afirmación de sensibilidad."),
        ("Acoplamiento aproximado a nivel de módulo", "Validez de constructo", "\\texttt{cbo\\_mod} no es el CBO de Chidamber--Kemerer a nivel de clase.", "Se explicita la definición operacional."),
    ]
    body = "\n".join(" & ".join([f"{i + 1}. {esc(row[0])}", esc(row[1]), row[2], row[3]]) + r" \\" for i, row in enumerate(rows))
    content = longtable(
        r"@{}p{3.5cm} p{2.1cm} p{5.4cm} p{3.4cm}@{}",
        "Síntesis de limitaciones metodológicas y su efecto sobre la interpretación",
        "tab:limitaciones",
        r"\textbf{Limitación} & \textbf{Dimensión} & \textbf{Efecto sobre la interpretación} & \textbf{Registro o mitigación}",
        body,
        4,
        size=r"\scriptsize",
        tabcolsep="3pt",
    )
    write("tab11_limitaciones.tex", content)


# ---------------------------------------------------------------------------
# Table 12. Reproducibility artifacts (appendix)
# ---------------------------------------------------------------------------
def tabla_artefactos() -> None:
    rows = [
        ("Selección ampliada", r"\texttt{data/repos\_candidatos\_ampliados.csv}", "915 candidatos deduplicados."),
        ("Preselección", r"\texttt{data/repos\_preseleccion\_ampliada.csv}", "120 repositorios, 40 por banda."),
        ("Exclusiones", r"\texttt{data/repos\_excluidos\_ampliada.csv}", "124 registros con motivo de exclusión."),
        ("Elegibilidad", r"\texttt{data/decision\_muestra\_ampliada.csv}", "24 incluidos y 96 excluidos."),
        ("Relevancia local", r"\texttt{data/evidencia\_relevancia.csv}", "23 CUMPLE y 1 NO CUMPLE."),
        ("Muestra final", r"\texttt{data/repos\_seleccionados.csv}", "23 repositorios con SHA fijado."),
        ("Hallazgos", r"\texttt{data/resultados/findings.csv}", "445 hallazgos con archivo y línea."),
        ("Métricas", r"\texttt{data/resultados/metricas.csv}", "15 768 módulos y cinco métricas."),
        ("Errores de métricas", r"\texttt{data/resultados/metricas\_errors.csv}", "1 error de sintaxis documentado."),
        ("Resumen de escaneo", r"\texttt{data/resultados/scan\_summary.csv}", "15 769 archivos, 0 errores de análisis."),
        ("Contrastes", r"\texttt{data/resultados/estadisticas.csv}", "3 primarios, 9 por tercil y 3 de sensibilidad."),
        ("Correlaciones", r"\texttt{data/resultados/spearman.csv}", "3 correlaciones de Spearman."),
        ("Decisiones", r"\texttt{data/resultados/decisiones\_hipotesis.csv}", "D9 y D10 apoyadas en el piloto."),
        ("Adjudicación IA", r"\texttt{data/resultados/validacion\_investigador.csv}", "60 casos con procedencia asistida por IA."),
        ("Figuras", r"\texttt{scripts/08\_generar\_figuras\_informe.py}", "8 figuras reproducibles en PNG."),
        ("Tablas", r"\texttt{scripts/09\_generar\_tablas\_latex.py}", "Tablas LaTeX generadas desde los CSV."),
    ]
    body = "\n".join(" & ".join([esc(row[0]), row[1], esc(row[2])]) + r" \\" for row in rows)
    content = longtable(
        r"@{}p{3.2cm} p{6.2cm} p{4.6cm}@{}",
        "Inventario de artefactos y trazabilidad de la reproducibilidad",
        "tab:artefactos",
        r"\textbf{Artefacto} & \textbf{Ruta} & \textbf{Contenido}",
        body,
        3,
        size=r"\footnotesize",
        tabcolsep="3pt",
    )
    write("tab12_artefactos.tex", content)


def main() -> None:
    tabla_muestra()
    tabla_taxonomia()
    tabla_distribucion()
    tabla_descriptivos()
    tabla_mann_whitney()
    tabla_spearman()
    tabla_terciles()
    tabla_sensibilidad()
    tabla_hipotesis()
    tabla_adjudicacion()
    tabla_limitaciones()
    tabla_artefactos()
    print(f"\nTotal de tablas generadas: {len(list(OUT.glob('*.tex')))}")


if __name__ == "__main__":
    main()
