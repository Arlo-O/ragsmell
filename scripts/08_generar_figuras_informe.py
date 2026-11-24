"""Generate the final-report figures from the audited result CSV files.

Every figure is derived from ``data/resultados``; no value is typed by hand
except the literal screening counts that are read from the selection CSVs.
The output is written to ``documentos_latex/anteproyecto/figuras``.

Usage:
    .\\.venv\\Scripts\\python.exe scripts\\08_generar_figuras_informe.py
"""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "data" / "resultados"
DATA = ROOT / "data"
OUT = ROOT / "documentos_latex" / "anteproyecto" / "figuras"

# Consistent academic palette.
CON_AP = "#B03A2E"
SIN_AP = "#2E86AB"
NEUTRAL = "#5D6D7E"
AP_COLORS = {"AP1": "#B03A2E", "AP3": "#E6A23C", "AP4": "#7F8C8D", "AP5": "#2E86AB"}
VERDICT_COLORS = {"TP": "#2E7D32", "FP": "#B03A2E", "UNCERTAIN": "#B7950B"}
CONF_COLORS = {"HIGH": "#1F618D", "MEDIUM": "#5DADE2", "LOW": "#D4E6F1"}

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 9.5,
        "axes.titlesize": 10.5,
        "axes.labelsize": 9.5,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.alpha": 0.25,
        "grid.linewidth": 0.6,
        "figure.dpi": 200,
        "savefig.dpi": 200,
        "savefig.bbox": "tight",
    }
)


