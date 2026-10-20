/*
  Influencer Audience Report PPTX Generator
  ----------------------------------------
  Purpose:
    Generate a fully editable PowerPoint deck from REPORT_DATA.

  Expected input:
    The same REPORT_DATA object used by the HTML report:
    {
      title: string,
      subtitle: string,
      generatedAt: string,
      creators: [
        {
          publisherId: string,
          name: string,
          inputInstagramHandle: string,
          whoIs: string,
          recentPartnerships: [{ brand, description, source, date }],
          networks: [
            {
              network: "instagram" | "tiktok" | "facebook" | "twitter" | ...,
              handle: string,
              followers: number,
              engagementRate: number,
              avgLikesPerPost: number | null,
              avgCommentsPerPost: number | null,
              avgViewsPerPost: number | null,
              verified: boolean,
              dateSocialStatsUpdated: string,
              history: { supported: boolean, period: "month", points: [{ label, followers, views }] },
              audience: {
                gender: [{ label, percentage }],
                age: [{ label, percentage }],
                countries: [{ label, percentage }],
                cities: [{ label, percentage }],
                interests: [{ label, percentage }],
                brands: [{ label, percentage }],
                audienceCredibility: number | null,
                timestamp: number | null
              } | null
            }
          ]
        }
      ]
    }

  Usage as CLI:
    npm install pptxgenjs jszip
    node pptx_report_generator.js report-data.json influencer-audience-report.pptx

  The input can also be an HTML file containing:
    <script id="report-data" type="application/json"> ... </script>
*/

const fs = require("fs");
const path = require("path");
const JSZip = require("jszip");
const pptxgen = require("pptxgenjs");
const { ShapeType: SHAPE_TYPE } = new pptxgen();

const THEME = {
  ink: "111827",
  muted: "667085",
  muted2: "98A2B3",
  line: "E4E7EC",
  lineSoft: "EEF1F5",
  panel: "F3F3F3",
  card: "FFFFFF",
  blue: "3D8FE8",
  blueSoft: "D7E9FB",
  orange: "F4AA2A",
  orangeSoft: "FFF0CE",
  green: "1F9D6D",
  white: "FFFFFF",
  danger: "F04438",
  purple: "7F56D9",
};

const LAYOUT = {
  w: 13.333,
  h: 7.5,
  margin: 0.35,
  leftX: 0.55,
  leftW: 5.35,
  rightX: 6.15,
  rightW: 6.65,
};

const NETWORK_ORDER = [
  "instagram",
  "tiktok",
  "youtube",
  "facebook",
  "twitter",
  "twitch",
  "pinterest",
  "snapchat",
  "web",
];

const WARNING_ICON_FILENAME = "warning(1).png";

function resolveOptionalAsset(filename) {
  const candidates = [
    path.join(__dirname, filename),
    path.join(process.cwd(), filename),
  ];

  for (const candidate of candidates) {
    try {
      if (
        fs.existsSync(candidate) &&
        fs.statSync(candidate).isFile()
      ) {
        return candidate;
      }
    } catch (_) {}
  }

  return null;
}

const WARNING_ICON_PATH = resolveOptionalAsset(WARNING_ICON_FILENAME);
let didWarnMissingWarningIcon = false;

const LOGO_FILENAME = "creatoriq-logo.png";
const LOGO_PATH = resolveOptionalAsset(LOGO_FILENAME);
const LOGO_ASPECT = 124 / 24; // from the SVG viewBox 0 0 124 24
let didWarnMissingLogo = false;

function addLogo(slide, x, y, width) {
  if (LOGO_PATH) {
    slide.addImage({
      path: LOGO_PATH,
      x,
      y,
      w: width,
      h: width / LOGO_ASPECT,
    });
  } else if (!didWarnMissingLogo) {
    console.warn(
      `Optional asset ${LOGO_FILENAME} was not found. ` +
        `The CreatorIQ logo will be omitted.`
    );
    didWarnMissingLogo = true;
  }
}

function addWarningIcon(slide, x, y, size = 0.15) {
  if (WARNING_ICON_PATH) {
    slide.addImage({
      path: WARNING_ICON_PATH,
      x,
      y,
      w: size,
      h: size,
    });
    return;
  }

  if (!didWarnMissingWarningIcon) {
    console.warn(
      `Optional asset ${WARNING_ICON_FILENAME} was not found. ` +
      `The "Puntos a discutir" icon will be omitted.`
    );
    didWarnMissingWarningIcon = true;
  }
}

function safeText(value, fallback = "") {
  if (value === null || value === undefined) return fallback;
  return String(value).replace(/\s+/g, " ").trim();
}

function cleanHandle(value) {
  return safeText(value).replace(/^@+/, "").trim();
}

function isFiniteNumber(value) {
  return (
    value !== null &&
    value !== undefined &&
    value !== "" &&
    Number.isFinite(Number(value))
  );
}

function formatCompact(value) {
  if (!isFiniteNumber(value)) return "—";

  const n = Number(value);
  const abs = Math.abs(n);

  if (abs >= 1e9) {
    return `${(n / 1e9).toFixed(abs >= 1e10 ? 0 : 1)}B`;
  }

  if (abs >= 1e6) {
    return `${(n / 1e6).toFixed(abs >= 1e7 ? 0 : 1)}M`;
  }

  if (abs >= 1e3) {
    return `${(n / 1e3).toFixed(abs >= 1e5 ? 0 : 1)}K`;
  }

  return new Intl.NumberFormat("en-US", {
    maximumFractionDigits: 0,
  }).format(n);
}

