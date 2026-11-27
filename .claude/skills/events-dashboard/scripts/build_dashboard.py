#!/usr/bin/env python3
"""
Build Quilmes Rock 2027 dashboard HTML from raw data files.

Usage:
  python3 build_dashboard.py [--qr27 PATH] [--qr25 PATH] --output PATH

Defaults:
  --qr27  <skill>/references/Tickets Info-data-*.csv
  --qr25  <skill>/references/Venta diaria Quilmes 2025.xlsx
  --output <workdir>/uploads/quilmes-rock-2027-dashboard.html
"""
import csv, json, zipfile, xml.etree.ElementTree as ET, sys, re
from datetime import datetime, timedelta, date
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent
REFS      = SKILL_DIR / "references"
WORK_DIR  = Path("/home/agent/work/2026-09-14_9muktr")

DEFAULT_QR27   = REFS / "Tickets Info-data-2026-11-16 10_21_10.csv"
DEFAULT_QR25   = REFS / "Venta diaria Quilmes 2025.xlsx"
DEFAULT_OUTPUT = WORK_DIR / "uploads" / "quilmes-rock-2027-dashboard.html"
TEMPLATE       = REFS / "template.html"

FESTIVAL_DATE = date(2027, 4, 1)
QR27_LAUNCH   = date(2026, 4, 16)
QR25_LAUNCH   = date(2024, 6, 25)
LINEUP_DATE   = "2026-11-02"

CONS_RATE = 40
BASE_RATE = 80
OPT_RATE  = 160

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def excel_serial_to_date(serial):
    """Convert Excel date serial to date string YYYY-MM-DD."""
    try:
        s = int(float(serial))
        return (date(1899, 12, 30) + timedelta(days=s)).isoformat()
    except Exception:
        return ""


def parse_qr27_csv(path):
    """Parse QR27 ticket CSV. Returns list of row dicts."""
    path = Path(path)
    # Try UTF-8 BOM, then latin-1
    for enc in ('utf-8-sig', 'utf-8', 'latin-1'):
        try:
            with open(path, encoding=enc, newline='') as f:
                sample = f.read(2048)
            with open(path, encoding=enc, newline='') as f:
                delim = ';' if sample.count(';') > sample.count(',') else ','
                reader = csv.DictReader(f, delimiter=delim)
                rows = [r for r in reader if any(v.strip() for v in r.values())]
            return rows
        except UnicodeDecodeError:
            continue
    raise ValueError(f"Cannot decode {path}")


def parse_fecha(s):
    """Normalize date string to YYYY-MM-DD."""
    if not s:
        return ""
    s = s.strip().strip('"')
    if re.match(r'^\d{4}-\d{2}-\d{2}', s):
        return s[:10]
    m = re.match(r'^(\d{1,2})/(\d{1,2})/(\d{4})', s)
    if m:
        a, b, y = int(m.group(1)), int(m.group(2)), m.group(3)
        if a > 12:   # DD/MM/YYYY
            return f"{y}-{b:02d}-{a:02d}"
        return f"{y}-{a:02d}-{b:02d}"
    return ""


def day_multiplier(butaca):
    """Ticket day multiplier from seat category name."""
    if not butaca:
        return 1
    m = re.search(r'(\d+)\s*d[ií]', butaca, re.IGNORECASE)
    return int(m.group(1)) if m else 1


def parse_qr25_xlsx(path):
    """
    Parse QR25 XLSX using stdlib zipfile + xml.
    Returns list of {fecha: 'YYYY-MM-DD', daily: float, cumul: float, day: int}
    """
    with zipfile.ZipFile(path) as z:
        ns = {'s': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}

        # Shared strings
        shared = []
        if 'xl/sharedStrings.xml' in z.namelist():
            root = ET.fromstring(z.read('xl/sharedStrings.xml'))
            for si in root.findall('.//s:si', ns):
                parts = [t.text or '' for t in si.findall('.//s:t', ns)]
                shared.append(''.join(parts))

        ws_root = ET.fromstring(z.read('xl/worksheets/sheet1.xml'))
        rows = ws_root.findall('.//s:row', ns)

    def cell_val(c):
        t = c.get('t')
        v_el = c.find('s:v', ns)
        raw = (v_el.text or '') if v_el is not None else ''
        if t == 's':
            return shared[int(raw)] if raw else ''
        return raw

    headers = None
    result = []
    cum = 0.0
    for row in rows:
        cells = {c.get('r', '')[0]: cell_val(c) for c in row.findall('s:c', ns)}
        vals = [cell_val(c) for c in row.findall('s:c', ns)]
        if headers is None:
            headers = vals
            continue
        if not vals or not any(v for v in vals):
            continue
        row_dict = {}
        for i, h in enumerate(headers):
            row_dict[h] = vals[i] if i < len(vals) else ''

        fecha_raw = row_dict.get('fecha', '')
        total_raw = row_dict.get('total_tickets', '')

        if not fecha_raw:
            continue
        fecha = excel_serial_to_date(fecha_raw) if re.match(r'^\d+', fecha_raw) else parse_fecha(fecha_raw)
        if not fecha:
            continue

        daily = 0.0
        try:
            daily = float(total_raw) if total_raw else 0.0
        except Exception:
            continue

        cum += daily
        d = datetime.fromisoformat(fecha).date()
        day_num = (d - QR25_LAUNCH).days + 1
        result.append({'fecha': fecha, 'day': day_num, 'daily': daily, 'cumul': cum})

    return [r for r in result if r['day'] > 0]


