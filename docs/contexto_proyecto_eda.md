# Contexto del proyecto EDA — Mini Datathon

> Documento de trabajo generado a partir de la conversación de planificación.
> Fecha: 2026-11-05
> Repositorio base: <https://github.com/Factoria-F5-madrid/ai_project_EDA>
> Directorio local: `/home/brian/Documentos/F5 IA/M2_Data_Analytics_Machine_Learning/Proyectos/P1_Exploratory_data_analysis`

---

## 1. Enunciado y entregables

El repo base es **greenfield**: solo contiene `README.md` y `assets/minidatathon.PNG`. El encargo es un **EDA tipo mini datathon**:

> Eres el equipo de datos de una consultora. El CEO de un cliente te entrega un dataset sin explorar y quiere **datos limpios, con sentido y la historia detrás**, en un informe que pueda leer sin saber código.

### Entregables obligatorios

| # | Entregable | Formato |
|---|---|---|
| 1 | Notebook ordenado y explicado paso a paso (markdown entre celdas) | `.ipynb` |
| 2 | Informe ejecutivo para público no técnico | 1–2 páginas (nivel Medio) |
| 3 | README con origen de datos, instalación y ejecución | `.md` |
| 4 | Dependencias reproducibles | `requirements.txt` |

### Stack exigido

- Python 3 + Jupyter Notebook (VS Code o similar)
- `requests` / `pandas` para carga
- `pandas` / `numpy` para limpieza
- `matplotlib`, `seaborn` y/o `plotly` para visualización
- Git + GitHub con ramas ordenadas y commits claros

**Plazo:** una semana.

---

## 2. Requisitos del dataset

- ≥ 1.000 filas y ≥ 8 columnas
- Mezcla de variables numéricas, categóricas y fechas
- Valores faltantes o datos sucios reales
- Que interese de verdad (se nota en el informe)

---

## 3. Dataset propuesto: COVID Tracking Project

**Fuente:** <https://covidtracking.com/data/download>

| Característica | Valor |
|---|---|
| Filas | ~20.780 |
| Columnas | ~56 |
| Cobertura | EE. UU., por estado y día |
| Tipos | fechas (`20200313` como entero), numéricas acumuladas, categóricas (estado) |
| Suciedad real | columnas >80 % nulas, incrementos negativos, acumulados inconsistentes |

**Por qué encaja:** cumple de sobra los requisitos y permite atacar todos los niveles (normalización por 100k, merge con población, media móvil, escala log, segmentación por estado/ola, plotly).

---

## 4. Niveles de entrega

| Nivel | Qué añade | Decisión |
|---|---|---|
| 🟢 Esencial | Carga, `shape/info/head/describe`, nulos/duplicados, tipos, 3 univariados, 3 bivariados, 5 gráficos, 3 preguntas | Mínimo obligatorio |
| 🟡 Medio | Justificar limpieza, outliers (IQR/boxplot), `groupby/agg/pivot_table`, 3 features nuevas, correlación + heatmap, tendencias, informe 1–2 págs | Objetivo realista |
| 🟠 Avanzado | Normalizar (ratios por 100k), segunda fuente con `merge`, calidad dudosa, transformación justificada (media móvil/log), segmentos, plotly, limpieza en `.py` | **Nivel objetivo** |
| 🔴 Experto | Dashboard Streamlit/Dash, pipeline de un comando, tests `pytest`, informe de calidad, presentación 5 min, publicación online | Opcional si sobra tiempo |

### Cómo se cubre Avanzado con COVID

- **Normalizar** → casos/muertes por 100k habitantes (población por estado).
- **Merge** → población o región censal.
- **Calidad dudosa** → incrementos negativos, columnas casi vacías, acumulados inconsistentes.
- **Transformación** → media móvil de 7 días + escala log.
- **Segmentos** → por estado/región y por olas.
- **Plotly** → evolución temporal interactiva.

---

## 5. Arquitectura propuesta del repositorio

