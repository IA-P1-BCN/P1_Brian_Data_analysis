# AGENTS.md · EDA COVID Tracking Project

Punto de entrada **común** para cualquier agente de IA que trabaje en este
repositorio (OpenCode, Claude Code, Cursor, Aider…). Léelo entero antes de
tocar nada. El detalle vive en `openspec/`, en `.agents/` y en las skills.

## 1. Qué es este proyecto

Mini datathon de análisis exploratorio de datos (EDA) sobre el **COVID
Tracking Project**. El objetivo es demostrar, con un notebook reproducible y
un informe ejecutivo, que sabemos:

- cargar y perfilar un dataset real y sucio;
- limpiarlo con criterios justificados;
- responder preguntas de negocio con estadística y visualización;
- construir features (ratios por 100k, media móvil, log, segmentos);
- integrar una segunda fuente (población por estado);
- empaquetar el trabajo en `src/eda/` con tests y CI.

Nivel objetivo: **Avanzado**. El nivel Experto es opcional y solo se aborda
cuando Esencial, Medio y Avanzado están cerrados.

- Enunciado original: `README.md`
- Contexto y plan: `docs/contexto_proyecto_eda.md`
- Especificaciones: `openspec/`
- Tablero: GitHub Project del repositorio
- Milestones: `N1 · Esencial`, `N2 · Medio`, `N3 · Avanzado`

## 2. Fuentes de verdad (en este orden)

1. `AGENTS.md` (este archivo): reglas del proyecto.
2. `openspec/config.yaml` y `openspec/specs/`: qué debe hacer el sistema.
3. `openspec/changes/<change>/`: propuesta, diseño y tareas en curso.
4. Issues y milestones de GitHub: qué se está ejecutando y en qué nivel.
5. `docs/contexto_proyecto_eda.md` y `README.md`: contexto y enunciado.

Si una spec y un issue se contradicen, **manda la spec** y se avisa en el
issue. Si el código y la spec se contradicen, manda la spec: se arregla el
código o se actualiza la spec, nunca se ignora.

## 3. Mapa del repositorio

```text
.
├── AGENTS.md                  reglas para agentes
├── openspec/                  especificaciones (OpenSpec CLI)
│   ├── config.yaml            contexto y reglas de redacción
│   ├── specs/                 specs vigentes por capacidad
│   └── changes/               propuestas en curso (una por épica)
├── .agents/                   capa de trabajo con IA
│   ├── agents/                subagentes (fuente)
│   ├── commands/              comandos (fuente)
│   ├── skills/                skills (globales + propias)
│   ├── decisions/             ADRs de la infraestructura de IA
│   └── templates/             plantillas (bitácora)
├── .opencode/                 configuración de OpenCode
│   ├── opencode.jsonc         permisos
│   ├── agents/                GENERADO desde .agents/agents
│   └── commands/              GENERADO desde .agents/commands
├── data/
│   ├── raw/                   datos originales (no se versionan los CSV)
│   ├── processed/             datos limpios (no se versionan)
│   └── external/              segunda fuente (población)
├── notebooks/
│   ├── 01_profiling.ipynb     perfilado del dataset
│   └── 02_eda.ipynb           análisis narrativo
├── src/eda/                   lógica reutilizable (load, clean, features, viz)
├── reports/                   figuras e informe ejecutivo
├── tests/                     pytest
├── scripts/
│   ├── sync_agents.py         .agents → .opencode
│   ├── new_change.py          crea openspec/changes/<slug>
│   └── validate_agent_infra.py
├── docs/
│   ├── ai-log.md              bitácora de IA (entregable)
│   └── contexto_proyecto_eda.md
├── package.json               solo OpenSpec (Node)
├── pyproject.toml             ruff + pytest
└── requirements.txt           dependencias Python
```

## 4. Reglas no negociables

1. **Datos crudos inmutables.** Nunca se edita un fichero de `data/raw/`.
   La limpieza se hace en código y se escribe en `data/processed/`.
2. **La lógica vive en `src/eda/`.** Los notebooks solo narran, llaman a
   `src/eda/` y muestran resultados. No se duplica limpieza entre celdas.
3. **Notebooks top-down.** `01_profiling.ipynb` y `02_eda.ipynb` deben
   ejecutarse de arriba abajo, sin outputs versionados y sin estado oculto.
4. **Idioma.** Prosa, comentarios de negocio y documentación en **español**;
   nombres de variables, funciones, columnas y código en **inglés**.
5. **No inventar datos.** Toda cifra del informe debe salir de una celda o
   de un artefacto reproducible. Si falta un dato, se escribe
   `<<PENDIENTE>>`, no se estima a ojo.
6. **No secretos.** Nunca se commitean `.env`, tokens, credenciales ni
   contenido de `data/raw/` o `.venv/`.
7. **Una tarea, una rama, una PR.** No se mezclan cambios de niveles
   distintos en la misma PR.
8. **Trazabilidad.** Cada tarea hecha con IA se registra en
   `docs/ai-log.md` con modelo, prompts clave y decisiones.

