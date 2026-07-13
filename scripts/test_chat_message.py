"""
Envio da mensagem W28 ao Google Chat com dados reais do BigQuery.
Execução: python scripts/test_chat_message.py <WEBHOOK_URL>
"""

import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from chat_notifier import build_message, send_to_chat


# ── W28 (11/07/2026) — Julho ──────────────────────────────────────────────────

curr_kpi = {
    "MLB": {
        "3P":        {"bs": 9.47,  "u": 90443934,  "bu": 8561137},
        "3P+CBT":    {"bs": 9.47,  "u": 90443934,  "bu": 8561137},
        "MELI PRO":  {"bs": 7.04,  "u": 23230000,  "bu": 1635000},
        "SELLER DEV":{"bs": 10.27, "u": 67215000,  "bu": 6906000},
        "TOTAL":     {"bs": 9.48,  "u": 107716187, "bu": 10214963},
    },
    "MLM": {
        "3P":        {"bs": 12.15, "u": 47313412,  "bu": 5749014},
        "CBT":       {"bs": 13.88, "u": 20872028,  "bu": 2896928},
        "3P+CBT":    {"bs": 12.68, "u": 68185440,  "bu": 8645942},
        "MELI PRO":  {"bs": 9.33,  "u": 12490000,  "bu": 1165000},
        "SELLER DEV":{"bs": 13.66, "u": 34820000,  "bu": 4752000},
        "TOTAL":     {"bs": 13.60, "u": 77729837,  "bu": 10569972},
    },
    "MLA": {
        "3P":        {"bs": 14.39, "u": 7331068,   "bu": 1054606},
        "3P+CBT":    {"bs": 14.39, "u": 7331068,   "bu": 1054606},
        "MELI PRO":  {"bs": 11.48, "u": 2574000,   "bu": 295000},
        "SELLER DEV":{"bs": 12.82, "u": 4757000,   "bu": 610000},
        "TOTAL":     {"bs": 17.01, "u": 8397443,   "bu": 1428634},
    },
    "MLC": {
        "3P":        {"bs": 13.33, "u": 5872285,   "bu": 782750},
        "CBT":       {"bs": 20.93, "u": 322921,    "bu": 67594},
        "3P+CBT":    {"bs": 13.73, "u": 6195206,   "bu": 850344},
        "MELI PRO":  {"bs": 12.15, "u": 1755000,   "bu": 213000},
        "SELLER DEV":{"bs": 12.31, "u": 4117000,   "bu": 506000},
        "TOTAL":     {"bs": 14.38, "u": 7014316,   "bu": 1008916},
    },
    "MCO": {
        "3P":        {"bs": 18.17, "u": 942245,    "bu": 171199},
        "3P+CBT":    {"bs": 18.17, "u": 942245,    "bu": 171199},
        "MELI PRO":  {"bs": 14.68, "u": 292000,    "bu": 43000},
        "SELLER DEV":{"bs": 19.99, "u": 650000,    "bu": 128000},
        "TOTAL":     {"bs": 18.48, "u": 1037104,   "bu": 191708},
    },
}