```text
P1_Exploratory_data_analysis/
├── README.md
├── requirements.txt
├── pyproject.toml
├── .gitignore
├── .gitattributes
├── .pre-commit-config.yaml
├── .env.example
├── data/
│   ├── raw/                     # CSV original (gitignored si pesa mucho)
│   └── processed/               # salida limpia (gitignored)
├── notebooks/
│   ├── 01_profiling.ipynb
│   └── 02_eda.ipynb             # notebook principal entregable
├── src/eda/
│   ├── __init__.py
│   ├── load.py                  # descarga/lectura + caché CSV
│   ├── clean.py                 # nulos, tipos, duplicados, negativos
│   ├── features.py              # ratios, fechas, media móvil, grupos
│   └── viz.py                   # helpers de gráficos
├── scripts/
│   └── run_pipeline.py          # un comando: raw → processed
├── reports/
│   └── informe_ejecutivo.md     # + PDF
├── dashboard/
│   └── app.py                   # Streamlit (nivel Experto)
├── tests/
│   └── test_clean.py
├── AGENTS.md
├── openspec/                    # specs y cambios
└── .opencode/
    ├── agents/
    ├── skills/
    └── commands/
```

**Regla clave:** el notebook consume `src/eda`, no reimplementa la limpieza. Así el pipeline, los tests y el dashboard reutilizan el mismo código, y el notebook sigue siendo el entregable narrativo.

---

## 6. Soporte de IA

### 6.1 `AGENTS.md` (contexto permanente)

Debe incluir:

- Objetivo del proyecto y rúbrica de niveles.
- Dataset elegido y contrato de datos.
- Convenciones: español en markdown, inglés en código, type hints, docstrings.
- Comandos: `python scripts/run_pipeline.py`, `pytest`, `jupyter lab`.
- Reglas: no meter datos en git, no ejecutar celdas fuera de orden, no inventar conclusiones.
- Definición de "hecho": notebook ejecuta de arriba abajo sin errores + tests verdes + informe actualizado.

### 6.2 Agentes y subagentes

| Agente | Modo | Rol | Modelo sugerido |
|---|---|---|---|
| `eda-lead` | primary | Orquesta, decide alcance, revisa entregables | modelo fuerte |
| `data-profiler` | subagent | Perfila dataset, nulos, tipos, duplicados; solo lectura | modelo barato |
| `data-cleaner` | subagent | Implementa `clean.py` + tests; edición en `src/` | modelo medio/fuerte |
| `eda-analyst` | subagent | Preguntas, univariado/bivariado, outliers, correlación | modelo fuerte |
| `viz-designer` | subagent | Gráficos con estándares | modelo medio |
| `notebook-reviewer` | subagent | QA: orden, reproducibilidad, markdown, outputs | modelo barato |
| `report-writer` | subagent | Informe ejecutivo para no técnicos | modelo fuerte |
| `git-steward` | subagent | Ramas, commits convencionales, PRs | modelo barato |

Ejemplo de subagente (`.opencode/agents/notebook-reviewer.md`):

```markdown
---
description: Revisa el notebook entregable (orden, reproducibilidad, narrativa)
mode: subagent
model: opencode-go/deepseek-v4.1-flash
permissions:
  - action: edit
    resource: "*"
    effect: deny
  - action: shell
    resource: "jupyter nbconvert *"
    effect: ask
---
Eres revisor de notebooks. Comprueba:
1. Ejecución de arriba abajo sin errores.
2. Markdown explicativo antes de cada bloque de código.
3. Sin outputs obsoletos ni celdas duplicadas.
4. Conclusiones apoyadas en gráficos concretos.
Devuelve hallazgos por severidad con celda y línea.
```

### 6.3 Skills de skills.sh

Instalación (requiere Node ≥ 22.20):

```bash
npx skills add <repo-de-github> --skill <nombre> -a opencode
```

Con `-a opencode` se instalan en `.agents/skills/` (descubierto por OpenCode V2). Con `-g` van a `~/.config/opencode/skills/`.

**Set recomendado:**

```bash
npx skills add https://github.com/k-dense-ai/scientific-agent-skills --skill exploratory-data-analysis -a opencode
npx skills add https://github.com/jeffallan/claude-skills --skill pandas-pro -a opencode
npx skills add https://github.com/anthropics/knowledge-work-plugins --skill statistical-analysis -a opencode
npx skills add https://github.com/anthropics/knowledge-work-plugins --skill data-visualization -a opencode
npx skills add https://github.com/mindrally/skills --skill data-analysis-jupyter -a opencode
npx skills add https://github.com/openai/skills --skill jupyter-notebook -a opencode
npx skills add https://github.com/wshobson/agents --skill data-storytelling -a opencode
npx skills add https://github.com/obra/superpowers --skill test-driven-development -a opencode
npx skills add https://github.com/addyosmani/agent-skills --skill git-workflow-and-versioning -a opencode
npx skills add https://github.com/streamlit/agent-skills --skill developing-with-streamlit -a opencode
```

