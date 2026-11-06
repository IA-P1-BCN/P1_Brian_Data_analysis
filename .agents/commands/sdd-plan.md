---
description: Escribe el diseño técnico de un change con spec aprobada
---

Escribe `openspec/changes/$ARGUMENTS/design.md`.

Antes de escribir:

1. Comprueba que `proposal.md` y `specs/<capacidad>/spec.md` existen y que la
   persona los ha revisado.
2. Lee `AGENTS.md`, `openspec/config.yaml` y el estado actual de `src/eda/`.
3. Identifica las decisiones técnicas que hay que tomar.

El `design.md` debe incluir:

```markdown
## Contexto
## Decisiones
### Decisión 1 · <título>
- **Qué:** ...
- **Por qué:** ...
- **Alternativas:** ...
- **Consecuencias:** ...

## Contratos
<funciones, firmas, columnas y formatos>

## Flujo de datos
<raw → processed → notebook → informe>

## Riesgos
## Validación
<tests, comprobaciones y comandos>
```

Reglas:

- No repitas la spec; explica **cómo** se implementa.
- No inventes columnas ni endpoints.
- Si hay una decisión que no puedes tomar, escribe `<<PENDIENTE>>` y
  pregúntame.
- No escribas código ni `tasks.md`.
