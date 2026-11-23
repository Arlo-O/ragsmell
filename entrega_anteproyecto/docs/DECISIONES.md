 # Decisiones metodológicas y de diseño

> Estado: reconstruido a partir de `PLAN_OPENCODE_COPILOT_DESDE_PASO_10.md`; pendiente de confirmación formal del investigador. No se han alterado decisiones observadas en resultados.

## D1–D15

- **D1:** unidad de análisis estadístico: módulo Python `.py`; los repositorios son unidades de selección y agrupación.
- **D2:** excluir tests, documentación, ejemplos, migraciones, scripts, entornos, dependencias instaladas, builds y archivos mayores de 1 MB.
- **D3:** núcleo AP1, AP3, AP4 y AP5; AP2 y AP6 son ampliaciones sujetas a evaluación técnica.
- **D4:** independientes: `con_ap` (0/1) y `n_ap` (hallazgos por módulo).
- **D5:** primarias: `cc_max`, `mi`, `cbo_mod`; secundarias descriptivas: `cc_media`, `sloc`.
- **D6:** `cbo_mod` es una aproximación: módulos distintos importados no estándar, incluyendo importaciones relativas documentadas; no es el CBO original de Chidamber–Kemerer.
- **D7:** control de tamaño por terciles de `sloc` y sensibilidad agregada por repositorio mediante medianas; persiste la dependencia entre módulos del mismo repositorio.
- **D8:** Mann–Whitney U para presencia, Spearman para conteo, delta de Cliff, alfa 0,05 y Holm para las tres métricas primarias.
- **D9:** H1 se apoya si cada antipatrón implementado aparece en al menos dos repositorios y al menos 50 % de repositorios tiene uno o más antipatrones.
- **D10:** H2 se apoya si al menos dos de tres métricas cumplen conjuntamente `p_holm < 0,05`, dirección esperada y `|delta| >= 0,147`; el piloto no confirma por sí solo la hipótesis.
- **D11:** paquete y repositorio: `ragsmell`.
- **D12:** repositorio privado hasta aprobación del asesor.
- **D13:** identificadores/código en inglés; documentación, comentarios extensos y commits en español.
- **D14:** conservar formato y fuente LaTeX existente si aparece en el workspace.
- **D15:** Python `>=3.11`.

## Trazabilidad

No se encontró un documento de decisiones previo con contenido ni una fuente alternativa en la auditoría inicial. Si el investigador proporciona una versión aprobada, debe compararse antes de sustituir esta reconstrucción.
