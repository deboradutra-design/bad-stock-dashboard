"""
Updates index.html with new week data.

Strategy: for each JS object constant (KPI, INIT_KPI, etc.), finds the last
week entry using brace-counting and inserts the new week entry after it.
Also updates the WEEKS array, dropdown options, state, and footer.
"""

import re
from datetime import date


# ─── Formatting helpers ────────────────────────────────────────────────────────

def _r(v, dp=2):
    """Round a value or return 0 if None."""
    return round(float(v or 0), dp)


def _fmt_kpi_entry(week_id: str, kpi: dict, breakdown: dict) -> str:
    """
    Build a KPI constant entry line.
    kpi:       {site: {initiative: {bs, u, bu}}}
    breakdown: {site: {initiative: {str, sv, ag, exc}}}
    Returns: '  W16: { MLB:{bs:9.5,...,u:70000000,bu:7000000}, ...},\n'
    """
    sites = ["MLB", "MLM", "MLA", "MLC", "MCO"]
    parts = []
    for site in sites:
        d = kpi.get(site, {}).get("TOTAL") or {}
        b = breakdown.get(site, {}).get("TOTAL") or {}
        bs  = _r(d.get("bs", 0))
        str_ = _r(b.get("str", 0))
        sv   = _r(b.get("sv", 0))
        ag   = _r(b.get("ag", 0))
        exc  = _r(b.get("exc", 0))
        u    = int(d.get("u", 0))
        bu   = int(d.get("bu", 0))
        parts.append(
            f"{site}:{{bs:{bs},str:{str_},sv:{sv},ag:{ag},exc:{exc},u:{u},bu:{bu}}}"
        )
    return f"  {week_id}: {{ {', '.join(parts)} }},\n"


def _fmt_init_kpi_entry(week_id: str, kpi: dict, breakdown: dict) -> str:
    """
    Build an INIT_KPI constant entry.
    One line per site, with per-initiative breakdown.
    """
    sites = ["MLB", "MLM", "MLA", "MLC", "MCO"]
    initiatives = ["3P", "CBT", "3P+CBT", "1P/PL"]
    site_lines = []
    for site in sites:
        ini_parts = []
        for ini in initiatives:
            d = kpi.get(site, {}).get(ini)
            b = breakdown.get(site, {}).get(ini) or {}
            if d is None:
                ini_parts.append(f"'{ini}':null")
                continue
            bs   = _r(d["bs"])
            str_ = _r(b.get("str", 0))
            sv   = _r(b.get("sv", 0))
            ag   = _r(b.get("ag", 0))
            exc  = _r(b.get("exc", 0))
            ini_parts.append(
                f"'{ini}':{{bs:{bs},str:{str_},sv:{sv},ag:{ag},exc:{exc}}}"
            )
        site_lines.append(f"    {site}:{{ {', '.join(ini_parts)} }}")
    inner = ",\n".join(site_lines)
    return f"  {week_id}: {{\n{inner},\n  }},\n"


def _fmt_seg_kpi_entry(week_id: str, kpi: dict, breakdown: dict) -> str:
    """Build a SEG_KPI constant entry (Meli Pro + Seller Dev)."""
    sites = ["MLB", "MLM", "MLA", "MLC", "MCO"]
    site_lines = []
    for site in sites:
        parts = []
        for seg in ["MELI PRO", "SELLER DEV"]:
            d = kpi.get(site, {}).get(seg)
            b = breakdown.get(site, {}).get(seg) or {}
            if d is None:
                continue
            bs   = _r(d["bs"])
            str_ = _r(b.get("str", 0))
            sv   = _r(b.get("sv", 0))
            ag   = _r(b.get("ag", 0))
            exc  = _r(b.get("exc", 0))
            u    = int(d.get("u", 0))
            parts.append(
                f"'{seg}':{{bs:{bs},str:{str_},sv:{sv},ag:{ag},exc:{exc},u:{u}}}"
            )
        if parts:
            site_lines.append(f"    {site}: {{ {', '.join(parts)} }}")
    inner = ",\n".join(site_lines)
    return f"  {week_id}: {{\n{inner},\n  }},\n"


