 # Amenazas a la validez

## Construcción

Las reglas AST son heurísticas v1 y pueden producir falsos positivos o negativos. `cbo_mod` es una aproximación por módulo basada en imports, no el CBO original por clase. La precisión confirmada está pendiente de etiquetas humanas; las sugerencias del agente no se cuentan como confirmación y no se estima recall por falta de un conjunto exhaustivo de casos.

## Interna

Los módulos están anidados dentro de repositorios, por lo que no son completamente independientes. El tamaño (`sloc`) puede confundir asociaciones. También influyen APIs cambiantes, aliases, archivos que no parsean y la exclusión D2.

## Externa

La población operacional se limita a repositorios públicos Python de GitHub, con búsqueda por topics, actividad reciente y selección por criterios. No se afirma representatividad de GitHub ni de todas las aplicaciones GenAI/RAG.

## Conclusión estadística

Se predefine Mann–Whitney, Spearman, delta de Cliff, alfa 0,05, Holm, terciles y sensibilidad por repositorio. Los grupos insuficientes, datos faltantes y resultados no calculables se reportan como tales. Con la corrida actual no hay N analítica porque la clonación falló; no es válido concluir ausencia de asociación.

## Reproducibilidad

La extracción registra fecha, corte, queries y autenticación en `data/metadata_muestra.json`; las selecciones usan URLs y los clones deben registrar SHA. La ejecución actual conserva `data/clone_errors.csv`. Se requieren una nueva corrida exitosa y confirmación humana para completar el piloto.
