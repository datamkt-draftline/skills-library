---
name: design-survey
description: Diseña una encuesta completa de consumidores a partir de marca, objetivo y vertical. Hace entrevista guiada, propone preguntas obligatorias y bloques recomendados según el "kit" (8 verticales estandarizadas), y muestra learnings de las 45 encuestas de referencia. Invocar cuando el usuario pida crear, armar, diseñar o redactar una encuesta.
action: true
---

# Design Survey — Skill guiada

Esta skill construye una encuesta completa siguiendo el estándar identificado en los findings de 45 archivos de resultados de encuestas ABI (Guía Agile). El output final es un documento con el cuestionario listo para subir a Agile/Braze, estructurado en 3 secciones: **demográficos obligatorios → bloque core del kit → cierre legal**.

El flujo es conversacional: **preguntar primero, generar después**. No generes la encuesta hasta tener claros marca, objetivo y vertical.

---

## Paso 0 — Reconocer la invocación

Activate cuando el usuario diga cosas como "quiero armar una encuesta", "necesito redactar un cuestionario", "ayudame a diseñar una survey para [marca]", "/design-survey", etc.

Si el usuario invoca la skill sin contexto, respondé con un saludo corto y pasá al Paso 1.

---

## Paso 1 — Entrevista inicial (obligatoria)

Hacé estas 3 preguntas al usuario **antes de proponer ninguna pregunta de encuesta**. Usá `AskUserQuestion` si son varias o preguntás en bloque; respetá las respuestas tal como las dé el usuario.

### 1.1. Marca

> ¿Para qué marca es la encuesta?

Ejemplos válidos: Stella Artois, Quilmes, Corona, Brahma, Patagonia, Andes, Michelob, Flying Fish, Viajero, Corona Cero, Quilmes Sin Alcohol, 1890, Michelob Gluten Free, etc. Si el usuario dice una marca que no existe en los findings, aceptala igual y aplicá el kit que mejor encaje por vertical.

### 1.2. Objetivo / Vertical

> ¿Cuál es el objetivo principal de la encuesta?

Mostrá al usuario los 8 "kits" estandarizados (ver Paso 2) y pedile que elija uno (o combinación). Si no sabe, inferilo de la marca + contexto que te dio y confirmá antes de avanzar.

### 1.3. Canal y contexto

> ¿Cómo se va a tomar la encuesta? (sampling en vivo, post‑evento, email/CRM, QR en PDV, Braze push, etc.) ¿Hay sorteo o beneficio por completarla?

Esto define:
- **Largo**: sampling en vivo → 4–6 preguntas (Flying Fish, Rugby NEA SA). Post‑evento CRM → 10–15 preguntas (Corona Sunset, Andes Q3).
- **Pregunta de email**: solo se incluye si hay sorteo/regalo.
- **Tono**: "vos/tenés" (canon Agile) vs "usted/tiene" (solo AO ORO PDVS). Default = voseo.

### 1.4. Extras opcionales

Preguntá si querés sumarlos solo si aplica:
- ¿Hay producto nuevo a probar? (define si va "¿Conocías [marca]?")
- ¿Mide shift actitudinal antes/después? (solo Corona Sunset lo hace)
- ¿Necesita enriquecimiento Clearbit/B2O? (define si pedís email corporativo)

---

## Paso 2 — Mapear vertical → kit de preguntas

Los 8 kits identificados en los findings. Cada uno tiene sus preguntas‑core:

| Kit | Preguntas‑core | Ejemplos de encuestas de referencia |
|---|---|---|
| **Sampling / degustación** | Overall Liking (1–9) + Intención de compra + Motivos (sí/no) + Ocasiones | Flying Fish, Brahma Mezcla, Viajero, Andes Oro, 27 Eazy |
| **Producto Sin Alcohol** | ¿Conocías? + Overall Liking (1–5) + Intención + Bloque Ocasiones SA | Stella SA, Quilmes SA, Corona Cero |
| **Experiencias / Eventos** | Overall Liking (1–9) + NPS + Opinión antes/después + Atributos de marca | Corona Sunset Q1/Q2/Q4, Quilmes Rock, Patagonia Lockers, Andes Q3 |
| **Pricing / beneficios** | Relevancia + Adecuación + Elección entre alternativas + Motivos | Brahma Precio, Brahma Beneficio Q1, Retornable, Brahma 2000 & Chapitas |
| **Envase / formato** | Preferencia de envase + Intención por envase + Atributos funcionales | Patagonia Latón vs Porrón, Corona Lata vs Porrón |
| **Naming / diseño** | Elección entre nombres + Motivo + Adecuación nombre‑líquido + Reconocimiento | 1890, Brahma Latita SED |
| **Música / asociación de marca** | Adecuación marca‑género (1–5) + Preferencia de género + Intención | Respuestas Música, Quilmes Rock Cervezas |
| **Boliches / contexto de consumo** | Frecuencia + Marca asociada + Formato preferido + Atributos marca + Intención | Boliches, Stella Boliches CRM, Rugby, Tennis |