function formatInteger(value) {
  if (!isFiniteNumber(value)) return "—";

  const n = Number(value);

  return new Intl.NumberFormat("en-US", {
    maximumFractionDigits: 0,
  }).format(n);
}

function formatPct(value, digits = 1) {
  if (!isFiniteNumber(value)) return "—";

  const n = Number(value);
  return `${n.toFixed(digits)}%`;
}

function formatRate(value) {
  if (!isFiniteNumber(value)) return "—";

  const n = Number(value);
  const pct = Math.abs(n) <= 1 ? n * 100 : n;

  return `${pct.toFixed(2)}%`;
}

function titleCaseNetwork(network) {
  const n = safeText(network).toLowerCase();

  const map = {
    instagram: "Instagram",
    tiktok: "TikTok",
    youtube: "YouTube",
    facebook: "Facebook",
    twitter: "X / Twitter",
    twitch: "Twitch",
    pinterest: "Pinterest",
    snapchat: "Snapchat",
    web: "Website",
  };

  return map[n] || (
    n
      ? n[0].toUpperCase() + n.slice(1)
      : "Network"
  );
}

function networkRank(network) {
  const idx = NETWORK_ORDER.indexOf(
    safeText(network).toLowerCase()
  );

  return idx >= 0 ? idx : 999;
}

function isMeaningfulNetwork(network) {
  const n = safeText(network.network).toLowerCase();

  if (n !== "web") return true;

  const hasFollowers =
    Number.isFinite(Number(network.followers)) &&
    Number(network.followers) > 0;

  const hasAudience = !!network.audience;

  const hasHistory = !!(
    network.history &&
    network.history.supported &&
    Array.isArray(network.history.points) &&
    network.history.points.length
  );

  return hasFollowers || hasAudience || hasHistory;
}

function monthValue(label) {
  const s = safeText(label);

  const m = s.match(
    /^([A-Za-zÁÉÍÓÚáéíóú]+)\s+(\d{4})$/
  );

  if (!m) return NaN;

  const months = {
    january: 0,
    enero: 0,
    janeiro: 0,

    february: 1,
    febrero: 1,
    fevereiro: 1,

    march: 2,
    marzo: 2,
    marco: 2,
    março: 2,

    april: 3,
    abril: 3,

    may: 4,
    mayo: 4,
    maio: 4,

    june: 5,
    junio: 5,
    junho: 5,

    july: 6,
    julio: 6,
    julho: 6,

    august: 7,
    agosto: 7,

    september: 8,
    septiembre: 8,
    setembro: 8,

    october: 9,
    octubre: 9,
    outubro: 9,

    november: 10,
    noviembre: 10,
    novembro: 10,

    december: 11,
    diciembre: 11,
    dezembro: 11,
  };

  const month = months[m[1].toLowerCase()];

  return Number.isInteger(month)
    ? Number(m[2]) * 12 + month
    : NaN;
}

function chronologicalHistory(points) {
  const arr = Array.isArray(points)
    ? points.filter(
        (p) =>
          p &&
          Number.isFinite(Number(p.followers))
      )
    : [];

  const sortable = arr.every(
    (p) => Number.isFinite(monthValue(p.label))
  );

  return [...arr].sort(
    (a, b) =>
      sortable
        ? monthValue(a.label) - monthValue(b.label)
        : 0
  );
}

function shortMonth(label) {
  const s = safeText(label);
  const first = s.split(/\s+/)[0] || s;

  const map = {
    January: "Ene",
    February: "Feb",
    March: "Mar",
    April: "Abr",
    May: "May",
    June: "Jun",
    July: "Jul",
    August: "Ago",
    September: "Sep",
    October: "Oct",
    November: "Nov",
    December: "Dic",

    Enero: "Ene",
    Febrero: "Feb",
    Marzo: "Mar",
    Abril: "Abr",
    Mayo: "May",
    Junio: "Jun",
    Julio: "Jul",
    Agosto: "Ago",
    Septiembre: "Sep",
    Octubre: "Oct",
    Noviembre: "Nov",
    Diciembre: "Dic",
  };

  return map[first] || first.slice(0, 3);
}

function firstN(items, n) {
  return Array.isArray(items)
    ? items.filter(Boolean).slice(0, n)
    : [];
}

function validPctItems(items, maxItems = 10) {
  return firstN(items, maxItems).filter(
    (x) => x && isFiniteNumber(x.percentage)
  );
}

function initials(name) {
  const parts = safeText(name, "?")
    .split(/\s+/)
    .filter(Boolean)
    .slice(0, 2);

  return (
    parts
      .map((x) => x[0])
      .join("")
      .toUpperCase() || "?"
  );
}

function hyperlinkOrUndefined(url) {
  if (!url) return undefined;

  try {
    const u = new URL(String(url));

    if (
      u.protocol === "http:" ||
      u.protocol === "https:"
    ) {
      return { url: u.href };
    }
  } catch (_) {}

  return undefined;
}

