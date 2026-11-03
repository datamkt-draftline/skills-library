---
name: github-updater
description: Actualiza el repositorio datamkt-draftline/skills-library en GitHub: sincroniza archivos de skills modificadas, valida el checklist para nuevas skills, y mantiene CHANGELOG.md y README.md al día. Activar cuando el usuario pida sincronizar, publicar o pushear cambios al repo de skills.
action: true
---

# Propósito

Sincronizar cambios del entorno local con el repositorio `datamkt-draftline/skills-library` en GitHub, garantizando que el CHANGELOG, el README y el checklist de nueva skill estén siempre en orden.

---

## Paso 0 — Solicitar contraseña de modificación

**OBLIGATORIO. Hacerlo antes de cualquier otra acción.**

Usar `AskUserQuestion` para solicitar la contraseña de modificación. Continuar únicamente si la respuesta es exactamente `datamkt`. Si no coincide, detener la ejecución e informar al usuario.

Esta contraseña está definida en el `CLAUDE.md` del repositorio.

---

## Paso 1 — Determinar el tipo de operación

Identificar qué tipo de cambio se está publicando. Puede ser uno o varios simultáneamente:

- **A) Actualización de skill existente** — cambios en archivos de una skill ya publicada.
- **B) Nueva skill** — skill que todavía no existe en el repo.
- **C) Archivos raíz** — cambios directos en `README.md`, `CHANGELOG.md` u otros archivos fuera de `.claude/skills/`.

Si el usuario no especificó el tipo, inferirlo a partir de los archivos mencionados o del contexto de la conversación. Si hay ambigüedad, preguntar antes de continuar.

---

## Paso 2A — Actualización de skill existente

### 2A.1 — Identificar archivos modificados

Determinar qué archivos dentro de `.claude/skills/<skill>/` cambiaron. Si el usuario no los listó, preguntar o inferirlos del contexto de la sesión.

### 2A.2 — Determinar versión

Consultar el CHANGELOG actual para conocer la última versión publicada de la skill:

```bash
gh api repos/datamkt-draftline/skills-library/contents/CHANGELOG.md --jq '.content' | base64 -d
```

Determinar el bump semántico según los cambios:
- **patch** (x.y.**Z**): correcciones, typos, ajustes menores sin impacto en comportamiento.
- **minor** (x.**Y**.0): nuevas instrucciones, secciones, parámetros o capacidades que no rompen lo anterior.
- **major** (**X**.0.0): cambios de comportamiento que rompen compatibilidad con versiones previas.

Si hay dudas sobre el tipo de bump, preguntar al usuario.

### 2A.3 — Preparar la entrada de CHANGELOG

Redactar los bullet points del cambio en base a lo que se modificó. Formato:

```
### X.Y.Z — YYYY-MM-DD
- Descripción del cambio en español, concisa, orientada al comportamiento.
```

### 2A.4 — Subir archivos modificados (secuencial)

Para cada archivo a actualizar, ejecutar estos tres comandos **en orden, uno a la vez** (nunca en paralelo: las escrituras concurrentes generan errores 409):

```bash
# 1. Obtener el blob SHA actual del archivo en el repo
SHA=$(gh api repos/datamkt-draftline/skills-library/contents/<path> --jq '.sha')

# 2. Codificar el contenido local en base64
CONTENT=$(base64 -w0 < "<ruta-local>")

# 3. Actualizar el archivo
gh api --method PUT repos/datamkt-draftline/skills-library/contents/<path> \
  --field message="<skill>: <descripción breve del cambio>" \
  --field content="$CONTENT" \
  --field sha="$SHA" \
  --field branch="main" \
  --jq '.commit.sha'
```

Confirmar el commit SHA en stdout antes de pasar al siguiente archivo.

### 2A.5 — Actualizar CHANGELOG.md

Leer el CHANGELOG actual, insertar la nueva entrada bajo el encabezado `## <skill-name>` (al inicio de esa sección, antes de la entrada más reciente) y subirlo con el mismo método secuencial del paso 2A.4.

---

## Paso 2B — Nueva skill

### 2B.1 — Validar checklist de estructura

Antes de subir nada, verificar que la skill local cumpla el checklist de `NEW_SKILL_CHECKLIST.md`. Recorrer cada ítem:

**Estructura de carpeta**
- [ ] Carpeta `.claude/skills/<nombre-kebab-case>/` existe localmente.
- [ ] Archivo `SKILL.md` presente con frontmatter mínimo: `name`, `description`, y `action: true` si se activa como comando `/`.
- [ ] El campo `name:` del frontmatter coincide exactamente con el nombre de la carpeta (kebab-case, minúsculas).

