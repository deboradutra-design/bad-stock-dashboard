"""
Envio da mensagem W23 ao Google Chat com dados reais do BigQuery.
Execução: python scripts/test_chat_message.py <WEBHOOK_URL>
"""

import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from chat_notifier import build_message, send_to_chat


# ── W23 (06/06/2026) — primeiro week de Junho ─────────────────────────────────

curr_kpi = {
    "MLB": {
        "3P":        {"bs": 9.52,  "u": 67203409, "bu": 6399515},
        "3P+CBT":    {"bs": 9.52,  "u": 67203409, "bu": 6399515},
        "MELI PRO":  {"bs": 7.17,  "u": 17173797, "bu": 1231809},
        "SELLER DEV":{"bs": 10.33, "u": 50029612, "bu": 5167706},
        "TOTAL":     {"bs": 9.89,  "u": 78022169, "bu": 7720193},
    },
    "MLM": {
        "3P":        {"bs": 12.72, "u": 37156038, "bu": 4724620},
        "CBT":       {"bs": 13.90, "u": 18057867, "bu": 2509573},
        "3P+CBT":    {"bs": 13.10, "u": 55213905, "bu": 7234193},
        "MELI PRO":  {"bs": 9.31,  "u": 9849412,  "bu": 916987},
        "SELLER DEV":{"bs": 13.94, "u": 27306626, "bu": 3807633},
        "TOTAL":     {"bs": 13.39, "u": 60513535, "bu": 8105217},
    },
    "MLA": {
        "3P":        {"bs": 11.40, "u": 6373644,  "bu": 726901},
        "3P+CBT":    {"bs": 11.40, "u": 6373644,  "bu": 726901},
        "MELI PRO":  {"bs": 9.83,  "u": 2258298,  "bu": 222012},
        "SELLER DEV":{"bs": 12.27, "u": 4115346,  "bu": 504889},
        "TOTAL":     {"bs": 13.11, "u": 7369102,  "bu": 965990},
    },
    "MLC": {
        "3P":        {"bs": 13.30, "u": 4581202,  "bu": 609124},
        "CBT":       {"bs": 27.15, "u": 279336,   "bu": 75834},
        "3P+CBT":    {"bs": 14.09, "u": 4860538,  "bu": 684958},
        "MELI PRO":  {"bs": 12.71, "u": 1421766,  "bu": 180682},
        "SELLER DEV":{"bs": 13.56, "u": 3159436,  "bu": 428442},
        "TOTAL":     {"bs": 14.59, "u": 5429637,  "bu": 792377},
    },
    "MCO": {
        "3P":        {"bs": 18.03, "u": 882345,   "bu": 159129},
        "3P+CBT":    {"bs": 18.03, "u": 882345,   "bu": 159129},
        "MELI PRO":  {"bs": 14.23, "u": 267449,   "bu": 38063},
        "SELLER DEV":{"bs": 19.69, "u": 614896,   "bu": 121066},
        "TOTAL":     {"bs": 18.53, "u": 956246,   "bu": 177226},
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
        "CBT":       {"str": 1.11, "sv": 4.68, "ag": 3.01, "exc": 14.15},
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
    "MLB": {"BEAUTY":8.42,"CONSTRUCTION & INDUSTRY":10.18,"CPG":7.72,"ENTERTAINMENT":11.08,"FASHION":9.16,"FURNISHING & HOUSEWARE":8.94,"HEALTH":7.23,"HOME ELECTRONICS":11.11,"OTHERS":10.55,"SPORTS":11.03,"T & B":14.78,"TECHNOLOGY":10.55,"VEHICLE PARTS & ACCESSORIES":10.01},
    "MLM": {"BEAUTY":10.69,"CONSTRUCTION & INDUSTRY":11.36,"CPG":8.54,"ENTERTAINMENT":18.31,"FASHION":14.32,"FURNISHING & HOUSEWARE":12.08,"HEALTH":10.43,"HOME ELECTRONICS":10.01,"OTHERS":13.56,"SPORTS":12.83,"T & B":18.90,"TECHNOLOGY":17.25,"VEHICLE PARTS & ACCESSORIES":13.85},
    "MLA": {"BEAUTY":11.32,"CONSTRUCTION & INDUSTRY":10.52,"CPG":12.52,"ENTERTAINMENT":12.76,"FASHION":15.31,"FURNISHING & HOUSEWARE":10.43,"HEALTH":6.69,"HOME ELECTRONICS":8.57,"OTHERS":18.84,"SPORTS":11.76,"T & B":16.66,"TECHNOLOGY":11.18,"VEHICLE PARTS & ACCESSORIES":11.44},
    "MLC": {"BEAUTY":10.66,"CONSTRUCTION & INDUSTRY":15.22,"CPG":8.84,"ENTERTAINMENT":20.57,"FASHION":19.86,"FURNISHING & HOUSEWARE":12.76,"HEALTH":14.84,"HOME ELECTRONICS":10.74,"OTHERS":13.60,"SPORTS":18.98,"T & B":21.72,"TECHNOLOGY":15.95,"VEHICLE PARTS & ACCESSORIES":16.81},
    "MCO": {"BEAUTY":15.38,"CONSTRUCTION & INDUSTRY":15.74,"CPG":15.86,"ENTERTAINMENT":24.94,"FASHION":21.98,"FURNISHING & HOUSEWARE":23.15,"HEALTH":17.28,"HOME ELECTRONICS":12.52,"OTHERS":24.13,"SPORTS":18.73,"T & B":22.29,"TECHNOLOGY":19.41,"VEHICLE PARTS & ACCESSORIES":17.56},
}


# ── W22 (30/05/2026) ─────────────────────────────────────────────────────────

prev_kpi = {
    "MLB": {
        "3P":        {"bs": 9.36,  "u": 67930656, "bu": 6359923},
        "3P+CBT":    {"bs": 9.36,  "u": 67930656, "bu": 6359923},
        "MELI PRO":  {"bs": 7.32,  "u": 17720918, "bu": 1297534},
        "SELLER DEV":{"bs": 10.08, "u": 50209738, "bu": 5062389},
        "TOTAL":     {"bs": 9.59,  "u": 78619431, "bu": 7539076},
    },
    "MLM": {
        "3P":        {"bs": 12.72, "u": 37929909, "bu": 4826409},
        "CBT":       {"bs": 13.70, "u": 18779624, "bu": 2571899},
        "3P+CBT":    {"bs": 13.05, "u": 56709533, "bu": 7398308},
        "MELI PRO":  {"bs": 8.99,  "u": 10601722, "bu": 953237},
        "SELLER DEV":{"bs": 14.17, "u": 27328187, "bu": 3873172},
        "TOTAL":     {"bs": 13.20, "u": 63226185, "bu": 8347198},
    },
    "MLA": {
        "3P":        {"bs": 11.59, "u": 6571635,  "bu": 761557},
        "3P+CBT":    {"bs": 11.59, "u": 6571635,  "bu": 761557},
        "MELI PRO":  {"bs": 9.23,  "u": 2374989,  "bu": 219214},
        "SELLER DEV":{"bs": 12.92, "u": 4196646,  "bu": 542343},
        "TOTAL":     {"bs": 13.11, "u": 7630010,  "bu": 1000212},
    },
    "MLC": {
        "3P":        {"bs": 12.25, "u": 5603060,  "bu": 686366},
        "CBT":       {"bs": 23.89, "u": 288027,   "bu": 68801},
        "3P+CBT":    {"bs": 12.82, "u": 5891087,  "bu": 755167},
        "MELI PRO":  {"bs": 11.25, "u": 1963521,  "bu": 220917},
        "SELLER DEV":{"bs": 12.79, "u": 3639539,  "bu": 465449},
        "TOTAL":     {"bs": 13.45, "u": 6774362,  "bu": 910956},
    },
    "MCO": {
        "3P":        {"bs": 18.21, "u": 902420,   "bu": 164341},
        "3P+CBT":    {"bs": 18.21, "u": 902420,   "bu": 164341},
        "MELI PRO":  {"bs": 15.86, "u": 273469,   "bu": 43376},
        "SELLER DEV":{"bs": 19.23, "u": 628951,   "bu": 120965},
        "TOTAL":     {"bs": 18.81, "u": 976013,   "bu": 183619},
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
        "CBT":       {"str": 1.11, "sv": 4.68, "ag": 3.01, "exc": 14.15},
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
    "MLB": {"BEAUTY":7.99,"CONSTRUCTION & INDUSTRY":10.00,"CPG":8.09,"ENTERTAINMENT":10.26,"FASHION":9.04,"FURNISHING & HOUSEWARE":8.68,"HEALTH":6.90,"HOME ELECTRONICS":10.67,"OTHERS":9.71,"SPORTS":10.74,"T & B":14.47,"TECHNOLOGY":10.75,"VEHICLE PARTS & ACCESSORIES":9.69},
    "MLM": {"BEAUTY":10.26,"CONSTRUCTION & INDUSTRY":11.40,"CPG":8.21,"ENTERTAINMENT":18.38,"FASHION":14.32,"FURNISHING & HOUSEWARE":12.13,"HEALTH":10.59,"HOME ELECTRONICS":9.68,"OTHERS":13.35,"SPORTS":13.01,"T & B":18.87,"TECHNOLOGY":17.34,"VEHICLE PARTS & ACCESSORIES":13.66},
    "MLA": {"BEAUTY":10.85,"CONSTRUCTION & INDUSTRY":10.83,"CPG":11.43,"ENTERTAINMENT":26.66,"FASHION":15.40,"FURNISHING & HOUSEWARE":10.63,"HEALTH":6.88,"HOME ELECTRONICS":8.92,"OTHERS":20.26,"SPORTS":11.99,"T & B":17.00,"TECHNOLOGY":12.44,"VEHICLE PARTS & ACCESSORIES":11.34},
    "MLC": {"BEAUTY":9.20,"CONSTRUCTION & INDUSTRY":14.25,"CPG":8.81,"ENTERTAINMENT":20.16,"FASHION":17.69,"FURNISHING & HOUSEWARE":11.33,"HEALTH":13.99,"HOME ELECTRONICS":9.13,"OTHERS":13.17,"SPORTS":17.13,"T & B":20.67,"TECHNOLOGY":13.49,"VEHICLE PARTS & ACCESSORIES":15.48},
    "MCO": {"BEAUTY":15.98,"CONSTRUCTION & INDUSTRY":17.03,"CPG":16.58,"ENTERTAINMENT":30.71,"FASHION":23.46,"FURNISHING & HOUSEWARE":18.51,"HEALTH":16.46,"HOME ELECTRONICS":12.73,"OTHERS":27.67,"SPORTS":18.86,"T & B":26.59,"TECHNOLOGY":19.99,"VEHICLE PARTS & ACCESSORIES":17.38},
}


# ── Envio ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python scripts/test_chat_message.py <WEBHOOK_URL>")
        sys.exit(1)

    webhook_url = sys.argv[1]

    msg = build_message(
        week_id="W23",
        week_date=date(2026, 6, 6),
        curr_kpi=curr_kpi,
        prev_kpi=prev_kpi,
        curr_bd=curr_bd,
        prev_bd=prev_bd,
        curr_vert=curr_vert,
        prev_vert=prev_vert,
        month=6,
    )

    import io, sys as _sys
    _sys.stdout = io.TextIOWrapper(_sys.stdout.buffer, encoding="utf-8", errors="replace")
    print("--- Previa da mensagem ---")
    print(msg)
    print("-" * 57)
    print()

    send_to_chat(webhook_url, msg)