def _fmt_seg_units_entry(week_id: str, kpi: dict) -> str:
    """
    Build a SEG_UNITS constant entry.
    Uses KPI_DENOMINADOR_VAL (total_units) and KPI_NUMERADOR_VAL (bad_units).
    """
    sites = ["MLB", "MLM", "MLA", "MLC", "MCO"]
    site_lines = []
    for site in sites:
        s = kpi.get(site, {})
        parts = []
        for ini in ["3P", "MELI PRO", "SELLER DEV", "CBT", "1P/PL", "3P+CBT"]:
            d = s.get(ini)
            if d and d.get("u"):
                parts.append(f"'{ini}':{{u:{d['u']},bu:{d['bu']}}}")
        if parts:
            site_lines.append(f"    {site}: {{ {', '.join(parts)} }}")
    inner = ",\n".join(site_lines)
    return f"  {week_id}: {{\n{inner},\n  }},\n"


# ─── HTML insertion helpers ───────────────────────────────────────────────────

def _find_last_week_end(html: str, const_start: int, const_end: int) -> int:
    """
    Within html[const_start:const_end], finds the position right after
    the closing '  },' of the last 'W\d+:' entry.
    Returns absolute position in html (or const_end if not found).
    """
    pattern = re.compile(r'^\s{2}W\d+\s*:', re.MULTILINE)
    last_match = None
    for m in pattern.finditer(html, const_start, const_end):
        last_match = m

    if not last_match:
        return const_end

    # Count braces from the '{' of that entry to find its end
    start_brace = html.find('{', last_match.start())
    if start_brace == -1 or start_brace > const_end:
        return const_end

    depth = 1
    pos = start_brace + 1
    while pos < const_end and depth > 0:
        if html[pos] == '{':
            depth += 1
        elif html[pos] == '}':
            depth -= 1
        pos += 1

    # pos is now right after the closing '}'
    # Advance past optional ',' and newline
    if pos < len(html) and html[pos] == ',':
        pos += 1
    if pos < len(html) and html[pos] == '\n':
        pos += 1
    return pos


def _insert_after_last_week(html: str, const_name: str, new_entry: str) -> str:
    """Insert new_entry after the last Wxx entry in the named JS constant."""
    # Find constant boundaries
    start_marker = f"const {const_name} = {{"
    start = html.find(start_marker)
    if start == -1:
        print(f"⚠️  Constant '{const_name}' not found in HTML — skipping.")
        return html

    # Find the matching closing '};'
    brace_start = html.find('{', start + len(start_marker) - 1)
    depth = 1
    pos = brace_start + 1
    while pos < len(html) and depth > 0:
        if html[pos] == '{':
            depth += 1
        elif html[pos] == '}':
            depth -= 1
        pos += 1
    const_end = pos  # right after the top-level '}'

    insert_at = _find_last_week_end(html, start, const_end)
    return html[:insert_at] + new_entry + html[insert_at:]


def _week_already_exists(html: str, week_id: str) -> bool:
    """Check if a week entry already exists in the HTML."""
    return bool(re.search(rf'\b{re.escape(week_id)}\b.*?:', html))


# ─── Main update function ─────────────────────────────────────────────────────

