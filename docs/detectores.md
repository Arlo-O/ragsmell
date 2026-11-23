 # Detectores

| ID | Estado | Regla | Umbral |
|---|---|---|---|
| AP1 | Implementado núcleo | Literal o f-string largo en función con control y variable de prompt | 80 caracteres |
| AP2 | Ampliación pendiente | Framework web + cliente vectorial o credencial literal | Fixtures por crear |
| AP3 | Implementado núcleo | `model`/`model_name` literal de modelo reconocido | Regex declarativa |
| AP4 | Implementado núcleo | Recuperación y generación en la misma función | >60 líneas |
| AP5 | Implementado núcleo | Llamada crítica en `try` y handler amplio sin propagación | Handler silenciador |
| AP6 | Ampliación pendiente | Salida LLM a sumidero sensible sin validación | Fixtures por crear |

Las llamadas genéricas `query` y `search` no se consideran críticas sin receptor/contexto. Los ejemplos automatizados están en `tests/test_detectors.py`; la precisión confirmada es `pendiente` porque no hay revisión humana confirmada. `cbo_mod` se define en `metrics.py` como aproximación por módulo.
