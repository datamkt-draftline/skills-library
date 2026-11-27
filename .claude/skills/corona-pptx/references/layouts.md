# Guía técnica de implementación — Corona

## Método recomendado: XML directo + zipfile (sin `add_chart`)

**NO usar `add_chart` de python-pptx.** Embebe xlsx que causan el diálogo de reparación en PowerPoint, incluso con `fix_content_types`. El método correcto es construir el PPTX directamente como zip, usando XML DrawingML para todo: texto, shapes y gráficos como rectángulos proporcionales.

### Setup

```python
import os, zipfile, re, html

W  = 12192000   # slide width  (16:9)
H  = 6858000    # slide height
MH = 457200     # margen horizontal
MV = 350000     # margen vertical
CW = W - 2 * MH   # 11277600

BLUE   = "0C2340"
WHITE  = "FFFFFF"
YELLOW = "FFC72C"
LGRAY  = "E8E8E8"   # solo para tracks de barras / placeholders
MGRAY  = "B3B3B3"   # solo para gridlines
DGRAY  = "7A7A7A"   # solo para texto terciario / footnotes

BASE      = os.path.dirname(os.path.abspath(__file__))   # ajustar según el script
ASSETS    = os.path.join(BASE, ".claude", "skills", "corona-pptx", "references", "assets")
TEMPLATE  = os.path.join(BASE, "presentacion_corona_2025_2026-09-30.pptx")  # o cualquier corona pptx
OUTPUT    = os.path.join(BASE, "presentacion_corona_<tema>_<fecha>.pptx")
```

### Colores de series con transparencia (alpha-compositing sobre fondo)

Cuando hay más de 2 series, componer variantes con transparencia calculada:

```
# Sobre fondo BLANCO: alpha_result = alpha * source + (1 - alpha) * 255
# Sobre fondo AZUL (12,35,64): alpha_result = alpha * source + (1-alpha) * fondo

# Para 4 series sobre BLANCO:
COL_S1 = "FFC72C"  # Serie 1: Yellow sólido
COL_S2 = "0C2340"  # Serie 2: Blue full
COL_S3 = "798696"  # Serie 3: Blue 55% sobre blanco → R=0.55*12+0.45*255=121, G=134, B=150
COL_S4 = "C2C8CF"  # Serie 4: Blue 25% sobre blanco → R=0.25*12+0.75*255=194, G=200, B=207

# Para 4 series sobre AZUL (12,35,64):
COL_S1_B = "FFC72C"  # Serie 1: Yellow sólido
COL_S2_B = "FFFFFF"  # Serie 2: White full
COL_S3_B = "929CA9"  # Serie 3: White 55% sobre azul → R=0.55*255+0.45*12=146, G=156, B=169
COL_S4_B = "495A70"  # Serie 4: White 25% sobre azul → R=0.25*255+0.75*12=73, G=90, B=112
```

---

## Helpers XML

### ID counter

```python
_id_ctr = [9]
def nid():
    _id_ctr[0] += 1
    return _id_ctr[0]
def reset_ids():
    _id_ctr[0] = 9
```

### Texto

