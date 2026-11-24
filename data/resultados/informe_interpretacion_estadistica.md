# Informe de interpretación estadística

> Auditoría de solo lectura sobre las salidas de
> `scripts/05_analisis_estadistico.py`. No se modificaron CSV estadísticos,
> datos experimentales, código, taxonomía, detectores, decisiones D1–D10, la
> muestra ni la semilla 42. Fecha de auditoría: 2026-11-23.

## 1. Verificación de ejecución

### 1.1 Archivos inspeccionados

| Archivo | Filas de datos | Contenido verificado |
|---|---:|---|
| `data/resultados/estadisticas.csv` | 15 | 3 contrastes primarios Mann–Whitney, 9 contrastes por tercil de `sloc`, 3 sensibilidades por repositorio |
| `data/resultados/spearman.csv` | 3 | Correlaciones de `n_ap` con `cc_max`, `mi` y `cbo_mod` |
| `data/resultados/resumen_descriptivo.csv` | 15 | 5 métricas × 3 grupos (`todos`, `con_ap`, `sin_ap`) |
| `data/resultados/resumen_repositorio.csv` | 23 | Una fila por repositorio seleccionado |
| `data/resultados/resumen_ejecucion.csv` | 14 | Conteos de ejecución, faltantes y claves duplicadas |
| `data/resultados/decisiones_hipotesis.csv` | 2 | Evaluación literal de D9 y D10 |
| `data/resultados/tabla_repo_ap.csv` | 23 | Matriz repositorio × AP1–AP6 |

### 1.2 Consistencia con la salida de ejecución

La salida reportada fue:

```text
selftest=ok
modules=15768 repos=23 findings=445 stats=15 spearman=3 terciles=3 findings_without_metrics=0
```

Verificación independiente de solo lectura:

- `resumen_ejecucion.csv`: `modules=15768`, `repositories_selected=23`,
  `repositories_with_modules=23`, `repositories_without_modules=0`,
  `findings=445`, `findings_without_metric_module=0`,
  `duplicate_metric_keys_removed=0`, `sloc_tercile_groups=3`.
- Suma de `modules` en `resumen_repositorio.csv`: **15.768**.
- Suma de `findings` en `resumen_repositorio.csv`: **445**.
- Suma de `modules_with_ap` en `resumen_repositorio.csv`: **201**.
- Suma de AP1+AP3+AP4+AP5 en `tabla_repo_ap.csv`: **445**.
- `estadisticas.csv`: **15** filas = 3 primarias + 9 por tercil + 3 por repositorio.
- `spearman.csv`: **3** filas; `resumen_descriptivo.csv`: **15** filas.
- Faltantes: `0` en `cc_max`, `mi`, `cbo_mod`, `cc_media` y `sloc`.
- Los `findings` por repositorio de `resumen_repositorio.csv` coinciden
  exactamente con la suma AP1+AP3+AP4+AP5 de `tabla_repo_ap.csv` (diferencia
  absoluta total = 0).
- `repositories_without_modules=0` no contradice los dos repositorios sin
  hallazgos: esos repositorios sí tienen módulos métricos, pero cero
  hallazgos.

**Resultado de la auditoría: APROBADA.** Todos los archivos existen, contienen
datos y son internamente consistentes con la salida de ejecución. No se
detectaron valores faltantes ni claves métricas duplicadas.

## 2. Resultados descriptivos

### 2.1 Unidades y grupos

- Unidad de análisis (D1): módulo Python.
- Módulos analizados: **15.768**.
- Módulos con al menos un hallazgo (`con_ap=True`): **201 (1,27 %)**.
- Módulos sin hallazgos (`con_ap=False`): **15.567 (98,73 %)**.
- Repositorios: **23**; con al menos un hallazgo: **21 (91,3 %)**.
- Repositorios sin hallazgos: `ZhishaBai-web/help-you-find-job` (8 módulos) y
  `LibreChat-AI/rag-api` (22 módulos). Se conservan en las matrices.
- Hallazgos totales: **445**.

### 2.2 Distribución de hallazgos por detector

