---
description: "Revisa un change o una PR antes de mergear"
---

<!-- GENERADO por scripts/sync_agents.py desde .agents/commands/sdd-review.md. No editar a mano. -->

Revisa: **$ARGUMENTS**.

1. Identifica el diff (`git diff develop...HEAD` o la PR indicada) y el
   `spec.md` del change.
2. Delega en el subagente `eda-reviewer` para una revisión de solo lectura.
3. Pídele que compruebe:
   - cumplimiento de la spec y del issue;
   - reproducibilidad del notebook;
   - tratamiento de nulos, negativos, duplicados y outliers;
   - validez estadística de las conclusiones;
   - ejes, unidades y trazabilidad de las cifras;
   - limitaciones del informe.
4. Ejecuta la verificación automática:
   ```bash
   ruff check .
   pytest -q
   npm run spec:validate
   python scripts/sync_agents.py --check
   ```
5. Si el change toca notebooks, ejecútalos de arriba abajo.
6. Devuélveme:
   - veredicto (`APROBADO` / `CAMBIOS NECESARIOS`);
   - hallazgos ordenados por gravedad;
   - comandos ejecutados y su resultado.

No mergees ni archives el change. No edites archivos durante la revisión.