# ---------------------------------------------------------------------------
# QR25 Milestone analysis
# ---------------------------------------------------------------------------
QR25_MILESTONES = [
    {"date": "2024-08-30", "label": "Lanzamiento + Early Birds"},
    {"date": "2024-10-03", "label": "Refuerzo de lineup"},
    {"date": "2024-10-08", "label": "Grilla por día"},
    {"date": "2024-10-10", "label": "Preventa Galicia"},
]

def compute_qr25_milestones(qr25_days):
    daily_map = {r['fecha']: r['daily'] for r in qr25_days}
    dates_sorted = sorted(daily_map.keys())
    result = []
    for m in QR25_MILESTONES:
        d = m['date']
        idx = next((i for i, x in enumerate(dates_sorted) if x >= d), None)
        if idx is None:
            continue
        before = [daily_map[dates_sorted[j]] for j in range(max(0, idx-7), idx)]
        after  = [daily_map[dates_sorted[j]] for j in range(idx, min(len(dates_sorted), idx+7))]
        b_avg = sum(before) / len(before) if before else 0
        a_avg = sum(after)  / len(after)  if after  else 0
        pct = round((a_avg / b_avg - 1) * 1000) / 10 if b_avg > 0 else 0
        result.append({
            'date': d,
            'label': m['label'],
            'before7_avg': round(b_avg * 10) / 10,
            'after7_avg': round(a_avg * 10) / 10,
            'pct_change': pct,
        })
    return result


# ---------------------------------------------------------------------------
# Core data processing
# ---------------------------------------------------------------------------

