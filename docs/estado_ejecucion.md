# Estado de ejecución — `ragsmell`

**Fecha de auditoría:** 2026-11-23  
**Fuente de verdad:** árbol de trabajo y Git local.  
**Convención:** `COMPLETADO` requiere evidencia ejecutada; `PARCIAL` indica artefactos existentes sin aceptación completa; `BLOQUEADO` requiere una fuente, credencial o decisión humana; `PENDIENTE` aún no se ejecutó.

## Auditoría de los pasos 1–9

| Paso | Estado verificado | Evidencia actual | Pendiente o discrepancia |
|---:|---|---|---|
| 1–3 | PARCIAL | Repositorio Git, remoto `origin`, estructura `src/`, `tests/`, `scripts/`, `docs/` y `data/` presentes | No se encontró evidencia suficiente para certificar cada actividad original |
| 4–6 | PARCIAL | `pyproject.toml`, `.gitignore`, `.env.example` y paquete `src/ragsmell` presentes | Instalación y configuración deben verificarse en el entorno de trabajo |
| 7–8 | PARCIAL | Código AST, detectores, scripts y fixtures existen en commits previos | La cobertura actual del árbol de trabajo está reducida por eliminaciones locales |
| 9 | PARCIAL | Hay `.venv` y configuración editable | `pytest` global faltaba; la suite debe ejecutarse desde `.venv` y con `testpaths` restringido |

**No se repiten ni se declaran completos los pasos 1–9 solo por existir archivos.**

## Estado de pasos 10–46

| Paso | Estado | Evidencia / bloqueo |
|---:|---|---|
| 10 | EN_CURSO | Decisiones D1–D15 y arquitectura reconstruidas desde el commit previo; requieren confirmación formal si existe otra versión aprobada |
| 11 | EN_CURSO | Entry point y CLI existen; instalación/pruebas deben repetirse después de estabilizar el árbol |
| 12–16 | PENDIENTE_DE_VERIFICACIÓN | Existen scripts y datos previos, pero no se aceptan como nueva evidencia hasta validar sus archivos y SHAs |
| 17–20 | PARCIAL | Taxonomía y documentación base presentes; no se encontró fuente editable LaTeX/BibTeX ni Estado del Arte editable |
| 21–28 | PARCIAL | Código de modelo, AST, escáner, cuatro detectores y CLI presentes; faltan pruebas eliminadas localmente y auditoría completa |
| 29–30 | PENDIENTE | No se acepta humo/AP2/AP6 sin una corrida y fixtures verificables |
| 31–34 | PARCIAL | Métricas y scripts existen; resultados locales versionados fueron eliminados en el árbol de trabajo |
| 35–39 | BLOQUEADO | Las secciones requieren fuente editable y datos verificables; presupuesto y bibliografía tienen campos pendientes |
| 40–42 | PARCIAL | Scripts/documentos existen; precisión humana no puede afirmarse sin etiquetas confirmadas |
| 43–45 | PENDIENTE | Requiere resultados reales y consolidación documental |
| 46 | PENDIENTE | Suite completa, Ruff, `pip check`, compilación y entrega aún no verificadas en este estado |

## Cambios locales preexistentes protegidos

- El árbol de trabajo ya contenía modificaciones y eliminaciones antes de esta ejecución.
- Se creó una copia de los archivos locales vacíos que fueron reconstruidos desde el commit previo en `%TEMP%/opencode/ragsmell-preexisting-empty-20261123`.
- No se restauraron CSV eliminados ni se ejecutaron comandos destructivos.
- `data/clones/` se considera material local de terceros y permanece fuera del control de versiones.

## Evidencia ejecutada en esta sesión

- `git status --short --branch`, `git log --oneline -5`, `git remote -v`.
- Inventarios de `docs/`, `data/`, `scripts/`, `src/` y `tests/`.
- Python global: `3.14.6`; Python del entorno `.venv` disponible.
- `\.venv\Scripts\python.exe -m pytest -q tests`: primera ejecución **4 passed, 1 skipped**; después de reponer fixtures nuevos, suite actual **13 passed**.
- `\.venv\Scripts\ruff.exe check src tests scripts`: **All checks passed**.
- `python -m pytest -q` sin restricción: no válido antes del ajuste porque recolectó pruebas de `data/clones/`.

## Bloqueos reales