---

## Paso 3 — Proponer la encuesta en 3 bloques

Siempre devolvé la encuesta propuesta al usuario con esta estructura. Marcá claramente cada bloque.

### Bloque A — PREGUNTAS OBLIGATORIAS (se repiten en ~90% de las encuestas)

Estas tres + cierre legal son **no negociables**. Siempre inclúyelas salvo que el usuario diga explícitamente que no.

1. **Filtro etario** (canon exacto):
   > ¿Tenés más de 18 años? (Sí / No) → si No, cerrar encuesta.

2. **Edad**. Ofrecer **3 variantes de wording** (dejar que el usuario elija):
   - a) `¿Qué edad tenés?` — **recomendada** (canon Agile, mayoritario)
   - b) `Edad` o `Fecha de nacimiento` — útil si después derivás rango etario (Viajero, Andes Q3, Quilmes Rock, Quilmes SA Canchas)
   - c) `¿Qué edad tiene?` (usted) — solo si todo el cuestionario va en usted. **Desaconsejado** salvo réplica de AO ORO PDVS.

3. **Género**. Variantes:
   - a) `¿Con qué género te autopercibís?` — **recomendada** (canon Agile)
   - b) `Género` — solo si ya hay constraint de largo (Stella PureGold)
   - c) `¿Con qué género se autopercibe?` — usted, consistente con 2.c

4. **Email** (opcional, solo si hay sorteo/regalo):
   > `Dejános tu email para contactarte en caso de que salgas ganador.`

### Bloque B — PREGUNTAS RECOMENDADAS POR KIT

Según el kit elegido en el Paso 1, proponé las preguntas‑core del kit **con variantes de formato**. El patrón es: por cada pregunta, mostrar 2–3 opciones de wording/escala y que el usuario elija.

Los tipos de pregunta de la Guía Agile y sus wordings típicos:

| Tipo Agile | Escala | Wording recomendado |
|---|---|---|
| Overall Liking (1 a 9) | 1–9 | `"Del 1 al 9, ¿cuánto dirías que te gustó [experiencia / producto]?"` |
| Overall Liking TaDa (1 a 5) | 1–5 | `"Del 1 al 5, ¿cuánto te agradó [marca]?"` |
| Overall Liking Sin Alcohol | 1–5 | `"¿Cuánto dirías que te agrada o desagrada [marca] Sin Alcohol?"` |
| NPS | 0–10 | `"¿Qué tan probable es que recomiendes [experiencia / marca] a un amigo?"` |
| Intención de compra | 1–5 | `"¿Cuál de estas frases reflejaría mejor la probabilidad de que compres [marca]?"` (opciones: Definitivamente la compraría / Probablemente la compraría / No estoy seguro / Probablemente no la compraría / Definitivamente no la compraría) |
| Adecuación | 1–5 | `"¿Qué tan adecuado te parece que [marca] [acción]?"` |
| Relevancia | 1–5 | `"¿Qué tan relevante te parece el beneficio de [X]?"` |
| Valoración | 1–5 | Uso marginal — no recomendar salvo caso específico (Michelob GF) |

### Bloque C — MÓDULOS REUTILIZABLES (copia literal entre encuestas)

Si el kit lo pide, inyectá uno de estos módulos **tal cual** (son plantillas verificadas que se copian entre proyectos):

#### C.1 — Bloque "Ocasiones Sin Alcohol" (para kit Producto Sin Alcohol)
> ¿En qué ocasiones tomarías [marca] Sin Alcohol?
> - Mismas situaciones que cerveza con alcohol
> - Cuando tengo que manejar
> - Cuando no puedo tomar alcohol por razones médicas (embarazo, antibióticos, etc.)
> - Cuando busco no consumir alcohol
> - Nunca

#### C.2 — Batería "Stella Boliches/Rugby" (para kit Boliches / Rugby / Tennis con Stella)
> ¿Qué tanto te identificás con estas frases? (escala 1–5)
> - Es ideal para compartir con amigos
> - Me gusta que me vean tomando Stella Artois
> - Es la favorita para juntadas, fiestas o boliche
> - Es una marca joven y canchera

#### C.3 — Batería "Experiencia" (para kit Experiencias / Eventos)
> Después de [evento], pensás que [marca]… (escala 1–5)
> - Me hace querer más a [marca]
> - Me hace pensar que [marca] es una marca para alguien como yo
> - Me da lo que busco
> - Es diferente a otras
> - Me dio ganas de comprar más seguido