**Opcionales:** `scientific-visualization`, `technical-writing`, `conventional-commit`, `query` (DuckDB).

**Mapeo a subagentes:**

| Subagente | Skills |
|---|---|
| `data-profiler` | `exploratory-data-analysis`, `pandas-pro` |
| `data-cleaner` | `pandas-pro`, `statistical-analysis`, `test-driven-development` |
| `eda-analyst` | `statistical-analysis`, `data-analysis-jupyter` |
| `viz-designer` | `data-visualization` (+ `scientific-visualization`) |
| `notebook-reviewer` | `jupyter-notebook` |
| `report-writer` | `data-storytelling` (+ `technical-writing`) |
| `git-steward` | `git-workflow-and-versioning` (+ `conventional-commit`) |
| `dashboard-dev` | `developing-with-streamlit` |

Las skills se "atan" a cada agente con permisos en `opencode.jsonc`:

```jsonc
{
  "agents": {
    "viz-designer": {
      "permissions": [
        { "action": "skill", "resource": "*", "effect": "deny" },
        { "action": "skill", "resource": "data-visualization", "effect": "allow" }
      ]
    }
  }
}
```

### 6.4 Skills propias (español y rúbrica)

| Skill | Para qué |
|---|---|
| `dataset-triage` | Validar el dataset contra los requisitos exactos del README |
| `rubric-checklist` | Mapear cada nivel a tareas concretas |
| `executive-report-es` | Estructura del informe para un CEO, en español |
| `notebook-hygiene` | Markdown entre celdas, ejecución top-down, sin outputs obsoletos |
| `covid-data-dictionary` | Contrato del dataset COVID: `date` entero, negativos, columnas >80 % nulas |
| `viz-standards-es` | Títulos, ejes, unidades y leyendas en español; paleta accesible |

**Regla:** técnica genérica → skills.sh; convenciones del proyecto → skills propias.

### 6.5 MCPs

| MCP | Para qué | Instalación |
|---|---|---|
| Context7 | Documentación actualizada de pandas, seaborn, plotly, Streamlit | `opencode mcp add context7 --url https://mcp.context7.com/mcp` |
| GitHub | Issues, PRs, milestones, Project board | remoto con OAuth (`/mcps` → sign in) |
| DuckDB/SQLite (opcional) | Consultar CSV/Parquet grandes | solo si el dataset crece |
| Playwright (opcional) | E2E del dashboard | solo nivel Experto |

Verificación: `opencode mcp list` → debe decir `connected`.

