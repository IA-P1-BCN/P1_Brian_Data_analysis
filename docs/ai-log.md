# Bitácora de IA

Registro del uso de IA en el proyecto. Cada entrada sigue la plantilla
`.agents/templates/ai-log-entry.md` y la skill `trazabilidad-ia`.

## 2026-11-06 · Infraestructura de agentes, skills y OpenSpec

- **Issue / change:** infraestructura inicial (sin issue todavía)
- **Herramienta:** OpenCode
- **Modelo:** `opencode/deepseek-v4.1-flash-free`
- **Rol del agente:** agente principal (diseño de la infraestructura)

### Objetivo

Montar una capa de trabajo con IA para el EDA: reglas del proyecto, subagentes
con permisos, skills propias y OpenSpec como motor de especificaciones.

### Prompts clave

1. "Quiero poder hacer con OpenSpec y agentes y subagentes con sus skills,
   como el proyecto de n8n."
2. "¿Épica te refieres por niveles?"
3. "Las 26 issues, ¿estarán dentro de cada nivel de milestone que
   corresponde?"

### Qué produjo la IA

- `AGENTS.md` con reglas, mapa del repositorio, gates y DoD.
- `.agents/agents/` con 7 subagentes: `spec-writer`, `data-engineer`,
  `eda-analyst`, `viz-designer`, `report-writer`, `eda-reviewer` y
  `ai-scribe`.
- `.agents/commands/` con 7 comandos: `/sdd-spec`, `/sdd-plan`,
  `/sdd-tasks`, `/sdd-build`, `/sdd-review`, `/bitacora` y `/verify`.
- `.agents/skills/` con 6 skills propias: `sdd-workflow`,
  `covid-data-dictionary`, `eda-convenciones`, `notebook-hygiene`,
  `executive-report-es` y `trazabilidad-ia`.
- `scripts/sync_agents.py`, `scripts/new_change.py` y
  `scripts/validate_agent_infra.py`.
- `openspec/config.yaml` y los 7 changes por épica.

### Errores y alucinaciones

- La primera propuesta de la IA usaba 8 subagentes e incluía `git-steward` y
  `dashboard-dev`. Se descartaron: git lo hace el agente principal y Streamlit
  es un extra de nivel Experto. Faltaban `spec-writer` y `ai-scribe`.
- Se asumió que OpenCode permite `skills:` en el frontmatter del subagente.
  No es así: las skills se declaran en el cuerpo y se cargan con la
  herramienta `skill`. Se corrigió el diseño.
- Se aclaró que los subagentes no se llaman entre sí: el agente principal
  orquesta y el testigo se pasa por ficheros.

### Decisiones

- **Aceptadas:** OpenSpec CLI como motor de specs; 7 changes por épica; 7
  subagentes; 6 skills propias; niveles en etiquetas y milestones, no en
  changes.
- **Rechazadas:** 26 changes (uno por issue) por exceso de ceremonia; 3
  changes por nivel por mezclar capacidades; 8 subagentes por añadir ruido.

### Verificación humana

- [ ] Revisar el diff completo de la rama `feat/infra-ia`.
- [ ] Ejecutar `python scripts/sync_agents.py --check`.
- [ ] Ejecutar `python scripts/validate_agent_infra.py`.
- [ ] Ejecutar `npm run spec:validate`.
- [ ] Confirmar que los 7 changes corresponden a las 7 épicas.

## 2026-11-06 · Backlog de 26 issues y GitHub Project

- **Issue / change:** #2 · `add-entorno-reproducible` (y backlog completo)
- **Herramienta:** OpenCode
- **Modelo:** `opencode/deepseek-v4.1-flash-free`
- **Rol del agente:** agente principal (backlog + orquestación)

### Objetivo

Convertir los 7 changes de OpenSpec en un backlog ejecutable de 26 issues
(N1 8, N2 10, N3 8), cada uno con nivel, área, dependencias y criterios de
aceptación, y reflejarlo en un GitHub Project con campos y vistas.

### Prompts clave

1. "Sigue con el siguiente paso del plan: issues y Project."
2. "Un issue = un entregable = un nivel = una PR."
3. "Los niveles son etiquetas y milestones, no changes."

### Qué produjo la IA

