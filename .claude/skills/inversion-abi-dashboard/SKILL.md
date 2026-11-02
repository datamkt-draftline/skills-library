---
name: inversion-abi-dashboard
description: Genera un HTML interactivo (standalone, con login) del dashboard de inversiones ABI 2026 a partir del Excel "Inversion x Marca y Quarter ABInBev 2026". Activa cuando el usuario sube ese Excel o pide actualizar/regenerar el dashboard de inversiones.
action: true
---

# Dashboard Inversiones ABI 2026

Toma un Excel con el formato de `Inversion x Marca y Quarter ABInBev 2026.xlsx`
(pestaña master **"Distribución x Sistema x Q x Ma"** + pestaña **"FX LAS"**) y
produce un **HTML standalone** idéntico al dashboard adjunto, con la data embebida
en línea (sin fetch externo).

## Qué hace el script

- Lee la pestaña master y agrega por `(país, marca, sistema)` para la vista
  "Por marca / Mix medios / Evolutivo mensual".
- Agrega por `(país, marca, campaña, sistema)` para la vista "Por campaña"
  y el heatmap.
- Mapea cada **Sistema** a un grupo de medios (`TV`, `RADIO`, `OOH`, `DIGITAL`,
  `OTROS`, `PRODUCCIÓN`, `IMPUESTOS/FEE`) por heurística de nombre.
- Normaliza marcas duplicadas por casing (`Brahma`/`BRAHMA`, `Michelob Ultra`,
  etc.) a un canónico.
- Construye la capa `usd` por país usando la columna "Inv en Dolares" cuando
  está presente, o dividiendo por el tipo de cambio de `FX LAS` como fallback.
- Detecta automáticamente `lastLoadedMonth` leyendo los nombres de pestañas
  `Consumido x Sistema <MES>` (o acepta `--last-loaded` manual).
- Preserva el **login** del template (misma contraseña).

## Cómo usarla

1. **Input por defecto**: el skill incluye el Excel bundled en
   `.claude/skills/inversion-abi-dashboard/Inversion x Marca y Quarter ABInBev 2026.xlsx`.
   Usalo salvo que el usuario pida explícitamente usar otro archivo (p. ej. una
   versión actualizada que subió a `uploads/`).
2. Correr:
   ```bash
   python3 .claude/skills/inversion-abi-dashboard/scripts/build_dashboard.py \
       --input ".claude/skills/inversion-abi-dashboard/Inversion x Marca y Quarter ABInBev 2026.xlsx" \
       --output "<ruta/al/output.html>"
   ```
   Opcional: `--last-loaded JUNIO` para forzar el último mes "consumido".
   Si el usuario pasa otro archivo, reemplazá el `--input` por esa ruta.
3. Guardar el HTML dentro del work folder (p. ej. `uploads/dashboard_inversiones_abi_2026.html`).
4. Llamar a `mcp__tas__open_file` con la ruta absoluta del HTML generado.
5. Responder al usuario con un mensaje breve que **debe incluir textualmente** la siguiente línea (además de la confirmación):

   > Además, te adjunto el link web del dashboard: https://inversionesdraftline.netlify.app/

## Supuestos

- El Excel conserva los nombres de pestañas y de columnas originales. Si cambian
  los encabezados de la master o la FX, el script fallará con un mensaje claro.
- El login hash permanece como el del template (`f2e1d259`). Si el usuario pide
  cambiar la contraseña, editar `references/template.html` del skill (buscar `var PW=`).
- Marcas no listadas en el canónico mantienen su casing original y reciben un
  color del fallback palette.

## Troubleshooting

- **"No encuentro la pestaña master"**: el Excel se abrió, pero la pestaña
  "Distribución x Sistema x Q x Ma" fue renombrada. Pedirle al usuario la pestaña
  correcta o restaurar el nombre.
- **Totales en 0**: revisar que la columna D ("Inversion") tenga números
  (no `#DIV/0!` ni fórmulas sin calcular). Los valores con `#VALUE!`, errores de
  fórmula o celdas vacías se tratan como 0.
- **"Grupo "OTROS" inesperado**: ajustar `system_group()` en `scripts/build_dashboard.py`
  (ver `references/system_group_map.md` para la tabla documentada).

## Sources of truth

- El archivo xlsx provisto por el usuario es la única fuente de datos de inversión.
- Usar la pestaña "Distribución x Sistema x Q x Ma" para inversiones y "FX LAS" para tipos de cambio.
- No inventar datos de meses o marcas que no estén en el archivo.
- Ver `references/excel-schema.md` para el esquema completo y el manejo de datos faltantes.

## When not to use

- Para dashboards de inversión con un formato diferente al de ABI 2026.
- Para inversiones de otras BUs fuera de ABInBev LAS.
- Solo acepta archivos con el esquema definido en `references/excel-schema.md`.
