# Protocolo de validación del investigador

Este protocolo prepara la revisión humana de los 60 hallazgos. Las propuestas
de IA son auxiliares y no se transfieren automáticamente a decisiones humanas.

## TP, FP y UNCERTAIN

- **TP:** el código inspeccionado satisface la definición operacional completa
  del detector, incluyendo contexto suficiente de función, llamadas y manejo.
- **FP:** el código no satisface la definición operacional; existe evidencia
  concreta de que es una query, fixture, adapter, factory, template, fallback
  legítimo, ejemplo excluible u otro caso fuera de la regla.
- **UNCERTAIN:** la evidencia es insuficiente, contradictoria o depende de
  intención arquitectónica/contexto que no puede establecerse con los archivos
  disponibles.

No use el hecho de que el detector se activó como prueba de TP.

## Procedimiento por hallazgo

1. Abra `validacion_investigador.csv` y use `original_id` para localizar la
   fila en `validacion_manual.csv`.
2. Compruebe el checkout fijado y abra `data/clones/<owner>__<repo>/<file>`.
3. Lea al menos la función completa, su clase cuando exista y las llamadas a
   las que se refiere el hallazgo. Use el comando sugerido en
   `validacion_asistida.md` como punto de partida, no como límite de lectura.
4. Consulte `docs/taxonomia.md` y aplique la regla del detector, no una
   definición genérica de code smell.
5. Registre evidencia a favor y en contra con ruta y líneas concretas.
6. Escriba una sola decisión en `researcher_verdict`: `TP`, `FP` o `UNCERTAIN`.
7. Explique la decisión en `researcher_note`, complete `reviewer` y use una
   fecha reproducible en `review_date`.
8. Cambie `review_status` a `reviewed` solo cuando haya leído y decidido la
   fila; manténgalo vacío o `pending` antes de revisarla.

## Criterios específicos

### AP1 — Hardcoded Prompt Infiltration

Confirme que la cadena/f-string es realmente un prompt LLM, que alcanza el
contexto de generación y que está incrustada en una función con lógica de
control. Diferencie prompts legítimos centralizados, templates, defaults de
backend y consultas Cypher/SQL. Evalúe si el código representa una decisión
arquitectónica problemática, no solo una cadena larga.

### AP3 — Hardcoded Provider Lock-in

Confirme si el literal impone un proveedor/modelo sin una abstracción o
configuración razonable. No marque automáticamente adapters, factories,
implementaciones específicas de un proveedor, defaults inyectables, fixtures,
tests, evaluadores o ejemplos. Revise si existe selección por configuración,
inyección de dependencias o soporte de múltiples proveedores.

### AP4 — Monolithic RAG Function

Verifique el cuerpo completo de la misma función. Debe superar 60 líneas y
contener recuperación y generación en el mismo flujo/ámbito. No basta con que
la función sea un bootstrap, dispatcher o fábrica larga, ni con que llamadas
de funciones anidadas aparezcan en su AST. Considere si la coordinación es una
responsabilidad legítima del componente.

### AP5 — Non-Deterministic Exception Suppression

Determine qué llamada crítica está protegida y qué ocurre después del handler.
Diferencie propagación posterior, reintentos, estados de fallo explícitos,
conversiones de error documentadas, fallos de telemetría no críticos y loops
interactivos de un fallback que oculta una falla LLM/vectorial y devuelve un
resultado constante o incompleto.

## Hallazgos relacionados

No elimine filas relacionadas. Revise conjuntamente, cuando corresponda:

- Las dos filas del mismo sitio `browser_use/agent/service.py`.
- Las dos ramas del mismo `browser_use/cli.py`.
- Las dos consultas `system_query` de automem.
- Los dos métodos del code interpreter de LlamaIndex.
- Los dos fallbacks de capacidades de LiteLLM.

Cada fila conserva su identificador y puede recibir un veredicto distinto si
la evidencia lo justifica.

## Progreso y trazabilidad

El progreso se calcula exclusivamente desde `researcher_verdict` y
`review_status` de `validacion_investigador.csv`. Las columnas `ai_proposal` y
`ai_confidence` son informativas y no cuentan como revisión. `UNCERTAIN` siempre
requiere decisión humana explícita; no debe recodificarse por conveniencia.
