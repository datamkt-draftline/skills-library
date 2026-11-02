# Esquema del Excel de Gantt

El archivo Excel debe seguir exactamente la estructura del template `gantt-template.xlsx`.

## Hojas requeridas

- **Una hoja por área**: cada área del proyecto tiene su propia pestaña con las tareas y fechas de inicio/fin.
- **Hitos**: hoja con los hitos clave del proyecto.

## Columnas requeridas (por hoja de área)

| Columna | Descripción |
|---------|-------------|
| Tarea | Nombre de la tarea |
| Inicio | Fecha de inicio (formato fecha Excel) |
| Fin | Fecha de fin (formato fecha Excel) |
| Responsable | Persona o equipo responsable |
| Estado | Estado actual de la tarea |

## Qué hacer si el archivo no cumple la estructura

Si el archivo no tiene las hojas o columnas requeridas, notificar al usuario con detalle de qué falta antes de continuar. Ejemplo: "El archivo no tiene la hoja 'Hitos'. Por favor agregala o descargá el template desde esta skill."

## Template oficial

Descargar desde esta skill con el comando `/gantt` y seleccionar "entregame el template".