curr_bd = {
    "MLB": {
        "3P":        {"str": 1.95, "sv": 1.01, "ag": 2.55, "exc": 3.96},
        "3P+CBT":    {"str": 1.95, "sv": 1.01, "ag": 2.55, "exc": 3.96},
        "MELI PRO":  {"str": 1.53, "sv": 0.75, "ag": 1.66, "exc": 3.80},
        "SELLER DEV":{"str": 2.10, "sv": 1.10, "ag": 2.85, "exc": 4.02},
    },
    "MLM": {
        "3P":        {"str": 1.08, "sv": 1.85, "ag": 4.16, "exc": 6.49},
        "CBT":       {"str": 1.00, "sv": 2.24, "ag": 3.80, "exc": 7.32},
        "3P+CBT":    {"str": 1.08, "sv": 1.85, "ag": 4.16, "exc": 6.49},
        "MELI PRO":  {"str": 1.21, "sv": 1.25, "ag": 2.80, "exc": 4.30},
        "SELLER DEV":{"str": 1.08, "sv": 1.83, "ag": 4.91, "exc": 6.78},
    },
    "MLA": {
        "3P":        {"str": 1.04, "sv": 1.07, "ag": 4.41, "exc": 4.64},
        "3P+CBT":    {"str": 1.04, "sv": 1.07, "ag": 4.41, "exc": 4.64},
        "MELI PRO":  {"str": 0.59, "sv": 0.76, "ag": 2.58, "exc": 4.98},
        "SELLER DEV":{"str": 1.31, "sv": 1.26, "ag": 5.51, "exc": 4.44},
    },
    "MLC": {
        "3P":        {"str": 0.69, "sv": 2.08, "ag": 5.14, "exc": 6.56},
        "CBT":       {"str": 1.00, "sv": 2.24, "ag": 3.80, "exc": 7.32},
        "3P+CBT":    {"str": 0.69, "sv": 2.08, "ag": 5.14, "exc": 6.56},
        "MELI PRO":  {"str": 0.73, "sv": 2.21, "ag": 3.95, "exc": 5.84},
        "SELLER DEV":{"str": 0.64, "sv": 1.80, "ag": 5.87, "exc": 6.24},
    },
    "MCO": {
        "3P":        {"str": 0.98, "sv": 2.22, "ag": 8.87, "exc": 7.34},
        "3P+CBT":    {"str": 0.98, "sv": 2.22, "ag": 8.87, "exc": 7.34},
        "MELI PRO":  {"str": 0.96, "sv": 2.13, "ag": 5.41, "exc": 7.85},
        "SELLER DEV":{"str": 0.99, "sv": 2.27, "ag": 10.51, "exc": 7.10},
    },
}

curr_vert = {
    "MLB": {"BEAUTY":8.82,"CONSTRUCTION & INDUSTRY":9.78,"CPG":8.96,"ENTERTAINMENT":11.86,"FASHION":7.22,"FURNISHING & HOUSEWARE":10.19,"HEALTH":7.37,"HOME ELECTRONICS":11.84,"OTHERS":11.42,"SPORTS":14.04,"T & B":15.26,"TECHNOLOGY":11.18,"VEHICLE PARTS & ACCESSORIES":11.35},
    "MLM": {"BEAUTY":11.38,"CONSTRUCTION & INDUSTRY":11.22,"CPG":10.49,"ENTERTAINMENT":17.69,"FASHION":11.82,"FURNISHING & HOUSEWARE":12.93,"HEALTH":8.84,"HOME ELECTRONICS":11.88,"OTHERS":12.66,"SPORTS":14.35,"T & B":19.32,"TECHNOLOGY":16.53,"VEHICLE PARTS & ACCESSORIES":13.84},
    "MLA": {"BEAUTY":13.04,"CONSTRUCTION & INDUSTRY":13.19,"CPG":17.92,"ENTERTAINMENT":18.19,"FASHION":13.68,"FURNISHING & HOUSEWARE":13.06,"HEALTH":9.49,"HOME ELECTRONICS":11.52,"OTHERS":20.75,"SPORTS":14.83,"T & B":18.57,"TECHNOLOGY":15.10,"VEHICLE PARTS & ACCESSORIES":17.23},
    "MLC": {"BEAUTY":13.48,"CONSTRUCTION & INDUSTRY":14.01,"CPG":8.37,"ENTERTAINMENT":20.65,"FASHION":18.69,"FURNISHING & HOUSEWARE":12.24,"HEALTH":14.68,"HOME ELECTRONICS":10.15,"OTHERS":11.90,"SPORTS":19.11,"T & B":21.56,"TECHNOLOGY":14.11,"VEHICLE PARTS & ACCESSORIES":15.49},
    "MCO": {"BEAUTY":15.55,"CONSTRUCTION & INDUSTRY":17.79,"CPG":15.77,"ENTERTAINMENT":19.89,"FASHION":23.29,"FURNISHING & HOUSEWARE":19.53,"HEALTH":19.59,"HOME ELECTRONICS":12.14,"OTHERS":17.51,"SPORTS":19.49,"T & B":27.50,"TECHNOLOGY":17.58,"VEHICLE PARTS & ACCESSORIES":19.71},
}


# ── W27 (04/07/2026) ─────────────────────────────────────────────────────────

