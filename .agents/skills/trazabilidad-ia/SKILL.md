---
name: trazabilidad-ia
description: Cómo registrar en docs/ai-log.md el uso de IA del proyecto (modelo, prompts clave, errores, alucinaciones y decisiones aceptadas o rechazadas). Úsala al cerrar una tarea hecha con IA o al detectar un fallo del agente.
---

# Trazabilidad de IA

`docs/ai-log.md` es un **entregable** del proyecto. No es un diario íntimo:
es la evidencia de cómo se usó la IA y qué se verificó.

## Cuándo escribir

- Al cerrar una tarea o un issue.
- Al detectar una alucinación o un error del agente.
- Al tomar una decisión de diseño con ayuda de IA.
- Al comparar modelos o prompts.

## Formato

Cada entrada sigue `.agents/templates/ai-log-entry.md`:

```markdown
## 2026-11-07 · Limpieza de incrementos negativos

- **Issue / change:** #12 · `add-limpieza-calidad`
- **Herramienta:** OpenCode
- **Modelo:** <modelo>
- **Rol del agente:** `data-engineer`

### Objetivo
...

### Prompts clave
1. ...

### Qué produjo la IA
...

### Errores y alucinaciones
- ...

### Decisiones
- **Aceptadas:** ...
- **Rechazadas:** ... → ...

### Verificación humana
- [ ] ...
```

## Qué registrar

- **Modelo exacto** si lo sabes; si no, `<<PENDIENTE>>`.
- **Prompts resumidos**, no el volcado completo.
- **Errores concretos**: “inventó una columna `population` que no existía”,
  “usó `date` como string y el gráfico salió vacío”.
- **Decisiones**: qué aceptaste, qué rechazaste y por qué.
- **Verificación**: qué comandos ejecutaste y qué viste.

## Qué NO registrar

- Secretos, tokens, `.env`, credenciales.
- Datos personales.
- Contenido íntegro de ficheros grandes.
- Opiniones sobre personas.
- Resultados inventados o “pendientes de comprobar” presentados como hechos.

## Reglas

1. **Solo se añade al final.** No se editan entradas anteriores.
2. **Una entrada por tarea**, no una por prompt.
3. **Si falta un dato, `<<PENDIENTE>>`.** No lo inventes.
4. **Si la IA se equivocó, se escribe.** La bitácora no es marketing.
5. **La entrada se escribe antes de la PR**, no después.

## Ejemplo de error bien registrado

```markdown
### Errores y alucinaciones
- El agente propuso `df["population"]` sin haber hecho el merge con la tabla
  de población. Detectado al ejecutar el notebook (`KeyError`). Se corrigió
  añadiendo `merge_population()` y un test que verifica que no se pierden
  estados.
```
