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
