# Auditoría de datos empíricos

**Fecha:** 2026-11-23  
**No se modificaron detectores ni decisiones metodológicas.**

## Integridad general

| Control | Resultado |
|---|---:|
| Repositorios en `scan_summary.csv` | 23 |
| Repositorios en `metricas.csv` | 23 |
| Repositorios en `tabla_repo_ap.csv` | 23 |
| Repositorios con hallazgos | 21 |
| Repositorios sin hallazgos | 2 |
| Duplicados de `(repo,file)` en métricas | 0 |
| Hallazgos sin clave correspondiente en métricas | 0 |
| Parse errors | 0 |
| Metric errors | 1 |

Los dos repositorios sin hallazgos no se eliminaron: permanecen representados
en `scan_summary.csv` y `tabla_repo_ap.csv`.

## Conteos

- Archivos Python elegibles escaneados: **15.769**.
- Registros métricos: **15.768**.
- Hallazgos: **445**.
- AP1: **273**.
- AP3: **17**.
- AP4: **3**.
- AP5: **152**.
- AP2 y AP6: columnas presentes en la matriz, pero no implementados.

La diferencia de un archivo se explica por el error de métricas registrado en:

```text
BerriAI/litellm/litellm/secret_managers/base_secret_manager.py
SyntaxError: SyntaxError at line: 9
```

Ese archivo no produjo hallazgos. El escáner no registró un parse error para
él; el fallo ocurrió durante `module_metrics`, por lo que queda como error de
métrica y no como error de escaneo. No se reparó código de terceros.

## Matriz repositorio × antipatrón

`tabla_repo_ap.csv` tiene 23 filas y las columnas:

```text
repo, AP1, AP2, AP3, AP4, AP5, AP6, tiene_ap
```

Los ceros de AP2/AP6 representan que esos detectores no están implementados
en el núcleo; no constituyen evidencia de ausencia del antipatrón.

## Archivos auditados

Se revisaron `findings.csv`, `parse_errors.csv`, `scan_summary.csv`,
`metricas.csv`, `metricas_errors.csv`, `tabla_repo_ap.csv` y
`validacion_manual.csv`. La suma de `n_findings` de `scan_summary.csv` es 445,
igual que el número de filas de `findings.csv` y la suma por detector.

## Estado

La auditoría de datos está COMPLETADA. La limitación pendiente es el único
error de métrica, que se conserva explícitamente. No se ejecutó inferencia.