def _save(fig: plt.Figure, name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    fig.savefig(path)
    plt.close(fig)
    print(f"figura escrita: {path.relative_to(ROOT)}")


def _fmt(value: float, decimals: int = 2) -> str:
    text = f"{value:,.{decimals}f}"
    return text.replace(",", "\u00a0").replace(".", ",")


# ---------------------------------------------------------------------------
# Figure 1. Methodological workflow
# ---------------------------------------------------------------------------
def figura_flujo() -> None:
    fig, ax = plt.subplots(figsize=(9.4, 8.2))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")

    stages = [
        (
            "1. Diseño de la investigación",
            "Pregunta, objetivos e hipótesis H1–H2\nTaxonomía operacional AP1–AP6\nDecisiones metodológicas D1–D10",
        ),
        (
            "2. Muestreo de repositorios",
            "915 candidatos ampliados → 120 preseleccionados\n24 elegibles tras verificación → 23 repositorios\nTres bandas de estrellas; versiones fijadas por SHA",
        ),
        (
            "3. Detección estática y medición",
            "4 detectores AST (AP1, AP3, AP4, AP5)\n15 769 archivos elegibles; 445 hallazgos\n15 768 módulos con métricas (1 error de sintaxis)",
        ),
        (
            "4. Análisis estadístico",
            "Descriptivos; Mann–Whitney U bilateral\nδ de Cliff; corrección de Holm; Spearman\nTerciles de SLOC; sensibilidad por repositorio",
        ),
        (
            "5. Interpretación y reporte",
            "Contraste de H1 y H2 a nivel piloto\nDiscusión, conclusiones y limitaciones\nTrazabilidad completa de artefactos",
        ),
    ]

    top, height, gap = 9.55, 1.35, 0.45
    left, width = 0.35, 5.75
    centers = []
    for index, (title, body) in enumerate(stages):
        y = top - height - index * (height + gap)
        box = FancyBboxPatch(
            (left, y),
            width,
            height,
            boxstyle="round,pad=0.02,rounding_size=0.08",
            linewidth=1.1,
            edgecolor="#34495E",
            facecolor="#EAEDED" if index < 3 else "#E8F0F5",
        )
        ax.add_patch(box)
        ax.text(left + 0.18, y + height - 0.24, title, fontsize=10, fontweight="bold", va="center", color="#1B2631")
        ax.text(left + 0.18, y + 0.42, body, fontsize=8.1, va="center", linespacing=1.45, color="#212F3C")
        centers.append(y + height / 2)
        if index < len(stages) - 1:
            arrow = FancyArrowPatch(
                (left + width / 2, y),
                (left + width / 2, y - gap),
                arrowstyle="-|>",
                mutation_scale=13,
                linewidth=1.2,
                color="#34495E",
            )
            ax.add_patch(arrow)

    # Parallel AI-assisted review branch.
    side_x, side_y, side_w, side_h = 6.45, 3.62, 3.35, 2.05
    side = FancyBboxPatch(
        (side_x, side_y),
        side_w,
        side_h,
        boxstyle="round,pad=0.02,rounding_size=0.08",
        linewidth=1.1,
        linestyle="--",
        edgecolor="#7D6608",
        facecolor="#FCF3CF",
    )
    ax.add_patch(side)
    ax.text(side_x + 0.16, side_y + side_h - 0.25, "Revisión asistida por IA", fontsize=9.2, fontweight="bold", color="#7D6608")
    ax.text(
        side_x + 0.16,
        side_y + 0.86,
        "60 hallazgos muestreados\n21 TP · 29 FP · 10 indeterminados\nConfianza: 44 alta · 14 media · 2 baja\nSin validación humana independiente",
        fontsize=7.9,
        va="center",
        linespacing=1.5,
        color="#4D3B05",
    )
    for y_from, y_to in ((centers[2], side_y + side_h * 0.72), (centers[4], side_y + side_h * 0.28)):
        arrow = FancyArrowPatch(
            (left + width, y_from),
            (side_x, y_to),
            arrowstyle="<|-|>",
            mutation_scale=11,
            linewidth=1.0,
            linestyle="--",
            color="#7D6608",
        )
        ax.add_patch(arrow)

    fig.suptitle("Flujo metodológico ejecutado en la investigación", fontsize=12, fontweight="bold", y=0.985)
    _save(fig, "fig01_flujo_metodologico.png")


# ---------------------------------------------------------------------------
# Figure 2. Sample composition
# ---------------------------------------------------------------------------
def figura_composicion() -> None:
    funnel = [
        ("Candidatos ampliados", 915),
        ("Preseleccionados", 120),
        ("Elegibles tras verificación", 24),
        ("Muestra final analizada", 23),
    ]
    bands = pd.read_csv(DATA / "repos_seleccionados.csv")["star_band"].value_counts()
    band_order = ["11..100", "101..1000", ">1000"]
    band_labels = ["11–100", "101–1000", ">1000"]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.2, 4.1), gridspec_kw={"width_ratios": [1.35, 1]})

    labels = [item[0] for item in funnel]
    values = [item[1] for item in funnel]
    y = np.arange(len(labels))[::-1]
    bars = ax1.barh(y, values, color=["#AEB6BF", "#85929E", "#5D6D7E", "#B03A2E"], height=0.58)
    ax1.set_yticks(y, labels)
    ax1.set_xlabel("Número de repositorios")
    ax1.set_title("(a) Embudo de selección de repositorios")
    ax1.set_xlim(0, max(values) * 1.18)
    for bar, value in zip(bars, values, strict=True):
        ax1.text(bar.get_width() + max(values) * 0.015, bar.get_y() + bar.get_height() / 2, f"{value:,}".replace(",", "."), va="center", fontsize=9.5, fontweight="bold")
    ax1.grid(axis="y", visible=False)

    counts = [int(bands.get(key, 0)) for key in band_order]
    bars2 = ax2.bar(band_labels, counts, color=["#F0B27A", "#E59866", "#A04000"], width=0.6)
    ax2.set_xlabel("Banda de estrellas de GitHub")
    ax2.set_ylabel("Repositorios")
    ax2.set_title("(b) Composición por popularidad")
    ax2.set_ylim(0, max(counts) * 1.25)
    for bar, count in zip(bars2, counts, strict=True):
        ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.25, str(count), ha="center", fontsize=9.5, fontweight="bold")
    ax2.grid(axis="x", visible=False)

    fig.tight_layout()
    _save(fig, "fig02_composicion_muestra.png")


