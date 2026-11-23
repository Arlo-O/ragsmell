# ragsmell

Prototipo de investigación para detectar, mediante AST, antipatrones arquitectónicos en aplicaciones Python GenAI/RAG. No es una auditoría certificada ni prueba causal sobre mantenibilidad.

## Requisitos e instalación

Se requiere Python 3.11 o superior. Desde la raíz del repositorio:

```text
python -m pip install -e ".[dev]"
```

## Uso

```text
ragsmell version
ragsmell scan ruta/al/repositorio --out data/resultados/findings.csv
ragsmell scan ruta/al/repositorio --only AP1,AP5
ragsmell metrics ruta/al/repositorio --out data/resultados/metricas.csv
```

Los detectores núcleo son AP1, AP3, AP4 y AP5. AP2 y AP6 permanecen en evaluación y no se incluyen en el análisis hasta superar fixtures y revisión técnica. La precisión confirmada queda pendiente mientras no existan etiquetas humanas; las sugerencias asistidas por IA no la sustituyen.

## Reproducción del piloto

Ejecutar en orden `scripts/01_recolectar_repos.py`, `02_clonar_repos.py`, `03_ejecutar_detectores.py`, `04_calcular_metricas.py`, `05_analisis_estadistico.py` y `06_muestra_validacion.py`. Los scripts dejan metadatos, SHAs y errores; no rellenan resultados ausentes.

El token GitHub, si se usa, debe ser de solo lectura y nunca se pega en el chat ni se versiona. En PowerShell: `$env:GITHUB_TOKEN = "..."`; en Bash: `export GITHUB_TOKEN="..."`. `.env`, clones y caches están ignorados.

## Limitaciones

`cbo_mod` cuenta módulos externos distintos importados y no equivale al CBO original por clase. Las reglas son heurísticas, el análisis es piloto, la muestra es no probabilística y por criterios, y la dependencia entre módulos de un mismo repositorio limita la independencia estadística. Los CSV usan `repo` y `file` como clave conjunta.