#### C.4 — Batería "Atributos de envase" (para kit Envase / formato)
> Por cada envase evaluado (lata vs porrón vs retornable), marcá qué tan de acuerdo estás: (escala 1–5)
> - Es la medida justa
> - Es fácil de llevar
> - Conserva mejor el frío
> - Se ve mejor al servirlo
> - Buena relación precio‑calidad
> - Genera menos residuos
> - Sirve para compartir
> - Mantiene mejor el gas

#### C.5 — Shift actitudinal antes/después (solo si el usuario lo pidió explícitamente)
> - ¿Qué pensabas de la marca [X] antes de asistir al evento?
> - ¿Tu opinión sobre la marca [X] cambió? (Sí, mejoró / No cambió / Sí, empeoró)

### Bloque D — CIERRE LEGAL (obligatorio, final de la encuesta)

> ¡Estás a un paso de finalizar! He leído y acepto Términos y Condiciones, Políticas de Privacidad y activaciones de Marketing.

---

## Paso 4 — Preguntas abiertas (uso restringido)

Solo hay 2 abiertas que se repiten entre encuestas en los findings — proponelas únicamente si encajan:
- `¿Probaste otras marcas de cerveza sin alcohol disponibles en Argentina?` → solo familia Sin Alcohol.
- `¿Qué te gustaría que [marca] proponga para que te sientas más cerca de la marca?` → Rugby / Stella.

Por defecto, mantené todo cerrado o semi‑abierto con un campo "Otro".

---

## Paso 5 — Reglas de formato Multi‑choice

**Importante** (afecta la bajada de datos): en Agile, cada opción de una pregunta multi‑choice ocupa **su propia columna** con el texto literal de la opción. Avisá al usuario si una pregunta de 8+ opciones multi‑choice puede inflar la bajada (ej. Rugby tiene 74 columnas de las cuales ~8 son preguntas reales).

Recomendación: para baterías de atributos, usar escala Likert por fila (no multi‑choice) para mantener el ancho controlado.

---

## Paso 6 — Chequeos de consistencia antes de entregar

Antes de darle la encuesta final al usuario, validá:

- [ ] Filtro etario 18+ al inicio.
- [ ] Demográficos (edad + género) presentes.
- [ ] Tono consistente (todo en voseo o todo en usted, no mezclar).
- [ ] Si es Sin Alcohol → bloque C.1 Ocasiones SA incluido.
- [ ] Si es Evento → NPS + C.3 Experiencia.
- [ ] Email solo si hay sorteo.
- [ ] Cierre legal al final.
- [ ] Largo coherente con canal (sampling en vivo ≤ 6 preguntas sustantivas).
- [ ] No mezcles formatos para la misma métrica entre canales.

---

## Paso 7 — Entregar la encuesta recomendada

Devolvé la encuesta final al usuario en formato numerado, por bloques (A / B / C / D). Incluí:

- El tipo Agile de cada pregunta entre paréntesis (ej. "P3. [Overall Liking 1–9] ...").
- La escala explícita.
- Las variantes de wording que elegiste y por qué.
- Un mini resumen al final: "Encuesta de [N] preguntas sustantivas, kit [X], canal [Y], largo estimado [Z] min."

Si el usuario pide exportable (.docx, .xlsx, .json), generalo con las convenciones habituales del entorno. Si no lo pide, entregá en markdown dentro del chat.

---

## Paso 8 — Sección "Estudios Previos" (obligatoria, va **debajo** de la encuesta entregada)

Después de la encuesta recomendada, **siempre** agregá esta sección.

### 8.1 — Elegir qué encuestas mostrar

Leé `references/surveys_catalog.md` (catálogo embebido en la skill con los 45 archivos de referencia). Filtrá las entradas que apliquen según:

1. **Kit/vertical** elegido en el Paso 1 (match primario).
2. **Marca** o marca análoga (match secundario).
3. **Canal** similar.

Mostrá entre **3 y 8 estudios previos**. Si hay más candidatos, priorizá por match de marca > kit > canal. Si hay menos de 3 en el kit exacto, ampliá a kits adyacentes y aclaralo.

### 8.2 — Formato de la sección

```
## Estudios Previos

Estas encuestas de referencia fueron las que más aportaron a las recomendaciones de arriba:

1. **[Nombre del archivo]** — [Marca] — [kit] — [canal]. [1 línea con lo relevante que aportó].
2. **[Nombre del archivo]** — [Marca] — [kit] — [canal]. [1 línea con lo relevante que aportó].
...

¿Querés que te cuente los learnings/resultados de alguna de estas? Decime el nombre (o el número) y la analizo.
```

### 8.3 — Esperar respuesta del usuario

Después de listar, **parate ahí**. No analices nada hasta que el usuario pida un análisis específico.

---

