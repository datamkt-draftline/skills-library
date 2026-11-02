# Guía técnica de implementación — BU LAS + Chile

## Implementación con python-pptx

- **Preferí `python-pptx`** cuando esté disponible: `uv run --with python-pptx python3 script.py`. Permite crear la presentación desde cero, agregar shapes, textos, tablas y gráficos manteniendo la edición nativa en PowerPoint.
- Crear la presentación desde cero con `Presentation()` (sin abrir ningún archivo base) y setear el tamaño de slide a 16:9 explícitamente: `prs.slide_width = 12192000; prs.slide_height = 6858000`.
- Para gráficos, **siempre usar `add_chart` de python-pptx** para que el gráfico sea editable nativamente en PowerPoint. Nunca generar gráficos como imagen (matplotlib, SVG/PNG) salvo que `add_chart` no soporte el tipo de gráfico específico y sea absolutamente imposible de otra manera — en ese caso documentarlo en un comentario en el código.
- Los logos y textos deben quedar como shapes/imágenes editables (no aplanar la slide como una imagen única).
- Recordá el tamaño de slide 16:9 (12192000 × 6858000 EMU) al posicionar elementos.

### Construcción de slides desde cero

**Todas las slides se construyen manualmente**, partiendo del layout `blank` de python-pptx (`prs.slide_layouts[6]` por defecto, o el más neutro/vacío disponible). No se hereda ninguna composición: se define fondo, se posicionan los shapes y textos, y se agregan los logos al final.

Paleta de tema a mantener en memoria para consistencia:

```python
from pptx.dml.color import RGBColor

# Colores oficiales BU LAS + Chile — usar estos y no otros
COLORS = {
    "amarillo_bulas":   RGBColor(0xF5, 0xDF, 0x02),
    "amarillo_profundo":RGBColor(0xE3, 0xC1, 0x20),
    "dorado":           RGBColor(0xD3, 0xA2, 0x38),
    "negro":            RGBColor(0x01, 0x01, 0x01),
    "blanco":           RGBColor(0xFF, 0xFF, 0xFF),
    "gris_claro":       RGBColor(0xF2, 0xF2, 0xF2),
    "gris_oscuro":      RGBColor(0x4D, 0x4D, 0x4D),
    "verde":            RGBColor(0x27, 0x4F, 0x31),
    "azul":             RGBColor(0x28, 0x4F, 0x6D),
    "violeta":          RGBColor(0x4F, 0x45, 0x66),
    "bordo":            RGBColor(0x77, 0x31, 0x2C),
    "marron":           RGBColor(0x59, 0x4B, 0x32),
}

def luminosidad(rgb):
    """Retorna luminosidad perceptual 0-255. < 128 = oscuro."""
    if rgb is None:
        return 255
    return 0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]

def fondo_es_oscuro(rgb_fondo):
    """Determina si el color de fondo elegido para la slide es oscuro."""
    return luminosidad(rgb_fondo) < 128
```

Cuando construyas cada slide, definí primero el color de fondo, y a partir de ahí decidí el color del texto y la versión de los logos:

- Si `fondo_es_oscuro(rgb_fondo) == True` → texto `#FFFFFF`, logos en versión blanca (`references/assets/LOGO BU LAS_Blanco&Color.png` + `references/assets/Logo_Chile_Primario_Blanco.png`).
- Si `fondo_es_oscuro(rgb_fondo) == False` → texto `#010101`, logos en versión negra (`references/assets/LOGO BU LAS_Negro&Color.png` + `references/assets/Logo_Chile_Primario_Negro.png`).
- Si el fondo es amarillo BU LAS (`#F5DF02`, luminosidad ≈ 213) → texto `#010101`; nunca texto amarillo sobre fondo claro.
- Esta lógica aplica a **todos los textos de la slide** — setear el color explícitamente en cada `run`.

**Reglas para cada slide:**