```python
def run(text, sz=1800, bold=False, color=WHITE, font="Helvetica Neue",
        italic=False, upper=False):
    t = html.escape(str(text).upper() if upper else str(text), quote=True)
    b = ' b="1"' if bold else ""
    it = ' i="1"' if italic else ""
    return (f'<a:r><a:rPr lang="es-AR" sz="{sz}"{b}{it} dirty="0">'
            f'<a:solidFill><a:srgbClr val="{color}"/></a:solidFill>'
            f'<a:latin typeface="{font}"/><a:cs typeface="{font}"/></a:rPr>'
            f'<a:t>{t}</a:t></a:r>')

def para(runs_xml, algn="l", spc_bef=0, spc_aft=0):
    r = runs_xml if isinstance(runs_xml, str) else "".join(runs_xml)
    a = f' algn="{algn}"' if algn else ""
    return (f'<a:p><a:pPr{a}>'
            f'<a:spcBef><a:spcPts val="{spc_bef}"/></a:spcBef>'
            f'<a:spcAft><a:spcPts val="{spc_aft}"/></a:spcAft>'
            f'</a:pPr>{r}</a:p>')

def txtbox(x, y, cx, cy, paras_xml, anchor="t", wrap="square",
           lIns=91440, rIns=91440, tIns=45720, bIns=45720):
    p = paras_xml if isinstance(paras_xml, str) else "".join(paras_xml)
    i1, i2 = nid(), nid()
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="{i1}" name="tb_{i2}"/>'
            f'<p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>'
            f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
            f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/></p:spPr>'
            f'<p:txBody><a:bodyPr wrap="{wrap}" lIns="{lIns}" rIns="{rIns}" '
            f'tIns="{tIns}" bIns="{bIns}" anchor="{anchor}"/>'
            f'<a:lstStyle/>{p}</p:txBody></p:sp>')
```

### Rectángulo

```python
def rect_sh(x, y, cx, cy, fill, border_color=None, border_w=12700):
    if cx <= 0 or cy <= 0:
        return ""
    ln = (f'<a:ln w="{border_w}"><a:solidFill><a:srgbClr val="{border_color}"/></a:solidFill></a:ln>'
          if border_color else '<a:ln><a:noFill/></a:ln>')
    i1, i2 = nid(), nid()
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="{i1}" name="r_{i2}"/>'
            f'<p:cNvSpPr/><p:nvPr/></p:nvSpPr>'
            f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
            f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
            f'<a:solidFill><a:srgbClr val="{fill}"/></a:solidFill>{ln}</p:spPr>'
            f'<p:txBody><a:bodyPr/><a:lstStyle/><a:p/></p:txBody></p:sp>')
```

### Imagen

```python
def pic_xml(rid, x, y, cx, cy, name="img"):
    i1, i2 = nid(), nid()
    return (f'<p:pic><p:nvPicPr>'
            f'<p:cNvPr id="{i1}" name="{html.escape(name)}_{i2}"/>'
            f'<p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr>'
            f'<p:nvPr/></p:nvPicPr>'
            f'<p:blipFill><a:blip r:embed="{rid}"/>'
            f'<a:stretch><a:fillRect/></a:stretch></p:blipFill>'
            f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
            f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr></p:pic>')

# Calcular dimensiones respetando la proporción real del archivo:
#   logo_h = int(logo_w / ratio)   donde ratio = imagen_px_w / imagen_px_h
# NUNCA usar un ratio inventado — leer las dimensiones reales del PNG antes de codear.
```

### Slide wrapper

```python
def slide_xml(body, bg=None):
    bg_xml = ""
    if bg:
        bg_xml = (f'<p:bg><p:bgPr>'
                  f'<a:solidFill><a:srgbClr val="{bg}"/></a:solidFill>'
                  f'<a:effectLst/></p:bgPr></p:bg>')
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
            'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
            'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">'
            f'<p:cSld>{bg_xml}'
            '<p:spTree>'
            '<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>'
            '<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/>'
            '<a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'
            f'{body}'
            '</p:spTree></p:cSld>'
            '<p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>'
            '</p:sld>')
```

### Slide relationships

```python
def slide_rels_xml(image_rids):
    """
    image_rids: dict { rid_string: media_filename }
    Ejemplo: {"rId10": "corona_logo_dark.png", "rId11": "corona_logo_light.png"}
    """
    rels = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">',
            '<Relationship Id="rId1" '
            'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" '
            'Target="../slideLayouts/slideLayout1.xml"/>']
    for rid, media_name in image_rids.items():
        rels.append(
            f'<Relationship Id="{rid}" '
            f'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" '
            f'Target="../media/{media_name}"/>')
    rels.append('</Relationships>')
    return "".join(rels)
```

