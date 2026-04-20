"""
Formats and sends the weekly Bad Stock summary to Google Chat.
Uses a simple webhook (no OAuth needed).
"""

import requests

DASHBOARD_URL = "https://deboradutra-design.github.io/bad-stock-dashboard/"

SITE_NAMES = {
    "MLB": "MLB · Brasil",
    "MLM": "MLM · México",
    "MLA": "MLA · Argentina",
    "MLC": "MLC · Chile",
    "MCO": "MCO · Colombia",
}

# Monthly targets 2026 — 3P+CBT bad stock %
TARGETS_2026 = {
    1: {"MLB": 13.0, "MLM": 13.3, "MLA": 12.6, "MLC": 16.4, "MCO": 23.6},
    2: {"MLB": 12.0, "MLM": 12.8, "MLA": 11.5, "MLC": 15.4, "MCO": 21.2},
    3: {"MLB": 11.0, "MLM": 13.2, "MLA": 11.1, "MLC": 14.8, "MCO": 23.4},
    4: {"MLB": 11.0, "MLM": 13.3, "MLA": 10.5, "MLC": 15.2, "MCO": 26.0},
    5: {"MLB": 11.0, "MLM": 13.3, "MLA": 10.5, "MLC": 15.2, "MCO": 26.0},
    6: {"MLB": 11.0, "MLM": 13.3, "MLA": 10.5, "MLC": 15.2, "MCO": 26.0},
}


def _delta_icon(delta: float, threshold_red: float = 1.0) -> str:
    if abs(delta) < 0.05:
        return "➡️"
    return "✅" if delta < 0 else ("🔴" if abs(delta) >= threshold_red else "⚠️")


def _fmt_delta(delta: float) -> str:
    sign = "+" if delta > 0 else ""
    return f"{sign}{delta:.1f}pp"


def _get_3p_cbt(site_data: dict) -> dict | None:
    """Get 3P+CBT data, falling back to 3P."""
    return site_data.get("3P+CBT") or site_data.get("3P")


