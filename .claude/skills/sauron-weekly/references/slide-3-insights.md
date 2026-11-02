# Instrucciones detalladas — Slide 3: Formatos exactos, history_snapshot y publicación

## 3D — Formato EXACTO de `dashboard_data`

Antes de publicar, verificá que `dashboard_data` respete exactamente esta estructura y no contenga propiedades adicionales:

```json
{
  "schema_version": 3,
  "methodology_version": "VALOR_DEVUELTO_POR_GET_THIRD_SLIDE_HISTORY",
  "period": {
    "period_id": "PERIOD_ID_DE_GET_X_POSTS",
    "from_date": "YYYY-MM-DD",
    "to_date": "YYYY-MM-DD",
    "days": 7
  },
  "trend_status": {
    "emerging": [
      {
        "topic_id": "snake_case_ascii",
        "title": "Título explicativo",
        "summary": "Explicación detallada de la señal y su relevancia.",
        "current_value": 0,
        "historical_value": null,
        "source_support": ["x", "news"]
      }
    ],
    "persistent": [],
    "declining": []
  },
  "market_radar": {
    "brand": [
      {
        "entity": "Entidad",
        "headline": "Territorio o passion point",
        "summary": "Explicación detallada del territorio y su oportunidad.",
        "asset_key": null
      }
    ],
    "category": [],
    "competition": [],
    "takeaway": "Conclusión transversal y accionable"
  }
}
```

### Reglas estrictas de `dashboard_data`

A nivel superior debe contener SOLAMENTE:

- `schema_version`
- `methodology_version`
- `period`
- `trend_status`
- `market_radar`

NO incluyas:

- `cultural_radar`
- `pillar_comparison`
- `generated_at`
- `citations`
- `evidence`
- `discovery`
- `cost`
- `x_search_calls`
- `history_snapshot`
- `period_id` a nivel superior
- `from_date` a nivel superior
- `to_date` a nivel superior
- ninguna otra propiedad auxiliar.

`period` debe contener SOLAMENTE:

- `period_id`
- `from_date`
- `to_date`
- `days`

Usá como `period_id` el valor devuelto por `get_x_posts`. No inventes un identificador diferente.

Cada item de `trend_status` debe contener SOLAMENTE:

- `topic_id`
- `title`
- `summary`
- `current_value`
- `historical_value`
- `source_support`

Cada item de `market_radar.brand`, `market_radar.category` y `market_radar.competition` debe contener SOLAMENTE:

- `entity`
- `headline`
- `summary`
- `asset_key`

`market_radar` debe contener SOLAMENTE:

- `brand`
- `category`
- `competition`
- `takeaway`

`source_support` sólo puede contener `"x"` y/o `"news"`.

Todos los `topic_id` deben usar snake\_case ASCII y ser estables entre períodos cuando el concepto sea semánticamente equivalente.

## 3E — Construcción del `history_snapshot`

Construí `history_snapshot` para el MISMO período que `dashboard_data`.

`history_snapshot` NO representa todo el histórico. Es solamente el snapshot del período actual que el backend mergeará con `third_slide_history.json`.

El agente NO debe reescribir manualmente los períodos anteriores. El backend preservará el histórico existente y agregará o reemplazará únicamente el punto correspondiente al mismo `period_id`.

### Qué incluir en `topics`

Incluí prioritariamente todos los conceptos utilizados en `trend_status` y cualquier otra señal actual que realmente merezca seguimiento longitudinal.

- Evitá duplicar un mismo concepto: un `topic_id` debe aparecer una sola vez dentro del snapshot.
- Si un concepto actual equivale a uno histórico, reutilizá el `topic_id` existente.
- Conservá o ampliá aliases útiles.
- No guardes todos los hallazgos posibles solamente porque fueron mencionados; almacená conceptos que realmente merecen seguimiento.

Para cada concepto:

- `x_volume`: volumen observado directamente asociado al concepto, si existe; de lo contrario `null`.
- `x_engagement`: engagement observado directamente asociado al concepto, si existe; de lo contrario `null`.
- `x_views`: views observadas directamente asociado al concepto, si existe; de lo contrario `null`.
- `news_articles`: cantidad de noticias SELECCIONADAS del período que respaldan directamente esa señal.

No transformes una métrica desconocida en cero. Usá `null` para métricas X desconocidas.

No sumes posts de X con artículos. Se almacenan en campos diferentes.

### Qué incluir en `pillars`

Aunque el bloque visible `7 días vs. histórico` fue retirado, mantené el histórico de pilares para preservar continuidad de datos y permitir análisis futuros sin tener que reconstruir períodos pasados.

Incluí cada pilar para el que exista información válida del período.