---

## Helpers de gráficos (rectángulos proporcionales)

### Barras verticales apiladas

```python
def stacked_columns(data_by_series, categories, x, y, w, h,
                    colors, bg, label_color=None, val_color=None,
                    show_labels=False, axis_sz=800, gap_ratio=0.3, y_axis=True):
    """
    data_by_series: dict ordenado {serie: [val_por_categoría]}
    categories: lista de etiquetas del eje X
    colors: lista de colores (mismo orden que series)
    """
    if not label_color: label_color = WHITE if bg == BLUE else BLUE
    if not val_color:   val_color   = YELLOW if bg == BLUE else BLUE

    series_names = list(data_by_series.keys())
    col_totals = [sum(data_by_series[s][i] for s in series_names) for i in range(len(categories))]
    max_total = max(col_totals) if max(col_totals) > 0 else 1

    gap = int(w / len(categories) * gap_ratio)
    bar_w = int((w - gap * (len(categories) - 1)) / len(categories))
    chart_bottom = y + h

    xml = ""
    if y_axis:
        for gi in range(5):
            gv = max_total * gi / 4
            gy = int(chart_bottom - h * gi / 4)
            xml += rect_sh(x, gy - 6000, w, 12000, MGRAY if gi > 0 else label_color)
            xml += txtbox(x - 950000, gy - 150000, 900000, 300000,
                          para(run(f"${gv/1e6:,.0f} M", sz=axis_sz, color=label_color,
                                   font="Helvetica Neue"), algn="r"), anchor="ctr")

    for i, cat in enumerate(categories):
        bx = x + i * (bar_w + gap)
        cum_h = 0
        for si, sname in enumerate(series_names):
            val = data_by_series[sname][i]
            if val <= 0: continue
            bh = max(2, int(h * val / max_total))
            xml += rect_sh(bx, chart_bottom - cum_h - bh, bar_w, bh, colors[si])
            cum_h += bh
        xml += txtbox(bx - 20000, chart_bottom + 30000, bar_w + 40000, 220000,
                      para(run(cat, sz=750, color=label_color, font="Helvetica Neue"), algn="ctr"))
        if show_labels and col_totals[i] > 0:
            top_y = chart_bottom - int(h * col_totals[i] / max_total)
            xml += txtbox(bx - 50000, top_y - 230000, bar_w + 100000, 200000,
                          para(run(f"${col_totals[i]/1e6:,.0f}", sz=750, bold=True,
                                   color=val_color, font="Helvetica Neue"), algn="ctr"))
    return xml
```

### Barras horizontales apiladas (absolutas)

```python
def stacked_bars_h(data_by_series, categories, x, y, w, h,
                   colors, bg, label_color=None, val_color=None,
                   label_w=1000000, gap_ratio=0.35):
    if not label_color: label_color = WHITE if bg == BLUE else BLUE
    if not val_color:   val_color   = YELLOW if bg == BLUE else BLUE

    series_names = list(data_by_series.keys())
    row_totals = [sum(data_by_series[s][i] for s in series_names) for i in range(len(categories))]
    max_total = max(row_totals) if max(row_totals) > 0 else 1

    gap = int(h / len(categories) * gap_ratio)
    bar_h = int((h - gap * (len(categories) - 1)) / len(categories))
    bar_area_w = w - label_w - 80000
    bar_x = x + label_w + 80000

    xml = ""
    for i, cat in enumerate(categories):
        by = y + i * (bar_h + gap)
        xml += txtbox(x, by, label_w, bar_h,
                      para(run(cat, sz=1200, bold=True, color=label_color,
                               font="Helvetica Neue Condensed Bold"), algn="r"), anchor="ctr")
        cx = bar_x
        for si, sname in enumerate(series_names):
            val = data_by_series[sname][i]
            if val <= 0: continue
            seg_w = max(2, int(bar_area_w * val / max_total))
            xml += rect_sh(cx, by, seg_w, bar_h, colors[si])
            cx += seg_w
        xml += txtbox(bar_x + int(bar_area_w * row_totals[i] / max_total) + 40000,
                      by, 1200000, bar_h,
                      para(run(f"${row_totals[i]/1e6:,.0f} M", sz=1100, bold=True,
                               color=val_color, font="Helvetica Neue"), algn="l"), anchor="ctr")
    return xml
```

