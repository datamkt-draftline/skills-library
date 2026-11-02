# Esquema del Excel — Inversion x Marca y Quarter ABInBev 2026

## Pestañas requeridas

### Distribución x Sistema x Q x Ma
Contiene los datos de inversión por marca, sistema/grupo de medios, y mes.

| Columna | Descripción |
|---------|-------------|
| marca | Nombre de la marca (Quilmes, Patagonia, Brahma, etc.) |
| grupo | Grupo de medios / sistema (TV, Digital, OOH, etc.) |
| sistema | Subsistema específico |
| campaña | Nombre de la campaña |
| enero ... diciembre | Inversión ejecutada por mes |
| anual | Plan anual total |

### FX LAS
Contiene los tipos de cambio para conversión LOCAL → USD por país.

| Columna | Descripción |
|---------|-------------|
| país | Nombre del país |
| moneda | Código de moneda local |
| tasa | Tipo de cambio respecto al USD |

## Qué hacer si faltan datos

- Si falta alguna pestaña: notificar al usuario con el nombre exacto de la pestaña faltante.
- Si falta una columna requerida: notificar al usuario antes de proceder.
- Si `lastLoadedMonth` no está presente en los datos: usar el mes más reciente con datos como referencia.
- No inventar datos de meses, marcas o países que no estén en el archivo.
