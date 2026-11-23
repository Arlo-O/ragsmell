# Estado de ejecución — `ragsmell`

Fecha de auditoría: 2026-11-23. La fecha corresponde al entorno de ejecución; los resultados de datos solo se registrarán cuando se obtengan realmente.

## Auditoría inicial

- Repositorio Git existente, rama `main`, remoto `origin` configurado.
- Commit previo: `a64f5c2 Initial commit`.
- Python global observado: 3.14.6; `.venv` existente con dependencias instaladas.
- Estructura base presente, pero módulos, scripts, pruebas y documentos iniciales estaban vacíos salvo `__init__.py` y configuración.
- `ragsmell version` inicial: BLOQUEADO por `ImportError` (`cli.py` no definía `app`).
- No se encontraron fuente editable LaTeX/BibTeX ni Estado del Arte editable; solo `Anteproyecto_MIS.pdf` y dos PDFs en `Referencias/`.
- No hay token GitHub en logs ni se solicitó al usuario.

## Estados por paso

| Paso | Estado inicial/actual | Evidencia o pendiente |
|---:|---|---|
| 1–9 | PARCIAL / no demostrados | Estructura, `.venv` y `pyproject.toml` existen; funcionalidad no estaba verificada. |
| 10 | COMPLETADO | Decisiones reconstruidas, arquitectura y esta bitácora creadas; pendiente confirmación del investigador. |
| 11 | COMPLETADO | Instalación editable, CLI `version`, `scan`, `metrics`, 7 pruebas y Ruff verificados. |
| 12 | COMPLETADO | Sin token expuesto; API pública usada y autenticación registrada como falsa. |
| 13 | COMPLETADO | 685 candidatos, fecha/queries en `metadata_muestra.json`; no se inventan candidatos. |
| 14 | COMPLETADO | Preselección y exclusiones auditables en CSV; evidencia adicional quedó pendiente donde la API no bastó. |
| 15 | BLOQUEADO | Solo 1 candidato pasó la verificación de manifiesto; no se alcanzó N=20 y falta inspección completa/criterio de commits. |
| 16 | BLOQUEADO | El único candidato falló en `git clone`; consta en `data/clone_errors.csv`, N analítica=0. |
| 17–20 | PARCIAL | Taxonomía, conocimiento y texto metodológico preparados; fuente editable y evidencia bibliográfica específica ausentes. |
| 21–28 | COMPLETADO | Modelo, AST, escáner, cuatro detectores núcleo, CLI, fixtures y pruebas implementados. |
| 29–30 | BLOQUEADO/PARCIAL | No hay repositorio elegible clonado; AP2/AP6 permanecen como ampliaciones pendientes. |
| 31–34 | PARCIAL | Métricas/scripts/tablas implementados; corrida real tiene cero módulos por bloqueo de clonación. |
| 35–39 | PARCIAL/BLOQUEADO | Texto metodológico y presupuesto pendiente preparados; no hay fuente LaTeX/BibTeX editable. |
| 40–42 | PARCIAL | Hoja de validación y análisis reproducible preparados; precisión humana y figuras de datos reales pendientes. |
| 43–45 | PARCIAL | Documentación técnica creada; Anexo integrado y fuente académica pendientes. |
| 46 | PENDIENTE | Requiere resolver clonación/fuente editable y realizar controles finales sin bloquear por datos faltantes. |

## Registro

### Paso 10 — COMPLETADO

Archivos: `docs/DECISIONES.md`, `docs/ARQUITECTURA_ARCHIVOS.md`, `docs/taxonomia.md`, `docs/estado_ejecucion.md`.

Comandos de auditoría: `Get-Location`; `git status --short --branch`; `git log --oneline -5`; `git remote -v`; inventarios de `docs/`, `data/`, `scripts/`, `src/`, `tests/`; `python --version`; `python -m pytest -q`; prueba de `.venv`.

Resultado: la base de pasos 1–9 es parcial; no se repite su creación y no se inventan resultados.

### Paso 11 — COMPLETADO

Se ejecutaron instalación editable, `ragsmell version`, `scan`, `metrics`, pruebas y Ruff; la CLI funciona desde el entorno `.venv`.

### Pasos 12–16 — corrida de muestra

La API pública produjo 685 candidatos al 2026-11-23. La preselección auditó los criterios iniciales y dejó un candidato verificable por manifiesto; el clon superficial falló con código 128. No se convierte este fallo en una muestra ni se reporta una N analítica positiva.

### Pasos 21–34 — prototipo y salidas

`python -m pytest -q` aislado a `tests/`: 7 passed. `ruff check src tests scripts`: limpio después de los ajustes. `pip check`: sin dependencias rotas. Los CSV de resultados tienen encabezados; `findings.csv`, `metricas.csv` y `scan_summary.csv` no contienen filas analíticas porque no existe clon aceptado.

## Convenciones de actualización

Cada paso añadirá archivos modificados, comandos, resultados de pruebas, commit y bloqueos. `PENDIENTE_DE_VERIFICACIÓN`, `PENDIENTE_DEL_INVESTIGADOR` y `NO_DISPONIBLE` se conservarán literalmente cuando corresponda.
