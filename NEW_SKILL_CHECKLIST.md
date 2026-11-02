# Checklist para nueva skill

Seguir estos pasos cada vez que se agrega una nueva skill al repositorio.

---

## 1. Estructura de carpetas

- [ ] Crear carpeta `.claude/skills/<nombre-en-kebab-case>/`
- [ ] Crear `SKILL.md` con frontmatter mínimo: `name`, `description`, y `action: true` si se activará como comando `/`
- [ ] Verificar que el campo `name:` coincida **exactamente** con el nombre de la carpeta (kebab-case, minúsculas)

## 2. Contenido de SKILL.md

Incluir las siguientes secciones (adaptar según el tipo de skill):

- [ ] `## Purpose` — qué resultado produce la skill en una oración
- [ ] `## When to use it` — cuándo activarla (frases e intenciones típicas que la disparan)
- [ ] `## When not to use it` — casos que no le corresponden o que pertenecen a otra skill
- [ ] `## Required inputs` — qué necesita del usuario para funcionar; si falta algo esencial, pedirlo antes de continuar
- [ ] `## Sources of truth` — fuentes autorizadas y qué hacer si no están disponibles (¿abortar? ¿continuar sin esa fuente?)
- [ ] `## Workflow` — pasos ordenados que sigue el agente
- [ ] `## Rules and constraints` — restricciones, confirmaciones requeridas, permisos, acciones irreversibles
- [ ] `## Output format` — formato, idioma y nivel de detalle esperado del output
- [ ] `## Error handling` — qué hacer si una fuente falla, los datos están incompletos o la request es ambigua

## 3. Archivos de soporte

- [ ] Templates HTML de output → colocar como `template.html` en la raíz de la skill (patrón compartido)
- [ ] Documentación de referencia, assets (imágenes, fuentes), schemas → colocar en `references/`
- [ ] Scripts auxiliares → colocar en `scripts/`; documentar dependencias, versión de runtime y cómo ejecutarlos
- [ ] Casos de prueba → crear `tests/positive-cases.md` y `tests/negative-cases.md` (cuando aplica)

## 4. Actualizar el repositorio

- [ ] Agregar la skill a la tabla de catálogo en `README.md`
- [ ] Agregar entrada inicial en `CHANGELOG.md`:
  ```
  ## <skill-name>
  ### 1.0.0 — YYYY-MM-DD
  - Versión inicial publicada.
  ```
- [ ] Crear tag de git para la versión inicial:
  ```bash
  git tag <skill-name>/1.0.0
  git push origin <skill-name>/1.0.0
  ```

## 5. Desde Treasure AI Studio

- [ ] Solicitar la contraseña de modificación al usuario antes de proceder con cualquier cambio al repositorio
- [ ] Solo continuar si el usuario proporciona la contraseña correcta
