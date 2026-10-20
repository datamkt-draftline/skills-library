---
name: Influencer Audience Report
description: Genera una presentación PPTX editable con audience intelligence de uno o más influencers (biografía, partnerships, demographics, follower history) a partir de datos de CreatorIQ. Se activa cuando el usuario pide un reporte, deck o presentación de un creator o lista de creators.
action: true
---

Sos un asistente que arma reportes de audience intelligence para influencers en formato PPTX editable. Combinás datos cuantitativos de CreatorIQ con investigación web (biografía + partnerships recientes).

## Qué entrega la skill

Un archivo `.pptx` con:
- **Cover slide** — logo + nombre del creator + "Who Is" (bio ~40-80 palabras en español) + partnerships verificados recientes.
- **Un slide por red social** (Instagram, TikTok, Twitter, Facebook, etc.) con:
  - Followers actuales + verificación + engagement rate + avg likes/comments
  - Evolución de followers (último semestre)
  - Demographics agregados: género, edades, país, ciudad, estado (USA), etnicidad
  - Top intereses y afinidad de marcas
  - Audience credibility (si está disponible)
  - Sección "Puntos a discutir" cuando hay señales (ej: engagement 0, audiencia en descenso, baja credibilidad)

## Archivos que vienen con la skill

```
.claude/skills/influencer-audience/
├── SKILL.md                       # este archivo
├── config.json                    # api_key + base_url
├── package.json                   # dependencias node
├── pptx_report_generator.js       # generador canónico
├── creatoriq-logo.png             # logo (top-left del deck)
├── warning(1).png                 # icono para "Puntos a discutir"
└── scripts/
    ├── fetch_creator.py           # wrapper del MCP /api/creator (full data)
    └── fetch_audience.py          # legacy: sólo demographics agregados
```

## Prerequisito: dependencias Node

Antes del primer uso en el entorno, instalá dependencias **adentro del folder de la skill** (donde está el .js):

```bash
cd .claude/skills/influencer-audience && npm install
```

Esto crea `.claude/skills/influencer-audience/node_modules/` con `pptxgenjs`, `jszip` y `sharp`. Si ya existe `node_modules/` en esa ruta, no lo reinstales.

## Parseo de input del usuario

El usuario te va a pasar uno o más handles / nombres / URLs. Normalizalos a `(handle, network)`.

| Input | handle | network |
|---|---|---|
| `@zaira.nara` | zaira.nara | instagram (default) |
| `luquitarodrigue tiktok` | luquitarodrigue | tiktok |
| `https://www.instagram.com/therock/` | therock | instagram |
| `https://www.tiktok.com/@khaby.lame` | khaby.lame | tiktok |
| `publisherId: 4079237` | — | pasar el id a `--publisher-id` (si lo soportás) |

Aliases: `ig`→instagram, `tt`→tiktok, `yt`→youtube, `fb`→facebook, `x`→twitter. Default si falta la red: `instagram`.

Si el usuario te pasa varios en una sola frase (ej: "zaira.nara y luquitarodrigue"), procesá cada uno y generá **un deck por creator** (o un único deck multi-creator si lo pide explícitamente; el generador soporta `creators[]` con N elementos).

## Workflow (por cada creator)

### Paso 1 — Fetch de datos cuantitativos

```bash
python3 .claude/skills/influencer-audience/scripts/fetch_creator.py \
  --handle HANDLE \
  --network NETWORK \
  --out /tmp/creator_HANDLE.json
```

- Devuelve el payload completo del MCP: publisherId, lookup, networks[] (una entrada por red con audience + history de 6 meses).
- La **última línea de stdout** es el JSON (podés parsearlo directamente).
- Si `success: false`, mostrá el error al usuario y pedí aclaración.

### Paso 2 — Investigación web (biografía + partnerships)

Usá `mcp__tas__web_search`:

1. **Who Is** — búsqueda tipo `"<nombre completo> biografía"` o `"<nombre> wikipedia"`. Redactá un párrafo en **español** de 40-80 palabras con: nombre completo, fecha/lugar de nacimiento si disponibles, carrera, logros destacados.
2. **Partnerships recientes** — búsquedas `"<nombre> campaña <marca o año>"` o `"<nombre> embajador marca"`. Confirmá al menos 2 colaboraciones verificables de los últimos 2 años, cada una con URL fuente real.

Reglas:
- No inventes partnerships. Si no encontrás ninguno verificable, dejá el array vacío.
- Incluí fuentes en el campo `source` (URL real que verificaste).
- `date` como año o `YYYY-MM`.

### Paso 3 — Construir `report-data.json`

Mapeá los datos a este schema. Guardalo en el working directory actual del usuario (no dentro del folder de la skill):

```json
{
  "title": "Influencer Audience Report",
  "subtitle": "Audience intelligence",
  "generatedAt": "<ISO 8601 ahora>",
  "creators": [
    {
      "publisherId": "<del fetch>",
      "name": "<del fetch — limpiá doble espacio>",
      "inputInstagramHandle": "<handle original>",
      "whoIs": "<párrafo español 40-80 palabras>",
      "recentPartnerships": [
        { "brand": "...", "description": "...", "source": "https://...", "date": "2026" }
      ],
      "networks": [ /* copiar networks[] del fetch tal cual */ ]
    }
  ]
}
```

**Normalizaciones importantes antes de guardar:**

- Si `avgLikesPerPost`, `avgCommentsPerPost`, `avgViewsPerPost` o `engagementRate` vienen como `0.0` en una cuenta con muchos followers, convertí a `null` (son valores dormidos/falsos cero del provider).
- Dejá `audience: null` tal cual cuando no hay demographics (ej: Twitter, Facebook).
- Dejá `history.points` con los 6 meses que vinieron.

### Paso 4 — Ejecutar el generador

**Pedí aprobación con AskUserQuestion sólo si el workflow lo requiere.** El generador no es `tdx`, así que no necesita aprobación especial — ejecutalo directamente:

```bash
node .claude/skills/influencer-audience/pptx_report_generator.js \
  <path-a-report-data.json> \
  <output-pptx>
```

Convención de nombre de salida: `<handle-slug>-audience-report-YYYY-MM-DD.pptx` en el working directory del usuario.

El generador imprime un JSON con `success`, `outputPath`, `slideCount`, `networkSlideCount`.

### Paso 5 — Entregar el archivo

```
mcp__tas__open_file  path=<output-pptx>
```

Después, en el texto de respuesta, resumí al usuario:
- Followers totales por red
- Señales relevantes (crecimiento/decrecimiento, engagement alto/bajo, mix de audiencia)
- Partnerships encontrados

## Multi-creator en un solo deck

Si el usuario pide "un deck con A, B y C", agregá los 3 objetos al array `creators[]` del mismo `report-data.json`. El generador crea cover separado y bloques de slides por creator.

## Errores comunes

| Síntoma | Causa / fix |
|---|---|
| `Cannot find module 'pptxgenjs'` | Falta `npm install` dentro del folder de la skill. |
| `success: false, code: HTTP_404` | El handle no existe en CreatorIQ. Verificar typo o pedir otro. |
| `code: HTTP_0` | DNS / sin red. El entorno probablemente no tiene acceso externo. |
| Deck sin logo | El .png de logo no está junto al .js. Comprobá que `creatoriq-logo.png` esté en la carpeta de la skill. |
| Mojibake (`Ã³`, `â€"`) en el deck | El `report-data.json` se guardó con encoding erróneo. Guardalo siempre en UTF-8. |
| `removedDanglingContentTypeOverrides` en el output | No es error — es una autorepración del zip del generador. Ignorar. |

## Notas sobre audience data

- CreatorIQ expone demographics **agregados**, no por follower individual.
- `country` / `location` = ubicación geográfica, **no** ciudadanía ni nacionalidad.
- `audienceCredibility` es un score 0-100: valores < 70 ameritan señalarse como "revisar" en Puntos a discutir.
- No todos los networks exponen audience — Twitter/Facebook suelen venir con `audience: null`.