function addText(
  slide,
  text,
  x,
  y,
  w,
  h,
  opts = {}
) {
  slide.addText(
    safeText(text),
    {
      x,
      y,
      w,
      h,
      fontFace: opts.fontFace || "Aptos",
      fontSize: opts.fontSize || 12,
      color: opts.color || THEME.ink,
      bold: !!opts.bold,
      italic: !!opts.italic,
      valign: opts.valign || "top",
      breakLine: false,
      fit: opts.fit || "shrink",
      margin:
        opts.margin === undefined
          ? 0.04
          : opts.margin,
      hyperlink: opts.hyperlink,
      align: opts.align,
      bullet: opts.bullet,
      paraSpaceAfterPt: opts.paraSpaceAfterPt,
    }
  );
}

function addSectionLabel(
  slide,
  text,
  x,
  y,
  w
) {
  addText(
    slide,
    text.toUpperCase(),
    x,
    y,
    w,
    0.18,
    {
      fontSize: 7.5,
      bold: true,
      color: THEME.ink,
    }
  );
}

function addCard(
  slide,
  x,
  y,
  w,
  h,
  fill = THEME.card,
  line = THEME.lineSoft
) {
  slide.addShape(
    SHAPE_TYPE.roundRect,
    {
      x,
      y,
      w,
      h,
      rectRadius: 0.04,
      fill: {
        color: fill,
      },
      line: {
        color: line,
        width: 0.75,
      },
    }
  );
}

function addMissing(
  slide,
  message,
  x,
  y,
  w,
  h
) {
  slide.addShape(
    SHAPE_TYPE.roundRect,
    {
      x,
      y,
      w,
      h,
      rectRadius: 0.05,
      fill: {
        color: "FFFFFF",
        transparency: 10,
      },
      line: {
        color: "CFD5DD",
        width: 0.8,
        dash: "dash",
      },
    }
  );

  addText(
    slide,
    message,
    x + 0.12,
    y + h / 2 - 0.12,
    w - 0.24,
    0.25,
    {
      fontSize: 9,
      color: THEME.muted,
      italic: true,
      align: "center",
    }
  );
}

function addHeader(
  slide,
  reportData,
  creator,
  network,
  slideNumber,
  totalSlides
) {
  slide.addShape(
    SHAPE_TYPE.rect,
    {
      x: 0,
      y: 0,
      w: LAYOUT.w,
      h: 0.42,
      fill: {
        color: THEME.white,
      },
      line: {
        color: THEME.line,
        width: 0.7,
      },
    }
  );

  addLogo(slide, 0.26, 0.09, 1.1);

  addText(
    slide,
    reportData.title ||
      "Influencer Audience Report",
    1.5,
    0.12,
    1.6,
    0.15,
    {
      fontSize: 7.3,
      bold: true,
      color: THEME.ink,
    }
  );

  addText(
    slide,
    reportData.subtitle ||
      "Audience intelligence",
    1.5,
    0.26,
    1.6,
    0.12,
    {
      fontSize: 6.6,
      color: THEME.muted,
    }
  );

  const networkLabel =
    titleCaseNetwork(network.network);

  addText(
    slide,
    `${safeText(
      creator.name,
      "Creator"
    )} — ${networkLabel}`,
    3.15,
    0.11,
    5.25,
    0.22,
    {
      fontSize: 10.5,
      bold: true,
      color: THEME.ink,
      align: "center",
    }
  );

  const handle = cleanHandle(
    network.handle ||
    creator.inputInstagramHandle
  );

  addText(
    slide,
    handle
      ? `@${handle}`
      : networkLabel,
    8.7,
    0.12,
    1.75,
    0.17,
    {
      fontSize: 7.8,
      bold: true,
      color: THEME.muted,
      align: "right",
    }
  );

  addText(
    slide,
    `${slideNumber}/${totalSlides}`,
    12.35,
    0.14,
    0.55,
    0.15,
    {
      fontSize: 7,
      color: THEME.muted2,
      align: "right",
    }
  );
}