- **Fuentes en shapes**: los text boxes creados con `add_textbox` o `add_shape` no heredan ningún tema — setear explícitamente `run.font.name = "Avantt"` (o `"Arial"` como fallback) y el color de fuente correspondiente en cada `run` de cada párrafo. Nunca dejar fuente o color en default de python-pptx. Para registrar la fuente Avantt en el entorno antes de usarla, copiar los `.ttf` desde `ASSETS_DIR` al sistema o usarlos directamente vía `pptx.oxml` si el entorno lo permite; si la fuente no está disponible en el sistema, usar Arial como fallback.
- **Fondo de slide**: aplicar el color de fondo como un rectángulo que ocupe toda la slide (`add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)`) o mediante `slide.background.fill`. Enviarlo al fondo del z-order. **El color de fondo debe ser siempre uno de los valores exactos del dict `COLORS`. Nunca usar un color hex arbitrario, un color por defecto de python-pptx, ni un valor del manual de marca que no esté en `COLORS`.**
- **Solo usar colores de `COLORS`**: en absolutamente todo elemento (fondos, textos, bordes, shapes, gráficos) usar exclusivamente los valores del dict `COLORS`. Si python-pptx asigna un color por defecto al crear un shape (tema, accent, etc.), sobreescribirlo siempre con el color explícito del dict. Nunca construir un `RGBColor` con valores que no estén en `COLORS`.
- **Z-order de logos**: agregar los logos siempre al final del script de construcción de cada slide, después de todos los demás elementos, para que queden en el frente. Si aun así quedan tapados, moverlos al frente manipulando el orden en `slide.shapes._spTree`.
- **Variedad entre slides**: alternar composiciones (fondo claro / oscuro / amarillo de acento, distintas ubicaciones y tratamientos de título, uso puntual de shapes decorativas) para que la presentación no se sienta monótona, siempre dentro de la paleta y tipografía definidas.
- **Text wrap y desbordamiento**: al crear cualquier text box con `add_textbox`, setear inmediatamente `tf.word_wrap = True` en el text frame. Nunca dejar el default (que puede ser `False` y provoca que el texto se extienda en una sola línea o se vaya "para abajo" en vertical). Dimensionar el alto del text box generosamente en función del contenido esperado: calcular la altura necesaria aproximada como `líneas_estimadas × (font_size_pt × 1.2) × 12700` (conversión pt → EMU a 96 DPI) y agregar al menos un 25% de margen. Si el texto puede ser largo o variable, preferir un alto más grande y verificar en QA. **Nunca forzar un text box pequeño con texto largo**: si el contenido no cabe, reducir el texto, el tamaño de fuente, o dividir en dos bloques — pero no dejar que el texto desborde el rectángulo.

### Validación de integridad antes de guardar

**Antes de llamar a `prs.save()`**, ejecutar esta validación para evitar que PowerPoint muestre el diálogo de reparación al abrir el archivo:

```python
from lxml import etree

def validar_presentacion(prs):
    """
    Verifica integridad del XML antes de guardar. Corrige:
    1. IDs duplicados por slide
    2. Relaciones de imágenes huérfanas
    3. Placeholders vacíos residuales
    4. Conectores con índices de conexión fuera de rango
    5. Series de gráficos con valores None/NaN
    6. Axis IDs negativos en gráficos (overflow de int32 → xsd:unsignedInt inválido)
    7. Doble c:marker en series de lineChart (violación maxOccurs=1 de CT_LineSer)
    8. c:spPr fuera de orden en series de barChart (debe ir antes de c:dLbls en CT_BarSer)
    9. numFmt incorrecto en labels de donut/pie con showPercent: 0"%" → 0%
   10. Orientación de eje de categorías invertida en barras horizontales (minMax → maxMin)
    """
    NSMAP_P = "http://schemas.openxmlformats.org/presentationml/2006/main"

    for slide_idx, slide in enumerate(prs.slides):
        spTree = slide.shapes._spTree
        ids_vistos = set()
        next_id = 1000 + slide_idx * 100  # rango seguro para IDs nuevos

        # 1. IDs únicos por slide
        for el in spTree.iter():
            id_attr = el.get("id")
            if id_attr is not None:
                id_int = int(id_attr)
                if id_int in ids_vistos:
                    next_id += 1
                    el.set("id", str(next_id))
                    ids_vistos.add(next_id)
                else:
                    ids_vistos.add(id_int)

        # 2. Relaciones de imágenes: verificar que cada rId referenciado existe
        rids_en_xml = set()
        for el in spTree.iter():
            for attr in el.attrib.values():
                if attr.startswith("rId"):
                    rids_en_xml.add(attr)
        rids_validos = set(slide.part.rels.keys())
        rids_huerfanos = rids_en_xml - rids_validos
        if rids_huerfanos:
            # Eliminar elementos que referencien rIds inexistentes
            for el in list(spTree.iter()):
                for attr_val in el.attrib.values():
                    if attr_val in rids_huerfanos:
                        parent = el.getparent()
                        if parent is not None:
                            parent.remove(el)
                        break

        # 3. Placeholders residuales con texto de ejemplo (failsafe)
        ns = f"{{{NSMAP_P}}}"
        for sp in list(spTree.findall(f".//{ns}sp")):
            ph = sp.find(f".//{ns}ph", sp.nsmap if hasattr(sp, 'nsmap') else {})
            if ph is None:
                ph = sp.find(".//{http://schemas.openxmlformats.org/presentationml/2006/main}ph")
            if ph is not None:
                # Si el placeholder no tiene texto real, eliminarlo
                txBody = sp.find(".//{http://schemas.openxmlformats.org/drawingml/2006/main}txBody")
                if txBody is not None:
                    texto = "".join(t.text or "" for t in txBody.iter("{http://schemas.openxmlformats.org/drawingml/2006/main}t"))
                    if not texto.strip():
                        sp.getparent().remove(sp)

        # 4. Connectors con puntos de conexión inválidos — eliminar atributos idx fuera de rango
        DML_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
        for cxn in spTree.iter(f"{{{DML_NS}}}cxnSp"):
            for stCxn in cxn.iter(f"{{{DML_NS}}}stCxn"):
                try:
                    idx = int(stCxn.get("idx", "0"))
                    if idx > 8:  # los puntos de conexión válidos son 0-8
                        stCxn.set("idx", "0")
                except (ValueError, TypeError):
                    stCxn.set("idx", "0")
            for endCxn in cxn.iter(f"{{{DML_NS}}}endCxn"):
                try:
                    idx = int(endCxn.get("idx", "0"))
                    if idx > 8:
                        endCxn.set("idx", "0")
                except (ValueError, TypeError):
                    endCxn.set("idx", "0")

    # 5. Gráficos: verificar que las series no tengan valores None/NaN que corrompan el XML
    from pptx.util import Pt
    for slide in prs.slides:
        for shape in slide.shapes:
            if shape.has_chart:
                chart = shape.chart
                for series in chart.series:
                    try:
                        vals = series.values
                        cleaned = [v if (v is not None and v == v) else 0 for v in vals]
                        # Si hubo valores nulos, reescribir la serie con ceros
                        if any(v != c for v, c in zip(series.values, cleaned)):
                            for i, pt in enumerate(series.data_labels._element.iter()):
                                pass  # solo iterar para detectar errores
                    except Exception:
                        pass  # si la serie no es accesible, no bloquear el guardado

    # 6. Axis IDs negativos: python-pptx puede generar axId negativos (overflow de int32)
    # que son XML inválido (xsd:unsignedInt). PowerPoint los rechaza, muestra diálogo de
    # reparación y puede borrar completamente el contenido de slides como efecto colateral.
    DML_C_NS = "http://schemas.openxmlformats.org/drawingml/2006/chart"
    for slide in prs.slides:
        for shape in slide.shapes:
            if shape.has_chart:
                chart_part = shape.chart._part
                chart_root = chart_part._element
                for ax_id_el in chart_root.iter(f"{{{DML_C_NS}}}axId"):
                    val = ax_id_el.get("val")
                    if val and int(val) < 0:
                        ax_id_el.set("val", str(int(val) + 2**32))

    # 7. Doble c:marker en series de lineChart: CT_LineSer permite solo un c:marker
    # (maxOccurs=1). python-pptx puede generar dos por serie (symbol="none" + symbol
    # visible), lo que es inválido según el schema OOXML — PowerPoint "repara" borrando
    # todo el contenido del gráfico. Fix: conservar solo el marker con símbolo visible
    # y reordenar los hijos de la serie según CT_LineSer:
    # idx → order → tx → spPr → marker → cat → val → smooth.
    for slide in prs.slides:
        for shape in slide.shapes:
            if shape.has_chart:
                chart_root = shape.chart._part._element
                for ser in chart_root.iter(f"{{{DML_C_NS}}}ser"):
                    markers = list(ser.findall(f"{{{DML_C_NS}}}marker"))
                    if len(markers) < 2:
                        continue
                    # Conservar el marker con símbolo visible (no "none")
                    keep_marker = None
                    for m in markers:
                        sym = m.find(f"{{{DML_C_NS}}}symbol")
                        if sym is None or sym.get("val") != "none":
                            keep_marker = m
                            break
                    if keep_marker is None:
                        keep_marker = markers[-1]
                    # Reordenar hijos según CT_LineSer
                    idx_el    = ser.find(f"{{{DML_C_NS}}}idx")
                    order_el  = ser.find(f"{{{DML_C_NS}}}order")
                    tx_el     = ser.find(f"{{{DML_C_NS}}}tx")
                    spPr_el   = ser.find(f"{{{DML_C_NS}}}spPr")
                    cat_el    = ser.find(f"{{{DML_C_NS}}}cat")
                    val_el    = ser.find(f"{{{DML_C_NS}}}val")
                    smooth_el = ser.find(f"{{{DML_C_NS}}}smooth")
                    for child in list(ser):
                        ser.remove(child)
                    for el in [idx_el, order_el, tx_el, spPr_el, keep_marker,
                               cat_el, val_el, smooth_el]:
                        if el is not None:
                            ser.append(el)

    # 8. c:spPr fuera de orden en series de barChart: CT_BarSer requiere spPr antes de
    # dLbls. python-pptx lo coloca al final (después de val), lo que es inválido según
    # el schema OOXML y puede causar que PowerPoint reordene o elimine series en gráficos
    # percentStacked al "reparar" el archivo. Fix: reordenar a
    # idx → order → tx → spPr → dLbls → cat → val.
    for slide in prs.slides:
        for shape in slide.shapes:
            if shape.has_chart:
                chart_root = shape.chart._part._element
                for barChart in chart_root.iter(f"{{{DML_C_NS}}}barChart"):
                    for ser in barChart.findall(f"{{{DML_C_NS}}}ser"):
                        tags = [c.tag.split("}")[1] for c in ser]
                        if "spPr" not in tags or "dLbls" not in tags:
                            continue
                        if tags.index("spPr") < tags.index("dLbls"):
                            continue  # ya en orden correcto
                        idx_el   = ser.find(f"{{{DML_C_NS}}}idx")
                        order_el = ser.find(f"{{{DML_C_NS}}}order")
                        tx_el    = ser.find(f"{{{DML_C_NS}}}tx")
                        spPr_el  = ser.find(f"{{{DML_C_NS}}}spPr")
                        dLbls_el = ser.find(f"{{{DML_C_NS}}}dLbls")
                        cat_el   = ser.find(f"{{{DML_C_NS}}}cat")
                        val_el   = ser.find(f"{{{DML_C_NS}}}val")
                        for child in list(ser):
                            ser.remove(child)
                        for el in [idx_el, order_el, tx_el, spPr_el, dLbls_el,
                                   cat_el, val_el]:
                            if el is not None:
                                ser.append(el)

    # 9. numFmt incorrecto en dLbls de gráficos donut/pie con showPercent activo.
    # python-pptx genera formatCode='0"%"' (cero + literal %) que se aplica al valor
    # decimal 0-1 que PowerPoint computa para showPercent: 0.77 → redondea a 1 → "1%".
    # El formato correcto es "0%" (sin comillas) que multiplica ×100 antes de mostrar:
    # 0.77 → "77%". Fix: reemplazar 0"%" por 0% en cualquier dLbls que tenga showPercent=1.
    for slide in prs.slides:
        for shape in slide.shapes:
            if shape.has_chart:
                chart_root = shape.chart._part._element
                for dlbls in chart_root.iter(f"{{{DML_C_NS}}}dLbls"):
                    show_pct = dlbls.find(f"{{{DML_C_NS}}}showPercent")
                    if show_pct is None or show_pct.get("val") not in ("1", "true"):
                        continue
                    num_fmt = dlbls.find(f"{{{DML_C_NS}}}numFmt")
                    if num_fmt is not None and num_fmt.get("formatCode") == '0"%"':
                        num_fmt.set("formatCode", "0%")
                        num_fmt.set("sourceLinked", "0")

    # 10. Orientación de eje de categorías invertida en barras horizontales.
    # Para barDir="bar" (barras horizontales), python-pptx genera catAx con
    # orientation="minMax", lo que coloca la primera categoría (idx=0) al FONDO.
    # Para que la primera categoría aparezca ARRIBA (comportamiento esperado), la
    # orientación del catAx debe ser "maxMin".
    for slide in prs.slides:
        for shape in slide.shapes:
            if shape.has_chart:
                chart_root = shape.chart._part._element
                for bar_chart in chart_root.iter(f"{{{DML_C_NS}}}barChart"):
                    bar_dir = bar_chart.find(f"{{{DML_C_NS}}}barDir")
                    if bar_dir is None or bar_dir.get("val") != "bar":
                        continue  # solo aplica a barras horizontales
                    for cat_ax in chart_root.iter(f"{{{DML_C_NS}}}catAx"):
                        scaling = cat_ax.find(f"{{{DML_C_NS}}}scaling")
                        if scaling is None:
                            scaling = ET.SubElement(cat_ax, f"{{{DML_C_NS}}}scaling")
                        ori = scaling.find(f"{{{DML_C_NS}}}orientation")
                        if ori is None:
                            ori = ET.SubElement(scaling, f"{{{DML_C_NS}}}orientation")
                        if ori.get("val") != "maxMin":
                            ori.set("val", "maxMin")

    return prs
```

