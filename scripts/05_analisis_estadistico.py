"""Reproducible non-parametric analysis of module-level results."""
from __future__ import annotations

import csv
from pathlib import Path

import pandas as pd
from scipy.stats import mannwhitneyu, spearmanr
from statsmodels.stats.multitest import multipletests

ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/"data/resultados"
PRIMARY=["cc_max","mi","cbo_mod"]

def cliff(a,b):
    values=[(x>y)-(x<y) for x in a for y in b]
    return sum(values)/(len(a)*len(b)) if a and b else None

def write(name, rows, fields):
    with (OUT/name).open("w",newline="",encoding="utf-8") as handle:
        writer=csv.DictWriter(handle,fieldnames=fields); writer.writeheader(); writer.writerows(rows)

def main() -> None:
    OUT.mkdir(parents=True,exist_ok=True); findings=OUT/"findings.csv"; metrics=OUT/"metricas.csv"
    f=pd.read_csv(findings) if findings.exists() else pd.DataFrame(columns=["repo","file","ap_id"])
    m=pd.read_csv(metrics) if metrics.exists() else pd.DataFrame(columns=["repo","file",*PRIMARY,"cc_media","sloc"])
    if not m.empty:
        counts=f.groupby(["repo","file"]).size().rename("n_ap") if not f.empty else pd.Series(dtype=int)
        m=m.drop_duplicates(["repo","file"]).merge(counts,left_on=["repo","file"],right_index=True,how="left"); m["n_ap"]=m["n_ap"].fillna(0).astype(int); m["con_ap"]=m["n_ap"]>0
    rows=[]; pvals=[]
    for metric in PRIMARY:
        if m.empty or metric not in m: rows.append({"analysis":"mann_whitney","metric":metric,"status":"no_disponible"}); continue
        a=m.loc[m.con_ap,metric].dropna().tolist(); b=m.loc[~m.con_ap,metric].dropna().tolist(); base={"analysis":"mann_whitney","metric":metric,"n_con":len(a),"n_sin":len(b),"mediana_con":pd.Series(a).median() if a else None,"mediana_sin":pd.Series(b).median() if b else None,"delta_cliff":cliff(a,b)}
        if len(a)<5 or len(b)<5: base.update({"status":"n_insuficiente","U":None,"p":None}); rows.append(base); continue
        test=mannwhitneyu(a,b,alternative="two-sided"); base.update({"status":"calculado","U":test.statistic,"p":test.pvalue}); rows.append(base); pvals.append(test.pvalue)
    adjusted=multipletests(pvals,method="holm")[1].tolist() if pvals else []
    index=0
    for row in rows:
        if row.get("p") is not None: row["p_holm"]=adjusted[index]; index+=1
        else: row["p_holm"]=None
    spearman=[]
    for metric in PRIMARY:
        if m.empty or metric not in m or m["n_ap"].nunique()<2 or m[metric].dropna().empty: spearman.append({"metric":metric,"status":"no_calculable"}); continue
        subset=m[["n_ap",metric]].dropna()
        if len(subset)<5 or subset[metric].nunique()<2: spearman.append({"metric":metric,"status":"n_insuficiente"}); continue
        rho,p=spearmanr(subset["n_ap"],subset[metric]); spearman.append({"metric":metric,"rho":rho,"p":p,"status":"calculado","n":len(subset)})
    descriptive=[]
    for metric in [*PRIMARY,"cc_media","sloc"]:
        if metric in m: descriptive.append({"metric":metric,"n":int(m[metric].count()),"mediana":m[metric].median(),"q1":m[metric].quantile(.25),"q3":m[metric].quantile(.75)})
    write("estadisticas.csv",rows,["analysis","metric","n_con","n_sin","mediana_con","mediana_sin","U","p","p_holm","delta_cliff","status"]); write("spearman.csv",spearman,["metric","rho","p","n","status"]); write("resumen_descriptivo.csv",descriptive,["metric","n","mediana","q1","q3"])
    repos=int(m["repo"].nunique()) if not m.empty and "repo" in m else 0; decisions=[{"regla":"D9","estado":"no evaluable sin tabla repo/AP real" if repos==0 else "pendiente de tabla_repo_ap","repos":repos},{"regla":"D10","estado":"piloto; revisar estadísticas y validación"}]
    write("decisiones_hipotesis.csv",decisions,["regla","estado","repos"])
    print(f"modulos={len(m)} repos={repos} estadisticas={len(rows)}")
if __name__ == "__main__": main()