function addProfilePane(
  slide,
  creator
) {
  const x = LAYOUT.leftX;
  const w = LAYOUT.leftW;
  const y = 0.68;

  addText(
    slide,
    creator.name ||
      `@${cleanHandle(
        creator.inputInstagramHandle
      )}`,
    x,
    y,
    w,
    0.42,
    {
      fontSize: 22,
      bold: true,
      color: THEME.ink,
    }
  );

  const handle = cleanHandle(
    creator.inputInstagramHandle
  );

  addText(
    slide,
    handle ? `@${handle}` : "",
    x,
    y + 0.47,
    w,
    0.18,
    {
      fontSize: 8.5,
      color: THEME.muted,
    }
  );

  /*
    El panel gris original fue ampliado verticalmente
    para contener tres bloques:

    - Quién es
    - Objetivo de uso
    - Puntos a discutir

    Los dos últimos son placeholders editables y
    deliberadamente no se completan automáticamente.
  */

  const cardY = y + 0.88;
  const cardH = 2.86;

  const contentX = x + 0.18;
  const contentW = w - 0.36;

  addCard(
    slide,
    x,
    cardY,
    w,
    cardH,
    "F0F0F0",
    "F0F0F0"
  );

  /*
    QUIÉN ES
  */
  addSectionLabel(
    slide,
    "Quién es",
    contentX,
    cardY + 0.16,
    contentW
  );

  addText(
    slide,
    creator.whoIs ||
      "Descripción no disponible.",
    contentX,
    cardY + 0.40,
    contentW,
    0.92,
    {
      fontSize: 9.2,
      color: THEME.ink,
      fit: "shrink",
    }
  );

  /*
    OBJETIVO DE USO
  */
  addSectionLabel(
    slide,
    "Objetivo de uso",
    contentX,
    cardY + 1.45,
    contentW
  );

  addText(
    slide,
    "(Completar)",
    contentX,
    cardY + 1.70,
    contentW,
    0.28,
    {
      fontSize: 8.4,
      color: THEME.muted2,
      italic: true,
      align: "center",
      valign: "mid",
    }
  );

  /*
    PUNTOS A DISCUTIR
  */
  const discussLabelY =
    cardY + 2.08;

  addSectionLabel(
    slide,
    "Puntos a discutir",
    contentX,
    discussLabelY,
    1.45
  );

  /*
    El icono se busca con el nombre exacto:
    warning(1).png

    Se ubica junto al título y se mantiene pequeño
    para que quede visualmente alineado con el label.
  */
  addWarningIcon(
    slide,
    contentX + 1.43,
    discussLabelY - 0.005,
    0.15
  );

  addText(
    slide,
    "(Completar)",
    contentX,
    cardY + 2.33,
    contentW,
    0.28,
    {
      fontSize: 8.4,
      color: THEME.muted2,
      italic: true,
      align: "center",
      valign: "mid",
    }
  );

  /*
    Colaboraciones recientes comienza debajo del
    panel gris ampliado.
  */
  const pY =
    cardY + cardH + 0.17;

  addSectionLabel(
    slide,
    "Colaboraciones recientes",
    x + 0.72,
    pY,
    w - 0.9
  );

  const partnerships =
    firstN(
      creator.recentPartnerships,
      4
    );

  if (!partnerships.length) {
    addText(
      slide,
      "No se encontraron colaboraciones recientes verificables.",
      x,
      pY + 0.32,
      w,
      0.3,
      {
        fontSize: 8.6,
        color: THEME.muted,
        italic: true,
      }
    );

    return;
  }

  partnerships.forEach(
    (p, i) => {
      /*
        Se reduce levemente la distancia vertical
        entre colaboraciones para que sigan entrando
        cuatro filas después de bajar esta sección.
      */
      const rowY =
        pY + 0.33 + i * 0.55;

      slide.addShape(
        SHAPE_TYPE.ellipse,
        {
          x,
          y: rowY,
          w: 0.42,
          h: 0.42,
          fill: {
            color: "FAFAFA",
          },
          line: {
            color: THEME.line,
            width: 0.7,
          },
        }
      );

      addText(
        slide,
        initials(p.brand),
        x + 0.04,
        rowY + 0.14,
        0.34,
        0.11,
        {
          fontSize: 7,
          bold: true,
          color: "525866",
          align: "center",
        }
      );

      addText(
        slide,
        p.brand || "Marca",
        x + 0.58,
        rowY + 0.03,
        w - 0.75,
        0.16,
        {
          fontSize: 8.8,
          bold: true,
          color: THEME.ink,
        }
      );

      addText(
        slide,
        p.description || "",
        x + 0.58,
        rowY + 0.22,
        w - 1.2,
        0.15,
        {
          fontSize: 7.5,
          color: "202632",
        }
      );

      const link =
        hyperlinkOrUndefined(
          p.source
        );

      if (link) {
        addText(
          slide,
          "fuente ↗",
          x + w - 0.65,
          rowY + 0.22,
          0.55,
          0.14,
          {
            fontSize: 6.7,
            color: THEME.muted,
            hyperlink: link,
          }
        );
      }
    }
  );
}

function addMetricPills(
  slide,
  network,
  x,
  y,
  w
) {
  const metrics = [];

  metrics.push([
    "Seguidores",
    formatCompact(network.followers),
  ]);

  if (
    isFiniteNumber(
      network.engagementRate
    )
  ) {
    metrics.push([
      "Interacción",
      formatRate(
        network.engagementRate
      ),
    ]);
  }

  if (
    isFiniteNumber(
      network.avgLikesPerPost
    )
  ) {
    metrics.push([
      "Prom. Me gusta",
      formatCompact(
        network.avgLikesPerPost
      ),
    ]);
  }

  if (
    isFiniteNumber(
      network.avgViewsPerPost
    )
  ) {
    metrics.push([
      "Prom. vistas",
      formatCompact(
        network.avgViewsPerPost
      ),
    ]);
  }

  const pillW =
    w /
      Math.min(
        4,
        Math.max(
          1,
          metrics.length
        )
      ) -
    0.06;

  metrics
    .slice(0, 4)
    .forEach(
      (m, i) => {
        const px =
          x +
          i *
            (pillW + 0.08);

        slide.addShape(
          SHAPE_TYPE.roundRect,
          {
            x: px,
            y,
            w: pillW,
            h: 0.52,
            rectRadius: 0.08,
            fill: {
              color: THEME.white,
            },
            line: {
              color:
                THEME.lineSoft,
              width: 0.8,
            },
          }
        );

        addText(
          slide,
          m[0].toUpperCase(),
          px + 0.08,
          y + 0.08,
          pillW - 0.16,
          0.12,
          {
            fontSize: 5.8,
            bold: true,
            color: THEME.muted,
          }
        );

        addText(
          slide,
          m[1],
          px + 0.08,
          y + 0.23,
          pillW - 0.16,
          0.18,
          {
            fontSize: 12.2,
            bold: true,
            color: THEME.ink,
          }
        );
      }
    );
}

