# Corona Sunsets — logos

Hay dos sub-marcas dentro de Sunsets, cada una con su propio logo:

1. **Corona Sunsets** — el logo base ("Corona SUNSETS" sin subtítulo).
2. **Corona Sunsets Sessions** — formato de sesiones musicales dentro del universo Sunsets. Lleva "SESSIONS" bajo "SUNSETS".

Elegir según el contenido: si la slide habla del formato "Sessions" (eventos, line-up, DJ sets, sesiones audiovisuales), usar el logo Sessions. Si habla de Corona Sunsets como plataforma más amplia (ritual del atardecer, platform content, el programa general), usar el logo base.

## Archivos

### `corona-sunsets-logo-white-on-black.jpg`
**Corona SUNSETS base, trazo brush blanco, fondo NEGRO baked (JPG, no transparente, square 1:1).** Solo se puede usar sobre un fondo negro (o Corona Blue oscuro, aunque el recuadro negro quedará visible si no coincide exactamente). Para presentaciones con slides de fondo negro puro.

### `corona-sunsets-logo-fade.png`
**Corona SUNSETS con efecto fade (letras blancas con gradiente vertical fundiéndose hacia abajo), fondo gris claro baked.** La transparencia del PNG está deshabilitada (alpha completamente opaco) — el fondo gris está impreso en el archivo. **Usar solo sobre un fondo gris claro muy similar** o no usar — en Corona Blue o blanco se ve un recuadro extraño. Si la slide necesita un logo Sunsets con fade, preferir pedir al usuario un PNG con alpha real.

### `corona-sunset-sessions-logo-white-yellow.png`
**Corona Sunsets Sessions — logo horizontal, "SUN" en Corona Yellow + "SETS SESSIONS" en blanco + wordmark Corona arriba en blanco, textura grabada.** PNG transparente. **La versión default para fondos oscuros (Corona Blue).** Es el logo más representativo del formato Sessions.

### `corona-sunset-sessions-logo-story-white.png`
**Corona Sunsets Sessions — formato vertical 9:16 (Instagram / TikTok Stories).** Wordmark en blanco grunge, apilado y centrado arriba. Fondo transparente. **Uso específico**: sólo cuando la slide replica una story mobile o un asset de social; para slides de deck 16:9 regulares usar la versión horizontal arriba.

## Cómo elegir

| Contexto / fondo | Logo recomendado |
|---|---|
| Presentación de Corona Sunsets general sobre Corona Blue | `corona-sunset-sessions-logo-white-yellow.png` (si aplica Sessions) o pedir al usuario el logo base Sunsets con alpha transparente |
| Slide de fondo negro puro | `corona-sunsets-logo-white-on-black.jpg` |
| Slide de fondo gris claro específico | `corona-sunsets-logo-fade.png` (verificar que el gris coincide) |
| Formato vertical story / social | `corona-sunset-sessions-logo-story-white.png` |
| Presentación de World Tour | ver `../world-tour/` |

## Limitaciones conocidas

- **Fondo baked**: dos de los cuatro logos (`white-on-black.jpg` y `fade.png`) tienen fondo baked (no transparente). Solo funcionan bien sobre backgrounds muy similares al suyo. Si la presentación necesita un logo Sunsets sobre un fondo arbitrario, pedir al usuario un PNG con alpha real antes de improvisar.
- **Sin versión en color completa** con fondo transparente: todos los logos vienen en blanco (+ amarillo en el Sessions). Si se requiere un logo Sunsets en Corona Blue sobre fondo claro, pedir la variante al usuario.
