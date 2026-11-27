---
name: completion-status
description: Genera el reporte HTML de LAS Completion Status ejecutando el script de generación y abriendo el archivo resultante.
action: true
---

Cuando el usuario invoca este skill (ya sea con `/completion-status` o pidiendo el reporte de completion / status de completion), seguí estos pasos exactamente:

1. Ejecutá el script Python para generar el HTML:
   ```
   uv run /home/agent/work/2026-09-14_9muktr/.claude/skills/completion-status/generate_report.py
   ```
2. El script imprime la ruta del archivo generado. Usá `mcp__tas__open_file` con esa ruta para presentarlo al usuario.
3. Informá al usuario que el reporte fue generado con la fecha de hoy.

No modifiques el HTML ni agregues contenido extra. El reporte es siempre el mismo; solo la fecha "Last Update" se actualiza automáticamente.
