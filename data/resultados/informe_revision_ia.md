# Informe de revisión IA preliminar de hallazgos

## Alcance y metodología

Se revisaron los 60 registros originales de `validacion_manual.csv` con semilla 42. Para cada fila se verificó la existencia del checkout y archivo, se leyó el contexto alrededor de la línea indicada y se contrastó el caso con `docs/taxonomia.md`, `docs/DECISIONES.md` y la implementación vigente del detector. Las propuestas son asistidas por IA y no son etiquetas humanas.

Se conservaron los identificadores, rutas y líneas originales. Todas las filas requieren revisión del investigador; `UNCERTAIN` requiere atención prioritaria. Posteriormente, el investigador adoptó estas propuestas mediante adjudicación asistida por IA; véase la sección final de este informe.

## Resumen

- Hallazgos evaluados: **60**
- Propuestas TP: **21**
- Propuestas FP: **29**
- Propuestas UNCERTAIN: **10**
- Confianza HIGH: **44**; MEDIUM: **14**; LOW: **2**

**Corrección de consistencia:** la distribución anterior HIGH=37,
MEDIUM=20, LOW=3 no coincide con el archivo fuente. La distribución autoritativa
se calculó directamente desde `revision_ia_preliminar.csv` y es HIGH=44,
MEDIUM=14, LOW=2. No se modificaron clasificaciones ni campos humanos.

## Distribución por detector

| Detector | TP | FP | UNCERTAIN | Total |
|---|---:|---:|---:|---:|
| AP1 | 10 | 6 | 4 | 20 |
| AP3 | 1 | 15 | 1 | 17 |
| AP4 | 1 | 1 | 1 | 3 |
| AP5 | 9 | 7 | 4 | 20 |

## Interpretación cautelosa

- Las propuestas no estiman precisión confirmada.
- No se rellenó `veredicto_confirmado`, `nota_confirmada`, `revisor` ni `fecha_revision`.
- Los FP propuestos reflejan evidencia local contradictoria, como queries Cypher, fixtures, adapters, factories, defaults configurables o manejo explícito de fallas.
- Los TP propuestos no prueban por sí solos daño arquitectónico; indican correspondencia preliminar con la regla operacional.
- Las decisiones UNCERTAIN no deben convertirse en TP/FP sin revisión humana.
- Posible sesgo: la revisión depende del contexto disponible en snapshots locales y puede sobrevalorar evidencia textual visible; no sustituye conocimiento del sistema, intención del mantenedor ni historia del diseño.

## Archivos y limitaciones

- Los 60 archivos referenciados existían durante la revisión.
- La revisión no ejecutó código de terceros ni modificó clones.
- El contexto arquitectónico transversal, documentación externa, configuración de despliegue e intención del mantenedor no siempre estaban disponibles.
- La muestra original y su semilla no fueron regeneradas ni modificadas.

## Adjudicación posterior por el investigador

Por restricción de tiempo, el investigador adoptó las clasificaciones preliminares asistidas por IA como decisiones provisionales, sin inspección independiente a nivel de fuente. La adopción quedó registrada en `data/resultados/validacion_investigador.csv`:

- `researcher_verdict`: copia de `ai_proposal` para cada fila.
- `reviewer`: `Investigador (adopción de evaluación asistida por IA)`.
- `review_status`: `accepted_ai_assisted`.
- `review_date`: fecha efectiva de la adjudicación.
- `independent_human_verification`: `no` en las 60 filas.
- `researcher_note`: declara explícitamente que la decisión adopta una evaluación asistida por IA sin verificación independiente.

Distribución adoptada (condicional a la adjudicación asistida):

| Veredicto | Casos |
|---|---:|
| TP | 21 |
| FP | 29 |
| UNCERTAIN | 10 |

Los **10 casos UNCERTAIN permanecen sin resolver** y no se recodificaron como TP ni FP. No existe una estimación de precisión verificada de forma independiente. El cociente TP/(TP+FP) condicional es 21/50, pero **no debe presentarse como precisión confirmada** porque depende de la evaluación asistida por IA y excluye los 10 casos no resueltos.

### Cadena de procedencia

1. **Detección automática:** los 445 hallazgos de `findings.csv` y la muestra de 60 filas con semilla 42 en `validacion_manual.csv`.
2. **Clasificación preliminar asistida por IA:** `revision_ia_preliminar.csv`, sin modificar la muestra.
3. **Adopción del investigador:** `validacion_investigador.csv`, marcada como `accepted_ai_assisted`.
4. **Verificación humana independiente:** no realizada.

La distinción entre estos cuatro niveles debe conservarse en el artículo final. La limitación metodológica debe declararse explícitamente en la sección de amenazas a la validez y no debe describirse la adjudicación como validación manual independiente.