Para cada pilar:

- `x_volume` = `observed_metrics.volume_observed` de `get_x_posts`.
- `x_engagement` = `observed_metrics.engagement_observed` cuando esté disponible.
- `x_views` = `observed_metrics.views_observed` cuando esté disponible.
- `news_articles` = cantidad de noticias seleccionadas en el PASO 1 cuyo pilar final sea ese pilar.

Cuando `get_x_posts` haya sido válido para los siete pilares, el snapshot debe incluir los siete.

## 3F — Formato EXACTO de `history_snapshot`

`history_snapshot` debe contener EXACTAMENTE estas cuatro propiedades de nivel superior:

- `methodology_version`
- `period`
- `topics`
- `pillars`

NO incluyas a nivel superior:

- `schema_version`
- `generated_at`
- `period_id`
- `from_date`
- `to_date`
- ninguna otra propiedad.

`days` debe existir EXCLUSIVAMENTE dentro de `history_snapshot.period`.

`period_id`, `from_date` y `to_date` deben existir:

- dentro de `history_snapshot.period`; y
- dentro de cada `topics[].point` y `pillars[].point`, exactamente como exige el schema.

PROHIBIDO incluir `days` dentro de cualquier `topics[].point` o `pillars[].point`.

### Schema estricto de cada `point`

Cada objeto `topics[].point` y `pillars[].point` debe contener SOLAMENTE estas siete propiedades:

- `period_id`
- `from_date`
- `to_date`
- `x_volume`
- `x_engagement`
- `x_views`
- `news_articles`

No puede contener ninguna otra propiedad.

En particular, `days` está PROHIBIDO dentro de cualquier `point`.

La presencia de `days` dentro de un `point` invalida el payload aunque su valor sea `7`.

Formato obligatorio:

```json
{
  "methodology_version": "MISMO_VALOR_TECNICO_QUE_DASHBOARD_DATA",
  "period": {
    "period_id": "MISMO_PERIOD_ID_QUE_DASHBOARD_DATA",
    "from_date": "YYYY-MM-DD",
    "to_date": "YYYY-MM-DD",
    "days": 7
  },
  "topics": [
    {
      "topic_id": "snake_case_ascii",
      "label": "Nombre visible",
      "aliases": [
        "Alias útil si corresponde"
      ],
      "point": {
        "period_id": "MISMO_PERIOD_ID",
        "from_date": "MISMA_FROM_DATE",
        "to_date": "MISMA_TO_DATE",
        "x_volume": null,
        "x_engagement": null,
        "x_views": null,
        "news_articles": 0
      }
    }
  ],
  "pillars": [
    {
      "pillar": "Wellness",
      "point": {
        "period_id": "MISMO_PERIOD_ID",
        "from_date": "MISMA_FROM_DATE",
        "to_date": "MISMA_TO_DATE",
        "x_volume": 0,
        "x_engagement": 0,
        "x_views": 0,
        "news_articles": 0
      }
    }
  ]
}
```

### Reglas estrictas de `history_snapshot`

Antes de publicar, verificá explícitamente:

1. El nivel superior contiene únicamente `methodology_version`, `period`, `topics` y `pillars`.
2. NO existe `schema_version` dentro de `history_snapshot`.
3. NO existe `generated_at` dentro de `history_snapshot`.
4. `period_id`, `from_date` y `to_date` NO están duplicados en el nivel superior.
5. `dashboard_data.period` y `history_snapshot.period` son exactamente el mismo período semanal.
6. `methodology_version` está presente en ambos objetos. Usá el mismo valor técnico devuelto por `get_third_slide_history`; no lo uses como criterio de compatibilidad histórica.
7. `history_snapshot.period` contiene SOLAMENTE `period_id`, `from_date`, `to_date` y `days`.
8. `history_snapshot.period.days` debe ser exactamente `7`.
9. Cada `topics[].point` contiene SOLAMENTE `period_id`, `from_date`, `to_date`, `x_volume`, `x_engagement`, `x_views` y `news_articles`.
10. Cada `pillars[].point` contiene SOLAMENTE `period_id`, `from_date`, `to_date`, `x_volume`, `x_engagement`, `x_views` y `news_articles`.
11. `days` NO existe en ningún `topics[].point`.
12. `days` NO existe en ningún `pillars[].point`.
13. Todos los `point.period_id`, `point.from_date` y `point.to_date` coinciden exactamente con `history_snapshot.period`.
14. No hay `topic_id` duplicados dentro de `topics`.
15. No inventaste métricas faltantes.
16. Antes de invocar la herramienta, eliminá cualquier propiedad auxiliar usada durante el razonamiento que no pertenezca al schema.
