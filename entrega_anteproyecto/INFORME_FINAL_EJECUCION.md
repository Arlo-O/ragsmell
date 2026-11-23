# Informe de ejecución (cierre parcial verificable)

## Alcance

Este paquete contiene la implementación verificable realizada desde el paso 10. No se declara cierre total de los pasos 10–46 porque la muestra analítica quedó bloqueada por clonación y no existe fuente editable LaTeX/BibTeX en el workspace.

## Estados

- **Completados:** 10–14, 21–28.
- **Parciales:** 17–20, 31–34, 35–45.
- **Bloqueados:** 15–16, 29–30, 39, 43–44 y 46 por falta de clones válidos, confirmación humana o fuentes editables.
- **Pendientes del investigador:** confirmar `DECISIONES.md`, aportar fuente editable y Estado del Arte, completar presupuesto, revisar manualmente hallazgos y resolver/autorizar una nueva corrida de muestra.

## Evidencia

- Candidatos recolectados: 685, con fecha, corte y queries en `data/metadata_muestra.json`.
- Candidatos con preselección y exclusiones auditables: `data/repos_preseleccion.csv`, `data/repos_excluidos.csv` y `data/decision_muestra.csv`.
- Candidato verificable por manifiesto: 1; clon aceptado: 0; fallo: `data/clone_errors.csv`.
- Resultados analíticos: CSV con encabezados y cero filas de módulos por N analítica cero. No se reportan frecuencias, precisión ni p-valores como resultados del estudio.
- Pruebas: 14 passed; Ruff limpio; `pip check` limpio; CLI `version` imprime `0.1.0`.
- Commit: `44bc55d feat: prototipo AST y corrida reproducible`.

## Artefactos no incluidos

No se copiaron clones, `.venv`, `.env`, secretos ni el PDF existente como si fuera un documento final corregido. El PDF del usuario permanece fuera del commit y la integración académica requiere su fuente editable.
