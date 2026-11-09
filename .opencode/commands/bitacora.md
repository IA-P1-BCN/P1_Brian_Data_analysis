---
description: "Registra en docs/ai-log.md lo hecho con IA (delegando en ai-scribe)"
---

<!-- GENERADO por scripts/sync_agents.py desde .agents/commands/bitacora.md. No editar a mano. -->

Registra en la bitácora: **$ARGUMENTS**.

1. Reúne el contexto de la tarea:
   - issue y change;
   - modelo usado;
   - prompts clave (resumidos);
   - archivos producidos;
   - errores o alucinaciones detectadas;
   - decisiones aceptadas y rechazadas;
   - verificaciones ejecutadas.
2. Delega en el subagente `ai-scribe`.
3. Pídele que añada una entrada al final de `docs/ai-log.md` siguiendo
   `.agents/templates/ai-log-entry.md`.
4. Devuélveme la entrada y los `<<PENDIENTE>>` que debo completar.

No edites entradas anteriores. No incluyas secretos ni datos personales.