| Detector | Hallazgos | % de 445 | Repositorios con ≥1 |
|---|---:|---:|---:|
| AP1 | 273 | 61,35 % | 20 |
| AP2 | 0 | 0 % | 0 |
| AP3 | 17 | 3,82 % | 6 |
| AP4 | 3 | 0,67 % | 3 |
| AP5 | 152 | 34,16 % | 14 |
| AP6 | 0 | 0 % | 0 |

**AP2 y AP6 no están implementados.** Sus ceros son columnas de extensión no
evaluada y **no deben interpretarse como ausencia empírica del antipatrón**.

### 2.3 Métricas por grupo

Valores redondeados a dos decimales; los valores completos están en
`resumen_descriptivo.csv`.

| Métrica | Grupo | n | Media | Mediana | Q1 | Q3 | Mín | Máx |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| `cc_max` | todos | 15.768 | 8,28 | 5,00 | 1,00 | 11,00 | 0 | 533 |
| `cc_max` | con AP | 201 | 22,35 | 14,00 | 9,00 | 24,00 | 1 | 227 |
| `cc_max` | sin AP | 15.567 | 8,10 | 5,00 | 1,00 | 10,00 | 0 | 533 |
| `mi` | todos | 15.768 | 68,47 | 67,57 | 49,09 | 100,00 | 0 | 100 |
| `mi` | con AP | 201 | 38,09 | 39,74 | 25,71 | 51,79 | 0 | 100 |
| `mi` | sin AP | 15.567 | 68,87 | 68,04 | 49,46 | 100,00 | 0 | 100 |
| `cbo_mod` | todos | 15.768 | 2,20 | 2,00 | 1,00 | 3,00 | 0 | 43 |
| `cbo_mod` | con AP | 201 | 3,76 | 3,00 | 2,00 | 5,00 | 0 | 15 |
| `cbo_mod` | sin AP | 15.567 | 2,18 | 2,00 | 1,00 | 3,00 | 0 | 43 |
| `cc_media` | con AP | 201 | 5,60 | 5,00 | 3,74 | 6,95 | 1,00 | 22,03 |
| `cc_media` | sin AP | 15.567 | 2,92 | 2,38 | 1,00 | 4,00 | 0 | 120 |
| `sloc` | con AP | 201 | 614,05 | 399,00 | 209,00 | 660,00 | 21 | 10.241 |
| `sloc` | sin AP | 15.567 | 204,04 | 87,00 | 25,00 | 219,00 | 0 | 13.018 |

Lectura descriptiva:

- Los módulos con AP tienen mayor complejidad máxima (mediana 14 vs 5), menor
  índice de mantenibilidad (39,74 vs 68,04; menor es peor) y mayor acoplamiento
  aproximado (3 vs 2).
- Los módulos con AP son sustancialmente más grandes: mediana `sloc` 399 vs 87.
  Esta diferencia de tamaño es un confusor potencial y justifica el análisis por
  terciles.
- El grupo con AP es pequeño (1,27 % de los módulos), pero concentra valores
  altos de complejidad y bajos de mantenibilidad.

### 2.4 Concentración por repositorio

- `multimindlab/multimind-sdk`: **194** hallazgos (43,6 % del total), 42 módulos
  con AP de 392 (10,71 %).
- `bojieli/ai-agent-book`: **86** hallazgos (19,3 %), 49 módulos con AP de 1.037
  (4,73 %).
- Ambos repositorios concentran **280/445 = 62,9 %** de todos los hallazgos.
- La mayoría de los repositorios tiene menos del 3 % de módulos con AP.

Esta concentración implica dependencia entre observaciones del mismo
repositorio y riesgo de que los resultados estén dominados por pocos proyectos.

## 3. Resultados inferenciales

### 3.1 Método

- Contraste: Mann–Whitney U bilateral.
- Grupo A: `con_ap=True`; grupo B: `con_ap=False`.
- Nivel alfa: 0,05.
- Corrección Holm: familia separada de las tres métricas primarias
  (`cc_max`, `mi`, `cbo_mod`).