### Barras horizontales 100% apiladas

```python
def bars_100pct_h(data, x, y, w, h, colors_pair, bg,
                  label_color=None, label_w=1200000, gap_ratio=0.4):
    """data = [(label, [pct_seg1, pct_seg2, ...]), ...]"""
    if not label_color: label_color = WHITE if bg == BLUE else BLUE

    gap = int(h / len(data) * gap_ratio)
    bar_h = int((h - gap * (len(data) - 1)) / len(data))
    bar_area_w = w - label_w - 80000
    bar_x = x + label_w + 80000

    xml = ""
    for i, (label, pcts) in enumerate(data):
        by = y + i * (bar_h + gap)
        xml += txtbox(x, by, label_w, bar_h,
                      para(run(label, sz=1200, bold=True, color=label_color,
                               font="Helvetica Neue Condensed Bold"), algn="r"), anchor="ctr")
        cx = bar_x
        for si, pct in enumerate(pcts):
            seg_w = max(2, int(bar_area_w * pct / 100))
            xml += rect_sh(cx, by, seg_w, bar_h, colors_pair[si])
            tc = WHITE if colors_pair[si] == BLUE else BLUE
            if seg_w > 600000:
                xml += txtbox(cx + 40000, by, seg_w - 80000, bar_h,
                              para(run(f"{pct:.0f}%", sz=1100, bold=True, color=tc,
                                       font="Helvetica Neue"), algn="ctr"), anchor="ctr")
            cx += seg_w
    return xml
```

### Barras horizontales simples (una serie)

```python
def bars_h_simple(data, x, y, w, h, bar_color, bg,
                  label_color=None, val_color=None,
                  label_w=1200000, gap_ratio=0.3):
    """data = [(label, value), ...]"""
    if not label_color: label_color = WHITE if bg == BLUE else BLUE
    if not val_color:   val_color   = YELLOW if bg == BLUE else BLUE

    max_v = max(v for _, v in data) if data else 1
    gap = int(h / len(data) * gap_ratio)
    bar_h = int((h - gap * (len(data) - 1)) / len(data))
    bar_area_w = w - label_w - 80000
    bar_x = x + label_w + 80000

    xml = ""
    for i, (label, val) in enumerate(data):
        by = y + i * (bar_h + gap)
        bw = max(2, int(bar_area_w * val / max_v))
        xml += rect_sh(bar_x, by, bar_area_w, bar_h, LGRAY)   # track gris
        xml += rect_sh(bar_x, by, bw, bar_h, bar_color)
        xml += txtbox(x, by, label_w, bar_h,
                      para(run(label, sz=1050, color=label_color, font="Helvetica Neue"),
                           algn="r"), anchor="ctr")
        xml += txtbox(bar_x + bw + 50000, by, 1800000, bar_h,
                      para(run(f"${val/1e6:,.0f} M", sz=1050, bold=True,
                               color=val_color, font="Helvetica Neue"), algn="l"), anchor="ctr")
    return xml
```

### Leyenda horizontal

```python
def legend_row(items, x, y, swatch_w=160000, swatch_h=160000, gap=600000,
               text_color=WHITE, sz=900):
    """items = [(color_hex, label), ...]"""
    xml = ""
    cx = x
    for color, label in items:
        xml += rect_sh(cx, y, swatch_w, swatch_h, color)
        xml += txtbox(cx + swatch_w + 60000, y - 20000, gap - swatch_w - 100000, swatch_h + 40000,
                      para(run(label, sz=sz, color=text_color, font="Helvetica Neue"), algn="l"),
                      anchor="ctr")
        cx += gap
    return xml
```

