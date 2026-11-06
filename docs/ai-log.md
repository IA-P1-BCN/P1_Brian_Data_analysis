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