**Contenido de SKILL.md**
- [ ] `## Purpose` o equivalente — qué resultado produce la skill.
- [ ] `## When to use it` o equivalente — cuándo activarla.
- [ ] `## When not to use it` o equivalente — casos que no le corresponden.
- [ ] `## Required inputs` o equivalente — qué necesita del usuario.
- [ ] `## Sources of truth` o equivalente — fuentes autorizadas.
- [ ] `## Workflow` o equivalente — pasos ordenados.
- [ ] `## Rules and constraints` o equivalente — restricciones y permisos.
- [ ] `## Output format` o equivalente — formato del output.
- [ ] `## Error handling` o equivalente — manejo de errores.

**Archivos de soporte (cuando apliquen)**
- [ ] Templates HTML en `template.html` en la raíz de la skill.
- [ ] Documentación de referencia, assets y schemas en `references/`.
- [ ] Scripts auxiliares en `scripts/`, con dependencias documentadas.
- [ ] Casos de prueba en `tests/positive-cases.md` y `tests/negative-cases.md`.

Si falta algún ítem obligatorio (frontmatter, secciones de SKILL.md), **no subir** y notificar al usuario qué falta antes de continuar.

### 2B.2 — Subir todos los archivos de la skill

Subir cada archivo de la nueva skill usando el método de creación de la API (sin `sha` para archivos nuevos):

```bash
CONTENT=$(base64 -w0 < "<ruta-local>")
gh api --method PUT repos/datamkt-draftline/skills-library/contents/<path> \
  --field message="feat(<skill>): versión inicial" \
  --field content="$CONTENT" \
  --field branch="main" \
  --jq '.commit.sha'
```

Subir de a un archivo a la vez (secuencial).

### 2B.3 — Actualizar README.md

Agregar una fila a la tabla de catálogo en `README.md`:

```
| <skill-name> | `<carpeta>` | <descripción breve> | action |
```

Mantener el orden alfabético de la tabla. Subir el README actualizado con el método secuencial.

### 2B.4 — Actualizar CHANGELOG.md

Agregar una nueva sección con la versión inicial:

```markdown
## <skill-name>

### 1.0.0 — YYYY-MM-DD
- Versión inicial publicada.
```

Insertar la sección en orden alfabético respecto a las demás skills del CHANGELOG. Subir con el método secuencial.

### 2B.5 — Informar sobre el git tag

Notificar al usuario que, según el checklist, se debe crear un tag de versión inicial. Dado que `git push` por SSH no está disponible en este entorno, proporcionar los comandos para que lo haga manualmente:

```bash
git tag <skill-name>/1.0.0
git push origin <skill-name>/1.0.0
```

---

## Paso 2C — Archivos raíz

Para cambios directos en `README.md`, `CHANGELOG.md` u otros archivos raíz, usar el mismo método secuencial del paso 2A.4. No requiere validación de checklist.

---

## Reglas y restricciones

- **Contraseña siempre primero.** Sin contraseña verificada, ninguna acción sobre el repo.
- **Escrituras siempre secuenciales.** Nunca hacer múltiples `gh api PUT` en paralelo: el API de GitHub rechaza escrituras concurrentes sobre la misma rama con error 409.
- **SHA actualizado antes de cada PUT.** Leer el blob SHA del archivo justo antes de subirlo; un SHA obsoleto genera conflicto aunque la escritura sea válida.
- **Sin invención de contenido.** No modificar el contenido de los archivos locales; subir exactamente lo que está en el work folder.
- **Confirmar commit SHA en cada paso.** Si un PUT devuelve error en vez de SHA, detener y notificar al usuario antes de continuar.
- **Checklist bloqueante para nuevas skills.** Los ítems de frontmatter y secciones de SKILL.md son obligatorios; no publicar si faltan.

---

## Sources of truth

- **Archivos locales** en el work folder: fuente de verdad para el contenido a publicar.
- **`gh api`**: único método de escritura disponible (SSH bloqueado en este entorno).
- **`CHANGELOG.md` del repo**: fuente de verdad para la última versión publicada de cada skill.
- **`NEW_SKILL_CHECKLIST.md` del repo**: fuente de verdad para los requisitos de una nueva skill.
- **`README.md` del repo**: fuente de verdad para el catálogo oficial.

---

## Output

Al finalizar, reportar en el chat:

- Archivos subidos (path + commit SHA).
- Versión publicada y skill afectada.
- Ítems del checklist que no aplicaron (para nuevas skills).
- Cualquier error o bloqueo encontrado.