def update_html(
    html: str,
    week_id: str,
    week_date: date,
    month: int,
    kpi: dict,
    breakdown: dict,
) -> str:
    """
    Inserts a new week into all relevant JS constants and updates the UI.
    Returns the updated HTML string.
    """
    if _week_already_exists(html, week_id):
        print(f"ℹ️  {week_id} já existe no HTML — pulando inserção de dados.")
        return html

    prev_week_num = int(week_id[1:]) - 1
    prev_week_id  = f"W{prev_week_num}"

    print(f"📝 Inserindo {week_id} no HTML…")

    # 1. KPI (total por site)
    html = _insert_after_last_week(html, "KPI",
        _fmt_kpi_entry(week_id, kpi, breakdown))

    # 2. INIT_KPI (por iniciativa: 3P, CBT, 3P+CBT, 1P/PL)
    html = _insert_after_last_week(html, "INIT_KPI",
        _fmt_init_kpi_entry(week_id, kpi, breakdown))

    # 3. SEG_KPI (Meli Pro + Seller Dev)
    html = _insert_after_last_week(html, "SEG_KPI",
        _fmt_seg_kpi_entry(week_id, kpi, breakdown))

    # 4. SEG_UNITS (units por segmento)
    html = _insert_after_last_week(html, "SEG_UNITS",
        _fmt_seg_units_entry(week_id, kpi))

    # 5. WEEKS array — add new entry, remove current:true from previous
    date_str  = week_date.strftime("%d/%m/%Y")
    label_str = f"W{week_id[1:]} ({week_date.strftime('%d/%m')})"
    new_week_entry = (
        f"  {{ id:'{week_id}', date:'{date_str}', month:{month}, "
        f"label:'{label_str}★', current:true }},\n"
    )
    # Remove current:true from old week
    html = re.sub(r", current:true \}", " }", html)
    # Insert before the closing '];' of WEEKS
    weeks_start = html.find("const WEEKS = [")
    weeks_end   = html.find("];", weeks_start) + 2
    last_entry_end = html.rfind("  },\n", weeks_start, weeks_end) + len("  },\n")
    html = html[:last_entry_end] + new_week_entry + html[last_entry_end:]

    # 6. Week select dropdown — add new <option> and update selected
    # Remove selected from previous week option
    html = re.sub(
        rf'(<option value="{prev_week_id}")[^>]*(>.*?</option>)',
        r'\1\2',
        html
    )
    # Add new option after last <option> in week select
    week_label_html = f"W{week_id[1:]} — {date_str} ★ atual"
    new_option = f'      <option value="{week_id}" selected>{week_label_html}</option>\n'
    html = re.sub(
        r'(      <option value="' + prev_week_id + r'".*?</option>\n)',
        r'\1' + new_option,
        html,
    )

    # 7. Update state.selectedWeek
    html = re.sub(
        r"(selectedWeek:\s*')[^']+(')",
        rf"\g<1>{week_id}\g<2>",
        html,
    )

    # 8. Month select — update April option label if needed (or add new month)
    # (months are static; only the week count changes — no update needed)

    # 9. Footer date reference
    html = re.sub(
        r"(BigQuery[^·]*·[^·]*·\s*)W\d+ \([^)]+\)★ atual",
        rf"\g<1>{week_id} ({week_date.strftime('%d/%m/%Y')})★ atual",
        html,
    )
    html = re.sub(
        r"(Atualizado:\s*)\d{2}/\d{2}/\d{4}",
        rf"\g<1>{date.today().strftime('%d/%m/%Y')}",
        html,
    )

    # 10. Refresh panel — update "Dados atuais" line
    html = re.sub(
        r"W\d+ completo \(\d{2}/\d{2}/\d{4}\) · W\d+–W\d+ completo",
        f"{week_id} completo ({date_str}) · W1–{week_id} completo",
        html,
    )

    # 11. Add row to refresh history table
    today_str = date.today().strftime("%d/%m/%Y")
    new_hist_row = (
        f'        <tr><td>{week_id} ★</td>'
        f'<td>{date_str} (completo)</td>'
        f'<td>{today_str}</td>'
        f'<td><span style="color:var(--green)">✓ Atual via BigQuery</span></td></tr>\n'
    )
    html = re.sub(
        r'(<tbody>\n)',
        r'\1' + new_hist_row,
        html,
        count=1,
    )

    print(f"✅ HTML atualizado com {week_id}")
    return html
