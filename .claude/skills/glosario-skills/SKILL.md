---
name: glosario-skills
description: Genera un HTML interactivo con el glosario completo de skills disponibles, organizado en dos columnas (Tools | Reporting) con filtros por área. Cada skill es clickeable y muestra detalles (funcionalidad, comando, archivos requeridos, área) en un modal.
action: true
---

# Glosario de Skills

## Cómo funciona

1. Leé el bloque `GLOSARIO_DATA` más abajo y extraé dos arrays:
   - `AREAS`: lista de `{ nombre, color }` de cada área.
   - `SKILLS`: lista plana de todas las skills con sus campos (`tipo`, `area`, `nombre`, `comando`, `funcionalidad`, `archivos_requeridos`).
2. Tomá el `HTML_TEMPLATE` de abajo **exactamente como está** y reemplazá únicamente las dos líneas marcadas:
   - `/* AREAS_PLACEHOLDER */` → el array `AREAS` serializado como JS literal.
   - `/* SKILLS_PLACEHOLDER */` → el array `SKILLS` serializado como JS literal.
3. No modifiques ninguna otra parte del template. La estructura, el CSS y el JS son fijos.
4. Guardá el resultado en el working directory actual como `glosario-skills.html`.
5. Llamá a `mcp__tas__open_file` con el path absoluto del archivo generado.

## GLOSARIO_DATA

