# Progreso de validación del investigador

Este resumen se calcula exclusivamente desde los campos del investigador
en `validacion_investigador.csv`. Las columnas `ai_proposal` y
`ai_confidence` son informativas y no cuentan como verificación
independiente.

## Adjudicación registrada

Los 60 casos fueron adoptados mediante **adjudicación asistida por IA**:
el investigador aceptó las propuestas preliminares sin inspección
independiente del código fuente.

| Estado | Casos |
|---|---:|
| Total | 60 |
| Revisados (`researcher_verdict` no vacío) | 60 |
| Pendientes (`researcher_verdict` vacío) | 0 |
| Adoptados con `review_status=accepted_ai_assisted` | 60 |
| No resueltos (`UNCERTAIN`) | 10 |

## Distribución adoptada (condicional a la adjudicación asistida)

| Veredicto | Casos |
|---|---:|
| TP | 21 |
| FP | 29 |
| UNCERTAIN | 10 |

- Cociente TP/(TP+FP) condicional: **21/50**.
- Esta cifra **no es una precisión confirmada** porque no hubo
  verificación humana independiente y 10 casos permanecen sin resolver.

## Verificación independiente

- `independent_human_verification=si`: **0**.
- `independent_human_verification=no`: **60**.
- No se registró inspección independiente a nivel de fuente.

## Limitaciones

- La distribución TP/FP es condicional a la evaluación asistida por IA.
- Los 10 casos UNCERTAIN no están resueltos y no deben usarse como TP o FP.
- No existe una estimación de precisión independientemente verificada.
- Esta limitación metodológica debe declararse en el artículo final.