- Delta de Cliff: `δ = P(X_con > X_sin) − P(X_con < X_sin)`. Valores positivos
  indican valores mayores en el grupo con AP; los empates aportan cero.
- Direcciones esperadas:
  - `cc_max`: mayor en `con_ap` (δ positivo).
  - `mi`: menor en `con_ap` (δ negativo).
  - `cbo_mod`: mayor en `con_ap` (δ positivo).
- Umbrales de magnitud: `|δ| < 0,147` despreciable; `< 0,33` pequeño;
  `< 0,474` mediano; `≥ 0,474` grande.

### 3.2 Contrastes primarios

| Métrica | n con AP | n sin AP | Mediana con AP | Mediana sin AP | U | p | p Holm | δ de Cliff | Dirección | Magnitud | Estado |
|---|---:|---:|---:|---:|---:|---|---:|---:|---|---|---|
| `cc_max` | 201 | 15.567 | 14,0 | 5,0 | 2.517.200,5 | 2,423335302843669e-50 | 4,846670605687338e-50 | 0,6089658344111651 | mayor en con AP (acertada) | grande | calculado significativo |
| `mi` | 201 | 15.567 | 39,74063526807922 | 68,03901967094815 | 586.956,5 | 6,682091701650151e-54 | 2,0046275104950453e-53 | −0,6248241032903191 | menor en con AP (acertada) | grande | calculado significativo |
| `cbo_mod` | 201 | 15.567 | 3,0 | 2,0 | 2.194.635,0 | 7,405241100783632e-24 | 7,405241100783632e-24 | 0,40278564778727294 | mayor en con AP (acertada) | mediano | calculado significativo |

Interpretación:

- **`cc_max`:** los módulos con AP presentan complejidad ciclomática máxima
  sustancialmente mayor. La diferencia es estadísticamente significativa tras
  Holm y el tamaño de efecto es grande (δ ≈ 0,609). En términos prácticos, la
  distribución de complejidad de los módulos con AP está desplazada hacia
  valores altos.
- **`mi`:** los módulos con AP presentan menor mantenibilidad. La diferencia es
  significativa tras Holm y el efecto es grande en dirección negativa
  (δ ≈ −0,625). Como un `mi` mayor es mejor, el resultado indica peor
  mantenibilidad en el grupo con AP.
- **`cbo_mod`:** los módulos con AP presentan mayor acoplamiento aproximado. La
  diferencia es significativa tras Holm y el efecto es mediano
  (δ ≈ 0,403). `cbo_mod` sigue siendo una aproximación por módulo (D6), no el
  CBO original de Chidamber–Kemerer.

Los tres p-valores son extremadamente pequeños, pero con n = 15.768 la
significancia estadística por sí sola sería insuficiente. La relevancia
práctica se sustenta en los tamaños de efecto: dos grandes y uno mediano. Los
valores U no son directamente comparables entre métricas porque dependen de los
tamaños de grupo y de los empates; la dirección se interpreta con las medianas y
con delta de Cliff.

## 4. Análisis de correlación

### 4.1 Resultados de Spearman

Variable independiente: `n_ap` (número de hallazgos por módulo). n = 15.768 en
los tres contrastes.

| Métrica | ρ de Spearman | p | p Holm | n | Dirección | Estado |
|---|---:|---|---:|---:|---|---|
| `cc_max` | 0,11887044034791613 | 1,0133928795966231e-50 | 2,0267857591932462e-50 | 15.768 | positiva | calculado significativo |
| `mi` | −0,12319408749733604 | 2,259548268153525e-54 | 6,778644804460575e-54 | 15.768 | negativa | calculado significativo |
| `cbo_mod` | 0,08023738315897495 | 6,058804709036557e-24 | 6,058804709036557e-24 | 15.768 | positiva | calculado significativo |

Holm se aplicó como familia separada de tres contrastes, tal como exige D8. El
orden de ajuste fue: `mi` (p más pequeño, ×3), `cc_max` (×2) y `cbo_mod` (×1).

### 4.2 Interpretación