## 5. Ciclo SDD con OpenSpec

Cada épica tiene una carpeta en `openspec/changes/<change>/` con:

```text
proposal.md        por qué y qué cambia
design.md          cómo se implementa
tasks.md           tareas atómicas (con su issue)
specs/<cap>/spec.md requisitos y escenarios (SHALL / WHEN / THEN)
```

Estados de una tarea:

```text
Borrador → Aprobada (persona) → En construcción → En revisión → Archivada
```

### Gates

| Para escribir… | Requisito |
|---|---|
| `proposal.md` | Existe el issue en el Project |
| `specs/<cap>/spec.md` | El issue tiene criterios de aceptación |
| `design.md` | `proposal.md` revisado por una persona |
| `tasks.md` | `design.md` existe |
| Código o notebook | `tasks.md` existe y la tarea está asignada |
| PR | `/sdd-review` pasado y `/verify` verde |
| `openspec archive` | Todos los issues del change cerrados |

### Comandos OpenSpec

```bash
npm run spec:list          # lista cambios y specs
npm run spec:validate      # valida todos los cambios
npm run spec:view          # vista interactiva
npx openspec archive <change>   # archiva un cambio cerrado
```

## 6. Subagentes y comandos

Subagentes (`.opencode/agents/`):

| Subagente | Para qué |
|---|---|
| `spec-writer` | Redactar `proposal.md` y `specs/<cap>/spec.md`. No aprueba ni implementa. |
| `data-engineer` | Implementar `load.py`, `clean.py`, `features.py`. Solo `src/eda/`. |
| `notebook-builder` | Construir y editar notebooks top-down. |
| `eda-reviewer` | Revisar (solo lectura) validez, conclusiones y reproducibilidad. |
| `test-designer` | Diseñar `tests/` con un caso por criterio de aceptación. |
| `ai-scribe` | Añadir entradas a `docs/ai-log.md`. |

Comandos (`.opencode/commands/`):

| Comando | Qué hace |
|---|---|
| `/sdd-spec <issue\|change>` | Redacta la spec. |
| `/sdd-plan <change>` | Escribe `design.md`. |
| `/sdd-tasks <change>` | Descompone en tareas. |
| `/sdd-build <change\|tarea>` | Implementa código o notebook. |
| `/sdd-review <change\|PR>` | Revisión y tests. |
| `/bitacora <tarea>` | Registra en la bitácora. |
| `/verify` | `ruff`, `pytest`, notebooks y `openspec validate`. |

**Regla:** un subagente no llama a otro subagente. Si hace falta otro paso,
lo indica y vuelve al agente principal.

## 7. Skills

Propias del proyecto (en `.agents/skills/`):

- `sdd-workflow` · ciclo OpenSpec y gates.
- `dominio-covid` · columnas, estados, población y métricas del dataset.
- `eda-convenciones` · estructura, nombres y reglas de notebooks.
- `revision-eda` · checklist de revisión de la rúbrica.
- `trazabilidad-ia` · formato de la bitácora.

Globales que se reutilizan: `pandas-pro`, `statistical-analysis`,
`data-visualization`, `data-analysis-jupyter`, `exploratory-data-analysis`,
`data-storytelling`, `test-driven-development`, `code-review`,
`git-workflow-and-versioning` y `developing-with-streamlit` (solo Experto).

## 8. Definition of Done (global)

Cada PR debe cumplir:

- [ ] El notebook afectado ejecuta de arriba abajo sin errores.
- [ ] `ruff check .` limpio.
- [ ] `pytest -q` verde.
- [ ] `npm run spec:validate` verde.
- [ ] PR enlazada con `Closes #N`.
- [ ] Evidencia enlazada (commit, figura, tabla o notebook).
- [ ] Sin datos crudos, `.venv/` ni outputs de notebook en git.
- [ ] Entrada en `docs/ai-log.md` si se usó IA.

## 9. Bitácora de IA

`docs/ai-log.md` es un entregable. Cada entrada sigue
`.agents/templates/ai-log-entry.md` y recoge:

- fecha, tarea e issue;
- herramienta y modelo;
- prompts clave (resumidos, sin secretos);
- errores o alucinaciones detectadas;
- decisiones aceptadas y rechazadas;
- verificación humana.

## 10. Git y PR

- `main`: entregas. Solo recibe PR desde `develop`.
- `develop`: integración.
- Ramas: `feat/N-slug`, `fix/N-slug`, `docs/N-slug`, `test/N-slug`.
- Commits: Conventional Commits (`feat:`, `fix:`, `docs:`, `test:`,
  `chore:`).
- PR: título en Conventional Commits, `Closes #N`, CI verde, squash merge.
- No se hace push directo a `main` ni a `develop`.

## 11. Comandos rápidos

```bash
# Entorno
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Calidad
ruff check .
ruff format .
pytest -q

# Notebooks
jupyter lab
jupyter nbconvert --to notebook --execute notebooks/01_profiling.ipynb

# Specs
npm run spec:validate
python scripts/sync_agents.py --check
python scripts/validate_agent_infra.py
```