1. No se encontró fuente editable del anteproyecto ni `.bib`; solo existe `Anteproyecto_MIS.pdf` y PDFs en `Referencias/`.
2. No se puede afirmar validación humana ni precisión confirmada.
3. Las filas de datos eliminadas localmente no se regenerarán sin verificar primero scripts, criterios y acceso a GitHub.
4. No se solicitará ni se imprimirá ningún token; `GITHUB_TOKEN` queda como configuración local opcional.

La bitácora se actualizará después de cada paso ejecutado.

## Registro de esta continuación

### Paso 10 — COMPLETADO CON RESERVAS

Se verificaron las decisiones D1–D15 y la arquitectura existente en los
commits previos. Se conservaron sus contenidos y se añadió esta bitácora
actualizada. No apareció una versión alternativa aprobada ni una fuente
editable del anteproyecto. La reserva es la confirmación formal del
investigador, no una contradicción observada.

### Paso 11 — COMPLETADO

Se completó `GITHUB_TOKEN=` de `.env.example`, se restringió Pytest a `tests/`
mediante `pyproject.toml` para no recolectar pruebas de clones, y se verificó
la instalación editable, la CLI y la suite.

Pruebas: `pip install -e ".[dev]"` correcto; `pip check` sin dependencias
rotas; `pytest -q` **13 passed**; `ruff check src tests scripts` correcto;
`ragsmell version` imprime **0.1.0**; `ragsmell metrics tests/fixtures` genera
CSV con 9 módulos.

### Pasos 21–28 — PARCIAL / BASE VERIFICADA

Se conservaron los cuatro detectores núcleo existentes y se repusieron solo
fixtures ausentes para que el registro automatizado tuviera positivos y
negativos de AP1, AP3, AP4 y AP5. La suite pasó 13 pruebas y el escaneo de
fixtures produjo un hallazgo por detector. Esto no equivale a validación
humana ni a una corrida sobre la muestra GitHub.

### Pasos 12–16 y 29–46 — PENDIENTE/BLOQUEADO

Se añadió `scripts/02b_filtrar_seleccionar.py` para que la preselección pueda
registrar evidencia de manifiestos sin clasificar como elegible lo que no se
pueda verificar. Las corridas 03–06 ejecutadas con el CSV de selección vacío
produjeron salidas con encabezados y cero filas: `repos=0`, `metricas=0`,
`modulos=0`, `muestra=0`. No se interpreta ese cero como resultado de la
muestra. Permanecen bloqueados la fuente editable LaTeX/BibTeX, la selección
real de repositorios, la validación humana y la compilación documental.

### Pasos 13–16 — PARCIAL / BLOQUEADOS POR EVIDENCIA DE API

`scripts/01_recolectar_repos.py` se ejecutó el 2026-11-23 sin token:
**915 candidatos**, 15 consultas y fecha de corte calculada en tiempo de
ejecución; el resultado quedó en `data/repos_candidatos.csv` y
`data/metadata_muestra.json`. `scripts/02b_filtrar_seleccionar.py` aplicó
exclusión textual y tamaño: **40 preseleccionados**. Las consultas de
manifiestos y commits recibieron errores de la API pública y, conforme al plan,
los casos quedaron `PENDIENTE_DE_VERIFICACIÓN`; no se seleccionó ningún
repositorio ni se inventó N=20. `data/repos_seleccionados.csv` tiene solo
encabezados.

`scripts/02_clonar_repos.py` no clonó repositorios porque la selección está
vacía. Por ello, no se puede generar una muestra analítica ni ejecutar una
corrida de humo real.

### Pasos 31–42 — SALIDAS NULAS, NO RESULTADOS DE MUESTRA

Los scripts 03–06 se ejecutaron con la selección vacía y generaron CSV con
encabezados: `findings.csv`, `parse_errors.csv`, `scan_summary.csv`,
`tabla_repo_ap.csv`, `metricas.csv`, `metricas_errors.csv`, `estadisticas.csv`,
`spearman.csv`, `resumen_descriptivo.csv` y `validacion_manual.csv`.
Los conteos fueron `repos=0`, `hallazgos=0`, `metricas=0`, `modulos=0` y
`muestra=0`; esto es una corrida de control sin muestra, no evidencia para H1 o
H2. La precisión confirmada continúa como `no estimada / pendiente`.