- Las tres correlaciones tienen la dirección esperada: más hallazgos se asocian
  monotónicamente con mayor complejidad, menor mantenibilidad y mayor
  acoplamiento.
- Las tres son estadísticamente significativas tras Holm.
- Sin embargo, la **magnitud es débil**: |ρ| entre 0,080 y 0,123. La asociación
  monotónica es real en el piloto, pero pequeña en términos prácticos.
- La debilidad es coherente con una distribución de `n_ap` fuertemente
  inflada en cero: 15.567 de 15.768 módulos tienen `n_ap = 0`. Los rangos y
  empates masivos reducen la correlación de rangos aunque exista una diferencia
  clara entre los grupos “con” y “sin” AP.
- No debe interpretarse ninguna correlación como causalidad.

## 5. Análisis por terciles de `sloc`

Se formaron tres estratos reales (`sloc_tercile_groups=3`, sin notas de
empates). Los límites son: hasta 43 líneas; más de 43 y hasta 164; más de 164.
Los contrastes por tercil son **exploratorios** y no recibieron corrección Holm.

| Estrato `sloc` | n con AP | n sin AP | Métrica | Mediana con AP | Mediana sin AP | U | p | δ | Magnitud | Estado |
|---|---:|---:|---|---:|---:|---:|---|---:|---|---|
| ≤ 43 | 1 | 5.313 | `cc_max` | 1,0 | 1,0 | — | — | 0,18351214003387917 | pequeño | n insuficiente |
| ≤ 43 | 1 | 5.313 | `mi` | 83,46538196793512 | 100,0 | — | — | −0,6860530773574252 | grande | n insuficiente |
| ≤ 43 | 1 | 5.313 | `cbo_mod` | 1,0 | 1,0 | — | — | 0,01637492941840768 | despreciable | n insuficiente |
| 43–164 | 40 | 5.175 | `cc_max` | 8,5 | 5,0 | 143.965,5 | 1,8654073344467457e-05 | 0,3909710144927536 | mediano | calculado significativo |
| 43–164 | 40 | 5.175 | `mi` | 62,18215701074236 | 68,11691667389586 | 74.937,5 | 0,00257271570567511 | −0,27596618357487923 | pequeño | calculado significativo |
| 43–164 | 40 | 5.175 | `cbo_mod` | 2,0 | 2,0 | 127.306,0 | 0,009666574863502446 | 0,23000966183574878 | pequeño | calculado significativo |
| > 164 | 160 | 5.079 | `cc_max` | 15,5 | 12,0 | 516.101,0 | 5,460826707716442e-09 | 0,2701835991336877 | pequeño | calculado significativo |
| > 164 | 160 | 5.079 | `mi` | 35,08835280241968 | 43,692872508973124 | 282.043,5 | 4,173181595281906e-11 | −0,3058586828115771 | pequeño | calculado significativo |
| > 164 | 160 | 5.079 | `cbo_mod` | 3,0 | 3,0 | 464.100,5 | 0,0018552446052294582 | 0,1422044201614491 | despreciable | calculado significativo |

Interpretación:

- **Estrato ≤ 43 líneas:** solo hay **1** módulo con AP frente a 5.313 sin AP.
  No se calculó U ni p; el estado correcto es `n_insuficiente`. Los deltas
  mostrados se basan en una sola observación y **no deben interpretarse**.
- **Estrato 43–164:** persisten diferencias significativas en las tres
  métricas. `cc_max` muestra efecto mediano (δ ≈ 0,391); `mi` y `cbo_mod`
  muestran efectos pequeños. Este estrato aporta la evidencia más clara de que
  la asociación no se debe únicamente al tamaño.
- **Estrato > 164:** persisten diferencias significativas, con efectos pequeños
  para `cc_max` y `mi`. Para `cbo_mod`, el p-valor es 0,001855, pero
  δ = 0,1422 < 0,147 y las medianas son iguales (3 vs 3): **estadísticamente
  significativo, prácticamente despreciable**.
- El control por tamaño es parcial: el estrato inferior casi no contiene
  módulos con AP, de modo que no puede evaluarse allí. Además, los terciles no
  corrigen la dependencia entre módulos del mismo repositorio.