```json
{
  "areas": [
    {
      "nombre": "Marketing",
      "color": "#ff6b7a",
      "skills": [
        { "tipo": "tool", "nombre": "Presentaciones PPT-CMQ", "comando": "/presentacion-bu-las-cmq", "funcionalidad": "Genera presentaciones PowerPoint (.pptx) editables con la identidad visual de BU LAS + Cervecería y Maltería Quilmes a partir de un brief, información o archivos aportados por el usuario.", "archivos_requeridos": "Brief en texto, Word, PDF o imágenes de referencia. Opcional: logos, datos de la marca." },
        { "tipo": "tool", "nombre": "Generación de contenido Cont-Gen", "comando": "/cont-gen", "funcionalidad": "Genera piezas de contenido (copy, posteos, mails, scripts) alineadas a la voz de marca y al brief entregado.", "archivos_requeridos": "Brief del contenido a generar (texto o doc). Opcional: guía de tono de marca, ejemplos de referencia." },
        { "tipo": "reporting", "nombre": "Análisis/tracking de presupuesto Budget-Tracker", "comando": "/budget-tracker", "funcionalidad": "Analiza y hace seguimiento del presupuesto de marketing: ejecución vs. plan, desvíos por marca/mes/trimestre, alertas.", "archivos_requeridos": "Excel con el presupuesto planificado y ejecutado (columnas: marca, categoría, mes, planificado, ejecutado)." },
        { "tipo": "tool", "nombre": "Genome", "comando": "/genome", "funcionalidad": "Genera el genoma de una marca o campaña: atributos clave, posicionamiento, audiencias objetivo y pilares de comunicación.", "archivos_requeridos": "Información de la marca/campaña (brief, estudios previos, resultados). Opcional: data de competidores." }
      ]
    },
    {
      "nombre": "Data",
      "color": "#7aa2ff",
      "skills": [
        { "tipo": "reporting", "nombre": "Benchmarks Bench-CMQ", "comando": "/bench-cmq", "funcionalidad": "Genera benchmarks de categoría/competidores a partir de datos internos y fuentes externas, con comparativas visuales.", "archivos_requeridos": "Dataset de la categoría (xlsx/csv) con métricas de marca y competidores." },
        { "tipo": "reporting", "nombre": "Social Research Leila", "comando": "/leila", "funcionalidad": "Realiza research social (escucha activa, análisis de conversación, sentiment, trending topics) sobre un tema o marca.", "archivos_requeridos": "Opcional: dataset de menciones/posteos. Si no, parte de la consulta en texto libre." },
        { "tipo": "reporting", "nombre": "Análisis de performance de campañas Perfo-CMQ", "comando": "/perfo-cmq", "funcionalidad": "Analiza la performance de campañas digitales: reach, impresiones, CTR, CPM, CPC, conversiones, ROAS.", "archivos_requeridos": "Export de la plataforma (Meta, Google, TikTok, DV360, etc.) en xlsx/csv." },
        { "tipo": "reporting", "nombre": "Automatización SOE SOE-CMQ", "comando": "/soe-cmq", "funcionalidad": "Automatiza el cálculo de Share of Expenditure (SOE) por marca y categoría, con comparativas temporales.", "archivos_requeridos": "Reporte de inversión por marca/competidor (xlsx) y período a analizar." },
        { "tipo": "reporting", "nombre": "Mails Tracking Mails-Track", "comando": "/mails-track", "funcionalidad": "Hace tracking de performance de campañas de mail marketing: open rate, CTR, bounce, unsubscribes, por segmento.", "archivos_requeridos": "Export del ESP (ej. Salesforce Marketing Cloud, Mailchimp) en xlsx/csv." },
        { "tipo": "reporting", "nombre": "Automatización Encuestas y resultados", "comando": "/analyze-survey", "funcionalidad": "Analiza resultados de encuestas siguiendo una metodología por pasos y genera dashboard HTML + xlsx procesado con el detalle por pregunta.", "archivos_requeridos": "Archivo xlsx con los resultados de la encuesta (respuestas en bruto)." },
        { "tipo": "tool", "nombre": "Diccionario Estudios SL & Agile", "comando": "/diccionario-estudios", "funcionalidad": "Mantiene y consulta un diccionario de estudios realizados (Shopper Loyalty, Agile Research) con metodología, muestra, hallazgos clave y link al reporte original.", "archivos_requeridos": "Opcional: nuevo estudio para incorporar al diccionario (PDF o doc)." }
      ]
    },
    {
      "nombre": "Medios",
      "color": "#ffb86b",
      "skills": [
        { "tipo": "reporting", "nombre": "Análisis de inversión 1YP 2026-2027 1YP-Medios", "comando": "/1yp-medios", "funcionalidad": "Analiza la inversión 1YP (One Year Plan) 2026-2027 por marca, canal y trimestre con comparativas vs. año anterior.", "archivos_requeridos": "Excel con el plan de inversión 1YP (marca, canal, Q, monto)." },
        { "tipo": "reporting", "nombre": "Performance de influencers Influs-CMQ", "comando": "/influencer-audience", "funcionalidad": "Genera presentación PPTX editable con audience intelligence de uno o más influencers (biografía, partnerships, demographics, follower history) a partir de datos de CreatorIQ.", "archivos_requeridos": "Export de CreatorIQ con los influencers a analizar." },
        { "tipo": "reporting", "nombre": "TRPs TRPs-CMQ", "comando": "/trps-cmq", "funcionalidad": "Analiza TRPs (Target Rating Points) de campañas de TV: cobertura, frecuencia, GRPs, por canal/franja/target.", "archivos_requeridos": "Reporte de Kantar IBOPE / central de medios con TRPs por campaña." },
        { "tipo": "reporting", "nombre": "Content Tracker Cont-track", "comando": "/cont-track", "funcionalidad": "Hace tracking del contenido publicado por marca/plataforma: volumen, formatos, performance y gaps vs. plan.", "archivos_requeridos": "Export de plataformas (Meta Business, TikTok, YouTube Studio) o Google Sheet de planificación." }
      ]
    },
    {
      "nombre": "draftLine",
      "color": "#5eead4",
      "skills": [
        { "tipo": "tool", "nombre": "Armado de Briefs Briefs-dl", "comando": "/briefs-dl", "funcionalidad": "Genera briefs creativos estandarizados para draftLine a partir de la info del proyecto, con todos los campos requeridos (objetivos, target, mensajes, entregables, timings).", "archivos_requeridos": "Info del proyecto (texto, Word, PDF). Opcional: ejemplos de briefs anteriores." },
        { "tipo": "reporting", "nombre": "Agendas / visibilidad de proyectos Agenda-CMQ", "comando": "/agenda-cmq", "funcionalidad": "Genera una vista consolidada de todos los proyectos activos de draftLine con responsables, estado, próximos hitos.", "archivos_requeridos": "Export del sistema de gestión de proyectos (Monday, Asana, Google Sheet)." },
        { "tipo": "tool", "nombre": "Calendario digital Calendar-dl", "comando": "/calendar-dl", "funcionalidad": "Genera un calendario digital de contenido (RRSS, mails, web) con fechas de publicación, responsables y assets.", "archivos_requeridos": "Planificación de contenido en xlsx/csv o Google Sheet." },
        { "tipo": "tool", "nombre": "Cotización y seguimiento de proyectos Gantt-CMQ", "comando": "/gantt", "funcionalidad": "Genera un Gantt interactivo (HTML) a partir de un Excel para cotizar y hacer seguimiento de proyectos de draftLine.", "archivos_requeridos": "Excel con tareas, responsables, fechas inicio/fin y dependencias." }
      ]
    }
  ]
}
```

