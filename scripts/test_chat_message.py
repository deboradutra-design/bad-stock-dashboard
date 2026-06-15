"""
Envio da mensagem W24 ao Google Chat com dados reais do BigQuery.
Execução: python scripts/test_chat_message.py <WEBHOOK_URL>
"""

import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from chat_notifier import build_message, send_to_chat


# ── W24 (13/06/2026) ─────────────────────────────────────────────────────────

curr_kpi = {
    "MLB": {
        "3P":        {"bs": 9.65,  "u": 66929629, "bu": 6456857},
        "3P+CBT":    {"bs": 9.65,  "u": 66929629, "bu": 6456857},
        "MELI PRO":  {"bs": 7.57,  "u": 17041238, "bu": 1289383},
        "SELLER DEV":{"bs": 10.36, "u": 49888391, "bu": 5167474},
        "TOTAL":     {"bs": 9.84,  "u": 77884846, "bu": 7660187},
    },
    "MLM": {
        "3P":        {"bs": 12.43, "u": 37927433, "bu": 4715577},
        "CBT":       {"bs": 13.46, "u": 18615812, "bu": 2504769},
        "3P+CBT":    {"bs": 12.77, "u": 56543245, "bu": 7220346},
        "MELI PRO":  {"bs": 9.31,  "u": 9943829,  "bu": 925828},
        "SELLER DEV":{"bs": 13.54, "u": 27983604, "bu": 3789749},
        "TOTAL":     {"bs": 13.16, "u": 61932938, "bu": 8152402},
    },
    "MLA": {
        "3P":        {"bs": 11.64, "u": 6369213,  "bu": 741366},
        "3P+CBT":    {"bs": 11.64, "u": 6369213,  "bu": 741366},
        "MELI PRO":  {"bs": 10.24, "u": 2261977,  "bu": 231696},
        "SELLER DEV":{"bs": 12.41, "u": 4107236,  "bu": 509670},
        "TOTAL":     {"bs": 13.60, "u": 7323592,  "bu": 996330},
    },
    "MLC": {
        "3P":        {"bs": 12.48, "u": 4855840,  "bu": 605965},
        "CBT":       {"bs": 22.45, "u": 324401,   "bu": 72816},
        "3P+CBT":    {"bs": 13.10, "u": 5180241,  "bu": 678781},
        "MELI PRO":  {"bs": 12.02, "u": 1449235,  "bu": 174157},
        "SELLER DEV":{"bs": 12.68, "u": 3406605,  "bu": 431808},
        "TOTAL":     {"bs": 13.88, "u": 5742004,  "bu": 797088},
    },
    "MCO": {
        "3P":        {"bs": 18.02, "u": 863948,   "bu": 155659},
        "3P+CBT":    {"bs": 18.02, "u": 863948,   "bu": 155659},
        "MELI PRO":  {"bs": 15.20, "u": 266916,   "bu": 40563},
        "SELLER DEV":{"bs": 19.28, "u": 597032,   "bu": 115096},
        "TOTAL":     {"bs": 18.73, "u": 937565,   "bu": 175619},
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
    "MLB": {"BEAUTY":8.86,"CONSTRUCTION & INDUSTRY":10.28,"CPG":7.47,"ENTERTAINMENT":11.49,"FASHION":9.27,"FURNISHING & HOUSEWARE":9.45,"HEALTH":7.06,"HOME ELECTRONICS":11.41,"OTHERS":10.62,"SPORTS":11.46,"T & B":15.17,"TECHNOLOGY":10.61,"VEHICLE PARTS & ACCESSORIES":10.04},
    "MLM": {"BEAUTY":10.60,"CONSTRUCTION & INDUSTRY":11.02,"CPG":8.71,"ENTERTAINMENT":17.22,"FASHION":13.83,"FURNISHING & HOUSEWARE":11.70,"HEALTH":10.56,"HOME ELECTRONICS":9.92,"OTHERS":13.34,"SPORTS":12.84,"T & B":18.62,"TECHNOLOGY":16.61,"VEHICLE PARTS & ACCESSORIES":13.42},
    "MLA": {"BEAUTY":12.40,"CONSTRUCTION & INDUSTRY":10.36,"CPG":12.50,"ENTERTAINMENT":13.37,"FASHION":15.02,"FURNISHING & HOUSEWARE":10.56,"HEALTH":6.92,"HOME ELECTRONICS":9.00,"OTHERS":18.44,"SPORTS":12.23,"T & B":16.51,"TECHNOLOGY":12.21,"VEHICLE PARTS & ACCESSORIES":12.67},
    "MLC": {"BEAUTY":10.44,"CONSTRUCTION & INDUSTRY":13.88,"CPG":7.72,"ENTERTAINMENT":19.97,"FASHION":20.33,"FURNISHING & HOUSEWARE":11.13,"HEALTH":13.56,"HOME ELECTRONICS":9.99,"OTHERS":12.65,"SPORTS":17.52,"T & B":20.51,"TECHNOLOGY":15.22,"VEHICLE PARTS & ACCESSORIES":16.34},
    "MCO": {"BEAUTY":15.39,"CONSTRUCTION & INDUSTRY":15.78,"CPG":16.06,"ENTERTAINMENT":25.85,"FASHION":23.45,"FURNISHING & HOUSEWARE":19.87,"HEALTH":19.39,"HOME ELECTRONICS":12.36,"OTHERS":24.11,"SPORTS":19.37,"T & B":22.31,"TECHNOLOGY":19.06,"VEHICLE PARTS & ACCESSORIES":17.63},
}


# ── W23 (06/06/2026) ─────────────────────────────────────────────────────────

prev_kpi = {
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
    "MLB": {"BEAUTY":8.42,"CONSTRUCTION & INDUSTRY":10.18,"CPG":7.72,"ENTERTAINMENT":11.08,"FASHION":9.16,"FURNISHING & HOUSEWARE":8.94,"HEALTH":7.23,"HOME ELECTRONICS":11.11,"OTHERS":10.55,"SPORTS":11.03,"T & B":14.78,"TECHNOLOGY":10.55,"VEHICLE PARTS & ACCESSORIES":10.01},
    "MLM": {"BEAUTY":10.69,"CONSTRUCTION & INDUSTRY":11.36,"CPG":8.54,"ENTERTAINMENT":18.31,"FASHION":14.32,"FURNISHING & HOUSEWARE":12.08,"HEALTH":10.43,"HOME ELECTRONICS":10.01,"OTHERS":13.56,"SPORTS":12.83,"T & B":18.90,"TECHNOLOGY":17.25,"VEHICLE PARTS & ACCESSORIES":13.85},
    "MLA": {"BEAUTY":11.32,"CONSTRUCTION & INDUSTRY":10.52,"CPG":12.52,"ENTERTAINMENT":12.76,"FASHION":15.31,"FURNISHING & HOUSEWARE":10.43,"HEALTH":6.69,"HOME ELECTRONICS":8.57,"OTHERS":18.84,"SPORTS":11.76,"T & B":16.66,"TECHNOLOGY":11.18,"VEHICLE PARTS & ACCESSORIES":11.44},
    "MLC": {"BEAUTY":10.66,"CONSTRUCTION & INDUSTRY":15.22,"CPG":8.84,"ENTERTAINMENT":20.57,"FASHION":19.86,"FURNISHING & HOUSEWARE":12.76,"HEALTH":14.84,"HOME ELECTRONICS":10.74,"OTHERS":13.60,"SPORTS":18.98,"T & B":21.72,"TECHNOLOGY":15.95,"VEHICLE PARTS & ACCESSORIES":16.81},
    "MCO": {"BEAUTY":15.38,"CONSTRUCTION & INDUSTRY":15.74,"CPG":15.86,"ENTERTAINMENT":24.94,"FASHION":21.98,"FURNISHING & HOUSEWARE":23.15,"HEALTH":17.28,"HOME ELECTRONICS":12.52,"OTHERS":24.13,"SPORTS":18.73,"T & B":22.29,"TECHNOLOGY":19.41,"VEHICLE PARTS & ACCESSORIES":17.56},
}


# ── Envio ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python scripts/test_chat_message.py <WEBHOOK_URL>")
        sys.exit(1)

    webhook_url = sys.argv[1]

    msg = build_message(
        week_id="W24",
        week_date=date(2026, 6, 13),
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
