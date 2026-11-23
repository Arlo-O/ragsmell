# ragsmell

Prototipo de investigación para detectar, mediante AST, cuatro antipatrones
operacionales en aplicaciones Python de GenAI/RAG: AP1, AP3, AP4 y AP5.
No es una auditoría certificada ni prueba causal sobre mantenibilidad.

## Requisitos e instalación

- Python >= 3.11.
- Instalación editable: `python -m pip install -e ".[dev]"`.
- El entorno virtual y `.env` son locales y no se versionan.

## Uso

```text
ragsmell version
ragsmell scan ruta/al/repositorio --out data/resultados/findings.csv
ragsmell scan ruta/al/repositorio --only AP1,AP5
ragsmell metrics ruta/al/repositorio --out data/resultados/metricas.csv
```

El escáner excluye pruebas, documentación, ejemplos, scripts, entornos,
builds, dependencias instaladas y archivos mayores de 1 MB. Las rutas de los
CSV son relativas y POSIX. `cbo_mod` cuenta módulos importados distintos que
no pertenecen a la biblioteca estándar; es una aproximación por módulo, no el
CBO original por clase.

## Reproducción del piloto

Ejecutar desde la raíz y conservar los `commit_sha`:

```text
python scripts/01_recolectar_repos.py
python scripts/02b_filtrar_seleccionar.py
python scripts/02_clonar_repos.py
python scripts/03_ejecutar_detectores.py
python scripts/04_calcular_metricas.py
python scripts/05_analisis_estadistico.py
python scripts/06_muestra_validacion.py
```

Los scripts registran candidatos, exclusiones, errores de clonación,
hallazgos, errores de parseo, métricas, estadística y la hoja de validación en
`data/`. No se rellenan resultados cuando la evidencia no está disponible.

## Validación y límites

La hoja `validacion_manual.csv` separa las sugerencias asistidas por IA de las
etiquetas confirmadas por una persona. La precisión confirmada queda pendiente
hasta que existan etiquetas humanas; no se estima recall sin un conjunto de
referencia exhaustivo. La muestra es no probabilística, por criterios, y los
módulos de un mismo repositorio no son independientes.

## GitHub y secretos

La API puede usarse sin token, con límites públicos. Si se dispone de un token
de solo lectura, cargarlo únicamente en la sesión local de PowerShell
(`$env:GITHUB_TOKEN = "..."`) o Bash (`export GITHUB_TOKEN=...`). Nunca se
incluye en el prompt, código, CSV, logs o commits. `data/clones/`, `.env` y
caches están ignorados por Git.

La taxonomía, decisiones, arquitectura, amenazas a la validez y estado de
ejecución están en `docs/`.
