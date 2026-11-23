"""Prepare a seed-stable manual-validation sheet without fake human labels."""
from __future__ import annotations

import csv
import random
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def main() -> None:
    source=ROOT/"data/resultados/findings.csv"; rows=list(csv.DictReader(source.open(encoding="utf-8"))) if source.exists() else []
    random.Random(42).shuffle(rows); chosen=[]
    for ap in sorted({row["ap_id"] for row in rows}): chosen.extend(row for row in rows if row["ap_id"]==ap)[:20]
    fields=["repo","ap_id","file","line","col","message","snippet","veredicto_sugerido_agente","nota_sugerida_agente","veredicto_confirmado","nota_confirmada","revisor","fecha_revision"]
    for row in chosen: row.update({"veredicto_sugerido_agente":"","nota_sugerida_agente":"pendiente de revisión asistida por IA","veredicto_confirmado":"","nota_confirmada":"","revisor":"","fecha_revision":""})
    target=ROOT/"data/resultados/validacion_manual.csv"; target.parent.mkdir(parents=True,exist_ok=True)
    with target.open("w",newline="",encoding="utf-8") as handle:
        writer=csv.DictWriter(handle,fieldnames=fields); writer.writeheader(); writer.writerows(chosen)
    print(f"muestra={len(chosen)} semilla=42 precision_confirmada=no estimada / pendiente")
if __name__ == "__main__": main()
