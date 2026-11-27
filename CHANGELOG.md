# Changelog

Historial de cambios significativos por skill. Formato: `### X.Y.Z — YYYY-MM-DD`.

> **Regla de mantenimiento**: cualquier cambio en el contenido compartido de las skills `presentacion-bu-las-*` (layouts, manual de marca, fuentes, lógica común) **debe replicarse en las cinco variantes**: `cbn`, `cervepar`, `chile`, `cmq` y `fnc`.

---

## analyze-survey

### 1.0.0 — 2026-10-21
- Versión inicial publicada.

---

## completion-status

### 1.0.0 — 2026-11-27
- Versión inicial publicada.

---

## content-tracker

### 1.0.0 — 2026-11-27
- Versión inicial publicada.

---

## corona-pptx

### 1.0.0 — 2026-11-27
- Versión inicial publicada.

---

## create-survey

### 1.0.0 — 2026-11-27
- Versión inicial publicada como renombrado de `survey-creator`.
- El PAT de Typeform está embebido en el SKILL.md local; en el repo se reemplaza por placeholder `{{TYPEFORM_PAT}}` — reemplazar por el token real antes de usar en otra instancia.

---

## design-survey

### 1.0.0 — 2026-11-27
- Versión inicial publicada como extracción del flujo de diseño de `survey-helper` (Pasos 1–9).
- Incluye los 45 xlsx de encuestas de referencia y `surveys_catalog.md`, movidos desde `survey-helper`.

---

## events-dashboard

### 1.0.0 — 2026-11-27
- Versión inicial publicada.

---

## gantt

### 1.0.0 — 2026-10-16
- Versión inicial publicada.

---

## github-updater

### 1.0.0 — 2026-11-03
- Versión inicial publicada.

---

## glosario-skills

### 1.1.0 — 2026-10-30
- Agrega skills Sauron Weekly y Argos Influencer Discovery al glosario.
- Incorpora botón de copiar prompt por skill en el modal.
- Aplica tinte de color por tipo (herramienta/reporte) en los botones de items.
- Ajusta espaciado vertical para que todos los pilares quepan above the fold.

### 1.0.0 — 2026-10-22
- Versión inicial publicada.

---

## influencer-audience

### 1.0.0 — 2026-10-15
- Versión inicial publicada.

---

## inversion-abi-dashboard

### 1.2.0 — 2026-10-30
- Agrega tooltip con desglose por subsistema en el pie chart.
- Implementa filtro YTD como default (reemplaza "Todos").
- Campañas clickeables en el gráfico de campañas.
- Stack mensual diferencia barras de plan vs. real ejecutado con opacidad.
- Switch LOCAL/USD se oculta automáticamente para Paraguay.
- `lastLoadedMonth` default actualizado a SEPTIEMBRE.

### 1.1.0 — 2026-10-22
- Agrega soporte multi-país con selector de país y switch de moneda LOCAL/USD.

### 1.0.0 — 2026-10-15
- Versión inicial publicada.

---

## leila

### 1.0.0 — 2026-10-27
- Versión inicial publicada.

---

## presentacion-bu-las-cbn

### 1.0.0 — 2026-10-30
- Versión inicial publicada.

---

## presentacion-bu-las-cervepar

### 1.0.0 — 2026-10-30
- Versión inicial publicada.

---

## presentacion-bu-las-chile

### 1.0.0 — 2026-10-30
- Versión inicial publicada.

---

## presentacion-bu-las-cmq

### 1.0.0 — 2026-10-02
- Versión inicial publicada.

---

## presentacion-bu-las-fnc

### 1.0.0 — 2026-10-30
- Versión inicial publicada.

---

## survey-helper

### 2.0.0 — 2026-11-27
- Refactor completo: convertido en orquestador delgado.
- El flujo de diseño de encuestas se extrajo a `design-survey`.
- La capa de API Typeform se renombró a `create-survey`.
- El dashboard de resultados lo sigue manejando `analyze-survey`.
- Los 45 xlsx de referencia y `surveys_catalog.md` se movieron a `design-survey`.

### 1.0.0 — 2026-11-27
- Versión inicial publicada (monolítica, incluía diseño, Typeform y análisis).
