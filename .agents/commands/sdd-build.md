---
description: Implementa una tarea de un change delegando en el subagente adecuado
---

Implementa: **$ARGUMENTS**.

1. Localiza la tarea en `openspec/changes/<change>/tasks.md` y su issue.
2. Comprueba que el `design.md` existe y que la tarea está asignada.
3. Elige el subagente según el tipo de tarea:
   - `src/eda/` o `tests/` → `data-engineer`
   - `notebooks/` → `eda-analyst`
   - `src/eda/viz.py` o `reports/figures/` → `viz-designer`
   - `reports/informe.md` o `README.md` → `report-writer`
4. Pásale el contexto mínimo: issue, criterio de aceptación, archivos
   implicados y restricciones.
5. Cuando termine, ejecuta:
   ```bash
   ruff check .
   pytest -q
   ```
   y, si tocó un notebook, ejecútalo de arriba abajo.
6. Marca la tarea en `tasks.md` solo si la validación pasa.
7. Devuélveme: archivos, tests, evidencia y `<<PENDIENTE>>`.

No mezcles tareas de niveles distintos. No toques `AGENTS.md` ni
`openspec/config.yaml`.