prev_kpi = {
    "MLB": {
        "3P":        {"bs": 9.27,  "u": 75641810, "bu": 7012138},
        "3P+CBT":    {"bs": 9.27,  "u": 75641810, "bu": 7012138},
        "MELI PRO":  {"bs": 7.04,  "u": 19420000, "bu": 1367000},
        "SELLER DEV":{"bs": 10.27, "u": 56220000, "bu": 5774000},
        "TOTAL":     {"bs": 9.33,  "u": 88829547, "bu": 8291125},
    },
    "MLM": {
        "3P":        {"bs": 12.66, "u": 36797016, "bu": 4656866},
        "CBT":       {"bs": 14.20, "u": 19802268, "bu": 2811998},
        "3P+CBT":    {"bs": 13.20, "u": 56599284, "bu": 7468864},
        "MELI PRO":  {"bs": 9.33,  "u": 9630000,  "bu": 899000},
        "SELLER DEV":{"bs": 13.66, "u": 27170000, "bu": 3710000},
        "TOTAL":     {"bs": 13.20, "u": 56599284, "bu": 7468864},
    },
    "MLA": {
        "3P":        {"bs": 11.75, "u": 7180854,  "bu": 843539},
        "3P+CBT":    {"bs": 11.75, "u": 7180854,  "bu": 843539},
        "MELI PRO":  {"bs": 11.48, "u": 2520000,  "bu": 289000},
        "SELLER DEV":{"bs": 12.82, "u": 4660000,  "bu": 597000},
        "TOTAL":     {"bs": 14.49, "u": 8158567,  "bu": 1182368},
    },
    "MLC": {
        "3P":        {"bs": 12.87, "u": 4884803,  "bu": 628641},
        "CBT":       {"bs": 21.53, "u": 315388,   "bu": 67903},
        "3P+CBT":    {"bs": 13.39, "u": 5200191,  "bu": 696544},
        "MELI PRO":  {"bs": 12.15, "u": 1420000,  "bu": 173000},
        "SELLER DEV":{"bs": 12.31, "u": 3465000,  "bu": 426000},
        "TOTAL":     {"bs": 14.36, "u": 5855105,  "bu": 840895},
    },
    "MCO": {
        "3P":        {"bs": 17.97, "u": 837312,   "bu": 150440},
        "3P+CBT":    {"bs": 17.97, "u": 837312,   "bu": 150440},
        "MELI PRO":  {"bs": 14.68, "u": 259000,   "bu": 38000},
        "SELLER DEV":{"bs": 19.99, "u": 578000,   "bu": 112000},
        "TOTAL":     {"bs": 18.55, "u": 919704,   "bu": 170594},
    },
}

prev_bd = {
    "MLB": {
        "3P":        {"str": 1.95, "sv": 1.01, "ag": 2.55, "exc": 3.96},
        "3P+CBT":    {"str": 1.95, "sv": 1.01, "ag": 2.55, "exc": 3.96},
        "MELI PRO":  {"str": 1.53, "sv": 0.75, "ag": 1.66, "exc": 3.80},
        "SELLER DEV":{"str": 2.10, "sv": 1.10, "ag": 2.85, "exc": 4.02},
    },
    "MLM": {
        "3P":        {"str": 1.08, "sv": 1.85, "ag": 4.16, "exc": 6.49},
        "CBT":       {"str": 1.00, "sv": 2.24, "ag": 3.80, "exc": 7.32},
        "3P+CBT":    {"str": 1.08, "sv": 1.85, "ag": 4.16, "exc": 6.49},
        "MELI PRO":  {"str": 1.21, "sv": 1.25, "ag": 2.80, "exc": 4.30},
        "SELLER DEV":{"str": 1.08, "sv": 1.83, "ag": 4.91, "exc": 6.78},
    },
    "MLA": {
        "3P":        {"str": 1.04, "sv": 1.07, "ag": 4.41, "exc": 4.64},
        "3P+CBT":    {"str": 1.04, "sv": 1.07, "ag": 4.41, "exc": 4.64},
        "MELI PRO":  {"str": 0.59, "sv": 0.76, "ag": 2.58, "exc": 4.98},
        "SELLER DEV":{"str": 1.31, "sv": 1.26, "ag": 5.51, "exc": 4.44},
    },
    "MLC": {
        "3P":        {"str": 0.69, "sv": 2.08, "ag": 5.14, "exc": 6.56},
        "CBT":       {"str": 1.00, "sv": 2.24, "ag": 3.80, "exc": 7.32},
        "3P+CBT":    {"str": 0.69, "sv": 2.08, "ag": 5.14, "exc": 6.56},
        "MELI PRO":  {"str": 0.73, "sv": 2.21, "ag": 3.95, "exc": 5.84},
        "SELLER DEV":{"str": 0.64, "sv": 1.80, "ag": 5.87, "exc": 6.24},
    },
    "MCO": {
        "3P":        {"str": 0.98, "sv": 2.22, "ag": 8.87, "exc": 7.34},
        "3P+CBT":    {"str": 0.98, "sv": 2.22, "ag": 8.87, "exc": 7.34},
        "MELI PRO":  {"str": 0.96, "sv": 2.13, "ag": 5.41, "exc": 7.85},
        "SELLER DEV":{"str": 0.99, "sv": 2.27, "ag": 10.51, "exc": 7.10},
    },
}