## 6. Evaluación de hipótesis

### 6.1 D9 / H1 — presencia de antipatrones

Criterio literal (D9): cada antipatrón implementado aparece en al menos dos
repositorios y al menos el 50 % de los repositorios tiene uno o más
antipatrones.

| Condición | Resultado | Cumple |
|---|---|---|
| AP1 en ≥ 2 repositorios | 20 repositorios | Sí |
| AP3 en ≥ 2 repositorios | 6 repositorios | Sí |
| AP4 en ≥ 2 repositorios | 3 repositorios | Sí |
| AP5 en ≥ 2 repositorios | 14 repositorios | Sí |
| ≥ 50 % de repositorios con AP | 21/23 = 0,913 (91,3 %) | Sí |

`decisiones_hipotesis.csv` registra `estado=apoyada_en_el_piloto`.

**Veredicto:** H1 está **apoyada por la evidencia disponible del piloto** en
cuanto a patrones detectados automáticamente en 21 de 23 repositorios. No es una
confirmación definitiva: la presencia validada humanamente no está establecida,
porque la adjudicación fue asistida por IA. AP2 y AP6 no participan del
criterio.

### 6.2 D10 / H2 — asociación con mantenibilidad y calidad estructural

Criterio literal (D10): al menos dos de tres métricas primarias con
`p_holm < 0,05`, dirección esperada y `|δ| ≥ 0,147`.

| Métrica | p Holm | δ | Dirección esperada | \|δ\| ≥ 0,147 | Cumple |
|---|---:|---:|---|---|---|
| `cc_max` | 4,846670605687338e-50 | 0,6089658344111651 | Positiva | Sí | Sí |
| `mi` | 2,0046275104950453e-53 | −0,6248241032903191 | Negativa | Sí | Sí |
| `cbo_mod` | 7,405241100783632e-24 | 0,40278564778727294 | Positiva | Sí | Sí |

Resultado: **3/3 métricas cumplen**; `estado=apoyada_en_el_piloto`.

**Veredicto:** H2 está **apoyada como asociación en el piloto**, no como
relación causal ni como confirmación definitiva. La evidencia principal es la
comparación de presencia (`con_ap`): efectos grandes para `cc_max` y `mi`, y
mediano para `cbo_mod`. La evidencia de conteo (`n_ap`) es consistente en
dirección pero débil en magnitud.

### 6.3 Validación de detectores

- Adjudicación: **21 TP, 29 FP, 10 UNCERTAIN**.
- Casos verificados de forma independiente: **0**.
- Cociente condicional TP/(TP+FP) = **21/50 = 0,42**.
- No es una precisión confirmada y no debe reportarse como tal.
- Los 10 UNCERTAIN siguen sin resolver.

**Veredicto:** la precisión de los detectores es **evidencia insuficiente / no
verificada independientemente**. Esta limitación afecta la interpretación de H1
y H2 porque la validez de constructo de “antipatrón” depende de la validación.

### 6.4 Síntesis de la evaluación

| Cuestión evaluada | Veredicto |
|---|---|
| H1: presencia de antipatrones en la muestra | **Apoyada en el piloto** (D9; 21/23 repositorios; cada AP implementado en ≥2 repositorios), no confirmada humanamente |
| H2: asociación con mantenibilidad y calidad estructural | **Apoyada como asociación en el piloto** (D10; 3/3 métricas), no causal y con robustez parcial |
| Precisión de los detectores | **Insuficiente / no verificada independientemente** (21 TP, 29 FP, 10 UNCERTAIN; 0 verificados) |
| AP2 y AP6 | **No evaluables**: no implementados; los ceros no son ausencia |
| Sensibilidad por repositorio | **No concluyente**: `n_sin=2`, por debajo del mínimo de 5 |

No se observó evidencia que contradiga H1 o H2 en los contrastes primarios. La
falta de confirmación en la sensibilidad por repositorio no equivale a refutación,
porque ese contraste no alcanza el tamaño mínimo por grupo.

