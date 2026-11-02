# Guía Agile de escalas

Referencia de tipos de pregunta especiales que forman parte de la metodología Agile. Si una pregunta encaja con alguno de estos tipos (por su escala, frases o patrón textual), se analiza según lo indicado abajo.

Si el usuario adjunta un archivo `Agile - Guía de escalas.xlsx` propio, ese archivo **tiene prioridad** sobre esta referencia — parsealo y usá sus columnas (`Tipo de Pregunta`, `Escala`, `Frases`, `BNK Global (Es positivo si…)`, `Calculo`, `Cruce`).

---

## Tipos de pregunta

### Overall Liking
- **Escala**: 1 a 9 (1 desagrada mucho, 9 agrada mucho)
- **BNK Global**: ✅ si promedio ponderado > 7
- **Cálculo**: Promedio Ponderado
- **Cruce**: SÍ — por Rango Etario y Género

### Overall Liking (TaDa)
- **Escala**: 1 a 5 (1 desagrada mucho, 5 agrada mucho)
- **BNK Global**: ✅ si promedio ponderado > 3.9
- **Cálculo**: Promedio Ponderado
- **Cruce**: NO

### NPS
- **Escala**: 0 a 10 (0 no la recomendaría, 10 la recomendaría)
- **BNK Global**: ✅ si NPS > 30
- **Cálculo**: `NPS = %Promotores − %Detractores`
  - Promotores: 9–10
  - Neutrales: 7–8
  - Detractores: 0–6
- **Categorías del resultado**:
  - `-100 a 0`: Necesita mejorar
  - `0 a 30`: Bueno
  - `30 a 70`: Muy bueno
  - `> 70`: Excelente
- **Cruce**: NO

### Intención de compra
- **Escala**: 1 a 5
- **Frases (valor asociado)**:
  - 1 — Definitivamente no la compraría
  - 2 — Probablemente no la compraría
  - 3 — No sé si la compraría o no
  - 4 — Probablemente sí la compraría
  - 5 — Definitivamente sí la compraría
- **BNK Global**: ✅ si T2B (4+5) > 70%
- **Cálculo**: sumatoria de % agrupado en `1–2`, `3`, `4–5` (Bottom / Neutro / Top)
- **Cruce**: SÍ — por Rango Etario y Género
- **En la tabla del análisis, agregar como primera columna `Valor` (el número 1–5).**

### Adecuación
- **Escala**: 1 a 5 (1 nada adecuado, 5 muy adecuado)
- **BNK Global**: ✅ si promedio ponderado > 3.9 **y** T2B (4+5) > 70%
- **Cálculo**: Promedio Ponderado + T2B
- **Cruce**: SÍ — por Rango Etario y Género

### Relevancia
- **Escala**: 1 a 5 (1 nada relevante, 5 muy relevante)
- **BNK Global**: ✅ si promedio ponderado > 3.9 **y** T2B (4+5) > 70%
- **Cálculo**: Promedio Ponderado + T2B
- **Cruce**: SÍ — por Rango Etario y Género

### Valoración
- **Escala**: 1 a 5 (1 la valoraba muy poco, 5 era muy valorada)
- **BNK Global**: ✅ si promedio ponderado > 3.9 **y** T2B (4+5) > 70%
- **Cálculo**: Promedio Ponderado + T2B
- **Cruce**: NO

---

## Cómo matchear una pregunta con la guía

Una pregunta puede ser detectada como uno de estos tipos si:
1. Su **escala** coincide (rango numérico o cantidad de opciones).
2. Sus **frases de respuesta** coinciden (parcial o total, ignorando mayúsculas/tildes).
3. El **texto de la pregunta** contiene palabras clave: "recomend" → NPS, "compr" → Intención de compra, "agrad" / "gust" → Overall Liking, "adecuad" → Adecuación, "relevante" → Relevancia, "valor" → Valoración.

Si hay ambigüedad, priorizar el match por frases de respuesta.

Si **ninguna coincide**, la pregunta se analiza en formato simple (Pregunta / Cantidad de casos / tabla Respuesta·Peso·Porcentaje).

---

## Fórmulas

- **Promedio Ponderado**: `Σ(valor_i × cantidad_i) / Σ(cantidad_i)`
- **T2B (Top 2 Box)**: `(cant(4) + cant(5)) / total × 100`
- **NPS**: `%Promotores − %Detractores` (los porcentajes son sobre el total de respuestas válidas)