function addFollowerHistoryChart(
  pptx,
  slide,
  network,
  x,
  y,
  w,
  h
) {
  addCard(
    slide,
    x,
    y,
    w,
    h
  );

  addText(
    slide,
    "EVOLUCIÓN DE SEGUIDORES (6 MESES)",
    x + 0.14,
    y + 0.11,
    w - 0.28,
    0.14,
    {
      fontSize: 6.5,
      bold: true,
      color: THEME.muted,
    }
  );

  const points =
    chronologicalHistory(
      network.history &&
        network.history.points
    );

  if (
    !(
      network.history &&
      network.history.supported
    ) ||
    points.length < 2
  ) {
    addMissing(
      slide,
      (
        network.history &&
        network.history.reason
      ) ||
        "Historial de seguidores no disponible",
      x + 0.25,
      y + 0.48,
      w - 0.5,
      h - 0.75
    );

    return;
  }

  const labels =
    points.map(
      (p) =>
        shortMonth(p.label)
    );

  const values =
    points.map(
      (p) =>
        Number(p.followers)
    );

  const maxFollowers =
    Math.max(
      ...values.map(
        (value) =>
          Math.abs(value)
      )
    );

  const axisFormat =
    maxFollowers >= 1e6
      ? '0.00,,"M"'
      : maxFollowers >= 1e3
      ? '0.0,"K"'
      : "0";

  slide.addChart(
    pptx.ChartType.line,
    [
      {
        name: "Seguidores",
        labels,
        values,
      },
    ],
    {
      x: x + 0.18,
      y: y + 0.35,
      w: w - 0.32,
      h: h - 0.45,

      showLegend: false,
      showTitle: false,
      showValue: false,

      catAxisLabelFontFace:
        "Aptos",

      catAxisLabelFontSize:
        6,

      valAxisLabelFontFace:
        "Aptos",

      valAxisLabelFontSize:
        6,

      valAxisLabelFormatCode:
        axisFormat,

      valAxisMajorGridLines:
        true,

      valAxisMinVal:
        Math.min(...values) *
        0.985,

      valAxisMaxVal:
        Math.max(...values) *
        1.015,

      lineSize: 2,

      chartColors: [
        THEME.blue,
      ],

      showCatName: false,
      showValAxis: true,
      showCatAxis: true,
    }
  );
}

function addGenderChart(
  pptx,
  slide,
  audience,
  x,
  y,
  w,
  h
) {
  addCard(
    slide,
    x,
    y,
    w,
    h
  );

  addText(
    slide,
    "GÉNERO",
    x + 0.12,
    y + 0.1,
    w - 0.24,
    0.14,
    {
      fontSize: 6.6,
      bold: true,
      color: THEME.muted,
    }
  );

  const items =
    validPctItems(
      audience &&
        audience.gender,
      5
    );

  if (!items.length) {
    addMissing(
      slide,
      "Datos de género no disponibles",
      x + 0.16,
      y + 0.38,
      w - 0.32,
      h - 0.55
    );

    return;
  }

  slide.addChart(
    pptx.ChartType.doughnut,
    [
      {
        name: "Gender",
        labels:
          items.map(
            (i) => i.label
          ),
        values:
          items.map(
            (i) =>
              Number(
                i.percentage
              )
          ),
      },
    ],
    {
      x: x + 0.05,
      y: y + 0.3,
      w: w * 0.54,
      h: h - 0.45,

      holeSize: 58,

      showLegend: false,
      showValue: false,

      chartColors: [
        THEME.blue,
        THEME.orange,
        THEME.purple,
        THEME.green,
        THEME.danger,
      ],

      dataLabelPosition:
        "bestFit",
    }
  );

  const legendX =
    x + w * 0.56;

  items.forEach(
    (item, i) => {
      const yy =
        y +
        0.45 +
        i * 0.28;

      const colors = [
        THEME.blue,
        THEME.orange,
        THEME.purple,
        THEME.green,
        THEME.danger,
      ];

      slide.addShape(
        SHAPE_TYPE.ellipse,
        {
          x: legendX,
          y: yy + 0.04,
          w: 0.08,
          h: 0.08,
          fill: {
            color:
              colors[
                i %
                colors.length
              ],
          },
          line: {
            color:
              colors[
                i %
                colors.length
              ],
          },
        }
      );

      addText(
        slide,
        `${formatPct(
          item.percentage
        )} ${item.label}`,
        legendX + 0.13,
        yy,
        w * 0.38,
        0.15,
        {
          fontSize: 6.9,
          color: THEME.muted,
        }
      );
    }
  );
}

function addBarChart(
  pptx,
  slide,
  title,
  items,
  x,
  y,
  w,
  h,
  maxItems = 7
) {
  addCard(
    slide,
    x,
    y,
    w,
    h
  );

  addText(
    slide,
    title.toUpperCase(),
    x + 0.12,
    y + 0.1,
    w - 0.24,
    0.14,
    {
      fontSize: 6.6,
      bold: true,
      color: THEME.muted,
    }
  );

  const vals =
    validPctItems(
      items,
      maxItems
    );

  if (!vals.length) {
    addMissing(
      slide,
      `Datos de ${title.toLowerCase()} no disponibles`,
      x + 0.16,
      y + 0.38,
      w - 0.32,
      h - 0.55
    );

    return;
  }

  slide.addChart(
    pptx.ChartType.bar,
    [
      {
        name: title,
        labels:
          vals.map(
            (i) => i.label
          ),
        values:
          vals.map(
            (i) =>
              Number(
                i.percentage
              )
          ),
      },
    ],
    {
      x: x + 0.1,
      y: y + 0.3,
      w: w - 0.16,
      h: h - 0.42,

      showLegend: false,
      showTitle: false,
      showValue: true,
      showCategoryName: false,

      valAxisMinVal: 0,

      valAxisMaxVal:
        Math.max(
          100,
          Math.ceil(
            Math.max(
              ...vals.map(
                (i) =>
                  Number(
                    i.percentage
                  )
              )
            ) / 10
          ) * 10
        ),

      valAxisLabelFontSize:
        5,

      catAxisLabelFontSize:
        5.8,

      dataLabelPosition:
        "outEnd",

      dataLabelFontSize:
        5.8,

      chartColors: [
        THEME.blue,
      ],

      showValAxis: false,
      showCatAxis: true,
    }
  );
}