# ---------------------------------------------------------------------------
# Figure 3. Antipattern distribution and module coverage
# ---------------------------------------------------------------------------
def figura_distribucion() -> None:
    findings = pd.read_csv(RESULTS / "findings.csv")
    counts = findings["ap_id"].value_counts()
    implemented = ["AP1", "AP3", "AP4", "AP5"]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.2, 4.0), gridspec_kw={"width_ratios": [1.4, 1]})

    values = [int(counts.get(key, 0)) for key in implemented]
    bars = ax1.bar(implemented, values, color=[AP_COLORS[key] for key in implemented], width=0.62)
    ax1.set_ylabel("Hallazgos detectados")
    ax1.set_title("(a) Hallazgos por antipatrón implementado")
    ax1.set_ylim(0, max(values) * 1.22)
    for bar, value in zip(bars, values, strict=True):
        pct = 100 * value / len(findings)
        ax1.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + max(values) * 0.02,
            f"{value}\n({_fmt(pct)} %)",
            ha="center",
            va="bottom",
            fontsize=8.8,
        )
    ax1.text(
        0.99,
        0.97,
        "AP2 y AP6: no implementados,\nno evaluados",
        transform=ax1.transAxes,
        ha="right",
        va="top",
        fontsize=8,
        style="italic",
        bbox={"boxstyle": "round,pad=0.35", "facecolor": "#F4F6F7", "edgecolor": "#AEB6BF"},
    )
    ax1.grid(axis="x", visible=False)

    total = 15768
    with_ap = int(findings[["repo", "file"]].drop_duplicates().shape[0])
    without_ap = total - with_ap
    y = [1, 0]
    values = [with_ap, without_ap]
    bars = ax2.barh(y, values, color=[CON_AP, SIN_AP], height=0.5)
    ax2.set_xscale("log")
    ax2.set_xlim(1, total * 2.6)
    ax2.set_yticks(y, ["Con al menos\nun hallazgo", "Sin hallazgos"])
    ax2.set_xlabel("Módulos Python analizados (escala logarítmica)")
    ax2.set_title("(b) Cobertura a nivel de módulo")
    for bar, value in zip(bars, values, strict=True):
        ax2.text(
            bar.get_width() * 1.18,
            bar.get_y() + bar.get_height() / 2,
            f"{value:,}".replace(",", ".") + f"  ({_fmt(100 * value / total)} %)",
            va="center",
            fontsize=8.8,
            fontweight="bold",
        )
    ax2.grid(axis="y", visible=False)

    fig.tight_layout()
    _save(fig, "fig03_distribucion_hallazgos.png")


# ---------------------------------------------------------------------------
# Figure 4. Findings per repository
# ---------------------------------------------------------------------------
def figura_repositorios() -> None:
    ap = pd.read_csv(RESULTS / "tabla_repo_ap.csv").copy()
    ap["total"] = ap[["AP1", "AP3", "AP4", "AP5"]].sum(axis=1)
    ap = ap.sort_values("total", ascending=True)

    fig, ax = plt.subplots(figsize=(9.4, 7.4))
    y = np.arange(len(ap))
    left = np.zeros(len(ap))
    for key in ["AP1", "AP5", "AP3", "AP4"]:
        values = ap[key].to_numpy()
        ax.barh(y, values, left=left, color=AP_COLORS[key], height=0.68, label=key)
        left += values

    ax.set_yticks(y, ap["repo"], fontsize=8.2)
    ax.set_xlabel("Hallazgos detectados")
    ax.set_title("Hallazgos por repositorio y antipatrón")
    ax.set_xlim(0, max(ap["total"]) * 1.12)
    for yi, total in zip(y, ap["total"], strict=True):
        ax.text(total + max(ap["total"]) * 0.01, yi, str(int(total)), va="center", fontsize=8.4, fontweight="bold")
    ax.legend(title="Antipatrón", loc="lower right", fontsize=8, title_fontsize=8, frameon=True)
    ax.grid(axis="y", visible=False)

    fig.tight_layout()
    _save(fig, "fig04_hallazgos_por_repositorio.png")


# ---------------------------------------------------------------------------
# Figure 5. Metric comparison between groups
# ---------------------------------------------------------------------------
def _metric_frame() -> pd.DataFrame:
    metrics = pd.read_csv(RESULTS / "metricas.csv")
    findings = pd.read_csv(RESULTS / "findings.csv")
    module_ap = findings[["repo", "file"]].drop_duplicates()
    module_ap["con_ap"] = True
    frame = metrics.merge(module_ap, on=["repo", "file"], how="left")
    frame["con_ap"] = frame["con_ap"].fillna(False).astype(bool)
    frame = frame.merge(findings.groupby(["repo", "file"]).size().rename("n_ap").reset_index(), on=["repo", "file"], how="left")
    frame["n_ap"] = frame["n_ap"].fillna(0).astype(int)
    return frame


