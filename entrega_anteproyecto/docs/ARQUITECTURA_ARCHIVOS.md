 # Arquitectura de archivos de `ragsmell`

## Flujo lógico

`repositorios seleccionados → archivos Python elegibles → AST → detectores → findings.csv` y, en paralelo, `AST → Radon/importaciones → metricas.csv → análisis estadístico y figuras`.

## Componentes

| Ruta | Responsabilidad | Salida principal |
|---|---|---|
| `src/ragsmell/cli.py` | Interfaz Typer para versión, escaneo y métricas | CSV solicitado por el usuario |
| `src/ragsmell/models.py` | Modelos inmutables de hallazgos y métricas | Filas serializables |
| `src/ragsmell/astutils.py` | Resolución segura de llamadas e imports | Utilidades compartidas |
| `src/ragsmell/knowledge.py` | Vocabulario declarativo del dominio | Conjuntos y patrones de reconocimiento |
| `src/ragsmell/scanner.py` | Exclusión D2, parseo y continuidad ante errores | Hallazgos, errores y resumen |
| `src/ragsmell/detectors/` | Detectores AP1/AP3/AP4/AP5 y extensiones evaluadas | `Finding` |
| `src/ragsmell/metrics.py` | SLOC, complejidad, MI y `cbo_mod` | Métricas por módulo |
| `scripts/01–06` | Recolección, clonación, corridas, estadística y validación | CSV reproducibles |
| `data/` | Candidatos, clones ignorados y resultados | Datos del piloto |
| `docs/` | Decisiones, taxonomía, arquitectura, amenazas y bitácora | Evidencia metodológica |
| `tests/` | Unitarias, fixtures y pruebas de integración | Verificación automatizada |

## Límites

El escáner no ejecuta código de terceros ni analiza `data/clones` como raíz implícita. Los scripts de datos consumen rutas y SHAs fijados en CSV. `data/clones/`, `.venv/`, `.env` y caches son artefactos locales ignorados por Git.

## Archivos generados previstos

`data/repos_candidatos.csv`, `data/repos_preseleccion.csv`, `data/repos_seleccionados.csv`, `data/clone_errors.csv`, `data/resultados/*.csv` y `data/resultados/figuras/`. Su existencia y contenido deben reflejar corridas reales; no se rellenan con datos ficticios.
