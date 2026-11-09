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
