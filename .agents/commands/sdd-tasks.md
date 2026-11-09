---
description: Descompone el diseño de un change en tareas atómicas con su issue
---

Escribe `openspec/changes/$ARGUMENTS/tasks.md`.

Antes de escribir:

1. Lee `proposal.md`, `specs/<capacidad>/spec.md` y `design.md`.
2. Lee el backlog de issues y sus IDs (`N1-01`… `N3-08`).
3. Identifica qué tareas son de código, cuáles de notebook y cuáles de
   informe.

Formato:

```markdown
# Tareas · <change>

## <Bloque>
- [ ] `N1-04` Implementar `clean.py` (#12)
  - Criterio: ...
  - Validación: `pytest tests/test_clean.py`
```

Reglas:

- Una tarea = un issue = una PR.
- Cada tarea referencia su ID y su issue.
- Incluye validación en cada bloque: `ruff`, `pytest`, notebook.
- No mezcles niveles en la misma tarea.
- No incluyas tareas que no estén en el backlog sin avisar.
- No escribas código.