## Paso 9 — Analizar una encuesta previa (cuando el usuario pida learnings)

Si el usuario pide "contame los learnings de [X]" / "qué pasó en [X]" / "resultados de la encuesta [X]":

### 9.1 — Resolver el archivo

Buscá el archivo en `references/surveys/[nombre exacto del catálogo]`. Si el usuario dio un nombre parcial o un número, resolvé contra la lista que acabás de mostrar. Si hay ambigüedad, preguntá cuál.

### 9.2 — Leer el XLSX con Python puro

Usá `zipfile` + `xml.etree.ElementTree`, sin dependencias externas. Patrón recomendado:

```python
import zipfile, xml.etree.ElementTree as ET

NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"

def parse_xlsx(path):
    with zipfile.ZipFile(path) as z:
        ss = []
        try:
            with z.open("xl/sharedStrings.xml") as f:
                root = ET.parse(f).getroot()
                for si in root.findall(f"{{{NS}}}si"):
                    text = "".join(t.text or "" for t in si.iter(f"{{{NS}}}t"))
                    ss.append(text)
        except KeyError:
            pass
        sheets = [n for n in z.namelist() if n.startswith("xl/worksheets/sheet")]
        sheets.sort()
        with z.open(sheets[0]) as f:
            root = ET.parse(f).getroot()
        rows = []
        for row in root.find(f"{{{NS}}}sheetData").findall(f"{{{NS}}}row"):
            cells = {}
            for c in row.findall(f"{{{NS}}}c"):
                ref = c.get("r"); t = c.get("t",""); v = c.find(f"{{{NS}}}v")
                val = v.text if v is not None else None
                if val is not None and t == "s":
                    val = ss[int(val)]
                col = "".join(ch for ch in ref if ch.isalpha())
                cells[col] = val
            rows.append(cells)
        return rows
```

### 9.3 — Extraer insights

Para cada encuesta:

1. **Identificar columnas de preguntas** (primera fila = headers). Ignorar columnas de metadatos (ID, timestamp, email, enriquecimiento Clearbit).
2. **Contar respuestas por pregunta** (N válidos).
3. **Para escalas Likert (1–5, 1–9, 0–10)**: calcular promedio, distribución por valor, % top‑2‑box y % bottom‑2‑box.
4. **Para multi‑choice**: contar frecuencia por opción, calcular % sobre total de respuestas válidas.
5. **Para demográficos**: distribución por género y rango etario.
6. **Para preguntas abiertas**: listar las respuestas más frecuentes (top 5) o una muestra representativa si son pocas.

### 9.4 — Presentar los learnings

Formato:

```
## Learnings: [Nombre del archivo]

**Resumen**: [1 línea — marca, kit, N respuestas, canal].

**Demográficos**
- Edad promedio / rango dominante: ...
- Mix de género: ...

**Métricas core del kit** ([tipo Agile de pregunta])
- [Pregunta]: promedio X.X / N, top‑2‑box Y%, bottom‑2‑box Z%.
- ...

**Hallazgos destacados**
- [Lo que sorprendió].
- ...

**Implicancia para la encuesta nueva**
- [Conexión concreta con las recomendaciones del Paso 3].
```

Mantené el análisis en 150–300 palabras. Si el usuario pide más profundidad, expandí.

### 9.5 — Dejar la puerta abierta

Al final del análisis, ofrecé: "¿Querés que analice otra, o que compare dos?".

---

## Paso 10 — Qué sigue después del diseño

Una vez entregada la encuesta:

- **Si el usuario quiere crearla en Typeform**: pasale la especificación completa a `create-survey`. Incluí preguntas, tipos, opciones, escalas, lógica y tono.
- **Si el usuario quiere analizar resultados desde un xlsx existente**: derivalo a `analyze-survey` con el archivo.
- **Si quiere hacer todo**: el flujo natural es primero `create-survey` y después, cuando tenga respuestas, `analyze-survey`.

No ejecutes nada de Typeform ni generación de dashboards vos mismo: eso lo hacen las otras skills.

---

## Referencia rápida — Longitud típica por kit

- **Sampling en vivo**: 4–6 preguntas sustantivas (Flying Fish, Rugby NEA SA).
- **Producto Sin Alcohol CRM**: 7–10 preguntas.
- **Evento / Experiencia post‑asistencia**: 10–15 preguntas.
- **Pricing / Beneficios (comparación 4 alternativas)**: 15–20 preguntas.
- **Música / asociación género‑marca**: hasta 17 ítems de adecuación.
- **Envase con atributos por envase**: 12–18 preguntas.

---

## Archivos y rutas de la skill

- `SKILL.md` — este archivo.
- `references/surveys_catalog.md` — catálogo con metadata de las 45 encuestas.
- `references/surveys/*.xlsx` — las 45 encuestas listas para analizar.