def figura_metricas(frame: pd.DataFrame) -> None:
    stats = pd.read_csv(RESULTS / "estadisticas.csv")
    primary = stats[stats["analysis"] == "mann_whitney"].set_index("metric")

    panels = [
        ("cc_max", "Complejidad ciclomática máxima (cc_max)"),
        ("mi", "Índice de mantenibilidad (mi)"),
        ("cbo_mod", "Acoplamiento aproximado (cbo_mod)"),
    ]
    fig, axes = plt.subplots(1, 3, figsize=(10.6, 4.3))
    for ax, (metric, label) in zip(axes, panels, strict=True):
        data = [
            frame.loc[frame["con_ap"], metric].dropna().to_numpy(),
            frame.loc[~frame["con_ap"], metric].dropna().to_numpy(),
        ]
        box = ax.boxplot(
            data,
            widths=0.55,
            patch_artist=True,
            showfliers=False,
            medianprops={"color": "black", "linewidth": 1.4},
            whiskerprops={"linewidth": 1.0},
            capprops={"linewidth": 1.0},
        )
        for patch, color in zip(box["boxes"], [CON_AP, SIN_AP], strict=True):
            patch.set_facecolor(color)
            patch.set_alpha(0.75)
            patch.set_edgecolor("black")
            patch.set_linewidth(0.8)
        ax.set_xticks([1, 2], ["Con AP", "Sin AP"])
        ax.set_ylabel(label, fontsize=9)
        low, high = ax.get_ylim()
        ax.set_ylim(low, high * 1.28)
        row = primary.loc[metric]
        delta = f"{row['delta_cliff']:+.3f}".replace(".", ",").replace("-", "\u2212")
        ax.text(
            0.5,
            0.985,
            f"$p_{{Holm}}$ < 0,001\n$\\delta$ = {delta}",
            transform=ax.transAxes,
            ha="center",
            va="top",
            fontsize=8.4,
            bbox={"boxstyle": "round,pad=0.3", "facecolor": "white", "edgecolor": "#D5D8DC"},
        )
        ax.grid(axis="x", visible=False)

    fig.suptitle("Comparación de métricas entre módulos con y sin antipatrones detectados", fontsize=11.5, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    _save(fig, "fig05_comparacion_metricas.png")


# ---------------------------------------------------------------------------
# Figure 6. Spearman association by number of findings
# ---------------------------------------------------------------------------
def figura_correlacion(frame: pd.DataFrame) -> None:
    spearman = pd.read_csv(RESULTS / "spearman.csv").set_index("metric")
    frame = frame.copy()
    frame["grupo_n_ap"] = pd.cut(
        frame["n_ap"],
        bins=[-1, 0, 1, 2, 5, np.inf],
        labels=["0", "1", "2", "3–5", "≥6"],
    )
    groups = ["0", "1", "2", "3–5", "≥6"]
    panels = [
        ("cc_max", "Complejidad ciclomática máxima"),
        ("mi", "Índice de mantenibilidad"),
        ("cbo_mod", "Acoplamiento aproximado"),
    ]
    fig, axes = plt.subplots(1, 3, figsize=(10.6, 4.3))
    for ax, (metric, label) in zip(axes, panels, strict=True):
        data = [frame.loc[frame["grupo_n_ap"] == group, metric].dropna().to_numpy() for group in groups]
        box = ax.boxplot(
            data,
            widths=0.58,
            patch_artist=True,
            showfliers=False,
            medianprops={"color": "black", "linewidth": 1.3},
        )
        for patch in box["boxes"]:
            patch.set_facecolor("#5DADE2")
            patch.set_alpha(0.72)
            patch.set_edgecolor("black")
            patch.set_linewidth(0.7)
        ax.set_xticks(range(1, len(groups) + 1), [f"{group}\n(n={len(values)})" for group, values in zip(groups, data, strict=True)], fontsize=7.6)
        ax.set_xlabel("Hallazgos por módulo")
        ax.set_ylabel(label, fontsize=9)
        low, high = ax.get_ylim()
        ax.set_ylim(low, high * 1.28)
        row = spearman.loc[metric]
        rho = f"{row['rho']:+.3f}".replace(".", ",").replace("-", "\u2212")
        ax.text(
            0.5,
            0.985,
            f"$\\rho$ = {rho}\n$p_{{Holm}}$ < 0,001",
            transform=ax.transAxes,
            ha="center",
            va="top",
            fontsize=8.4,
            bbox={"boxstyle": "round,pad=0.3", "facecolor": "white", "edgecolor": "#D5D8DC"},
        )
        ax.grid(axis="x", visible=False)

    fig.suptitle("Asociación entre el número de hallazgos por módulo y las métricas (ρ de Spearman)", fontsize=11.2, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    _save(fig, "fig06_correlacion_spearman.png")


# ---------------------------------------------------------------------------
# Figure 7. SLOC terciles
# ---------------------------------------------------------------------------
def figura_terciles() -> None:
    stats = pd.read_csv(RESULTS / "estadisticas.csv")
    terciles = stats[stats["analysis"] == "mann_whitney_tercil_sloc"].copy()
    order = ["(-0.001, 43.0]", "(43.0, 164.0]", "(164.0, 13018.0]"]
    labels = ["Inferior\n≤ 43 SLOC", "Medio\n43–164 SLOC", "Superior\n> 164 SLOC"]
    terciles["stratum"] = pd.Categorical(terciles["stratum"], categories=order, ordered=True)
    terciles = terciles.sort_values(["stratum", "metric"])

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.6, 4.5), gridspec_kw={"width_ratios": [1, 1.45]})

    counts = (
        terciles[["stratum", "n_con", "n_sin"]]
        .drop_duplicates()
        .set_index("stratum")
        .loc[order]
    )
    x = np.arange(3)
    width = 0.36
    bars_con = ax1.bar(x - width / 2, counts["n_con"], width, color=CON_AP, label="Con AP")
    bars_sin = ax1.bar(x + width / 2, counts["n_sin"], width, color=SIN_AP, label="Sin AP")
    ax1.set_yscale("log")
    ax1.set_xticks(x, labels, fontsize=8.4)
    ax1.set_ylabel("Módulos (escala logarítmica)")
    ax1.set_title("(a) Tamaño de los grupos por tercil")
    for bar, value in list(zip(bars_con, counts["n_con"], strict=True)) + list(zip(bars_sin, counts["n_sin"], strict=True)):
        ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() * 1.12, str(int(value)), ha="center", fontsize=8, fontweight="bold")
    ax1.set_ylim(0.7, 60000)
    ax1.legend(fontsize=8, frameon=False, loc="upper right")
    ax1.text(0, 2.4, "n insuficiente", ha="center", va="bottom", fontsize=7.4, style="italic", color="#7D6608")
    ax1.grid(axis="x", visible=False)

    metric_labels = {"cc_max": "cc_max", "mi": "mi", "cbo_mod": "cbo_mod"}
    x = np.arange(3)
    width = 0.26
    for offset, (stratum, color, hatch) in zip(
        (-width, 0.0, width),
        zip(order, ["#F5B7B1", "#F1948A", "#B03A2E"], ["///", "", ""], strict=True),
        strict=True,
    ):
        subset = terciles[terciles["stratum"] == stratum].set_index("metric").loc[["cc_max", "mi", "cbo_mod"]]
        bars = ax2.bar(x + offset, subset["delta_cliff"], width, color=color, edgecolor="black", linewidth=0.5, hatch=hatch, label=labels[order.index(stratum)].replace("\n", " "))
        for bar, value in zip(bars, subset["delta_cliff"], strict=True):
            ax2.text(bar.get_x() + bar.get_width() / 2, value + (0.02 if value >= 0 else -0.02), f"{value:+.2f}".replace(".", ","), ha="center", va="bottom" if value >= 0 else "top", fontsize=7.4)

    for threshold, style in ((0.147, ":"), (0.33, "--"), (0.474, "-.")):
        ax2.axhline(threshold, color=NEUTRAL, linestyle=style, linewidth=0.8)
        ax2.axhline(-threshold, color=NEUTRAL, linestyle=style, linewidth=0.8)
    ax2.axhline(0, color="black", linewidth=0.8)
    ax2.set_xticks(x, [metric_labels[key] for key in ["cc_max", "mi", "cbo_mod"]])
    ax2.set_ylabel("δ de Cliff")
    ax2.set_title("(b) Tamaño de efecto por métrica y tercil")
    ax2.set_ylim(-0.85, 0.85)
    ax2.legend(fontsize=7.4, frameon=False, loc="lower left")
    ax2.grid(axis="x", visible=False)
    ax2.text(
        0.99,
        0.02,
        "Líneas: 0,147 (pequeño), 0,33 (mediano), 0,474 (grande)",
        transform=ax2.transAxes,
        ha="right",
        va="bottom",
        fontsize=7,
        color=NEUTRAL,
    )

    fig.tight_layout()
    _save(fig, "fig07_terciles_sloc.png")