function addNetworkAnalytics(
  pptx,
  slide,
  network
) {
  const x =
    LAYOUT.rightX;

  const w =
    LAYOUT.rightW;

  const top = 0.68;

  const label =
    titleCaseNetwork(
      network.network
    );

  slide.addShape(
    SHAPE_TYPE.rect,
    {
      x: x - 0.25,
      y: 0.42,
      w:
        LAYOUT.w -
        (x - 0.25),
      h:
        LAYOUT.h -
        0.42,

      fill: {
        color:
          THEME.panel,
      },

      line: {
        color:
          THEME.panel,
      },
    }
  );

  addText(
    slide,
    "ESTRATIFICACIÓN DE RED",
    x,
    top,
    3.5,
    0.18,
    {
      fontSize: 7,
      bold: true,
      color: THEME.ink,
    }
  );

  addText(
    slide,
    `Seguidores en ${label}:`,
    x + 4.15,
    top,
    1.2,
    0.12,
    {
      fontSize: 6.5,
      bold: true,
      color: THEME.ink,
      align: "right",
    }
  );

  addText(
    slide,
    formatCompact(
      network.followers
    ),
    x + 5.35,
    top - 0.02,
    1.15,
    0.22,
    {
      fontSize: 14,
      bold: true,
      color: THEME.ink,
      align: "right",
    }
  );

  const handle =
    cleanHandle(
      network.handle
    );

  addText(
    slide,
    handle
      ? `@${handle}`
      : label,
    x,
    top + 0.28,
    2.15,
    0.16,
    {
      fontSize: 7.6,
      bold: true,
      color: "4F5866",
    }
  );

  let bx = x + 2.05;

  if (
    network.audience
  ) {
    addBadge(
      slide,
      "Audiencia disponible",
      bx,
      top + 0.22,
      0.98,
      THEME.blueSoft,
      "286EAD"
    );

    bx += 1.05;
  }

  if (
    network.audience &&
    isFiniteNumber(
      network.audience
        .audienceCredibility
    )
  ) {
    addBadge(
      slide,
      `Credibilidad ${formatPct(
        network.audience
          .audienceCredibility
      )}`,
      bx,
      top + 0.22,
      1.05,
      THEME.orangeSoft,
      "9A6512"
    );

    bx += 1.13;
  }

  if (
    network.verified
  ) {
    addBadge(
      slide,
      "Verificada",
      bx,
      top + 0.22,
      0.55,
      "FFFFFF",
      "4F5866"
    );
  }

  addMetricPills(
    slide,
    network,
    x,
    top + 0.65,
    w
  );

  addFollowerHistoryChart(
    pptx,
    slide,
    network,
    x,
    top + 1.3,
    4.0,
    2.25
  );

  addGenderChart(
    pptx,
    slide,
    network.audience,
    x + 4.15,
    top + 1.3,
    2.35,
    2.25
  );

  if (
    network.audience
  ) {
    addBarChart(
      pptx,
      slide,
      "Edad",
      network.audience.age,
      x,
      top + 3.78,
      3.05,
      2.35,
      6
    );

    addBarChart(
      pptx,
      slide,
      "Principales países",
      network.audience
        .countries,
      x + 3.25,
      top + 3.78,
      3.25,
      2.35,
      7
    );
  } else {
    addMissing(
      slide,
      "CreatorIQ no devolvió datos demográficos para esta red.",
      x,
      top + 3.85,
      w,
      1.6
    );
  }

  const footerY = 7.12;

  addText(
    slide,
    "Datos de audiencia: CreatorIQ",
    x,
    footerY,
    1.6,
    0.1,
    {
      fontSize: 5.8,
      color: THEME.muted2,
    }
  );

  addText(
    slide,
    "País = ubicación de la audiencia, no ciudadanía ni nacionalidad",
    x + 1.72,
    footerY,
    3.2,
    0.1,
    {
      fontSize: 5.8,
      color: THEME.muted2,
    }
  );
}

function addBadge(
  slide,
  text,
  x,
  y,
  w,
  fill,
  color
) {
  slide.addShape(
    SHAPE_TYPE.roundRect,
    {
      x,
      y,
      w,
      h: 0.19,

      rectRadius: 0.05,

      fill: {
        color: fill,
      },

      line: {
        color:
          THEME.line,
        width: 0.5,
      },
    }
  );

  addText(
    slide,
    text,
    x + 0.04,
    y + 0.045,
    w - 0.08,
    0.07,
    {
      fontSize: 5.3,
      bold: true,
      color,
      align: "center",
    }
  );
}