prev_vert = {
    "MLB": {"BEAUTY":7.97,"CONSTRUCTION & INDUSTRY":9.77,"CPG":8.32,"ENTERTAINMENT":10.46,"FASHION":8.63,"FURNISHING & HOUSEWARE":8.83,"HEALTH":7.33,"HOME ELECTRONICS":10.01,"OTHERS":10.33,"SPORTS":11.74,"T & B":13.74,"TECHNOLOGY":10.06,"VEHICLE PARTS & ACCESSORIES":9.95},
    "MLM": {"BEAUTY":11.50,"CONSTRUCTION & INDUSTRY":11.26,"CPG":10.14,"ENTERTAINMENT":17.81,"FASHION":13.38,"FURNISHING & HOUSEWARE":12.39,"HEALTH":11.25,"HOME ELECTRONICS":11.50,"OTHERS":12.22,"SPORTS":13.79,"T & B":19.54,"TECHNOLOGY":16.93,"VEHICLE PARTS & ACCESSORIES":13.62},
    "MLA": {"BEAUTY":11.66,"CONSTRUCTION & INDUSTRY":10.60,"CPG":13.35,"ENTERTAINMENT":15.54,"FASHION":13.79,"FURNISHING & HOUSEWARE":10.66,"HEALTH":7.31,"HOME ELECTRONICS":8.27,"OTHERS":19.73,"SPORTS":12.86,"T & B":17.16,"TECHNOLOGY":12.56,"VEHICLE PARTS & ACCESSORIES":14.32},
    "MLC": {"BEAUTY":12.64,"CONSTRUCTION & INDUSTRY":13.60,"CPG":8.13,"ENTERTAINMENT":17.17,"FASHION":22.23,"FURNISHING & HOUSEWARE":10.92,"HEALTH":14.07,"HOME ELECTRONICS":9.84,"OTHERS":12.75,"SPORTS":17.04,"T & B":19.90,"TECHNOLOGY":14.09,"VEHICLE PARTS & ACCESSORIES":15.74},
    "MCO": {"BEAUTY":15.30,"CONSTRUCTION & INDUSTRY":16.29,"CPG":15.69,"ENTERTAINMENT":21.58,"FASHION":23.31,"FURNISHING & HOUSEWARE":18.76,"HEALTH":18.46,"HOME ELECTRONICS":14.23,"OTHERS":17.36,"SPORTS":19.48,"T & B":22.81,"TECHNOLOGY":19.93,"VEHICLE PARTS & ACCESSORIES":17.91},
}


# ── Envio ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python scripts/test_chat_message.py <WEBHOOK_URL>")
        sys.exit(1)

    webhook_url = sys.argv[1]

    msg = build_message(
        week_id="W28",
        week_date=date(2026, 7, 11),
        curr_kpi=curr_kpi,
        prev_kpi=prev_kpi,
        curr_bd=curr_bd,
        prev_bd=prev_bd,
        curr_vert=curr_vert,
        prev_vert=prev_vert,
        month=7,
    )

    import io, sys as _sys
    _sys.stdout = io.TextIOWrapper(_sys.stdout.buffer, encoding="utf-8", errors="replace")
    print("--- Previa da mensagem ---")
    print(msg)
    print("-" * 57)
    print()

    send_to_chat(webhook_url, msg)