---

## Ensamblado del ZIP

```python
def build_pptx(slides_xml_list, media_files, image_rids, output_path, template_path):
    """
    slides_xml_list: lista de strings XML (una por slide)
    media_files: dict { media_filename: bytes_or_path }
    image_rids: dict { rid: media_filename }  (para slide_rels_xml)
    """
    with zipfile.ZipFile(template_path, "r") as src:
        src_names = src.namelist()

        with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as out:
            # Copiar todo del template excepto slides/charts/embeddings/presentation/content_types
            skip = {f for f in src_names
                    if (f.startswith("ppt/slides/") or
                        f.startswith("ppt/charts/") or
                        f.startswith("ppt/embeddings/") or
                        f in ("ppt/presentation.xml",
                              "ppt/_rels/presentation.xml.rels",
                              "[Content_Types].xml"))}
            for f in src_names:
                if f not in skip:
                    out.writestr(f, src.read(f))

            # Inyectar imágenes
            for media_name, source in media_files.items():
                if isinstance(source, (str, bytes)):
                    data = open(source, "rb").read() if isinstance(source, str) else source
                    out.writestr(f"ppt/media/{media_name}", data)

            # Escribir slides
            rels = slide_rels_xml(image_rids)
            for i, xml in enumerate(slides_xml_list, start=1):
                out.writestr(f"ppt/slides/slide{i}.xml", xml)
                out.writestr(f"ppt/slides/_rels/slide{i}.xml.rels", rels)

            n = len(slides_xml_list)

            # presentation.xml — actualizar sldIdLst
            pres = src.read("ppt/presentation.xml").decode()
            sld_ids = "".join(
                f'<p:sldId id="{255+i}" r:id="rId{100+i}"/>' for i in range(1, n+1))
            pres = re.sub(r'<p:sldIdLst>.*?</p:sldIdLst>',
                          f'<p:sldIdLst>{sld_ids}</p:sldIdLst>', pres, flags=re.S)
            out.writestr("ppt/presentation.xml", pres)

            # presentation.xml.rels — reemplazar slide rels
            pr_rels = src.read("ppt/_rels/presentation.xml.rels").decode()
            pr_rels = re.sub(r'<Relationship [^>]*relationships/slide"[^>]*/>', '', pr_rels)
            pr_rels = re.sub(r'<Relationship [^>]*relationships/chart"[^>]*/>', '', pr_rels)
            new_rels = "".join(
                f'<Relationship Id="rId{100+i}" '
                f'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" '
                f'Target="slides/slide{i}.xml"/>' for i in range(1, n+1))
            pr_rels = pr_rels.replace("</Relationships>", new_rels + "</Relationships>")
            out.writestr("ppt/_rels/presentation.xml.rels", pr_rels)

            # [Content_Types].xml — limpiar slides/charts/embeddings viejos, agregar nuevos
            ct = src.read("[Content_Types].xml").decode()
            ct = re.sub(r'<Override PartName="/ppt/slides/slide[^>]*/>', '', ct)
            ct = re.sub(r'<Override PartName="/ppt/charts/[^>]*/>', '', ct)
            ct = re.sub(r'<Override PartName="/ppt/embeddings/[^>]*/>', '', ct)
            new_ct = "".join(
                f'<Override PartName="/ppt/slides/slide{i}.xml" '
                f'ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>'
                for i in range(1, n+1))
            for media_name in media_files:
                ext = media_name.rsplit(".", 1)[-1].lower()
                mime = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg"}.get(ext, "image/png")
                new_ct += f'<Override PartName="/ppt/media/{media_name}" ContentType="{mime}"/>'
            ct = ct.replace("</Types>", new_ct + "</Types>")
            out.writestr("[Content_Types].xml", ct)
```

