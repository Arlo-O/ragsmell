 # Taxonomía operacional v1

La taxonomía es una propuesta operacional para este piloto. La relación con literatura se conserva como evidencia o pendiente; un defecto funcional de integración no se presenta automáticamente como antipatrón arquitectónico.

| ID | Nombre | Definición | Atributo afectado | Regla AST v1 | Evidencia de literatura | Falso positivo probable | Exclusiones | Estado |
|---|---|---|---|---|---|---|---|---|
| AP1 | Hardcoded Prompt Infiltration | Prompt extenso incrustado en función que concentra lógica de control. | Mantenibilidad, evolvabilidad | Cadena/f-string >=80 caracteres en función con control, vinculada a pista de prompt o llamada LLM. | PENDIENTE_DE_VERIFICACIÓN | Mensajes largos o documentación | Constante de módulo sin contexto de prompt | Núcleo |
| AP2 | Vector Store Leakage | Acceso vectorial desde presentación o credencial literal. | Seguridad, separación de capas | Framework web + cliente vectorial, o credencial literal en constructor. | PENDIENTE_DE_VERIFICACIÓN | Código de configuración legítimo | Variables de entorno; cliente sin capa web | Ampliación |
| AP3 | Hardcoded Provider Lock-in | Proveedor/modelo rígido sin abstracción configurable. | Portabilidad, mantenibilidad | `model`/`model_name` literal reconocible en constructor o SDK documentado. | PENDIENTE_DE_VERIFICACIÓN | Fixture, ejemplo o adaptador explícito | Valores desde configuración/entorno; adaptadores | Núcleo |
| AP4 | Monolithic RAG Function | Una función concentra recuperación y generación. | Mantenibilidad, testabilidad | Función >60 líneas con llamada de recuperación y LLM. | PENDIENTE_DE_VERIFICACIÓN | Función coordinadora deliberada | Funciones <=60 líneas o con una sola etapa | Núcleo |
| AP5 | Non-Deterministic Exception Suppression | Error crítico silenciado o convertido en fallback constante. | Confiabilidad | `try` con llamada crítica y handler amplio sin `raise`, solo `pass`, logging o fallback constante. | PENDIENTE_DE_VERIFICACIÓN | Manejo real de reintento/validación | Excepciones ajenas a LLM/vectorial; propagación | Núcleo |
| AP6 | Unvalidated Generation Output | Salida generada llega a sumidero sensible sin validación reconocible. | Confiabilidad, seguridad | Salida LLM en `json.loads`, `eval`, `exec` o `.execute()` sin guardas. | PENDIENTE_DE_VERIFICACIÓN | Validación fuera del fragmento | Validación estructural reconocida | Ampliación |

## Correspondencia bibliográfica

No se afirma una equivalencia directa con nombres de patrones de Shao et al. porque la fuente disponible en el workspace no permite verificar esa correspondencia de forma suficiente. La revisión de la fuente original queda pendiente.

## Historial

- v1: reconstrucción inicial de las seis definiciones y reglas a partir del plan; pendiente de revisión del investigador.
