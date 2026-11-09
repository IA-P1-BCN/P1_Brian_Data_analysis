## Qué cambia

<!-- Resumen en 1-3 bullets. -->

## Issue

Closes #

## Nivel

- [ ] N1 · Esencial
- [ ] N2 · Medio
- [ ] N3 · Avanzado
- [ ] Infraestructura

## Change de OpenSpec

<!-- Ruta: openspec/changes/<change>/ -->

## Checklist

- [ ] El notebook afectado ejecuta de arriba abajo.
- [ ] `ruff check .` limpio.
- [ ] `pytest -q` verde.
- [ ] `npm run spec:validate` verde.
- [ ] `python scripts/sync_agents.py --check` verde.
- [ ] Sin datos crudos, `.venv/` ni outputs de notebook en git.
- [ ] Entrada en `docs/ai-log.md` si se usó IA.
- [ ] La spec o el README se actualizan si cambia el alcance.

## Evidencia

<!-- Commit, figura, tabla, salida de tests o enlace al notebook. -->

## Limitaciones

<!-- Qué no cubre esta PR. -->