- 26 issues (#2–#27) con cuerpo homogéneo: contexto, criterios, change,
  dependencias, evidencia y DoD.
- Etiquetas `task`, `nivel:*` y `area:*`, y milestone correcto en cada issue.
- Números de issue enlazados en los 7 `tasks.md`.
- Project #55 `EDA · P1 Exploratory Data Analysis` con campos `Level`,
  `Workstream`, `Day`, `Priority` y `Estimate`, y 3 vistas.
- Corrección del job `Notebooks`: `actions/setup-python` con `cache: pip`
  fallaba en el post-job cuando no había dependencias que cachear.

### Errores y alucinaciones

- El primer script de issues pasó el número de milestone (`1`) en vez del
  título (`N1 · Esencial`); `gh` lo rechazó con
  `could not add to milestone '1'`. Se corrigió antes de crear nada.
- Se intentó crear vistas del Project con `filter` en
  `createProjectV2View`; el campo no existe en esa mutación. Se crearon sin
  filtro y se aplicó con `updateProjectV2View`.
- No se pudo fijar la agrupación del tablero por `Level` por API: la
  configuración solo expone `visibleFieldIds`. Queda pendiente en la UI.

### Decisiones

- **Aceptadas:** 26 issues con ID `N?-??`; orden por dependencias y no por
  nivel; `Day` con 6 días + buffer; `P0` solo para la ruta crítica.
- **Rechazadas:** un issue por change; issues padre por épica (se
  representan con `Workstream` y `openspec/changes/`).

### Verificación humana

- [ ] Revisar los 26 issues y sus criterios de aceptación.
- [ ] Confirmar el orden de `Day` y la ruta crítica del Project.
- [ ] Ajustar en la UI la agrupación del tablero "Backlog por nivel".

## 2026-11-06 · Ingesta del dataset y diccionario de datos

- **Issue / change:** #3 · `add-ingesta-datos`
- **Herramienta:** OpenCode
- **Modelo:** `opencode/deepseek-v4.1-flash-free`
- **Rol del agente:** `data-engineer`

### Objetivo

Implementar una carga reproducible del COVID Tracking Project, con caché
local, validación de esquema y un diccionario de datos que permita
interpretar las 56 columnas.

### Prompts clave

1. "Implementa N1-02: load.py con descarga, caché y validación, tests sin red
   y docs/data_dictionary.md."
2. "Comprueba el dataset real y documenta nulos, negativos y limitaciones."

### Qué produjo la IA

- `src/eda/load.py` con `download_covid_data()`, `validate_schema()` y
  `load_covid_data()`.
- Descarga atómica: escribe un `.part` y solo lo renombra si termina bien.
- `tests/fixtures/covid_sample.csv` y 8 tests en `tests/test_load.py`.
- `docs/data_dictionary.md` con las 56 columnas, los porcentajes de nulos
  reales y las reglas de interpretación.

### Errores y alucinaciones

- La primera URL probada (`covidtracking.com/api/v1/states/daily.csv`)
  devuelve 404. Se cambió al CSV del repositorio archivado
  `COVID19Tracking/covid-tracking-data` (200, 5,5 MB).
- Se asumió que `dataQualityGrade` permitiría resolver duplicados por
  calidad; en esta copia está vacía al 100 %. Se documentó y se descartó ese
  criterio.
- `ruff format` intentó formatear el bloque de código del Markdown del
  diccionario; se aceptó el cambio porque no altera el contenido.

### Decisiones

- **Aceptadas:** usar `urllib` de la biblioteca estándar (sin dependencia
  nueva); validar tamaño y columnas antes de devolver el `DataFrame`; leer
  `state` y `fips` como texto.
- **Rechazadas:** depender de la API original (caída); añadir `requests` solo
  para una descarga.

### Verificación humana

- [ ] Revisar `src/eda/load.py` y los tests.
- [ ] Confirmar que el diccionario cubre las columnas usadas.
- [ ] Ejecutar `python -m pytest tests/test_load.py -q`.

## 2026-11-06 · Limpieza básica del dataset

- **Issue / change:** #5 · `add-limpieza-calidad`
- **Herramienta:** OpenCode
- **Modelo:** `opencode/deepseek-v4.1-flash-free`
- **Rol del agente:** `data-engineer`

### Objetivo

Convertir `date` a `datetime`, eliminar duplicados por `(state, date)` y
generar `data/processed/covid_clean.csv` sin tocar `data/raw/`.

### Prompts clave

1. "Implementa N1-04: fechas, duplicados, guardado y auditoría básica."
2. "Los tests no deben modificar el dataframe de entrada ni hacer red."

### Qué produjo la IA

- `src/eda/clean.py` con `parse_date_column()`, `drop_invalid_dates()`,
  `remove_duplicates()`, `clean_covid_data()`, `save_processed_data()`,
  `audit_cleaning()` y `build_clean_dataset()`.
- `tests/test_clean.py` con 15 tests, incluidos fecha imposible, duplicado
  con y sin `dateModified`, no mutación y pipeline completo.
- `data/processed/covid_clean.csv` regenerado: 20 780 filas, 0 fechas
  inválidas y 0 duplicados en la copia descargada.

### Errores y alucinaciones

- `build_clean_dataset()` validaba el esquema con el mínimo de 1000 filas y
  fallaba con el fixture de 12 filas. Se añadió `validate=False` para tests.
- `parse_date_column()` habría fallado con `date` ya convertida a
  `datetime`; se añadió el caso idempotente y su test.

### Decisiones

- **Aceptadas:** conservar el registro con `dateModified` más reciente;
  devolver `(df, auditoría)` en `build_clean_dataset()`; mantener el orden
  original de las filas.
- **Rechazadas:** eliminar duplicados por `dataQualityGrade` (columna vacía
  al 100 %); imputar fechas inválidas (no hay ninguna).

### Verificación humana

- [ ] Revisar que `data/raw/` no cambió.
- [ ] Confirmar que la auditoría coincide con el CSV procesado.
- [ ] Ejecutar `python -m pytest tests/test_clean.py -q`.

## 2026-11-06 · Mapa visual del proceso en docs/

- **Issue / change:** sin issue · documentación de arquitectura
- **Herramienta:** OpenCode
- **Modelo:** `opencode/deepseek-v4.1-flash-free`
- **Rol del agente:** agente principal (documentación)

### Objetivo

Documentar el plano general del proyecto con diagramas Mermaid: pipeline,
módulos, modelo de datos, ciclo SDD, flujo Git/PR, plan de 7 días y
orquestación de agentes.

### Prompts clave

1. "Quiero diagramas dentro de docs para visualizar el plano general del
   proceso."
2. "Un solo `docs/arquitectura.md`, Mermaid en Markdown y los siete
   diagramas."

### Qué produjo la IA

- `docs/arquitectura.md` con 7 diagramas Mermaid y tablas de "qué mirar".
- Enlaces desde `README.md` y `AGENTS.md` (mapa y fuentes derivadas).

### Errores y alucinaciones

- Ninguno detectado. Los 7 bloques Mermaid se validaron con `mermaid.parse`
  (mermaid 11 + jsdom) antes de cerrar la tarea.

### Decisiones

- **Aceptadas:** Mermaid embebido (sin imágenes ni CLI); un documento único;
  etiquetas en español y módulos en inglés.
- **Rechazadas:** exportar SVG/PNG → no hace falta para GitHub/VS Code;
  añadir diagramas al notebook → el notebook es narrativa de datos.

### Verificación humana

- [ ] Revisar `docs/arquitectura.md` y los enlaces.
- [ ] Previsualizar los diagramas en GitHub o VS Code.
- [ ] Ejecutar `ruff check .`, `pytest -q` y `npm run spec:validate`.

## 2026-11-06 · Separación del mapa visual en ficheros

- **Issue / change:** sin issue · documentación de arquitectura
- **Herramienta:** OpenCode
- **Modelo:** `opencode/deepseek-v4.1-flash-free`
- **Rol del agente:** agente principal (documentación)

### Objetivo

Separar `docs/arquitectura.md` en un índice y siete documentos de detalle,
uno por cada parte del proceso, para poder leer cada bloque sin cargar todo
el mapa.

### Prompts clave

1. "Me gustan los diagramas, pero separa cada parte por un fichero para
   tener el detalle de cada una."
2. "Mantén `docs/arquitectura.md` como índice y mueve y amplía el resto a
   `docs/arquitectura/`."

### Qué produjo la IA

- `docs/arquitectura.md` convertido en índice con diagrama de navegación y
  tabla de documentos.
- `docs/arquitectura/01_pipeline_datos.md` a
  `docs/arquitectura/07_orquestacion_agentes.md`, con tablas de etapas,
  contratos, gates, CI y subagentes.
- `AGENTS.md` actualizado con la nueva carpeta en el árbol de `docs/`.

### Errores y alucinaciones

- Ninguno detectado. Los 8 bloques Mermaid (índice + 7 detalles) se validaron
  con `mermaid.parse`.
- Se corrigió el estado de `features.py`, `viz.py` y los notebooks: están
  planificados, no implementados. Ahora se marcan como tal.

### Decisiones

- **Aceptadas:** índice en `docs/arquitectura.md`; detalle en
  `docs/arquitectura/`; `snake_case` con prefijo numérico.
- **Rechazadas:** mover el índice a `docs/arquitectura/README.md` → rompía
  los enlaces de README y AGENTS; duplicar cada diagrama en índice y detalle.

### Verificación humana

- [ ] Revisar los 7 documentos y sus enlaces relativos.
- [ ] Previsualizar los diagramas en GitHub o VS Code.
- [ ] Ejecutar `ruff check .`, `pytest -q` y `npm run spec:validate`.

## 2026-11-06 · Guía de lectura para empezar el EDA

- **Issue / change:** sin issue · documentación de arquitectura
- **Herramienta:** OpenCode
- **Modelo:** `opencode/deepseek-v4.1-flash-free`
- **Rol del agente:** agente principal (documentación)

### Objetivo

Añadir una guía de entrada para alguien que ya programa pero es nuevo en EDA:
glosario, leyenda de los diagramas, recorrido de un dato y recorrido de una
tarea.

### Prompts clave

1. "¿Con esos diagramas se puede entender el flujo del proyecto? Es un
   proyecto nuevo que es para aprender."
2. "Guía + glosario + dos trazas, para alguien que sabe programar pero es
   nuevo en EDA."

### Qué produjo la IA

- `docs/arquitectura/00_guia_lectura.md` con orden de lectura, glosario,
  leyenda, dos diagramas de secuencia y un primer ejercicio.
- `docs/arquitectura.md` actualizado con la guía en el diagrama de navegación
  y en la tabla de documentos.
- Línea "En una frase" y enlace a la guía en los 7 documentos de detalle.
- `AGENTS.md` actualizado con el nuevo documento en el árbol de `docs/`.

### Errores y alucinaciones

- Ninguno detectado. Los 10 bloques Mermaid (índice + guía + 7 detalles) se
  validaron con `mermaid.parse`.
- El ejercicio usa `shape` y la auditoría real, no cifras inventadas.

### Decisiones

- **Aceptadas:** una sola guía de entrada; glosario agrupado por datos,
  transformación y proceso; dos secuencias (dato y tarea); enlace desde cada
  detalle.
- **Rechazadas:** explicar sintaxis de Python → el público ya programa;
  añadir ejercicios a los 7 documentos → se deja para una iteración posterior.

### Verificación humana

- [ ] Leer `docs/arquitectura/00_guia_lectura.md` de arriba abajo.
- [ ] Comprobar que el glosario cubre las dudas reales.
- [ ] Ejecutar `ruff check .`, `pytest -q` y `npm run spec:validate`.

## 2026-11-09 · Notebook de perfilado del dataset

- **Issue / change:** #4 · `add-analisis-exploratorio`
- **Herramienta:** OpenCode
- **Modelo:** `opencode/deepseek-v4.1-flash-free`
- **Rol del agente:** `eda-analyst`

### Objetivo

Construir `01_profiling.ipynb` con perfilado crudo vs limpio, nulos,
duplicados, incrementos negativos y auditoría, sin duplicar lógica.

### Prompts clave

1. "Genera el notebook de perfilado con nbformat, ejecutable top-down."
2. "Incluye la comparativa antes/después usando audit_cleaning()."

### Qué produjo la IA

- `notebooks/01_profiling.ipynb` (22 celdas, 0 outputs versionados).
- Figura de las 15 columnas con más nulos.
- Verificación con `nbconvert --execute` en 125 KB de salida.
- `ipykernel` añadido a `requirements.txt` y registrado en la CI.

### Errores y alucinaciones

- El script de generación evaluaba `.format(audit=...)` en tiempo de
  generación, donde `audit` no existía. Se calculó antes con
  `build_clean_dataset()`.
- Faltaba `ipykernel` en el entorno y en CI; la ejecución del notebook
  fallaba con `NoSuchKernel`. Se añadió a `requirements.txt` y un paso
  `python -m ipykernel install --sys-prefix` en la CI.
- El notebook se guardó inicialmente con outputs; se limpió con `nbstripout`.

### Decisiones

- **Aceptadas:** perfilado sobre crudo y limpio en el mismo notebook;
  figura única de nulos; conclusión con cifras reales.
- **Rechazadas:** perfilar solo el crudo (dejaría la limpieza sin evidencia).

### Verificación humana

- [ ] Revisar las 22 celdas y la lectura de cada bloque.
- [ ] Confirmar que las cifras coinciden con `docs/data_dictionary.md`.
- [ ] Ejecutar `jupyter nbconvert --execute notebooks/01_profiling.ipynb`.

## 2026-11-09 · Notebook narrativo v0: preguntas e hipótesis

- **Issue / change:** #6 · `add-analisis-exploratorio`
- **Herramienta:** OpenCode
- **Modelo:** `opencode/deepseek-v4.1-flash-free`
- **Rol del agente:** `eda-analyst`

### Objetivo

Crear `02_eda.ipynb` con contexto, 3 preguntas de negocio, hipótesis,
métricas, periodo, criterio de respuesta y limitaciones, antes de cualquier
análisis.

### Prompts clave

1. "Crea el esqueleto de 02_eda.ipynb con las 3 preguntas propuestas."
2. "Las hipótesis deben escribirse antes de mirar los resultados."

### Qué produjo la IA

- `notebooks/02_eda.ipynb` con 10 secciones, carga desde `src.eda` y perfil
  rápido.
- 3 preguntas con hipótesis, métrica, periodo, criterio y limitación.
- Verificación con `nbconvert --execute` (13 946 bytes).

### Errores y alucinaciones

- Ninguno significativo. Se eliminó el import no usado en la celda de
  configuración.

### Decisiones

- **Aceptadas:** preguntas respondibles con los datos disponibles; se definen
  las métricas derivadas (positivity, death_rate) para N2.
- **Rechazadas:** añadir análisis en la misma PR (van en N1-06/N1-07).

### Verificación humana

- [ ] Revisar que las hipótesis son defendibles y no sesgadas.
- [ ] Confirmar que las 3 preguntas cubren el nivel Esencial.

## 2026-11-09 · Análisis univariado (3 variables)

- **Issue / change:** #7 · `add-analisis-exploratorio`
- **Herramienta:** OpenCode
- **Modelo:** `opencode/deepseek-v4.1-flash-free`
- **Rol del agente:** `eda-analyst`

### Objetivo

Añadir 3 análisis univariados con gráficos y lectura a `02_eda.ipynb`.

### Prompts clave

1. "Inserta univariado de casos, muertes y casos diarios con hist/boxplot."
2. "Cada gráfico con título, ejes, unidades y fuente, y lectura en español."

### Qué produjo la IA

- 3 subsecciones (6.1, 6.2, 6.3) con histograma, boxplot y top 10.
- 3 figuras en `reports/figures/`.
- Verificación con `nbconvert --execute` (292 KB).

### Errores y alucinaciones

- Ninguno. Se reutilizó el patrón de inserción por celda placeholder.

### Decisiones

- **Aceptadas:** counts absolutos con aviso de no comparabilidad; se deja
  la normalización para N3.
- **Rechazadas:** incluir positividad aquí (va en N2-05).

### Verificación humana

- [ ] Revisar las figuras y las lecturas.
- [ ] Confirmar que las cifras del top 10 son coherentes.

## 2026-11-09 · Análisis bivariado (3 relaciones)

- **Issue / change:** #8 · `add-analisis-exploratorio`
- **Herramienta:** OpenCode
- **Modelo:** `opencode/deepseek-v4.1-flash-free`
- **Rol del agente:** `eda-analyst`

### Objetivo

Añadir 3 análisis bivariados con gráfico y lectura a `02_eda.ipynb`.

### Prompts clave

1. "Inserta bivariado tests vs positivos, positividad vs mortalidad y boxplot
   por estado."
2. "Reporta correlación con su limitación y evita causalidad."

### Qué produjo la IA

- 3 subsecciones (7.1, 7.2, 7.3) con scatter + regplot y boxplot.
- 3 figuras en `reports/figures/`.
- Verificación con `nbconvert --execute` (431 KB).

### Errores y alucinaciones

- Ninguno. Se reutilizó `ultimo` (último día por estado) para los scatters.

### Decisiones

- **Aceptadas:** escala logarítmica para tests vs positivos; correlación de
  Pearson reportada con advertencia.
- **Rechazadas:** incluir el heatmap completo (va en N2-06).

### Verificación humana

- [ ] Revisar las figuras y las lecturas.
- [ ] Confirmar que no hay causalidad implícita.

## 2026-11-09 · Notebook narrativo v1 (conclusiones)

- **Issue / change:** #9 · `add-analisis-exploratorio`
- **Herramienta:** OpenCode
- **Modelo:** `opencode/deepseek-v4.1-flash-free`
- **Rol del agente:** `eda-analyst`

### Objetivo

Cerrar `02_eda.ipynb` con tendencias, limitaciones y conclusiones que
respondan a las 3 preguntas.

### Prompts clave

1. "Completa la sección 8 con serie diaria, media móvil 7d y por día de la
   semana."
2. "Escribe limitaciones y conclusiones con cifras trazables."

### Qué produjo la IA

- Secciones 8, 9 y 10 con 2 figuras nuevas (tendencia diaria y por día de
  la semana).
- Conclusiones que responden a las 3 preguntas con evidencia.
- Verificación con `nbconvert --execute` (684 KB).

### Errores y alucinaciones

- Se generaron ids de celda duplicados al insertar en bloque; se asignaron
  ids únicos antes de guardar.

### Decisiones

- **Aceptadas:** media móvil de 7 días para la tendencia; efecto fin de
  semana documentado como artefacto de reporting.
- **Rechazadas:** incluir el heatmap completo (va en N2-06).

### Verificación humana

- [ ] Revisar las conclusiones y las limitaciones.
- [ ] Confirmar que cada cifra remite a una celda anterior.

## 2026-11-09 · Limpieza avanzada: nulos, outliers y decisiones

- **Issue / change:** #10, #11, #12 · `add-limpieza-calidad`
- **Herramienta:** OpenCode
- **Modelo:** `opencode/deepseek-v4.1-flash-free`
- **Rol del agente:** `data-engineer` + `eda-analyst`

### Objetivo

Documentar las decisiones de limpieza avanzada: tabla antes/después,
exclusión de columnas con más del 80 % de nulos y outliers por IQR.

### Prompts clave

1. "Añade drop_high_null_columns, iqr_bounds y mark_outliers a clean.py con
   tests."
2. "Inserta la sección 6 de limpieza y calidad en 02_eda.ipynb."

### Qué produjo la IA

- `src/eda/clean.py`: 3 funciones nuevas + 3 tests (18 en total).
- `notebooks/02_eda.ipynb`: sección 6 con tabla de decisiones, lista de
  15 columnas excluidas y boxplot de outliers.
- Verificación con `nbconvert --execute` (725 KB).

### Errores y alucinaciones

- Se duplicó la celda de garantía de `raw` al insertar; se eliminó la
  segunda.
- Los ids de celda se duplicaron al renumerar secciones; se asignaron ids
  únicos.

### Decisiones

- **Aceptadas:** umbral estricto `> 0.80`; factor 1,5 para IQR; marcar
  outliers sin borrarlos.
- **Rechazadas:** excluir columnas con exactamente 80 % de nulos.

### Verificación humana

- [ ] Revisar la tabla de decisiones y los límites IQR.
- [ ] Confirmar que las 15 columnas excluidas coinciden con el diccionario.

## 2026-11-10 · Features base y ratios por 100k

- **Issue / change:** #14 · `add-features-temporales`
- **Herramienta:** OpenCode
- **Modelo:** `opencode/deepseek-v4.1-flash-free`
- **Rol del agente:** `data-engineer`

### Objetivo

Implementar `features.py` con positividad, tasa de mortalidad, media móvil
de 7 días, merge de población validado y ratios por 100k.

### Prompts clave

1. "Implementa features.py con add_base_features, merge_population y
   add_per_capita, más tests sin red."
2. "El merge debe fallar si falta un estado o cambia el número de filas."

### Qué produjo la IA

- `src/eda/features.py` con 8 funciones.
- `tests/test_features.py` con 12 tests.
- `add_all_features()` omite los ratios si no hay población disponible.

### Errores y alucinaciones

- Ninguno significativo. Los tests de merge usan un fixture temporal de
  población.

### Decisiones

- **Aceptadas:** media móvil con ventana completa (primeros 6 días NaN);
  `add_all_features` degrada con gracia sin población.
- **Rechazadas:** calcular ratios sin validar el merge.

### Verificación humana

- [ ] Revisar `features.py` y los tests.
- [ ] Confirmar que los ratios no son `inf`.

## 2026-11-10 · Agregados, correlación y tendencias avanzadas

- **Issue / change:** #13, #15, #16 · `add-analisis-exploratorio`
- **Herramienta:** OpenCode
- **Modelo:** `opencode/deepseek-v4.1-flash-free`
- **Rol del agente:** `eda-analyst`

### Objetivo

Añadir agregados por estado, matriz de correlación con heatmap y tendencias
por estado en escala lineal y logarítmica.

### Prompts clave

1. "Inserta agregados top 10, heatmap de correlación y tendencia top 5 en
   escala log."
2. "Añade una subsección de features derivadas (positividad, mortalidad)."

### Qué produjo la IA

- 4 subsecciones nuevas (7.4, 7.5, 8.4, 9.2) y 4 figuras.
- Verificación con `nbconvert --execute` (1 075 KB).

### Errores y alucinaciones

- `death_rate` salió como `object` por usar `pd.NA` en el denominador; se
  cambió a `float("nan")`.
- El heatmap falló porque `ultimo` no tenía `positivity`/`death_rate`; se
  recalculan en la celda.

### Decisiones

- **Aceptadas:** escala log para comparar velocidades de crecimiento;
  correlación reportada con advertencia.
- **Rechazadas:** incluir el heatmap completo de 56 columnas (solo las
  relevantes).

### Verificación humana

- [ ] Revisar las figuras y las lecturas.
- [ ] Confirmar que la escala log no oculta diferencias absolutas.

## 2026-11-10 · Informe ejecutivo y README

- **Issue / change:** #18, #19 · `add-informe-ejecutivo`
- **Herramienta:** OpenCode
- **Modelo:** `opencode/deepseek-v4.1-flash-free`
- **Rol del agente:** `report-writer`

### Objetivo

Redactar `reports/informe.md` (1–2 páginas, audiencia CEO) y actualizar el
`README.md` con instalación, ejecución, estructura y resultados.

### Prompts clave

1. "Redacta el informe ejecutivo con 4 hallazgos, recomendaciones y
   limitaciones, cifras trazables."
2. "Actualiza el README con instalación, ejecución, estructura y resultados."

### Qué produjo la IA

- `reports/informe.md` con resumen ejecutivo, 4 hallazgos, 3 recomendaciones
  y limitaciones.
- `README.md` con datos, instalación, ejecución, estructura y resultados.

### Errores y alucinaciones

- La hipótesis inicial (mayor positividad → mayor mortalidad) no se sostiene:
  la correlación es -0,05. Se reportó como hallazgo negativo en lugar de
  ocultarlo.

### Decisiones

- **Aceptadas:** cifras verificadas con un script de análisis; 1 figura por
  hallazgo en el notebook, no en el informe.
- **Rechazadas:** incluir gráficos en el informe (solo 1–2 páginas).

### Verificación humana

- [ ] Revisar el informe y las cifras.
- [ ] Confirmar que el README permite reproducir el proyecto.

## 2026-11-10 · Población, ratios por 100k, negativos y auditoría

- **Issue / change:** #20, #21, #22 · `add-features-temporales`,
  `add-limpieza-calidad`
- **Herramienta:** OpenCode
- **Modelo:** `opencode/deepseek-v4.1-flash-free`
- **Rol del agente:** `data-engineer` + `eda-analyst`

### Objetivo

Integrar la población por estado, calcular ratios por 100k, detectar y
tratar incrementos negativos y generar la auditoría completa.

### Prompts clave

1. "Crea data/external/population.csv con población por estado y territories."
2. "Añade merge_population con validación estricta y add_per_capita."
3. "Implementa clean_advanced con negativos a NaN y outliers marcados."

### Qué produjo la IA

- `data/external/population.csv` (56 estados/territorios) + README de fuente.
- `src/eda/clean.py`: `count_negative_increments`, `apply_negative_strategy`,
  `clean_advanced`.
- `notebooks/02_eda.ipynb`: sección 6.3 (negativos/auditoría) y 6.4 (ratios
  por 100k) con figura.
- Verificación con `nbconvert --execute` (1 114 KB).

### Errores y alucinaciones

- El CSV de población de Plotly incluía PR duplicado; se eliminó y se usó
  la cifra del Censo 2020.
- `population.csv` fue creado con 57 filas; se corrigió a 56.

### Decisiones

- **Aceptadas:** población de 2014 (estados) y 2020 (territorios), con
  advertencia en la fuente y en el informe.
- **Rechazadas:** buscar población exacta de 2020 por API (no disponible
  sin clave).

### Verificación humana

- [ ] Revisar `population.csv` y su README.
- [ ] Confirmar que los ratios por 100k son coherentes.

## 2026-11-10 · Segmentos y gráfico interactivo Plotly

- **Issue / change:** #23, #24, #25 · `add-features-temporales`,
  `add-informe-ejecutivo`
- **Herramienta:** OpenCode
- **Modelo:** `opencode/deepseek-v4.1-flash-free`
- **Rol del agente:** `eda-analyst` + `viz-designer`

### Objetivo

Añadir segmentos por región y por olas, escala logarítmica y un gráfico
interactivo con Plotly.

### Prompts clave

1. "Define regiones y olas con fechas explícitas y agrega por segmento."
2. "Añade un Plotly interactivo de tendencia por estado y exporta a HTML."

### Qué produjo la IA

- Secciones 9.3 y 9.4 con 2 figuras estáticas y 1 HTML interactivo.
- `reports/figures/plotly_tendencia.html`.
- Verificación con `nbconvert --execute` (1 301 KB).

### Errores y alucinaciones

- Ninguno significativo.

### Decisiones

- **Aceptadas:** olas con fechas explícitas; Plotly solo para una pregunta.
- **Rechazadas:** dashboard Streamlit (nivel Experto, opcional).

### Verificación humana

- [ ] Revisar los segmentos y el gráfico interactivo.
- [ ] Confirmar que las fechas de las olas son defendibles.

## 2026-11-10 · Pipeline reproducible y CI de notebooks

- **Issue / change:** #26 · `add-pipeline-release`
- **Herramienta:** OpenCode
- **Modelo:** `opencode/deepseek-v4.1-flash-free`
- **Rol del agente:** `data-engineer`

### Objetivo

Crear `scripts/run_pipeline.py` que ejecute carga, limpieza y guarde el
dataset procesado, y verificar la CI de notebooks.

### Prompts clave

1. "Crea run_pipeline.py con --force y manejo de errores."
2. "Verifica que el pipeline termina con código 0."

### Qué produjo la IA

- `scripts/run_pipeline.py` con `--force` y `--csv`.
- Ejecución verificada: 20 780 filas procesadas en ~16 s.

### Errores y alucinaciones

- La primera versión ejecutaba `build_clean_dataset` dos veces cuando se
  pasaba `--force`. Se simplificó.

### Decisiones

- **Aceptadas:** pipeline como script (no notebook); caché de descarga.
- **Rechazadas:** incluir features en el CSV procesado (separado).

### Verificación humana

- [ ] Revisar `run_pipeline.py`.
- [ ] Ejecutar `python scripts/run_pipeline.py`.

## 2026-11-10 · QA final y release v1.0.0

- **Issue / change:** #27 · `add-pipeline-release`
- **Herramienta:** OpenCode
- **Modelo:** `opencode/deepseek-v4.1-flash-free`
- **Rol del agente:** agente principal (QA y release)

### Objetivo

Verificación final del proyecto y preparación del release `v1.0.0`.

### Prompts clave

1. "Ejecuta /verify y prepara el release."
2. "Crea el PR develop → main y el tag v1.0.0."

### Qué produjo la IA

- `/verify` en verde: `ruff`, `pytest` (47 tests), notebooks, OpenSpec y
  agentes.
- Pipeline reproducible verificado.

### Errores y alucinaciones

- `ruff format` pendiente en `clean.py` y `features.py`; se corrigió antes
  del release.

### Decisiones

- **Aceptadas:** release desde `main` con tag `v1.0.0`.
- **Rechazadas:** incluir dashboard Streamlit (nivel Experto, opcional).

### Verificación humana

- [ ] Revisar el informe final.
- [ ] Confirmar el tag y la release en GitHub.