function addCoverSlide(
  pptx,
  reportData,
  allSlideCount
) {
  const slide =
    pptx.addSlide();

  slide.background = {
    color:
      THEME.white,
  };

  slide.addShape(
    SHAPE_TYPE.rect,
    {
      x: 0,
      y: 0,
      w: LAYOUT.w,
      h: LAYOUT.h,

      fill: {
        color:
          THEME.white,
      },

      line: {
        color:
          THEME.white,
      },
    }
  );

  slide.addShape(
    SHAPE_TYPE.rect,
    {
      x: 7.3,
      y: 0,
      w: 6.03,
      h: 7.5,

      fill: {
        color:
          THEME.panel,
      },

      line: {
        color:
          THEME.panel,
      },
    }
  );

  addLogo(slide, 0.75, 0.72, 1.75);

  addText(
    slide,
    reportData.title ||
      "Influencer Audience Report",
    0.75,
    1.75,
    5.9,
    1.15,
    {
      fontSize: 34,
      bold: true,
      color: THEME.ink,
    }
  );

  addText(
    slide,
    reportData.subtitle ||
      "Audience intelligence",
    0.78,
    3.05,
    4.8,
    0.28,
    {
      fontSize: 15,
      color: THEME.muted,
    }
  );

  addText(
    slide,
    reportData.generatedAt
      ? `Generado: ${safeText(
          reportData.generatedAt
        ).slice(0, 10)}`
      : "",
    0.78,
    3.45,
    4.8,
    0.18,
    {
      fontSize: 8,
      color: THEME.muted2,
    }
  );

  const creators =
    Array.isArray(
      reportData.creators
    )
      ? reportData.creators
      : [];

  const socialSlides =
    Math.max(
      0,
      allSlideCount - 1
    );

  const stats = [
    [
      "Creadores",
      String(
        creators.length
      ),
    ],
    [
      "Láminas de redes",
      String(
        socialSlides
      ),
    ],
    [
      "Gráficos editables",
      "Sí",
    ],
  ];

  stats.forEach(
    (s, i) => {
      const x =
        7.85 +
        (i % 1) * 1.6;

      const y =
        1.2 +
        i * 1.05;

      addCard(
        slide,
        x,
        y,
        3.7,
        0.72,
        THEME.white,
        THEME.lineSoft
      );

      addText(
        slide,
        s[0].toUpperCase(),
        x + 0.2,
        y + 0.14,
        3.3,
        0.12,
        {
          fontSize: 6.2,
          bold: true,
          color: THEME.muted,
        }
      );

      addText(
        slide,
        s[1],
        x + 0.2,
        y + 0.33,
        3.3,
        0.22,
        {
          fontSize: 17,
          bold: true,
          color: THEME.ink,
        }
      );
    }
  );

  addText(
    slide,
    "Contenido",
    7.85,
    4.8,
    1.5,
    0.18,
    {
      fontSize: 8,
      bold: true,
      color: THEME.ink,
    }
  );

  const names =
    creators
      .map(
        (c) =>
          c.name ||
          `@${cleanHandle(
            c.inputInstagramHandle
          )}`
      )
      .join(" · ");

  addText(
    slide,
    names,
    7.85,
    5.12,
    4.3,
    0.75,
    {
      fontSize: 10.5,
      color: THEME.muted,
    }
  );
}

function createNetworkSlide(
  pptx,
  reportData,
  creator,
  network,
  slideNumber,
  totalSlides
) {
  const slide =
    pptx.addSlide();

  slide.background = {
    color:
      THEME.white,
  };

  addHeader(
    slide,
    reportData,
    creator,
    network,
    slideNumber,
    totalSlides
  );

  addProfilePane(
    slide,
    creator
  );

  addNetworkAnalytics(
    pptx,
    slide,
    network
  );

  return slide;
}

function normalizeReportData(
  reportData
) {
  const root =
    reportData &&
    typeof reportData ===
      "object"
      ? reportData
      : {};

  const creators =
    Array.isArray(
      root.creators
    )
      ? root.creators
      : [];

  return {
    title:
      root.title ||
      "Influencer Audience Report",

    subtitle:
      root.subtitle ||
      "Audience intelligence",

    generatedAt:
      root.generatedAt ||
      new Date().toISOString(),

    creators:
      creators
        .map(
          (creator) => ({
            ...creator,

            networks:
              Array.isArray(
                creator.networks
              )
                ? creator.networks
                    .filter(
                      isMeaningfulNetwork
                    )
                    .sort(
                      (
                        a,
                        b
                      ) =>
                        networkRank(
                          a.network
                        ) -
                        networkRank(
                          b.network
                        )
                    )
                : [],

            recentPartnerships:
              Array.isArray(
                creator.recentPartnerships
              )
                ? creator.recentPartnerships
                : [],
          })
        )
        .filter(
          (creator) =>
            creator.networks
              .length > 0
        ),
  };
}

function countNetworkSlides(
  reportData
) {
  return reportData.creators.reduce(
    (sum, c) =>
      sum +
      c.networks.length,
    0
  );
}

