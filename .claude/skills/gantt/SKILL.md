---
name: gantt
description: Genera un Gantt interactivo (HTML) a partir de un Excel, o entrega el template Excel si el usuario pregunta cómo usarlo o pide un ejemplo.
action: true
---

# Gantt desde Excel

Esta skill tiene dos modos:

---

## Modo 1 — El usuario pide el template o pregunta cómo usarlo

Si el usuario pregunta cómo funciona, pide el template, o quiere saber la estructura del Excel:

1. Abrí el template con `mcp__tas__open_file`:
   ```
   /home/agent/work/2026-09-14_9muktr/gantt-template.xlsx
   ```

2. Explicá brevemente la estructura:
   - **`Areas`**: nombre, color (hex) y orden de cada área. El nombre debe coincidir exactamente con el nombre de la hoja de esa área.
   - **Una hoja por área** (ej. `AI`, `BI`, `Social Insights`): columnas `Tarea | Fecha inicio | Fecha fin | Estado | Tipo hito | Fecha hito | Link hito`. Las filas de hito tienen `Tarea` vacío y pertenecen a la tarea de la fila anterior.
   - **`TiposHito`** (opcional): `Tipo | Color | Icono` — iconos disponibles: `database`, `chart`, `message`, `users`, `flag`.
   - **`Config`** (opcional): claves `Titulo` y `Subtitulo`.

---

## Modo 2 — El usuario pasa un Excel y pide ver el Gantt

1. Identificá el archivo `.xlsx` (viene en `uploads/` o lo menciona el usuario).

2. Ejecutá el generador (sin segundo argumento: el script genera el HTML como `{titulo-slug}-gantt.html` en el mismo directorio del xlsx, usando el `Titulo` de la hoja `Config`):
   ```bash
   python3 /home/agent/work/2026-09-14_9muktr/.claude/skills/gantt/scripts/generate_gantt.py "<ruta-al-xlsx>"
   ```
   El comando imprime en stdout la ruta del HTML generado — usala para el paso siguiente.

3. Abrí el resultado con `mcp__tas__open_file` usando la ruta impresa.

4. Resumí brevemente: áreas encontradas, cantidad de tareas, rango temporal.

---

## Troubleshooting

- Si una tarea no aparece con barra: verificá que `Fecha inicio` y `Fecha fin` estén cargadas (no vacías).
- Si un hito no aparece: el valor de `Tarea` en la fila del hito debe quedar vacío — la tarea a la que pertenece se infiere de la fila anterior.
- Si el subtítulo da error de tipo: el script lo convierte a string automáticamente.