## HTML_TEMPLATE

Reemplazá `/* AREAS_PLACEHOLDER */` y `/* SKILLS_PLACEHOLDER */` con los arrays derivados de GLOSARIO_DATA y guardá el resultado como `glosario-skills.html`.

```html
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Glosario de Skills</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  :root {
    --bg: #0a0a0f;
    --bg-elev: #141420;
    --bg-elev-2: #1c1c2b;
    --border: #26263a;
    --border-strong: #363650;
    --text: #e8e8f0;
    --text-dim: #9797b0;
    --text-mute: #6b6b85;
  }
  html, body { height: 100%; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Inter", "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.5;
    min-height: 100vh;
    padding: 56px 32px 64px;
    position: relative;
    overflow-x: hidden;
  }
  body::before {
    content: "";
    position: fixed;
    inset: 0;
    background:
      radial-gradient(ellipse 800px 400px at 15% 0%, rgba(255, 107, 122, 0.08), transparent 60%),
      radial-gradient(ellipse 600px 400px at 85% 20%, rgba(94, 234, 212, 0.08), transparent 60%),
      radial-gradient(ellipse 700px 400px at 50% 90%, rgba(255, 184, 107, 0.06), transparent 60%);
    pointer-events: none;
    z-index: 0;
  }
  .container { max-width: 1320px; margin: 0 auto; position: relative; z-index: 1; }
  header {
    margin-bottom: 48px;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  h1 {
    font-size: 48px;
    font-weight: 700;
    letter-spacing: -1.4px;
    margin-bottom: 14px;
    background: linear-gradient(135deg, #ffffff 0%, #a0a0c0 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }
  .subtitle {
    color: var(--text-dim);
    font-size: 15px;
    margin-bottom: 32px;
    max-width: 580px;
  }
  .search-wrap {
    position: relative;
    width: 100%;
    max-width: 520px;
  }
  .search-icon {
    position: absolute;
    left: 18px;
    top: 50%;
    transform: translateY(-50%);
    color: var(--text-mute);
    pointer-events: none;
  }
  .search-box {
    width: 100%;
    padding: 14px 18px 14px 48px;
    font-size: 14px;
    border: 1px solid var(--border);
    border-radius: 12px;
    background: var(--bg-elev);
    color: var(--text);
    outline: none;
    transition: all 0.2s;
    font-family: inherit;
  }
  .search-box::placeholder { color: var(--text-mute); }
  .search-box:focus {
    border-color: var(--border-strong);
    background: var(--bg-elev-2);
    box-shadow: 0 0 0 4px rgba(255,255,255,0.03);
  }
  .filter-pills {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 16px;
    justify-content: center;
  }
  .pill {
    background: var(--bg-elev);
    border: 1px solid var(--border);
    color: var(--text-dim);
    font-size: 12.5px;
    font-weight: 500;
    padding: 7px 16px;
    border-radius: 999px;
    cursor: pointer;
    transition: all 0.15s;
    font-family: inherit;
    display: inline-flex;
    align-items: center;
    gap: 7px;
  }
  .pill:hover { background: var(--bg-elev-2); color: var(--text); border-color: var(--border-strong); }
  .pill .pill-dot { width: 7px; height: 7px; border-radius: 50%; background: var(--pill-color); box-shadow: 0 0 8px var(--pill-color); }
  .pill.active { background: var(--text); color: #0a0a0f; border-color: var(--text); font-weight: 600; }
  .pill.active .pill-dot { box-shadow: none; }
  .sections {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 32px;
    align-items: start;
    position: relative;
  }
  .sections::before {
    content: "";
    position: absolute;
    top: 0;
    bottom: 0;
    left: 50%;
    width: 3px;
    background: linear-gradient(180deg, transparent 0%, rgba(255,255,255,0.12) 15%, rgba(255,255,255,0.12) 85%, transparent 100%);
    transform: translateX(-50%);
    pointer-events: none;
    z-index: 1;
  }
  .section { position: relative; min-width: 0; }
  .section-header {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 22px;
    padding-bottom: 14px;
    border-bottom: 1px solid var(--border);
  }
  .section-icon {
    width: 38px; height: 38px; border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    background: var(--bg-elev-2); border: 1px solid var(--border); color: var(--text);
  }
  .section-title { font-size: 22px; font-weight: 700; letter-spacing: -0.3px; color: var(--text); }
  .section-sub { color: var(--text-mute); font-size: 12.5px; margin-top: 2px; }
  .section-count {
    margin-left: auto; font-size: 12px; font-weight: 600; color: var(--text-mute);
    background: var(--bg-elev); padding: 4px 11px; border-radius: 999px; border: 1px solid var(--border);
  }
  .skills-grid { display: flex; flex-direction: column; gap: 12px; }
  .skill-item {
    padding: 16px 18px; border-radius: 12px;
    background: var(--bg-elev); border: 1px solid var(--border);
    cursor: pointer; transition: all 0.2s ease; position: relative; overflow: hidden;
  }
  .skill-item::before {
    content: ""; position: absolute;
    left: 0; top: 50%; transform: translateY(-50%);
    width: 3px; height: 0;
    background: var(--area-color); border-radius: 0 2px 2px 0; transition: height 0.22s ease;
  }
  .skill-item:hover {
    background: var(--bg-elev-2); border-color: var(--border-strong);
    transform: translateY(-2px); box-shadow: 0 8px 24px rgba(0,0,0,0.25);
  }
  .skill-item:hover::before { height: 65%; }
  .skill-name { font-weight: 500; font-size: 14.5px; color: var(--text); margin-bottom: 10px; letter-spacing: -0.1px; line-height: 1.35; }
  .skill-cmd {
    font-family: "SF Mono", "JetBrains Mono", Monaco, "Courier New", monospace;
    font-size: 13px; color: var(--area-color); opacity: 0.9;
    background: rgba(255,255,255,0.03); padding: 3px 9px;
    border-radius: 6px; border: 1px solid var(--border);
    cursor: pointer; transition: all 0.15s; display: inline-block;
  }
  .skill-cmd:hover { background: rgba(255,255,255,0.08); border-color: var(--area-color); opacity: 1; }
  .skill-cmd:active { transform: scale(0.96); }
  .skill-cmd.copied { background: var(--area-color); color: #0a0a0f; border-color: var(--area-color); opacity: 1; }
  .section-empty {
    padding: 32px 20px; text-align: center; color: var(--text-mute); font-size: 13px;
    background: var(--bg-elev); border: 1px dashed var(--border); border-radius: 12px;
  }
  .no-results {
    grid-column: 1/-1; text-align: center; color: var(--text-mute);
    padding: 64px 16px; font-size: 14px;
    background: var(--bg-elev); border: 1px dashed var(--border); border-radius: 12px;
  }
  .modal-overlay {
    position: fixed; inset: 0; background: rgba(5,5,10,0.75);
    backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px);
    display: none; align-items: center; justify-content: center;
    padding: 24px; z-index: 100; animation: fadeIn 0.2s ease;
  }
  .modal-overlay.active { display: flex; }
  @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
  .modal {
    background: linear-gradient(180deg, #1a1a2a 0%, #141420 100%);
    border-radius: 18px; max-width: 620px; width: 100%; max-height: 85vh; overflow-y: auto;
    border: 1px solid var(--border-strong); position: relative;
    animation: slideUp 0.25s cubic-bezier(0.16, 1, 0.3, 1); box-shadow: 0 24px 60px rgba(0,0,0,0.6);
  }
  .modal::before {
    content: ""; position: absolute; top: 0; left: 0; right: 0; height: 3px;
    background: var(--modal-color, #666); box-shadow: 0 0 24px var(--modal-color, #666);
    border-radius: 18px 18px 0 0;
  }
  @keyframes slideUp {
    from { transform: translateY(20px) scale(0.98); opacity: 0; }
    to { transform: translateY(0) scale(1); opacity: 1; }
  }
  .modal-header {
    padding: 28px 32px 20px; border-bottom: 1px solid var(--border);
    display: flex; justify-content: space-between; align-items: flex-start; gap: 16px;
  }
  .modal-tags { display: flex; gap: 8px; margin-bottom: 10px; flex-wrap: wrap; }
  .modal-tag {
    display: inline-flex; align-items: center; gap: 6px;
    font-size: 10.5px; font-weight: 600; text-transform: uppercase; letter-spacing: 1.2px;
    padding: 4px 10px; border-radius: 999px; border: 1px solid var(--border); background: var(--bg-elev-2);
  }
  .modal-tag.area { color: var(--modal-color); }
  .modal-tag.area::before { content: ""; width: 6px; height: 6px; border-radius: 50%; background: var(--modal-color); box-shadow: 0 0 6px var(--modal-color); }
  .modal-tag.tipo { color: var(--text-dim); }
  .modal-title-row { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }
  .modal-title { font-size: 22px; font-weight: 600; color: var(--text); letter-spacing: -0.4px; line-height: 1.3; }
  .modal-cmd {
    font-family: "SF Mono", "JetBrains Mono", Monaco, "Courier New", monospace;
    background: var(--bg-elev-2); padding: 6px 12px; border-radius: 7px;
    color: var(--modal-color); font-weight: 500; font-size: 14px; border: 1px solid var(--border);
    cursor: pointer; transition: all 0.15s; display: inline-flex; align-items: center; gap: 8px;
  }
  .modal-cmd:hover { border-color: var(--modal-color); background: #22223a; }
  .modal-cmd:active { transform: scale(0.97); }
  .modal-cmd.copied { background: var(--modal-color); color: #0a0a0f; border-color: var(--modal-color); }
  .modal-cmd .copy-icon { opacity: 0.5; transition: opacity 0.15s; }
  .modal-cmd:hover .copy-icon { opacity: 1; }
  .modal-cmd.copied .copy-icon { opacity: 1; }
  .modal-close {
    background: var(--bg-elev-2); border: 1px solid var(--border);
    width: 34px; height: 34px; border-radius: 10px; cursor: pointer;
    font-size: 18px; color: var(--text-dim); flex-shrink: 0;
    display: flex; align-items: center; justify-content: center; transition: all 0.15s;
  }
  .modal-close:hover { background: #2a2a40; color: var(--text); border-color: var(--border-strong); }
  .modal-body { padding: 24px 32px 32px; }
  .field { margin-bottom: 22px; }
  .field:last-child { margin-bottom: 0; }
  .field-label { font-size: 10.5px; font-weight: 600; color: var(--text-mute); text-transform: uppercase; letter-spacing: 1.4px; margin-bottom: 8px; }
  .field-value { font-size: 14px; color: var(--text); line-height: 1.65; }
  .field-value.empty { color: var(--text-mute); font-style: italic; }
  .toast {
    position: fixed; bottom: 32px; left: 50%;
    transform: translateX(-50%) translateY(20px);
    background: var(--bg-elev-2); color: var(--text); border: 1px solid var(--border-strong);
    padding: 12px 20px; border-radius: 10px; font-size: 13.5px; font-weight: 500;
    display: flex; align-items: center; gap: 10px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.5); opacity: 0; pointer-events: none;
    transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1); z-index: 200;
  }
  .toast.show { opacity: 1; transform: translateX(-50%) translateY(0); }
  .toast .toast-icon {
    width: 18px; height: 18px; border-radius: 50%; background: #5eead4; color: #0a0a0f;
    display: flex; align-items: center; justify-content: center; flex-shrink: 0;
  }
  .toast code {
    font-family: "SF Mono", "JetBrains Mono", Monaco, "Courier New", monospace;
    font-size: 12.5px; color: var(--text-dim); background: var(--bg); padding: 1px 6px; border-radius: 4px;
  }
  ::-webkit-scrollbar { width: 10px; height: 10px; }
  ::-webkit-scrollbar-track { background: var(--bg); }
  ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 10px; border: 2px solid var(--bg); }
  ::-webkit-scrollbar-thumb:hover { background: var(--border-strong); }
  @media (max-width: 900px) { .sections { grid-template-columns: 1fr; gap: 40px; } .sections::before { display: none; } }
  @media (max-width: 640px) { body { padding: 36px 18px 48px; } h1 { font-size: 32px; } .modal-header, .modal-body { padding-left: 22px; padding-right: 22px; } }
</style>
</head>
<body>
<div class="container">
  <header>
    <h1>Glosario de Skills</h1>
    <p class="subtitle">Explorá las skills disponibles. Hacé click en cualquiera para ver su detalle completo.</p>
    <div class="search-wrap">
      <svg class="search-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
      <input type="text" class="search-box" id="search" placeholder="Buscar por nombre, comando o funcionalidad...">
    </div>
    <div class="filter-pills" id="filterPills"></div>
  </header>
  <div class="sections" id="sections"></div>
</div>
<div class="modal-overlay" id="modal">
  <div class="modal" id="modalContent">
    <div class="modal-header">
      <div>
        <div class="modal-tags">
          <span class="modal-tag area" id="mArea"></span>
          <span class="modal-tag tipo" id="mTipo"></span>
        </div>
        <div class="modal-title-row">
          <div class="modal-title" id="mTitle"></div>
          <span class="modal-cmd" id="mCmd" title="Click para copiar">
            <span id="mCmdText"></span>
            <svg class="copy-icon" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
          </span>
        </div>
      </div>
      <button class="modal-close" onclick="closeModal()" aria-label="Cerrar">×</button>
    </div>
    <div class="modal-body">
      <div class="field"><div class="field-label">Funcionalidad</div><div class="field-value" id="mFunc"></div></div>
      <div class="field"><div class="field-label">Archivos requeridos</div><div class="field-value" id="mFiles"></div></div>
    </div>
  </div>
</div>
<div class="toast" id="toast">
  <span class="toast-icon"><svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg></span>
  <span>Comando copiado: <code id="toastCmd"></code></span>
</div>
<script>
const AREAS = /* AREAS_PLACEHOLDER */;
const SKILLS = /* SKILLS_PLACEHOLDER */;

const SECTIONS = [
  { key:"tool", title:"Tools", subtitle:"Skills que generan assets, documentos o entregables", icon:'<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg>' },
  { key:"reporting", title:"Reporting", subtitle:"Skills que analizan datos y generan reportes/dashboards", icon:'<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>' }
];

const esc = s => (s == null ? "" : String(s).replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}[c])));
const areaColor = name => (AREAS.find(a => a.nombre === name) || {}).color || "#999";
let activeArea = null;

function renderPills() {
  const container = document.getElementById('filterPills');
  const pills = [`<button class="pill ${activeArea == null ? 'active' : ''}" data-area="">Todos</button>`]
    .concat(AREAS.map(a => `<button class="pill ${activeArea === a.nombre ? 'active' : ''}" style="--pill-color:${a.color}" data-area="${esc(a.nombre)}"><span class="pill-dot"></span>${esc(a.nombre)}</button>`));
  container.innerHTML = pills.join('');
  container.querySelectorAll('.pill').forEach(el => {
    el.addEventListener('click', () => {
      const name = el.getAttribute('data-area') || null;
      activeArea = (name && activeArea === name) ? null : name;
      update();
    });
  });
}

function render(query) {
  const container = document.getElementById('sections');
  const q = (query || '').trim().toLowerCase();
  const filtered = SKILLS.filter(s => {
    if (activeArea && s.area !== activeArea) return false;
    if (q && !(s.nombre.toLowerCase().includes(q) || s.comando.toLowerCase().includes(q) || (s.funcionalidad || '').toLowerCase().includes(q))) return false;
    return true;
  });
  if (filtered.length === 0) {
    container.innerHTML = '<div class="no-results">Sin resultados para esta búsqueda.</div>';
    return;
  }
  container.innerHTML = SECTIONS.map(sec => {
    const items = filtered.filter(s => s.tipo === sec.key);
    return `<section class="section">
      <div class="section-header">
        <div class="section-icon">${sec.icon}</div>
        <div><div class="section-title">${esc(sec.title)}</div><div class="section-sub">${esc(sec.subtitle)}</div></div>
        <span class="section-count">${items.length}</span>
      </div>
      ${items.length === 0
        ? '<div class="section-empty">Sin resultados en esta sección.</div>'
        : `<div class="skills-grid">${items.map(s => {
            const color = areaColor(s.area);
            return `<div class="skill-item" style="--area-color:${color}" data-skill='${JSON.stringify(s).replace(/'/g,"&#39;")}'>
              <div class="skill-name">${esc(s.nombre)}</div>
              <span class="skill-cmd" data-cmd="${esc(s.comando)}" title="Click para copiar">${esc(s.comando)}</span>
            </div>`;
          }).join('')}</div>`}
    </section>`;
  }).join('');
  document.querySelectorAll('.skill-item').forEach(el => {
    el.addEventListener('click', () => openModal(JSON.parse(el.getAttribute('data-skill').replace(/&#39;/g,"'"))));
  });
  document.querySelectorAll('.skill-cmd').forEach(el => {
    el.addEventListener('click', e => { e.stopPropagation(); copyCommand(el.getAttribute('data-cmd'), el); });
  });
}

function update() { renderPills(); render(document.getElementById('search').value); }

function openModal(s) {
  const color = areaColor(s.area);
  document.getElementById('modalContent').style.setProperty('--modal-color', color);
  const areaEl = document.getElementById('mArea');
  areaEl.textContent = s.area; areaEl.style.setProperty('--modal-color', color); areaEl.style.color = color;
  document.getElementById('mTipo').textContent = s.tipo === 'tool' ? 'Tool' : 'Reporting';
  document.getElementById('mTitle').textContent = s.nombre;
  document.getElementById('mCmdText').textContent = s.comando || '—';
  const cmdEl = document.getElementById('mCmd');
  cmdEl.classList.remove('copied'); cmdEl.style.color = color;
  cmdEl.onclick = e => { e.stopPropagation(); copyCommand(s.comando, cmdEl); };
  document.getElementById('mFunc').textContent = s.funcionalidad || '—';
  const files = document.getElementById('mFiles');
  files.textContent = s.archivos_requeridos || 'No requiere archivos';
  files.className = 'field-value' + (s.archivos_requeridos ? '' : ' empty');
  document.getElementById('modal').classList.add('active');
  document.body.style.overflow = 'hidden';
}

function closeModal() { document.getElementById('modal').classList.remove('active'); document.body.style.overflow = ''; }

let toastTimer = null;
function showToast(cmd) {
  const toast = document.getElementById('toast');
  document.getElementById('toastCmd').textContent = cmd;
  toast.classList.add('show'); clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove('show'), 1800);
}

function copyCommand(cmd, el) {
  if (!cmd) return;
  const done = () => { el.classList.add('copied'); showToast(cmd); setTimeout(() => el.classList.remove('copied'), 1200); };
  if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(cmd).then(done).catch(() => fallbackCopy(cmd, done));
  else fallbackCopy(cmd, done);
}

function fallbackCopy(text, cb) {
  const ta = document.createElement('textarea');
  ta.value = text; ta.style.position = 'fixed'; ta.style.opacity = '0';
  document.body.appendChild(ta); ta.select();
  try { document.execCommand('copy'); cb(); } catch(e) {}
  document.body.removeChild(ta);
}

document.getElementById('modal').addEventListener('click', e => { if (e.target.id === 'modal') closeModal(); });
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') {
    if (document.getElementById('modal').classList.contains('active')) closeModal();
    else if (activeArea) { activeArea = null; update(); }
  }
});
document.getElementById('search').addEventListener('input', () => update());
update();
</script>
</body>
</html>
```
