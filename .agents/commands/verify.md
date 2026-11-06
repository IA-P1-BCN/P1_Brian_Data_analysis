---
description: Verifica el repositorio (ruff, pytest, notebooks, OpenSpec y agentes)
---

Ejecuta la verificación completa del proyecto y devuélveme un resumen.

```bash
set -o pipefail

echo "== ruff =="
ruff check .

echo "== pytest =="
pytest -q

echo "== OpenSpec =="
npm run spec:validate

echo "== agentes =="
python scripts/sync_agents.py --check
python scripts/validate_agent_infra.py

echo "== notebooks =="
for nb in notebooks/01_profiling.ipynb notebooks/02_eda.ipynb; do
  [ -f "$nb" ] || continue
  jupyter nbconvert --to notebook --execute "$nb" --output "/tmp/$(basename "$nb")"
done
```

Reglas:

- No corrijas nada automáticamente hasta que te lo pida.
- Si un notebook no existe todavía, indícalo y sigue.
- Devuelve: comando, resultado y, si falla, la primera causa accionable.
- No commitees ni hagas push.