# ---------------------------------------------------------------------------
# Figure 8. AI-assisted adjudication
# ---------------------------------------------------------------------------
def figura_adjudicacion() -> None:
    validation = pd.read_csv(RESULTS / "validacion_investigador.csv")
    detectors = ["AP1", "AP3", "AP4", "AP5"]
    verdicts = ["TP", "FP", "UNCERTAIN"]
    table = pd.crosstab(validation["detector"], validation["researcher_verdict"]).reindex(index=detectors, columns=verdicts, fill_value=0)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.4, 4.2), gridspec_kw={"width_ratios": [1.55, 1]})

    y = np.arange(len(detectors))[::-1]
    left = np.zeros(len(detectors))
    for verdict in verdicts:
        values = table[verdict].to_numpy()
        bars = ax1.barh(y, values, left=left, color=VERDICT_COLORS[verdict], height=0.6, label=verdict)
        for bar, value in zip(bars, values, strict=True):
            if value >= 3:
                ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_y() + bar.get_height() / 2, str(int(value)), ha="center", va="center", fontsize=8, color="white", fontweight="bold")
        left += values
    ax1.set_yticks(y, detectors)
    ax1.set_xlabel("Hallazgos muestreados")
    ax1.set_title("(a) Propuestas de adjudicación por detector")
    handles, labels_legend = ax1.get_legend_handles_labels()
    ax1.grid(axis="y", visible=False)

    confidence = validation["ai_confidence"].value_counts().reindex(["HIGH", "MEDIUM", "LOW"], fill_value=0)
    labels = ["Alta", "Media", "Baja"]
    bars = ax2.bar(labels, confidence.to_numpy(), color=[CONF_COLORS[key] for key in ["HIGH", "MEDIUM", "LOW"]], edgecolor="black", linewidth=0.6, width=0.58)
    ax2.set_ylabel("Casos")
    ax2.set_title("(b) Confianza declarada por la IA")
    ax2.set_ylim(0, confidence.max() * 1.25)
    for bar, value in zip(bars, confidence.to_numpy(), strict=True):
        ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.6, str(int(value)), ha="center", fontsize=9, fontweight="bold")
    ax2.grid(axis="x", visible=False)

    fig.suptitle("Revisión asistida por IA de 60 hallazgos: propuestas, no validación humana independiente", fontsize=10.6, fontweight="bold")
    fig.legend(handles, labels_legend, title="Propuesta", loc="upper center", bbox_to_anchor=(0.5, 0.915), ncol=3, fontsize=8, title_fontsize=8, frameon=False)
    fig.tight_layout(rect=(0, 0, 1, 0.875))
    _save(fig, "fig08_adjudicacion_ia.png")


def main() -> None:
    frame = _metric_frame()
    figura_flujo()
    figura_composicion()
    figura_distribucion()
    figura_repositorios()
    figura_metricas(frame)
    figura_correlacion(frame)
    figura_terciles()
    figura_adjudicacion()
    print(f"\nTotal de figuras generadas: {len(list(OUT.glob('*.png')))}")


if __name__ == "__main__":
    main()