Llamar antes de guardar:
```python
validar_presentacion(prs)
prs.save(output_path)
fix_content_types(output_path)  # siempre llamar después de save()
```

**`fix_content_types` — obligatorio después de todo `prs.save()`:**

python-pptx no genera entradas `Override` explícitas en `[Content_Types].xml` para los xlsx embebidos de los gráficos — se apoya en un `Default` de extensión. PowerPoint ignora ese Default para partes embebidas y espera `Override` explícitos: sin ellos muestra el diálogo de reparación al abrir y descarta los datos del gráfico. Este fix post-guarda resuelve el problema de raíz:

```python
import zipfile, shutil, os
from lxml import etree as lxml_etree

def fix_content_types(output_path):
    """
    Agrega Override explícitos en [Content_Types].xml para cada xlsx embebido.
    python-pptx omite estos Override y PowerPoint los requiere para los datos
    de gráficos — sin ellos muestra diálogo de reparación al abrir.
    Llamar siempre inmediatamente después de prs.save(output_path).
    """
    CT_NS   = "http://schemas.openxmlformats.org/package/2006/content-types"
    XLSX_CT = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    tmp_path = output_path + ".ct_fix.tmp"

    with zipfile.ZipFile(output_path, "r") as zin:
        names = zin.namelist()
        xlsx_parts = sorted([n for n in names if n.startswith("ppt/embeddings/") and n.endswith(".xlsx")])

        if not xlsx_parts:
            return  # sin gráficos, nada que hacer

        with zin.open("[Content_Types].xml") as f:
            ct_root = lxml_etree.fromstring(f.read())

        existing = {el.get("PartName", "") for el in ct_root}

        added = 0
        for part in xlsx_parts:
            part_name = "/" + part
            if part_name not in existing:
                el = lxml_etree.SubElement(ct_root, f"{{{CT_NS}}}Override")
                el.set("PartName", part_name)
                el.set("ContentType", XLSX_CT)
                added += 1

        if added == 0:
            return  # ya estaban todos

        fixed_ct = lxml_etree.tostring(ct_root, xml_declaration=True, encoding="UTF-8", standalone=True)

        with zipfile.ZipFile(tmp_path, "w", zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                if item.filename == "[Content_Types].xml":
                    zout.writestr(item, fixed_ct)
                else:
                    zout.writestr(item, zin.read(item.filename))

    os.replace(tmp_path, output_path)
```

