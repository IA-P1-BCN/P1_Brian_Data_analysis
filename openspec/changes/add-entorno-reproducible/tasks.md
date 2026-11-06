# Tasks

## 1. Estructura

- [ ] 1.1 `N1-01` Crear `data/{raw,processed,external}`, `notebooks/`,
  `src/eda/`, `tests/`, `reports/figures/` con `.gitkeep`
  - Criterio: el árbol existe y `data/raw/*.csv` está ignorado
  - Validación: `git status --short` no muestra datos crudos

- [ ] 1.2 `N1-01` Crear `requirements.txt`, `pyproject.toml` y `.gitignore`
  - Criterio: `pip install -r requirements.txt` y `ruff check .` funcionan
  - Validación: `ruff check .`

## 2. Capa de IA

- [ ] 2.1 `N1-01` Crear `AGENTS.md`, `.agents/` y `.opencode/`
  - Criterio: 7 subagentes, 7 comandos y 6 skills propias
  - Validación: `python scripts/sync_agents.py --check`

- [ ] 2.2 `N1-01` Crear `scripts/sync_agents.py`,
  `scripts/new_change.py` y `scripts/validate_agent_infra.py`
  - Criterio: los tres scripts terminan con código 0
  - Validación: `python scripts/validate_agent_infra.py`

## 3. OpenSpec

- [ ] 3.1 `N1-01` Instalar `@fission-ai/openspec` y crear
  `openspec/config.yaml`
  - Criterio: `npx openspec list` reconoce el proyecto
  - Validación: `npm run spec:validate`

- [ ] 3.2 `N1-01` Crear los 7 changes por épica
  - Criterio: `openspec/changes/` contiene los 7 changes con
    `proposal.md`, `design.md`, `tasks.md` y `specs/<cap>/spec.md`
  - Validación: `npm run spec:validate`

## 4. CI

- [ ] 4.1 `N1-01` Crear `.github/workflows/ci.yml`
  - Criterio: jobs de `ruff`, `pytest`, `openspec` e infraestructura
  - Validación: la PR de `feat/infra-ia` muestra los jobs en verde

## 5. Cierre

- [ ] 5.1 Ejecutar `/sdd-review`
- [ ] 5.2 Ejecutar `/verify`
- [ ] 5.3 Registrar en `docs/ai-log.md`
