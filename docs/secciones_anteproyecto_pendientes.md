# Texto metodológico preparado para integrar en el anteproyecto

Este archivo no sustituye la fuente editable del anteproyecto. Se preparan las secciones para integración cuando aparezca el `.tex`/`.bib`; no se modifica el PDF existente.

## 8.1 Tipo de estudio

El trabajo se plantea como un estudio descriptivo con componente correlacional y una fase exploratoria para formular y refinar una taxonomía operacional de antipatrones en aplicaciones GenAI/RAG. Es exploratorio por el carácter emergente del dominio; es descriptivo porque cuantifica hallazgos en una muestra real; y es correlacional porque estudia la asociación entre `con_ap`/`n_ap` y `cc_max`, `mi` y `cbo_mod`. No es explicativo, causal ni experimental. El tamaño definitivo N queda `PENDIENTE_DE_VERIFICACIÓN` hasta completar clones válidos.

## 8.2 Método de investigación

Se emplean observación indirecta del código y metadatos, razonamiento deductivo desde architectural smells y deuda técnica, refinamiento inductivo limitado a los casos observados, análisis AST y síntesis de resultados. La recolección usa MSR; Radon calcula métricas; las comparaciones son Mann–Whitney U y Spearman con delta de Cliff y corrección de Holm. La revisión de literatura se denomina estructurada mientras no exista un protocolo reproducible completo.

| Objetivo | Método | Técnica |
|---|---|---|
| OE1 Taxonomía | Deductivo + documental | Revisión estructurada |
| OE2 Analizador | Análisis + síntesis | AST, reglas, fixtures y pruebas |
| OE3 Frecuencia/asociación | Observación + inductivo + estadístico | MSR, métricas y pruebas no paramétricas |

## 8.3 Fuentes y técnicas

Las fuentes primarias serán repositorios públicos fijados por `commit_sha`; su N, fecha final y módulos elegibles quedan pendientes por la falla de clonación actual. Las fuentes secundarias disponibles son los PDFs en `Referencias/`; no se incorporan metadatos no verificados. Los instrumentos son `ragsmell`, Radon, los CSV y la hoja de validación manual.

## 8.4 Tratamiento de la información

Los CSV se validan y unen por `repo` + `file`. Los módulos sin hallazgos reciben `n_ap=0` y `con_ap=False`; no se eliminan. Se reportan frecuencias, medianas, rango intercuartílico, Mann–Whitney para presencia, delta de Cliff, Spearman para conteo, Holm por familia, terciles de `sloc` y sensibilidad con medianas por repo. H1/H2 se juzgan literalmente según D9/D10; el piloto no demuestra causalidad.

| Variable | Tipo | Instrumento |
|---|---|---|
| `con_ap`, `n_ap` | Independientes | `ragsmell scan` |
| `cc_max`, `mi`, `cbo_mod` | Dependientes primarias | Radon/`ragsmell metrics` |
| `cc_media`, `sloc` | Descriptiva/control | Radon |

## 8.5 Esquema preliminar

La secuencia prevista es introducción, marco de referencia, taxonomía, analizador, metodología empírica, resultados, discusión/amenazas y conclusiones/trabajo futuro, vinculada respectivamente con OE1–OE3.

## 9. Cronograma

Se conserva un cronograma de diez semanas como planificación prevista: semanas 1–2 literatura/taxonomía; 3 muestra; 4–5 analizador; 6 validación; 7 métricas; 8 estadística; 9 verificación de objetivos/hipótesis y redacción; 10 presentación. El avance real queda registrado en `docs/estado_ejecucion.md`.

## 10. Presupuesto

Las tablas de horas, tarifas, sesiones, equipo, conectividad, energía, impresión y nube quedan `POR DEFINIR POR EL INVESTIGADOR`. Las fórmulas previstas son `cantidad × valor_unitario = subtotal` y `total = suma(subtotales)`; no se asigna COP 0 sin evidencia.

## 11. Bibliografía preliminar

La consolidación queda pendiente: no se encontró `.bib` ni fuente editable del Estado del Arte. Las referencias deben verificarse contra sus fuentes originales antes de integrarse.

## Anexo A

El prototipo y el flujo están descritos en `docs/ARQUITECTURA_ARCHIVOS.md`. Las tablas de muestra y resultados se completarán únicamente desde `data/resultados/` cuando haya clones y SHAs válidos; actualmente la corrida nula no permite presentar una conclusión sobre H1/H2.
