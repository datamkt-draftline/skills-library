---
name: events-dashboard
description: Genera y muestra el dashboard ejecutivo de ticketing de Quilmes Rock 2027 (KPIs comerciales, forecast, heatmap diario, SMI e insights). Activa cuando el usuario pide ver el dashboard de eventos / Quilmes Rock / ticketing.
action: true
---

# Events Dashboard — Quilmes Rock 2027

Genera un HTML standalone a partir de los archivos de datos, luego lo abre.
El dashboard incluye KPIs comerciales, ritmo de venta diario, comparación vs
QR25, forecast por escenarios, heatmap, SMI (Sales Momentum Index) e insights
automáticos. El botón "Actualizar datos" en el dashboard permite subir un CSV
o XLSX nuevo directamente desde el navegador sin re-ejecutar el script.

## Archivos de la skill

- `scripts/build_dashboard.py` — Script que procesa los datos y genera el HTML.
- `references/template.html` — HTML con layout, estilos y lógica JS; sin datos.
- `references/Tickets Info-data-2026-11-16 10_21_10.csv` — Export QR27 (default).
- `references/Venta diaria Quilmes 2025.xlsx` — Venta diaria QR25 (default).

## Cómo usarla

1. Correr el script (usa los archivos default de `references/`):
   ```bash
   python3 .claude/skills/events-dashboard/scripts/build_dashboard.py \
       --output uploads/quilmes-rock-2027-dashboard.html
   ```
   Para usar archivos distintos (el usuario subió una actualización):
   ```bash
   python3 .claude/skills/events-dashboard/scripts/build_dashboard.py \
       --qr27 "uploads/<nuevo_archivo>.csv" \
       --qr25 "uploads/<nuevo_qr25>.xlsx" \
       --output uploads/quilmes-rock-2027-dashboard.html
   ```
2. Llamar a `mcp__tas__open_file` con la ruta absoluta del HTML generado.
3. Responder con un mensaje breve.

## Actualizar la fuente de datos por defecto

Si el usuario sube un archivo nuevo y quiere que quede como default, copiar
el archivo a `references/` con el nombre original antes de correr el script.

## Supuestos

- El CSV QR27 tiene columnas: `Ticket, Forma_de_pago, Precio, Fecha_de_venta, Butaca, ...`
- El XLSX QR25 tiene columnas: `fecha, [categorías...], total_tickets`
- La fecha del festival es 2027-04-01. Si cambia, editar `FESTIVAL_DATE` en el script.

## When not to use

- Dashboards de eventos distintos a Quilmes Rock 2027.
