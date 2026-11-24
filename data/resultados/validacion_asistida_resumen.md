# Resumen de validación asistida

## Integridad

- Filas originales: **60**.
- Evaluaciones IA: **60**.
- Identificadores faltantes o extra: **0**.
- Duplicados: **0**.
- Lotes: **6**, con **10 filas cada uno**.
- La muestra original y semilla 42 se conservaron.

## Propuestas IA (no confirmadas)

| Propuesta | Total |
|---|---:|
| TP | 21 |
| FP | 29 |
| UNCERTAIN | 10 |

| Confianza | Total |
|---|---:|
| HIGH | 44 |
| MEDIUM | 14 |
| LOW | 2 |

La distribución anterior HIGH=37, MEDIUM=20, LOW=3 queda corregida: el conteo
directo de `revision_ia_preliminar.csv` es HIGH=44, MEDIUM=14, LOW=2.

## Duplicaciones lógicas identificadas

- AP1: dos consultas `system_query` en automem; dos prompts de procedimiento en `multimind-sdk`; dos prompts GUI de Khoj.
- AP3: dos defaults en `browser_use/agent/service.py`; dos ramas en `browser_use/cli.py`; varias familias de adapters/defaults en LlamaIndex.
- AP5: dos fallbacks de capacidades en LiteLLM; métodos síncrono/asíncrono del code interpreter de LlamaIndex.

Las filas relacionadas no se eliminaron ni fusionaron.

## Estado metodológico

No se modificaron campos humanos, conclusiones, detectores, taxonomía, decisiones D1–D10 ni el muestreo. No se ejecutó inferencia.

**Actualización 2026-11-23:** el investigador adoptó las 60 propuestas en
`validacion_investigador.csv` como decisiones provisionales
(`review_status=accepted_ai_assisted`), sin verificación independiente. Los 10
casos UNCERTAIN siguen sin resolver. La distribución resultante es condicional
a la adjudicación asistida y no constituye precisión confirmada.
