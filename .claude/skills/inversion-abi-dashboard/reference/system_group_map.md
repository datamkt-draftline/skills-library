# Mapeo Sistema → Grupo

El script clasifica cada valor de la columna "Sistema" de la master sheet en
uno de los grupos usados por el dashboard. La comparación se hace tras pasar
por `strip_accents().upper()`, por lo que no importa el casing ni los acentos.

| Grupo | Tokens / Reglas |
|-------|------------------|
| **IMPUESTOS/FEE** | contiene `FEE`, `IMPUESTO`, empieza con `IMP AL`, igual a `IMP AL DEB` |
| **PRODUCCIÓN** | contiene `PRODUCCION` |
| **DIGITAL** | contiene cualquiera de: META, FACEBOOK, TIKTOK, TIK TOK, TWITTER, YOUTUBE, GOOGLE, SPOTIFY, STREAMING, PROGRAMATIC, PROGRAMMATIC, PROGRAMATICA, MERCADO LIBRE, OOH DIGITAL, TWITCH, TAP TAP, TAPTAP, CABIFYADS, LA JUNTA DIGITAL, DAP MEDIA, DLT SPORTS, MEDIOS WEB, AUDIENCIA, ADSERVING, OTHER MEDIA DIGITAL, MEDIOS DIRECTOS |
| **RADIO** | empieza con `RADIO`, contiene ` RADIO`, o es: FM DOS PRODUCCION, PLAY FM PRODUCCION, PLAYFM.CL, 40 PRINCIPALES.CL, CAROLINA.CL, REVISTA ATREVETE |
| **OOH** | contiene: OOH, BILLBOARD, VIA PUBLICA, UBER |
| **TV** | contiene: TV, TVA, TVC, TVI, CINE, CLASE BASICA, TVN |
| **OTROS** | fallback (incluye PRINT, GRAFICA, PRENSA, REVISTA, OTROS, etc.) |

> Nota: el orden importa. Primero se evalúa `IMPUESTOS/FEE`, luego
> `PRODUCCIÓN`, luego `DIGITAL`, luego `RADIO`, `OOH`, `TV`, y `OTROS` como
> último recurso. Esto evita que `TVA` acuerdos se mezcle con digital o que
> `OOH DIGITAL` caiga en OOH.

## Cómo ajustar

Si una nueva plataforma aparece en el Excel y el dashboard la marca como
`OTROS` sin querer, editar la función `system_group()` en
`scripts/build_dashboard.py` y agregar el token al grupo correcto. Volver a
correr el script y regenerar el HTML.