def build_message(
    week_id: str,
    week_date,
    curr_kpi: dict,
    prev_kpi: dict,
    curr_bd: dict,
    prev_bd: dict,
    curr_vert: dict,
    prev_vert: dict,
    month: int,
) -> str:
    targets = TARGETS_2026.get(month, {})
    prev_week_id = f"W{int(week_id[1:]) - 1}"
    lines = []

    # ── Header ────────────────────────────────────────────────────────────────
    lines.append(f"📊 *Bad Stock Weekly Tracking · {week_id} | {week_date.strftime('%d/%m/%Y')}*")
    lines.append(f"🔗 {DASHBOARD_URL}")
    lines.append("")

    # ── Sites vs target ───────────────────────────────────────────────────────
    lines.append("━━━━━━━━━━━━━━━━━━━━━")
    above, below = [], []
    for site in ["MLB", "MLM", "MLA", "MLC", "MCO"]:
        d = _get_3p_cbt(curr_kpi.get(site, {}))
        tgt = targets.get(site)
        if d is None or tgt is None:
            continue
        diff = round(d["bs"] - tgt, 2)
        (above if diff > 0 else below).append((site, d["bs"], tgt, diff))

    if above:
        lines.append("*🚨 Sites ACIMA do target (3P+CBT)*")
        for site, bs, tgt, diff in above:
            lines.append(f"• *{SITE_NAMES[site]}:* {bs:.1f}% — target {tgt:.1f}% *(+{diff:.1f}pp)*")
    else:
        lines.append("*✅ Todos os sites abaixo do target!*")
    if below:
        lines.append("*✅ Sites abaixo do target*")
        for site, bs, tgt, diff in below:
            lines.append(f"• {SITE_NAMES[site]}: {bs:.1f}% — target {tgt:.1f}% ({diff:.1f}pp)")

    # ── W vs W-1 por país ─────────────────────────────────────────────────────
    lines.append("")
    lines.append("━━━━━━━━━━━━━━━━━━━━━")
    lines.append(f"*📊 {week_id} vs {prev_week_id} · Por País (3P+CBT)*")
    lines.append("━━━━━━━━━━━━━━━━━━━━━")
    for site in ["MLB", "MLM", "MLA", "MLC", "MCO"]:
        c = _get_3p_cbt(curr_kpi.get(site, {}))
        p = _get_3p_cbt(prev_kpi.get(site, {}))
        if not c or not p:
            continue
        delta = round(c["bs"] - p["bs"], 2)
        icon = _delta_icon(delta, threshold_red=1.0)
        lines.append(f"{icon} *{SITE_NAMES[site]}:* {c['bs']:.1f}% ({_fmt_delta(delta)})")

    # ── W vs W-1 por segmento ─────────────────────────────────────────────────
    lines.append("")
    lines.append("━━━━━━━━━━━━━━━━━━━━━")
    lines.append(f"*🔍 {week_id} vs {prev_week_id} · Por Segmento*")
    lines.append("━━━━━━━━━━━━━━━━━━━━━")
    for label, initiative in [("Meli Pro", "MELI PRO"), ("Seller Dev", "SELLER DEV"), ("CBT", "CBT")]:
        parts = []
        for site in ["MLB", "MLM", "MLA", "MLC", "MCO"]:
            c_s = curr_kpi.get(site, {}).get(initiative)
            p_s = prev_kpi.get(site, {}).get(initiative)
            if c_s and p_s:
                delta = round(c_s["bs"] - p_s["bs"], 2)
                if delta <= 0:
                    continue  # só mostra desvios positivos (piora)
                icon = _delta_icon(delta, threshold_red=1.0)
                parts.append(f"{site} {c_s['bs']:.1f}% ({_fmt_delta(delta)} {icon})")
        if parts:
            lines.append(f"*{label}:* " + " | ".join(parts))

    # ── W vs W-1 por tipo de bad stock ────────────────────────────────────────
    lines.append("")
    lines.append("━━━━━━━━━━━━━━━━━━━━━")
    lines.append(f"*📦 {week_id} vs {prev_week_id} · Por Tipo de Bad Stock (3P+CBT)*")
    lines.append("━━━━━━━━━━━━━━━━━━━━━")
    type_fields = [("str", "Stranded"), ("sv", "Sin Venta"), ("ag", "Aging"), ("exc", "Aging+Exc")]
    for field, label in type_fields:
        movers = []
        for site in ["MLB", "MLM", "MLA", "MLC", "MCO"]:
            c_b = (curr_bd.get(site, {}).get("3P+CBT") or curr_bd.get(site, {}).get("3P") or {})
            p_b = (prev_bd.get(site, {}).get("3P+CBT") or prev_bd.get(site, {}).get("3P") or {})
            if field in c_b and field in p_b:
                delta = round(c_b[field] - p_b[field], 2)
                if delta >= 0.1:  # só mostra desvios positivos (piora)
                    icon = _delta_icon(delta, threshold_red=0.5)
                    movers.append(f"{site} {_fmt_delta(delta)} {icon}")
        if movers:
            lines.append(f"*{label}:* " + " | ".join(movers))

    # ── Top variações por vertical ────────────────────────────────────────────
    lines.append("")
    lines.append("━━━━━━━━━━━━━━━━━━━━━")
    lines.append(f"*📂 {week_id} vs {prev_week_id} · Top Variações por Vertical*")
    lines.append("━━━━━━━━━━━━━━━━━━━━━")
    movers = []
    for site in ["MLB", "MLM", "MLA", "MLC", "MCO"]:
        cv, pv = curr_vert.get(site, {}), prev_vert.get(site, {})
        for vert in cv:
            if vert in pv:
                delta = round(cv[vert] - pv[vert], 2)
                if delta > 0:  # só mostra desvios positivos (piora)
                    movers.append((delta, site, vert, cv[vert]))
    movers.sort(reverse=True)
    for delta, site, vert, val in movers[:5]:
        icon = _delta_icon(delta, threshold_red=1.0)
        lines.append(f"{icon} {site} · {vert}: {val:.1f}% ({_fmt_delta(delta)})")

    # ── Footer ────────────────────────────────────────────────────────────────
    lines.append("")
    lines.append(f"_Fonte: BigQuery · Ref. {week_date.strftime('%d/%m/%Y')} · gerado automaticamente_")

    return "\n".join(lines)


def send_to_chat(webhook_url: str, message: str) -> None:
    resp = requests.post(webhook_url, json={"text": message}, timeout=15)
    resp.raise_for_status()
    print(f"✅ Mensagem enviada ao Google Chat ({len(message)} chars)")
