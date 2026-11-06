# Design

## Context

Repositorio recién creado, con `README.md`, `docs/contexto_proyecto_eda.md`
y `.gitignore`. No hay entorno, ni estructura, ni CI. El proyecto se ejecuta
en local con Python 3.12+ y necesita una herramienta Node solo para OpenSpec.

## Goals / Non-Goals

**Goals:**
- Un comando de instalación y otro de verificación.
- Estructura estable para los 26 issues del backlog.
- CI que bloquee PRs con errores de estilo, tests o specs.
- Una sola fuente para agentes y comandos.

**Non-Goals:**
- Publicar el paquete en PyPI.
- Docker o devcontainers.
- Notebooks o análisis reales en este change.

## Decisions

### Decisión 1 · `venv` + `pip` en vez de `uv`

- **Qué:** usar `python -m venv .venv` y `requirements.txt`.
- **Por qué:** el enunciado pide `requirements.txt` y es lo que usa el
  evaluador; `venv` está en cualquier máquina.
- **Alternativas:** `uv` (más rápido, pero añade una herramienta que el
  evaluador puede no tener).
- **Consecuencias:** instalación más lenta, pero universal.

### Decisión 2 · Node solo para OpenSpec

- **Qué:** `package.json` con `@fission-ai/openspec` como `devDependency`.
- **Por qué:** OpenSpec es la herramienta de specs elegida y no contamina
  las dependencias Python.
- **Alternativas:** instalar OpenSpec global (menos reproducible).
- **Consecuencias:** hay que tener Node 20+ para validar specs; se documenta
  en el README.

### Decisión 3 · Una fuente para agentes

- **Qué:** `.agents/` es la fuente; `.opencode/` se genera.
- **Por qué:** evita editar dos veces y permite añadir Claude Code después.
- **Alternativas:** editar `.opencode/` a mano (se desincroniza).
- **Consecuencias:** la CI comprueba `sync_agents.py --check`.

### Decisión 4 · CI en la PR, no solo en `develop`

- **Qué:** `ci.yml` se ejecuta en PRs hacia `develop` y `main`, y en pushes
  a `develop`.
- **Por qué:** el feedback llega antes del merge.
- **Alternativas:** solo en `main` (demasiado tarde).
- **Consecuencias:** hay que mantener los jobs rápidos (< 5 min).

## Risks / Trade-offs

- El job de notebooks puede ser lento; se limita a PRs que tocan
  `notebooks/` o `src/`.
- Si OpenSpec cambia de versión, hay que actualizar `package.json` y
  `openspec/config.yaml`.
- La CI no ejecuta notebooks vacíos: se añade cuando existan.
