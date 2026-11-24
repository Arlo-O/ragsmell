"""Reproducible non-parametric analysis of module-level results.

Implements D1-D10 without altering the approved tests, thresholds, hypotheses
or expected directions:

- D1: the statistical unit is the Python module; repositories are grouping and
  selection units.
- D4: dependent variables are ``con_ap`` (0/1) and ``n_ap`` (findings/module).
- D5: primary metrics are ``cc_max``, ``mi`` and ``cbo_mod``;
  ``cc_media`` and ``sloc`` are descriptive.
- D7: size control by ``sloc`` terciles and repository-level median sensitivity.
- D8: Mann-Whitney U, Spearman, Cliff's delta, alpha 0.05 and Holm correction.
- D9/D10: evaluated literally and reported as pilot evidence, not definitive
  confirmation.

Run ``python scripts/05_analisis_estadistico.py --selftest`` to verify the
effect-size and correction helpers with synthetic data without touching the
study outputs.
"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path

import pandas as pd
from scipy.stats import mannwhitneyu, spearmanr
from statsmodels.stats.multitest import multipletests

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/resultados"
PRIMARY = ["cc_max", "mi", "cbo_mod"]
DESCRIPTIVE = ["cc_media", "sloc"]
CORE_APS = ["AP1", "AP3", "AP4", "AP5"]
EXPECTED_SIGN = {"cc_max": 1, "mi": -1, "cbo_mod": 1}
EXPECTED_DIRECTION = {
    "cc_max": "mayor_en_con_ap",
    "mi": "menor_en_con_ap",
    "cbo_mod": "mayor_en_con_ap",
}
ALPHA = 0.05
CLIFF_MIN = 0.147
MIN_GROUP = 5
csv.field_size_limit(10_000_000)


def cliff_delta(a: list[float], b: list[float]) -> float | None:
    """Cliff's delta with a = con_ap and b = sin_ap.

    delta = P(a > b) - P(a < b). Positive values mean the con_ap group tends to
    have larger values. Ties contribute zero. This orientation must not change.
    """
    if not a or not b:
        return None
    comparisons = [(x > y) - (x < y) for x in a for y in b]
    return sum(comparisons) / (len(a) * len(b))


def effect_label(delta: float | None) -> str:
    if delta is None:
        return "no_calculable"
    magnitude = abs(delta)
    if magnitude < CLIFF_MIN:
        return "despreciable"
    if magnitude < 0.33:
        return "pequeno"
    if magnitude < 0.474:
        return "mediano"
    return "grande"


def direction_observed(delta: float | None) -> str:
    if delta is None:
        return "no_calculable"
    if delta > 0:
        return "mayor_en_con_ap"
    if delta < 0:
        return "menor_en_con_ap"
    return "sin_diferencia"


def holm(pvalues: list[float]) -> list[float]:
    if not pvalues:
        return []
    return multipletests(pvalues, method="holm")[1].tolist()


def write_csv(name: str, rows: list[dict[str, object]], fields: list[str]) -> None:
    with (OUT / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def tercile_table(modules: pd.DataFrame) -> tuple[pd.Series, list[str]]:
    """Assign sloc terciles, tolerating ties, missing values and few strata."""
    labels = pd.Series(pd.NA, index=modules.index, dtype="object")
    valid = modules["sloc"].notna()
    notes: list[str] = []
    if valid.sum() < 3:
        notes.append("sloc con menos de tres observaciones; no se forman terciles")
        return labels, notes
    try:
        bins = pd.qcut(modules.loc[valid, "sloc"], q=3, duplicates="drop")
    except ValueError as error:
        notes.append(f"qcut no calculable: {error}")
        return labels, notes
    distinct = bins.nunique()
    if distinct < 3:
        notes.append(f"los empates producen {distinct} estrato(s) reales en lugar de 3")
    labels.loc[valid] = bins.astype(str)
    return labels, notes


def mann_whitney_row(
    modules: pd.DataFrame,
    metric: str,
    analysis: str,
    stratum: str,
    note: str,
) -> dict[str, object]:
    subset = modules[[metric, "con_ap"]].dropna()
    a = subset.loc[subset["con_ap"], metric].tolist()
    b = subset.loc[~subset["con_ap"], metric].tolist()
    delta = cliff_delta(a, b)
    row: dict[str, object] = {
        "analysis": analysis,
        "metric": metric,
        "stratum": stratum,
        "n_con": len(a),
        "n_sin": len(b),
        "mediana_con": pd.Series(a).median() if a else None,
        "mediana_sin": pd.Series(b).median() if b else None,
        "U": None,
        "p": None,
        "p_holm": None,
        "delta_cliff": delta,
        "expected_direction": EXPECTED_DIRECTION[metric],
        "direction_observed": direction_observed(delta),
        "direction_matches": (
            None if delta is None else direction_observed(delta) == EXPECTED_DIRECTION[metric]
        ),
        "effect_magnitude": effect_label(delta),
        "missing": int(modules[metric].isna().sum()),
        "status": "no_calculable",
        "note": note,
    }
    if len(a) < MIN_GROUP or len(b) < MIN_GROUP:
        row["status"] = "n_insuficiente"
        row["note"] = (
            f"{note}; se requieren al menos {MIN_GROUP} observaciones por grupo"
        ).strip("; ")
        return row
    test = mannwhitneyu(a, b, alternative="two-sided")
    row["U"] = float(test.statistic)
    row["p"] = float(test.pvalue)
    row["status"] = "calculado_significativo" if test.pvalue < ALPHA else "calculado_no_significativo"
    return row


def spearman_row(modules: pd.DataFrame, metric: str) -> dict[str, object]:
    row: dict[str, object] = {
        "metric": metric,
        "rho": None,
        "p": None,
        "p_holm": None,
        "n": 0,
        "status": "no_calculable",
        "note": "",
    }
    if metric not in modules:
        row["note"] = "métrica ausente"
        return row
    subset = modules[["n_ap", metric]].dropna()
    row["n"] = len(subset)
    if len(subset) < MIN_GROUP:
        row["status"] = "n_insuficiente"
        row["note"] = f"se requieren al menos {MIN_GROUP} observaciones"
        return row
    if subset["n_ap"].nunique() < 2:
        row["note"] = "n_ap constante"
        return row
    if subset[metric].nunique() < 2:
        row["note"] = f"{metric} constante"
        return row
    rho, p = spearmanr(subset["n_ap"], subset[metric])
    row["rho"] = float(rho)
    row["p"] = float(p)
    row["status"] = "calculado_significativo" if p < ALPHA else "calculado_no_significativo"
    return row


def evaluate_d9(findings: pd.DataFrame, repo_ids: list[str]) -> dict[str, object]:
    counts = {ap: findings.loc[findings["ap_id"] == ap, "repo"].nunique() for ap in CORE_APS}
    repos_with_any = findings.loc[findings["ap_id"].isin(CORE_APS), "repo"].nunique()
    proportion = repos_with_any / len(repo_ids) if repo_ids else 0.0
    conditions = {ap: counts[ap] >= 2 for ap in CORE_APS}
    supported = all(conditions.values()) and proportion >= 0.5
    return {
        "regla": "D9",
        "criterio": (
            "cada antipatrón implementado aparece en >=2 repositorios y >=50% de "
            "los repositorios tiene uno o más antipatrones"
        ),
        "entradas": (
            f"repositorios={len(repo_ids)}; repos_con_ap={repos_with_any} "
            f"({proportion:.3f}); repos_por_ap="
            + ", ".join(f"{ap}={counts[ap]}" for ap in CORE_APS)
        ),
        "resultado": (
            "condiciones_por_ap="
            + ", ".join(f"{ap}={conditions[ap]}" for ap in CORE_APS)
            + f"; proporcion_repos={proportion:.3f}"
        ),
        "estado": "apoyada_en_el_piloto" if supported else "no_apoyada_en_el_piloto",
        "limitaciones": (
            "AP2/AP6 no están implementados y no entran en el criterio; los "
            "resultados del piloto no confirman definitivamente H1."
        ),
    }


def evaluate_d10(primary_rows: list[dict[str, object]]) -> dict[str, object]:
    evaluable = [row for row in primary_rows if row["p_holm"] is not None]
    satisfied = [
        row["metric"]
        for row in evaluable
        if row["p_holm"] < ALPHA
        and row["direction_matches"]
        and abs(row["delta_cliff"]) >= CLIFF_MIN
    ]
    if len(evaluable) < 2:
        state = "no_evaluable"
    elif len(satisfied) >= 2:
        state = "apoyada_en_el_piloto"
    else:
        state = "no_apoyada_en_el_piloto"
    detail = "; ".join(
        f"{row['metric']}: p_holm={row['p_holm']:.6g}, delta={row['delta_cliff']:.3f}, "
        f"direccion_ok={row['direction_matches']}"
        for row in evaluable
    )
    return {
        "regla": "D10",
        "criterio": (
            ">=2 de 3 métricas primarias con p_holm<0.05, dirección esperada y "
            "|delta de Cliff|>=0.147"
        ),
        "entradas": detail or "sin contrastes calculables",
        "resultado": f"metricas_que_cumplen={satisfied}; total={len(satisfied)}/3",
        "estado": state,
        "limitaciones": (
            "El piloto ensaya el procedimiento y no confirma por sí solo H2; la "
            "asociación es correlacional, no causal."
        ),
    }


def selftest() -> None:
    """Small synthetic checks for delta, Holm and Mann-Whitney orientation."""
    assert cliff_delta([1, 2, 3], [4, 5, 6]) == -1.0
    assert cliff_delta([1, 2, 3], [1, 2, 3]) == 0.0
    # Pairs for a=[1,2], b=[2,3]: three losses and one tie.
    assert abs(cliff_delta([1, 2], [2, 3]) - (-0.75)) < 1e-12
    expected = multipletests([0.01, 0.04, 0.03], method="holm")[1].tolist()
    assert holm([0.01, 0.04, 0.03]) == expected
    assert abs(mannwhitneyu([1, 2, 3], [4, 5, 6], alternative="two-sided").statistic - 0.0) < 1e-12
    print("selftest=ok")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--selftest", action="store_true", help="run synthetic checks only")
    args = parser.parse_args()
    if args.selftest:
        selftest()
        return

    OUT.mkdir(parents=True, exist_ok=True)
    findings_path = OUT / "findings.csv"
    metrics_path = OUT / "metricas.csv"
    selected_path = ROOT / "data/repos_seleccionados.csv"
    for path in (findings_path, metrics_path, selected_path):
        if not path.exists():
            raise SystemExit(f"missing required input: {path}")

    findings = pd.read_csv(findings_path)
    metrics = pd.read_csv(metrics_path)
    selected = pd.read_csv(selected_path)
    required_findings = {"repo", "file", "ap_id"}
    required_metrics = {"repo", "file", *PRIMARY, *DESCRIPTIVE}
    if not required_findings.issubset(findings.columns):
        raise SystemExit(f"findings.csv missing columns: {required_findings - set(findings.columns)}")
    if not required_metrics.issubset(metrics.columns):
        raise SystemExit(f"metricas.csv missing columns: {required_metrics - set(metrics.columns)}")
    if "full_name" not in selected.columns:
        raise SystemExit("repos_seleccionados.csv missing full_name")

    repo_ids = selected["full_name"].dropna().astype(str).drop_duplicates().tolist()
    duplicate_metrics = int(metrics.duplicated(["repo", "file"]).sum())
    if duplicate_metrics:
        metrics = metrics.drop_duplicates(["repo", "file"])

    counts = findings.groupby(["repo", "file"]).size().rename("n_ap")
    modules = metrics.merge(counts, left_on=["repo", "file"], right_index=True, how="left")
    modules["n_ap"] = modules["n_ap"].fillna(0).astype(int)
    modules["con_ap"] = modules["n_ap"] > 0

    module_keys = set(zip(modules["repo"], modules["file"]))
    findings_keys = set(zip(findings["repo"], findings["file"]))
    findings_without_metrics = findings_keys - module_keys
    repos_with_modules = set(modules["repo"])
    repos_without_modules = [repo for repo in repo_ids if repo not in repos_with_modules]
    modules["sloc_tercile"], tercile_notes = tercile_table(modules)

    stats_rows: list[dict[str, object]] = []
    for metric in PRIMARY:
        stats_rows.append(
            mann_whitney_row(
                modules,
                metric,
                "mann_whitney",
                "todos",
                "familia primaria; Holm sobre las tres métricas",
            )
        )
    primary_rows = stats_rows[:]
    family = [(index, row["p"]) for index, row in enumerate(stats_rows) if row["p"] is not None]
    for (index, _), adjusted in zip(family, holm([p for _, p in family]), strict=True):
        stats_rows[index]["p_holm"] = adjusted

    for label in sorted(modules["sloc_tercile"].dropna().unique()):
        stratum = modules.loc[modules["sloc_tercile"] == label]
        for metric in PRIMARY:
            stats_rows.append(
                mann_whitney_row(
                    stratum,
                    metric,
                    "mann_whitney_tercil_sloc",
                    str(label),
                    "estrato de tamaño; análisis exploratorio sin Holm",
                )
            )

    repo_presence = modules.groupby("repo")["con_ap"].any()
    repo_metrics = modules.groupby("repo")[
        ["cc_max", "mi", "cbo_mod", "cc_media", "sloc"]
    ].median()
    repo_frame = repo_metrics.copy()
    repo_frame["con_ap"] = repo_presence.reindex(repo_frame.index).fillna(False).astype(bool)
    for metric in PRIMARY:
        temp = repo_frame[[metric, "con_ap"]].dropna()
        # Reuse the module-level comparison machinery on repository medians.
        pseudo = pd.DataFrame({metric: temp[metric], "con_ap": temp["con_ap"]})
        stats_rows.append(
            mann_whitney_row(
                pseudo,
                metric,
                "sensibilidad_repositorio",
                "medianas_por_repositorio",
                "sensibilidad agregada; no reemplaza un modelo multinivel",
            )
        )

    spearman_rows = [spearman_row(modules, metric) for metric in PRIMARY]
    spearman_family = [row for row in spearman_rows if row["p"] is not None]
    for row, adjusted in zip(
        spearman_family, holm([row["p"] for row in spearman_family]), strict=True
    ):
        row["p_holm"] = adjusted

    descriptive_rows: list[dict[str, object]] = []
    for metric in [*PRIMARY, *DESCRIPTIVE]:
        groups = [
            ("todos", modules),
            ("con_ap", modules.loc[modules["con_ap"]]),
            ("sin_ap", modules.loc[~modules["con_ap"]]),
        ]
        for label, frame in groups:
            values = frame[metric].dropna()
            descriptive_rows.append(
                {
                    "metric": metric,
                    "group": label,
                    "n": int(values.count()),
                    "missing": int(frame[metric].isna().sum()),
                    "mean": values.mean() if len(values) else None,
                    "sd": values.std() if len(values) > 1 else None,
                    "median": values.median() if len(values) else None,
                    "q1": values.quantile(0.25) if len(values) else None,
                    "q3": values.quantile(0.75) if len(values) else None,
                    "min": values.min() if len(values) else None,
                    "max": values.max() if len(values) else None,
                }
            )

    ap_ids = ["AP1", "AP2", "AP3", "AP4", "AP5", "AP6"]
    ap_counts = findings.groupby(["repo", "ap_id"]).size()
    pivot_rows = []
    for repo in repo_ids:
        values = {ap: int(ap_counts.get((repo, ap), 0)) for ap in ap_ids}
        pivot_rows.append({"repo": repo, **values, "tiene_ap": any(values[ap] > 0 for ap in ap_ids)})
    write_csv("tabla_repo_ap.csv", pivot_rows, ["repo", *ap_ids, "tiene_ap"])

    repo_rows = []
    for repo in repo_ids:
        frame = modules.loc[modules["repo"] == repo]
        repo_rows.append(
            {
                "repo": repo,
                "modules": len(frame),
                "modules_with_ap": int(frame["con_ap"].sum()),
                "pct_modules_with_ap": (
                    float(frame["con_ap"].mean()) if len(frame) else None
                ),
                "findings": int((findings["repo"] == repo).sum()),
                "median_cc_max": frame["cc_max"].median() if len(frame) else None,
                "median_mi": frame["mi"].median() if len(frame) else None,
                "median_cbo_mod": frame["cbo_mod"].median() if len(frame) else None,
                "median_sloc": frame["sloc"].median() if len(frame) else None,
            }
        )
    write_csv(
        "resumen_repositorio.csv",
        repo_rows,
        [
            "repo",
            "modules",
            "modules_with_ap",
            "pct_modules_with_ap",
            "findings",
            "median_cc_max",
            "median_mi",
            "median_cbo_mod",
            "median_sloc",
        ],
    )

    decisions = [evaluate_d9(findings, repo_ids), evaluate_d10(primary_rows)]
    write_csv(
        "decisiones_hipotesis.csv",
        decisions,
        ["regla", "criterio", "entradas", "resultado", "estado", "limitaciones"],
    )
    write_csv(
        "estadisticas.csv",
        stats_rows,
        [
            "analysis",
            "metric",
            "stratum",
            "n_con",
            "n_sin",
            "mediana_con",
            "mediana_sin",
            "U",
            "p",
            "p_holm",
            "delta_cliff",
            "expected_direction",
            "direction_observed",
            "direction_matches",
            "effect_magnitude",
            "missing",
            "status",
            "note",
        ],
    )
    write_csv(
        "spearman.csv",
        spearman_rows,
        ["metric", "rho", "p", "p_holm", "n", "status", "note"],
    )
    write_csv(
        "resumen_descriptivo.csv",
        descriptive_rows,
        ["metric", "group", "n", "missing", "mean", "sd", "median", "q1", "q3", "min", "max"],
    )

    execution = [
        {"key": "modules", "value": len(modules)},
        {"key": "repositories_selected", "value": len(repo_ids)},
        {"key": "repositories_with_modules", "value": len(repos_with_modules)},
        {"key": "repositories_without_modules", "value": len(repos_without_modules)},
        {"key": "findings", "value": len(findings)},
        {"key": "findings_without_metric_module", "value": len(findings_without_metrics)},
        {"key": "duplicate_metric_keys_removed", "value": duplicate_metrics},
        {"key": "sloc_tercile_groups", "value": int(modules["sloc_tercile"].nunique())},
        {"key": "sloc_tercile_notes", "value": " | ".join(tercile_notes) or "sin observaciones"},
    ]
    for metric in [*PRIMARY, *DESCRIPTIVE]:
        execution.append(
            {"key": f"missing_{metric}", "value": int(modules[metric].isna().sum())}
        )
    write_csv("resumen_ejecucion.csv", execution, ["key", "value"])

    print(
        f"modules={len(modules)} repos={len(repo_ids)} findings={len(findings)} "
        f"stats={len(stats_rows)} spearman={len(spearman_rows)} "
        f"terciles={modules['sloc_tercile'].nunique()} "
        f"findings_without_metrics={len(findings_without_metrics)}"
    )


if __name__ == "__main__":
    main()