def process_qr27(rows):
    """
    Returns qr27_raw, categories, monthly_qr27, top_days, qr27_daily,
    smi_history, kpis_partial, heatmap
    """
    daily_map = {}
    cat_map   = {}

    for r in rows:
        fecha = parse_fecha(r.get('Fecha_de_venta', '') or r.get('fecha_de_venta', ''))
        if not fecha:
            continue
        butaca = (r.get('Butaca') or r.get('butaca') or '').strip()
        mult   = day_multiplier(butaca)
        try:
            precio = float((r.get('Precio') or r.get('precio') or '0').replace(',', '.'))
        except Exception:
            precio = 0.0

        if fecha not in daily_map:
            daily_map[fecha] = {'tickets_dia': 0, 'revenue_dia': 0.0}
        daily_map[fecha]['tickets_dia'] += mult
        daily_map[fecha]['revenue_dia'] += precio

        if butaca not in cat_map:
            cat_map[butaca] = {'tickets': 0, 'revenue': 0.0, 'transactions': 0}
        cat_map[butaca]['tickets']      += mult
        cat_map[butaca]['revenue']      += precio
        cat_map[butaca]['transactions'] += 1

    sorted_dates = sorted(daily_map.keys())
    cum = 0
    cum_rev = 0.0
    qr27_raw = []
    for f in sorted_dates:
        cum     += daily_map[f]['tickets_dia']
        cum_rev += daily_map[f]['revenue_dia']
        qr27_raw.append({
            'fecha':       f,
            'tickets_dia': daily_map[f]['tickets_dia'],
            'revenue_dia': daily_map[f]['revenue_dia'],
            'cumul':       cum,
            'rev_cumul':   cum_rev,
        })

    # qr27_daily with launch-relative day numbers
    qr27_daily = []
    for r in qr27_raw:
        d = datetime.fromisoformat(r['fecha']).date()
        day_num = (d - QR27_LAUNCH).days + 1
        qr27_daily.append({
            'fecha':     r['fecha'],
            'day':       day_num,
            'daily':     r['tickets_dia'],
            'cumul':     r['cumul'],
            'rev':       r['revenue_dia'],
            'rev_cumul': r['rev_cumul'],
        })

    # Monthly
    monthly = {}
    for r in qr27_raw:
        m = r['fecha'][:7]
        if m not in monthly:
            monthly[m] = {'tickets': 0, 'revenue': 0.0}
        monthly[m]['tickets'] += r['tickets_dia']
        monthly[m]['revenue'] += r['revenue_dia']

    # Top 10 days
    top_days = sorted(qr27_raw, key=lambda x: x['tickets_dia'], reverse=True)[:10]

    # SMI history (requires i >= 14 entries)
    smi_history = []
    for i in range(14, len(qr27_raw)):
        r7 = qr27_raw[i-7:i]
        p7 = qr27_raw[i-14:i-7]
        ra = sum(x['tickets_dia'] for x in r7) / 7
        pa = sum(x['tickets_dia'] for x in p7) / 7
        smi = round(ra / pa * 1000) / 10 if pa > 0 else 100.0
        smi_history.append({
            'fecha': qr27_raw[i]['fecha'],
            'smi':   smi,
            'avg7':  round(ra * 10) / 10,
        })

    # KPIs
    total_tickets = qr27_raw[-1]['cumul'] if qr27_raw else 0
    total_revenue = sum(r['revenue_dia'] for r in qr27_raw)
    avg_price     = round(total_revenue / len(rows)) if rows else 0
    cutoff        = sorted_dates[-1] if sorted_dates else ''

    last7  = qr27_raw[-7:]
    prev7  = qr27_raw[-14:-7]
    l7avg  = sum(x['tickets_dia'] for x in last7)  / 7
    p7avg  = sum(x['tickets_dia'] for x in prev7)  / 7
    l30    = qr27_raw[-30:]
    l30tot = sum(x['tickets_dia'] for x in l30)
    smi_now = round(l7avg / p7avg * 1000) / 10 if p7avg > 0 else 100.0

    # Lineup impact
    before7_lineup = [x for x in qr27_raw if x['fecha'] < LINEUP_DATE][-7:]
    after7_lineup  = [x for x in qr27_raw if x['fecha'] >= LINEUP_DATE][:7]
    if before7_lineup:
        lb_avg = round(sum(x['tickets_dia'] for x in before7_lineup) / len(before7_lineup) * 10) / 10
    else:
        lb_avg = 0.0
    if after7_lineup:
        la_avg = round(sum(x['tickets_dia'] for x in after7_lineup) / len(after7_lineup) * 10) / 10
    else:
        la_avg = 0.0
    la_acc = round((la_avg / lb_avg - 1) * 1000) / 10 if lb_avg > 0 else 0.0

    # Days remaining to festival
    cutoff_date   = datetime.fromisoformat(cutoff).date() if cutoff else date.today()
    days_remaining = (FESTIVAL_DATE - cutoff_date).days
    current_day    = qr27_daily[-1]['day'] if qr27_daily else 1

    kpis_partial = {
        'total_tickets':    total_tickets,
        'total_revenue':    total_revenue,
        'avg_price':        avg_price,
        'cutoff':           cutoff,
        'start':            QR27_LAUNCH.isoformat(),
        'last7_total':      sum(x['tickets_dia'] for x in last7),
        'last7_avg':        round(l7avg * 10) / 10,
        'prev7_avg':        round(p7avg * 10) / 10,
        'last30_total':     l30tot,
        'last30_avg':       round(l30tot / 30 * 10) / 10,
        'smi':              smi_now,
        'lineup_date':      LINEUP_DATE,
        'lineup_before_avg': lb_avg,
        'lineup_after_avg':  la_avg,
        'lineup_acceleration': la_acc,
        'days_remaining':   days_remaining,
        'current_day':      current_day,
        # QR25 fields filled in later
        'qr25_at_day197':   0,
        'vs_qr25_pct':      0,
        'qr25_equiv_tickets': 0,
        'qr25_equiv_date':  '',
        'qr25_festival':    '2025-04-10',
        'qr27_festival_est': '2027-04-01',
        'vs_equiv_abs':     0,
        'vs_equiv_pct':     0,
    }

    # Forecast with date/value arrays
    cur_tix  = total_tickets
    fc_start = datetime.fromisoformat(cutoff + 'T00:00:00')
    fc_dates, fc_cons, fc_base, fc_opt = [], [], [], []
    step = 7
    d_max = days_remaining + step
    for d in range(step, d_max + 1, step):
        iso  = (fc_start + timedelta(days=d)).date().isoformat()
        frac = min(d, days_remaining)
        fc_dates.append(iso)
        fc_cons.append(round(cur_tix + CONS_RATE * frac))
        fc_base.append(round(cur_tix + BASE_RATE * frac))
        fc_opt.append(round(cur_tix + OPT_RATE  * frac))

    forecast = {
        'cons_rate':     CONS_RATE,
        'base_rate':     BASE_RATE,
        'opt_rate':      OPT_RATE,
        'days_remaining': days_remaining,
        'cons_final':    round(cur_tix + CONS_RATE * days_remaining),
        'base_final':    round(cur_tix + BASE_RATE * days_remaining),
        'opt_final':     round(cur_tix + OPT_RATE  * days_remaining),
        'dates':         fc_dates,
        'cons':          fc_cons,
        'base':          fc_base,
        'opt':           fc_opt,
    }

    # Heatmap: 29 weeks starting Monday 2026-04-20
    hm_start  = date(2026, 4, 13)
    daily_lkp = {r['fecha']: r['tickets_dia'] for r in qr27_raw}
    heatmap   = []
    for w in range(29):
        week = []
        for d2 in range(7):
            dt   = hm_start + timedelta(days=w * 7 + d2)
            iso  = dt.isoformat()
            week.append({
                'date':      iso,
                'val':       0 if iso == '2026-04-16' else daily_lkp.get(iso, 0),
                'is_launch': iso == '2026-04-16',
            })
        heatmap.append(week)

    return {
        'qr27_raw':     qr27_raw,
        'qr27_daily':   qr27_daily,
        'categories':   cat_map,
        'monthly_qr27': monthly,
        'top_days':     top_days,
        'smi_history':  smi_history,
        'kpis':         kpis_partial,
        'forecast':     forecast,
        'heatmap':      heatmap,
    }