async function sanitizePptxPackage(
  outputPath
) {
  const packageBuffer =
    fs.readFileSync(
      outputPath
    );

  const zip =
    await JSZip.loadAsync(
      packageBuffer
    );

  const contentTypesPart =
    zip.file(
      "[Content_Types].xml"
    );

  if (
    !contentTypesPart
  ) {
    throw new Error(
      "Generated PPTX is missing [Content_Types].xml."
    );
  }

  const existingParts =
    new Set(
      Object.entries(
        zip.files
      )
        .filter(
          ([, entry]) =>
            !entry.dir
        )
        .map(
          ([name]) =>
            `/${name
              .replace(
                /^\/+/,
                ""
              )
              .replace(
                /\\/g,
                "/"
              )}`
        )
    );

  const contentTypesXml =
    await contentTypesPart.async(
      "string"
    );

  const removedOverrides =
    [];

  const sanitizedContentTypesXml =
    contentTypesXml.replace(
      /<Override\b[^>]*\bPartName="([^"]+)"[^>]*\/>/g,
      (
        overrideXml,
        partName
      ) => {
        if (
          existingParts.has(
            partName
          )
        ) {
          return overrideXml;
        }

        removedOverrides.push(
          partName
        );

        return "";
      }
    );

  if (
    removedOverrides.length
  ) {
    zip.file(
      "[Content_Types].xml",
      sanitizedContentTypesXml
    );

    const sanitizedPackage =
      await zip.generateAsync(
        {
          type: "nodebuffer",
          compression:
            "DEFLATE",
          compressionOptions: {
            level: 9,
          },
        }
      );

    fs.writeFileSync(
      outputPath,
      sanitizedPackage
    );
  }

  return removedOverrides;
}

async function buildInfluencerAudiencePptx(
  reportDataInput,
  outputPath,
  options = {}
) {
  const reportData =
    normalizeReportData(
      reportDataInput
    );

  if (
    !reportData.creators.length
  ) {
    throw new Error(
      "REPORT_DATA must contain at least one creator with at least one meaningful network."
    );
  }

  const pptx =
    new pptxgen();

  pptx.layout =
    "LAYOUT_WIDE";

  pptx.author =
    options.author ||
    "Influencer Audience Report Agent";

  pptx.company =
    options.company || "";

  pptx.subject =
    "Influencer audience intelligence";

  pptx.title =
    reportData.title ||
    "Influencer Audience Report";

  pptx.lang =
    "es-AR";

  pptx.theme = {
    headFontFace:
      "Aptos Display",

    bodyFontFace:
      "Aptos",

    lang:
      "es-AR",
  };

  pptx.defineLayout({
    name:
      "CUSTOM_WIDE",

    width:
      LAYOUT.w,

    height:
      LAYOUT.h,
  });

  pptx.layout =
    "CUSTOM_WIDE";

  const includeCover =
    options.includeCover !==
    false;

  const totalSlides =
    countNetworkSlides(
      reportData
    ) +
    (
      includeCover
        ? 1
        : 0
    );

  if (
    includeCover
  ) {
    addCoverSlide(
      pptx,
      reportData,
      totalSlides
    );
  }

  let slideNo =
    includeCover
      ? 2
      : 1;

  for (
    const creator
    of reportData.creators
  ) {
    for (
      const network
      of creator.networks
    ) {
      createNetworkSlide(
        pptx,
        reportData,
        creator,
        network,
        slideNo,
        totalSlides
      );

      slideNo += 1;
    }
  }

  fs.mkdirSync(
    path.dirname(
      path.resolve(
        outputPath
      )
    ),
    {
      recursive: true,
    }
  );

  await pptx.writeFile({
    fileName:
      outputPath,
  });

  const removedDanglingContentTypeOverrides =
    await sanitizePptxPackage(
      outputPath
    );

  return {
    success: true,

    outputPath,

    slideCount:
      totalSlides,

    creatorCount:
      reportData.creators
        .length,

    networkSlideCount:
      countNetworkSlides(
        reportData
      ),

    packageRepairs: {
      removedDanglingContentTypeOverrides,
    },
  };
}

function extractReportDataFromHtml(
  html
) {
  const match =
    html.match(
      /<script\s+id=["']report-data["'][^>]*>([\s\S]*?)<\/script>/i
    );

  if (!match) {
    throw new Error(
      'Could not find <script id="report-data"> in HTML input.'
    );
  }

  return JSON.parse(
    match[1]
  );
}

function loadReportData(
  inputPath
) {
  const raw =
    fs.readFileSync(
      inputPath,
      "utf8"
    );

  const ext =
    path.extname(
      inputPath
    ).toLowerCase();

  if (
    ext === ".html" ||
    ext === ".htm"
  ) {
    return extractReportDataFromHtml(
      raw
    );
  }

  return JSON.parse(
    raw
  );
}

async function main() {
  const inputPath =
    process.argv[2];

  const outputPath =
    process.argv[3] ||
    `influencer-audience-report-${new Date()
      .toISOString()
      .slice(
        0,
        10
      )}.pptx`;

  if (
    !inputPath
  ) {
    console.error(
      "Usage: node pptx_report_generator.js <report-data.json|report.html> <output.pptx>"
    );

    process.exit(1);
  }

  const reportData =
    loadReportData(
      inputPath
    );

  const result =
    await buildInfluencerAudiencePptx(
      reportData,
      outputPath,
      {
        includeCover: true,
      }
    );

  console.log(
    JSON.stringify(
      result,
      null,
      2
    )
  );
}

if (
  require.main ===
  module
) {
  main().catch(
    (err) => {
      console.error(
        err &&
        err.stack
          ? err.stack
          : err
      );

      process.exit(1);
    }
  );
}

module.exports = {
  buildInfluencerAudiencePptx,
  loadReportData,
  normalizeReportData,
  sanitizePptxPackage,
};