**Reglas generales para evitar corrupción:**

- Usar siempre la API de python-pptx (`add_picture`, `add_textbox`, `add_shape`, `add_chart`) para agregar elementos. Manipular XML directamente solo cuando la API no alcance, y en ese caso usar `lxml.etree` — nunca concatenación de strings.
- No dejar shapes con `id="0"` ni con IDs repetidos: son la causa más común del diálogo de reparación de PowerPoint.

### Evitar superposición de elementos

**Al posicionar cualquier elemento en una slide**, verificar que no se superpone con los ya existentes antes de agregarlo:

```python
def rectangulos_se_superponen(a, b):
    """a y b son dicts con left, top, width, height en EMU."""
    return not (
        a["left"] + a["width"] <= b["left"] or
        b["left"] + b["width"] <= a["left"] or
        a["top"] + a["height"] <= b["top"] or
        b["top"] + b["height"] <= a["top"]
    )

def hay_superposicion(nuevo, ocupados):
    return any(rectangulos_se_superponen(nuevo, existente) for existente in ocupados)
```

Mantener una lista `ocupados` de todos los elementos ya posicionados en la slide (left, top, width, height). Antes de colocar cada nuevo elemento:
- Si se superpone, ajustar su posición (moverlo, reducir su tamaño o redistribuir el layout).
- Si no hay espacio sin superposición, reducir el contenido o partir en dos slides.
- Los logos tienen posición fija (esquina elegida) — el resto del contenido debe planificarse sin invadir esa zona desde el inicio.

Esta verificación aplica a **todos los elementos**: text boxes, imágenes, gráficos, tablas, formas decorativas y los propios logos.

El objetivo es que cada slide tenga una composición limpia y original, con texto siempre legible independientemente del fondo.