### 6.6 `opencode.jsonc` base

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "default_agent": "eda-lead",
  "mcp": {
    "servers": {
      "context7": { "type": "remote", "url": "https://mcp.context7.com/mcp" }
    }
  },
  "permissions": [
    { "action": "shell", "resource": "git push *", "effect": "ask" },
    { "action": "edit", "resource": "data/**", "effect": "deny" }
  ]
}
```

---

## 7. OpenSpec: planificar antes de escribir código

Instalación:

```bash
curl -fsSL https://openspec.dev/cli/install.sh | sh
# o: npm install -g @fission-ai/openspec@latest  (Node >= 22.12)
cd "/home/brian/Documentos/F5 IA/M2_Data_Analytics_Machine_Learning/Proyectos/P1_Exploratory_data_analysis"
openspec init
```

Flujo, un cambio por bloque:

```text
/opsx:explore            → decidir dataset y alcance
/opsx:propose add-data-ingestion
/opsx:apply              → implementar load.py + descarga + caché
/opsx:archive
/opsx:propose add-cleaning
/opsx:propose add-eda
/opsx:propose add-report
/opsx:propose add-dashboard   (opcional)
```

Cada `propose` genera `proposal.md`, `specs/`, `design.md` y `tasks.md`. **El plan se revisa antes de tocar código.**

---

## 8. Preparación Git / GitHub

### Local

```bash
git init -b main
git remote add origin <tu-repo>
```

- `.gitignore`: `.venv/`, `__pycache__/`, `.ipynb_checkpoints/`, `data/raw/*.csv`, `data/processed/`, `.env`, `.DS_Store`
- `.gitattributes`: `*.ipynb diff=jupyter` y forzar LF
- `nbstripout` para no versionar outputs del notebook
- `pre-commit`: `ruff` (lint+format), `nbstripout`, `check-yaml`, `end-of-file-fixer`
- `requirements.txt` + `pyproject.toml` con `ruff` y `pytest` como dev

### GitHub

- Descripción y topics: `eda`, `python`, `pandas`, `dataviz`, `covid19`
- `LICENSE` (MIT), `CONTRIBUTING.md`, plantilla de PR y de issues
- **Milestone** "Entrega EDA — semana 1"
- **Project** con columnas: `Backlog → In progress → Review → Done`
- Issues por entregable/nivel, cerradas con `Closes #N` en los PRs
- **GitHub Actions** (`ci.yml`): instalar deps → `ruff check` → `pytest`. Opcional: ejecutar el notebook con `nbclient`/`papermill`.

### Ramas y commits (trunk-based, ramas cortas)

```text
main
├── feat/data-ingestion
├── feat/cleaning
├── feat/eda-univariate
├── feat/eda-bivariate
├── feat/features-time
├── feat/report
└── feat/dashboard
```

- Ramas: `feat/...`, `fix/...`, `docs/...`, `test/...`
- Commits: Conventional Commits (`feat: add covid data loader with cache`, `fix: handle negative deathIncrease`, `docs: add executive summary`)
- Cada rama → PR → squash merge a `main`
- Tag final `v1.0.0` y Release con el PDF del informe

---

## 9. Plan de ejecución en 7 días

| Día | Trabajo | Entregable |
|---|---|---|
| 1 | Setup repo, OpenSpec, agentes/skills/MCP; descarga y profiling | `openspec/` + `01_profiling.ipynb` + `load.py` |
| 2 | Limpieza + tests (nulos, tipos, duplicados, negativos) | `clean.py`, `test_clean.py`, `processed.csv` |
| 3 | Univariado + bivariado + 5–8 gráficos | secciones del notebook |
| 4 | Features, correlación, tendencias, merge población | `features.py` + heatmap + series |
| 5 | Normalización, outliers, segmentos, plotly | análisis avanzado |
| 6 | Informe ejecutivo, README, requirements, pulido del notebook | `reports/`, README final |
| 7 | Pipeline de un comando, dashboard (opcional), QA, CI, tag | `run_pipeline.py`, `app.py`, `v1.0.0` |

**Regla de oro:** cada día el notebook debe ejecutar de arriba abajo. Nada de "lo arreglo al final".

---

## 10. Decisiones pendientes

1. **Dataset**: COVID Tracking Project (recomendado) u otro.
2. **Nivel objetivo**: Avanzado (con Experto opcional) o Experto directo con dashboard.
3. **Repo destino (`origin`)**: fork del repo de `Factoria-F5-madrid` o repo propio nuevo.
4. **Modelos de los agentes**: Go para subagentes baratos y modelo actual para `eda-lead`.

---

## 11. Comandos de referencia

```bash
# Clonar en la carpeta actual
git clone https://github.com/Factoria-F5-madrid/ai_project_EDA.git .

# Entorno
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# OpenSpec
openspec init

# Skills
npx skills add <repo> --skill <nombre> -a opencode
npx skills list

# MCP
opencode mcp add context7 --url https://mcp.context7.com/mcp
opencode mcp list

# Rutas internas de OpenCode
opencode debug paths
```

---

## 12. Nota sobre el export de sesión (OpenCode V2)

En V2, `session.export` (`Ctrl+X` → `X`) guarda el transcript en la **carpeta temporal** del sistema:

```text
/tmp/session-<uuid>.md
```

No hay opción de configuración para cambiarlo: el `tmpdir()` está fijado en el código. Para llevarlo al proyecto:

```bash
cp "$(ls -t /tmp/session-*.md | head -1)" ./sesion_export.md
```

Función reutilizable para `~/.bashrc`:

```bash
oc-export() {
  local src dest title slug
  src="$(ls -t /tmp/session-*.md 2>/dev/null | head -1)"
  [ -n "$src" ] || { echo "No hay exports .md en /tmp"; return 1; }

  title="$(head -n1 "$src" | sed 's/^# *//')"
  slug="$(printf '%s' "$title" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]\+/-/g; s/^-//; s/-$//')"
  dest="${1:-${slug:-sesion}.md}"

  cp "$src" "$dest" && echo "Guardado en $dest"
}
```

Uso:

```bash
oc-export
oc-export informe_sesion.md
```

**Aviso:** `/tmp` se limpia al reiniciar.