> **Validación post-generación**: verificar que el PPTX no tenga `ppt/embeddings/` ni `ppt/charts/` antes de entregar.

```python
import zipfile, re
z = zipfile.ZipFile(output_path)
files = z.namelist()
assert not [f for f in files if "embedding" in f or f.startswith("ppt/charts/")], "Embeddings encontrados!"
ct = z.read("[Content_Types].xml").decode()
bad = re.findall(r'<Override [^>]*(chart|embedding)[^>]*/>', ct)
assert not bad, f"Bad overrides: {bad}"
```

---

## Logos — proporciones reales

Siempre usar `logo_h = int(logo_w / ratio)` con el ratio real medido del archivo:

| Archivo | Dimensiones | Ratio (w/h) | Fondo transparente |
|---|---|---|---|
| `marca/logo/corona-logo-white-yellow.png` | 440×266 | **1.654** | ✓ |
| `marca/logo/corona-logo-color.png` | 439×266 | **1.650** | ✓ |
| `marca/logo/corona-logo-blue.png` | 1191×842 | **1.414** | ✓ |
| `corona-cero/logo/corona-cero-logo-white.png` | 1719×1068 | **1.610** | ✓ |
| `corona-sunsets/logo/corona-sunset-sessions-logo-white-yellow.png` | 2430×2071 | **1.173** | ✓ |
| `corona-sunsets/logo/corona-sunsets-logo-fade.png` | 2560×1440 | 1.778 | ✗ — fondo gris #D3D3D3 bakeado |
| `this-is-living/corona-this-is-living-lockup-white.png` | 6390×3125 | **2.045** | ✓ |
| `this-is-living/this-is-living-tagline-clean-white.png` | 10453×2289 | **4.567** | ✓ |

> ⚠️ `corona-sunsets-logo-fade.png` tiene fondo gris sólido — usar `corona-sunset-sessions-logo-white-yellow.png` en su lugar.

Leer las dimensiones de cualquier PNG nuevo antes de usar:

```python
import struct
def png_dims(path):
    with open(path, 'rb') as f:
        f.read(16)
        return struct.unpack('>II', f.read(8))  # (width, height)

w, h = png_dims(logo_path)
ratio = w / h
logo_h = int(logo_w / ratio)
```

---

## Reglas de texto

- `sz` en centésimas de punto (1800 = 18pt, 2800 = 28pt).
- `anchor="ctr"` para alinear verticalmente al centro de un txtbox.
- Para headlines: `sz=2600–5600`, `bold=True`, `font="Helvetica Neue Condensed Bold"`, texto en mayúsculas.
- Para body: `sz=1000–1200`, `font="Helvetica Neue"`.
- Nunca inventar colores fuera de `BLUE`, `WHITE`, `YELLOW` para contenido de marca (gris solo para tracks/gridlines/placeholders).

---

## Referencia: `validar_presentacion` y `fix_content_types` (solo para python-pptx + add_chart)

Estas funciones son relevantes **únicamente** si se usa el enfoque legacy con python-pptx + `add_chart`. Con el enfoque XML directo descrito arriba, no son necesarias porque no hay charts ni embeddings.

```python
# validar_presentacion(prs) — corrige IDs duplicados, relaciones huérfanas,
#   placeholders vacíos, axis IDs negativos, doble marker en lineChart,
#   spPr fuera de orden en barChart, numFmt en showPercent, y orientación de eje.
# Llamar antes de prs.save(output_path).

# fix_content_types(output_path) — agrega Override explícitos para xlsx embebidos.
# Llamar inmediatamente después de prs.save(output_path).
# Nota: incluso con esta función, PowerPoint puede mostrar el diálogo de reparación.
# La solución definitiva es usar el enfoque XML directo (sin add_chart).
```