## 7. Limitaciones metodológicas

1. **Validación no independiente.** Las 60 clasificaciones fueron adoptadas de
   una evaluación asistida por IA, sin inspección humana independiente del
   código. No existe validación humana confirmada.
2. **Distribución de validación.** 21 TP, 29 FP y 10 UNCERTAIN; cero casos
   verificados independientemente. El cociente 21/50 es condicional y no una
   precisión validada.
3. **Riesgo de falsos positivos.** La adopción asistida sugiere un porcentaje
   elevado de FP propuestos. Si esos FP reflejan la realidad, parte de la señal
   estadística podría provenir de detecciones que no corresponden al
   antipatrón. No se ejecutó un análisis restringido a TP adoptados.
4. **Causalidad.** El diseño es observacional y transversal. Las diferencias y
   correlaciones son asociaciones; no permiten afirmar que los antipatrones
   causen el deterioro.
5. **Confusión por tamaño.** Los módulos con AP tienen mediana de 399 `sloc`
   frente a 87 en los sin AP. Los terciles reducen el problema, pero el estrato
   inferior contiene un solo módulo con AP y no permite un control completo.
6. **Dependencia por repositorio.** 15.768 módulos no son observaciones
   independientes: comparten repositorio, estilo y arquitectura. La sensibilidad
   por repositorio reduce la pseudo-replicación, pero no sustituye un modelo
   multinivel.
7. **Sensibilidad por repositorio no concluyente.** Solo 2 repositorios no
   tienen AP, por debajo del mínimo de 5 por grupo; los tres contrastes quedan
   `n_insuficiente`. Descriptivamente, `mi` y `cbo_mod` no reproducen la
   dirección esperada a nivel de repositorio (δ = +0,095 y −0,452,
   respectivamente). Esto no refuta H2 por falta de potencia, pero es una señal
   de robustez incompleta.
8. **Concentración de hallazgos.** Dos repositorios aportan el 62,9 % de los
   hallazgos. Los resultados pueden estar dominados por sus características
   particulares.
9. **Múltiples contrastes exploratorios.** Los nueve contrastes por tercil no
   tienen corrección Holm; son exploratorios. Aumenta el riesgo de falsos
   positivos en esa tabla.
10. **Sin intervalos de confianza ni potencia.** Las salidas reportan p-valores
    y tamaños de efecto, pero no intervalos de confianza ni análisis de
    potencia. No debe inferirse precisión de las estimaciones.
11. **AP2 y AP6 no implementados.** Sus conteos cero no son evidencia de
    ausencia. No están incluidos en D9 ni en el análisis.
12. **Hallazgos agrupados.** `con_ap` y `n_ap` agregan AP1, AP3, AP4 y AP5. No
    se estiman asociaciones específicas por antipatrón; AP4 tiene solo 3
    hallazgos y AP3 solo 17.
13. **Sin recall/exhaustividad.** No existe un conjunto exhaustivo de verdaderos
    positivos y negativos; no se mide recall.
14. **CBO aproximado.** `cbo_mod` es una aproximación por módulo (D6), no el CBO
    original por clase.

## 8. Implicaciones para la pregunta de investigación

La evidencia del piloto indica que, en la muestra de 23 aplicaciones open
source basadas en GenAI/RAG:

- Los patrones definidos por la taxonomía son detectados en la mayoría de los
  repositorios (21/23), con 445 hallazgos y 201 módulos afectados.
- Los módulos donde se detectan patrones presentan, en mediana, mayor
  complejidad máxima (14 vs 5), menor mantenibilidad (39,74 vs 68,04) y mayor
  acoplamiento aproximado (3 vs 2).
- Estas diferencias son estadísticamente significativas tras Holm y presentan
  tamaños de efecto grandes o medianos.
- El control por terciles de tamaño mantiene la dirección y la significancia en
  los dos estratos superiores, aunque con efectos menores.
- La asociación con el número de hallazgos es débil (|ρ| ≈ 0,08–0,12), lo que
  sugiere que la presencia/ausencia discrimina mejor que el conteo.