def merge_qr25(data, qr25_days):
    """Fill QR25-dependent KPI fields."""
    kpis = data['kpis']
    cur_day = kpis['current_day']

    # vs QR25 at same day
    at_day = next((r for r in qr25_days if r['day'] == cur_day), None)
    if at_day:
        kpis['qr25_at_day197'] = at_day['cumul']
        kpis['vs_qr25_pct'] = round((kpis['total_tickets'] / at_day['cumul'] - 1) * 1000) / 10

    # Equivalent date in QR25 timeline (day matching total ticket count)
    cur_tix = kpis['total_tickets']
    equiv   = next((r for r in qr25_days if r['cumul'] >= cur_tix), None)
    if equiv:
        kpis['qr25_equiv_tickets'] = equiv['cumul']
        kpis['qr25_equiv_date']    = equiv['fecha']
        kpis['vs_equiv_abs']       = round(kpis['total_tickets'] - equiv['cumul'])
        kpis['vs_equiv_pct']       = round((kpis['total_tickets'] / equiv['cumul'] - 1) * 1000) / 10

    data['qr25_days'] = qr25_days
    data['qr25_milestone_analysis'] = compute_qr25_milestones(qr25_days)
    return data


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--qr27',   default=str(DEFAULT_QR27))
    p.add_argument('--qr25',   default=str(DEFAULT_QR25))
    p.add_argument('--output', default=str(DEFAULT_OUTPUT))
    args = p.parse_args()

    print(f"[events-dashboard] Reading QR27: {args.qr27}")
    qr27_rows = parse_qr27_csv(args.qr27)
    print(f"  → {len(qr27_rows)} rows")

    data = process_qr27(qr27_rows)

    print(f"[events-dashboard] Reading QR25: {args.qr25}")
    try:
        qr25_days = parse_qr25_xlsx(args.qr25)
        print(f"  → {len(qr25_days)} days")
        data = merge_qr25(data, qr25_days)
    except Exception as e:
        print(f"  Warning: QR25 parse failed ({e}). Proceeding without QR25.")
        data['qr25_days'] = []
        data['qr25_milestone_analysis'] = []

    # Build RAW_DATA JSON
    raw_data_json = json.dumps(data, ensure_ascii=False, separators=(',', ':'))

    # Inject into template
    template = TEMPLATE.read_text(encoding='utf-8')
    html = template.replace('const RAW_DATA = ___DATA___;',
                            f'const RAW_DATA = {raw_data_json};', 1)

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding='utf-8')

    cutoff = data['kpis'].get('cutoff', '?')
    total  = data['kpis'].get('total_tickets', 0)
    print(f"[events-dashboard] Dashboard written to: {out_path}")
    print(f"  Corte: {cutoff}  |  Tickets totales: {total:,}")


if __name__ == '__main__':
    main()