Por tanto, la respuesta provisional es que **existe una asociación consistente
entre los patrones detectados y peores indicadores estructurales en el piloto**,
pero no puede afirmarse causalidad, ni generalización, ni precisión confirmada
de los detectores. La conclusión debe formularse como evidencia piloto
condicionada a la validez de los detectores y a la adjudicación asistida por IA.

## 9. Resultados que pueden reportarse legítimamente en el artículo final

### 9.1 Reportables con las salvedades indicadas

- Composición: 23 repositorios, 15.768 módulos, 445 hallazgos, 201 módulos con
  AP (1,27 %), 21/23 repositorios con al menos un hallazgo.
- Distribución: AP1 = 273, AP3 = 17, AP4 = 3, AP5 = 152.
- Descriptivos por grupo y por repositorio, incluidas medianas y cuartiles.
- Mann–Whitney con U, p, p Holm, delta de Cliff, direcciones y magnitudes.
- Spearman con ρ, p, p Holm y n, señalando la magnitud débil.
- Terciles de `sloc` como análisis exploratorio, indicando que el estrato
  inferior es insuficiente.
- D9 y D10 como criterios predefinidos **cumplidos en el piloto**, no como
  confirmación definitiva.
- La sensibilidad por repositorio como análisis no concluyente por n
  insuficiente, reportando sus direcciones descriptivas.
- La adjudicación 21 TP / 29 FP / 10 UNCERTAIN como evaluación asistida por IA,
  no como validación humana.

### 9.2 No reportable como resultado confirmado

- Precisión confirmada de los detectores.
- 21/50 como precisión validada.
- Recall o exhaustividad.
- Causalidad entre antipatrones y métricas.
- Ausencia de AP2/AP6.
- Validación humana independiente.
- Generalización a toda la población de aplicaciones GenAI/RAG.
- Superioridad de un detector específico sin análisis estratificado por
  detector.

## 10. Trabajo restante antes de la entrega final

1. **Validación independiente:** revisar humanamente una submuestra,
   prioritariamente los 10 UNCERTAIN y una selección de TP/FP adoptados, o
   declarar formalmente la limitación y su efecto en las conclusiones.
2. **Análisis de sensibilidad a la validación:** repetir la asociación usando
   solo TP adoptados (y, si se resuelven, solo TP confirmados). No se ejecutó
   todavía.
3. **Robustez por repositorio:** excluir los dos repositorios que concentran el
   62,9 % de los hallazgos y repetir los contrastes; considerar un modelo
   multinivel o estratificado por repositorio.
4. **Análisis por detector:** estimar asociaciones para AP1 y AP5, que
   concentran 425/445 hallazgos, y reportar AP3/AP4 solo descriptivamente por
   sus bases pequeñas.
5. **Corrección de comparaciones múltiples:** definir y documentar una familia
   para los terciles si se van a interpretar inferencialmente.
6. **Intervalos de confianza:** añadir IC para medianas, delta de Cliff y
   Spearman, o declarar explícitamente su ausencia.
7. **Potencia y precisión:** no presentar los p-valores como evidencia de
   precisión; documentar el tamaño de la muestra y la dependencia por
   repositorio.
8. **Resolución de UNCERTAIN:** mantener los 10 casos como no resueltos o
   documentar una decisión posterior; no recodificarlos por conveniencia.
9. **Declaración metodológica:** incluir en amenazas a la validez la
   adjudicación asistida por IA, la ausencia de verificación independiente y el
   riesgo de falsos positivos.
10. **Coherencia documental:** verificar que el artículo final no use lenguaje
    causal, no llame “precisión” al cociente 21/50 y no interprete los ceros de
    AP2/AP6 como ausencia.

## Cierre de auditoría

- Archivos inspeccionados: los siete CSV listados en la sección 1.1.
- Consistencia interna: **aprobada**.
- Valores faltantes: **0**.
- Claves métricas duplicadas: **0**.
- Hallazgos sin módulo métrico: **0**.
- Modificaciones realizadas a datos o CSV: **ninguna**.
- Inferencia adicional ejecutada: **ninguna**.
