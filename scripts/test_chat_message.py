"""
Envio da mensagem W25 ao Google Chat com dados reais do BigQuery.
Execução: python scripts/test_chat_message.py <WEBHOOK_URL>
"""

import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from chat_notifier import build_message, send_to_chat


# ── W25 (20/06/2026) ─────────────────────────────────────────────────────────

curr_kpi = {
    "MLB": {
        "3P":        {"bs": 9.34,  "u": 67833896, "bu": 6333831},
        "3P+CBT":    {"bs": 9.34,  "u": 67833896, "bu": 6333831},
        "MELI PRO":  {"bs": 6.98,  "u": 17343563, "bu": 1210286},
        "SELLER DEV":{"bs": 10.15, "u": 50490333, "bu": 5123545},
        "TOTAL":     {"bs": 9.67,  "u": 79467562, "bu": 7681771},
    },
    "MLM": {
        "3P":        {"bs": 12.45, "u": 37328810, "bu": 4648474},
        "CBT":       {"bs": 13.49, "u": 18761108, "bu": 2530070},
        "3P+CBT":    {"bs": 12.80, "u": 56089918, "bu": 7178544},
        "MELI PRO":  {"bs": 9.22,  "u": 9790182,  "bu": 902792},
        "SELLER DEV":{"bs": 13.60, "u": 27538628, "bu": 3745682},
        "TOTAL":     {"bs": 13.48, "u": 61736771, "bu": 8322061},
    },
    "MLA": {
        "3P":        {"bs": 12.12, "u": 6340759,  "bu": 768349},
        "3P+CBT":    {"bs": 12.12, "u": 6340759,  "bu": 768349},
        "MELI PRO":  {"bs": 10.76, "u": 2232835,  "bu": 240184},
        "SELLER DEV":{"bs": 12.86, "u": 4107924,  "bu": 528165},
        "TOTAL":     {"bs": 14.71, "u": 7288918,  "bu": 1072218},
    },
    "MLC": {
        "3P":        {"bs": 12.48, "u": 4985664,  "bu": 621963},
        "CBT":       {"bs": 22.16, "u": 319445,   "bu": 70795},
        "3P+CBT":    {"bs": 13.06, "u": 5305109,  "bu": 692758},
        "MELI PRO":  {"bs": 12.58, "u": 1452280,  "bu": 182758},
        "SELLER DEV":{"bs": 12.43, "u": 3533384,  "bu": 439205},
        "TOTAL":     {"bs": 13.91, "u": 5862155,  "bu": 815304},
    },
    "MCO": {
        "3P":        {"bs": 18.10, "u": 857652,   "bu": 155217},
        "3P+CBT":    {"bs": 18.10, "u": 857652,   "bu": 155217},
        "MELI PRO":  {"bs": 15.75, "u": 267097,   "bu": 42080},
        "SELLER DEV":{"bs": 19.16, "u": 590555,   "bu": 113137},
        "TOTAL":     {"bs": 18.79, "u": 931011,   "bu": 174917},
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
    "MLB": {"BEAUTY":8.42,"CONSTRUCTION & INDUSTRY":9.89,"CPG":7.52,"ENTERTAINMENT":11.33,"FASHION":9.00,"FURNISHING & HOUSEWARE":8.65,"HEALTH":7.15,"HOME ELECTRONICS":10.57,"OTHERS":10.38,"SPORTS":11.50,"T & B":14.29,"TECHNOLOGY":10.51,"VEHICLE PARTS & ACCESSORIES":9.95},
    "MLM": {"BEAUTY":11.13,"CONSTRUCTION & INDUSTRY":10.93,"CPG":9.15,"ENTERTAINMENT":16.95,"FASHION":13.36,"FURNISHING & HOUSEWARE":11.50,"HEALTH":10.60,"HOME ELECTRONICS":9.93,"OTHERS":12.39,"SPORTS":13.01,"T & B":19.82,"TECHNOLOGY":16.74,"VEHICLE PARTS & ACCESSORIES":13.61},
    "MLA": {"BEAUTY":12.96,"CONSTRUCTION & INDUSTRY":10.87,"CPG":12.37,"ENTERTAINMENT":14.97,"FASHION":15.26,"FURNISHING & HOUSEWARE":10.92,"HEALTH":7.82,"HOME ELECTRONICS":9.50,"OTHERS":17.77,"SPORTS":13.32,"T & B":17.39,"TECHNOLOGY":12.85,"VEHICLE PARTS & ACCESSORIES":14.06},
    "MLC": {"BEAUTY":10.80,"CONSTRUCTION & INDUSTRY":14.02,"CPG":7.39,"ENTERTAINMENT":19.33,"FASHION":21.54,"FURNISHING & HOUSEWARE":11.26,"HEALTH":12.84,"HOME ELECTRONICS":10.04,"OTHERS":12.22,"SPORTS":18.07,"T & B":20.69,"TECHNOLOGY":15.31,"VEHICLE PARTS & ACCESSORIES":15.72},
    "MCO": {"BEAUTY":16.09,"CONSTRUCTION & INDUSTRY":17.28,"CPG":15.62,"ENTERTAINMENT":26.32,"FASHION":23.96,"FURNISHING & HOUSEWARE":18.92,"HEALTH":17.96,"HOME ELECTRONICS":12.81,"OTHERS":23.86,"SPORTS":18.23,"T & B":23.35,"TECHNOLOGY":19.70,"VEHICLE PARTS & ACCESSORIES":17.96},
}


# ── W24 (13/06/2026) ─────────────────────────────────────────────────────────

prev_kpi = {
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
    "MLB": {"BEAUTY":8.86,"CONSTRUCTION & INDUSTRY":10.28,"CPG":7.47,"ENTERTAINMENT":11.49,"FASHION":9.27,"FURNISHING & HOUSEWARE":9.45,"HEALTH":7.06,"HOME ELECTRONICS":11.41,"OTHERS":10.62,"SPORTS":11.46,"T & B":15.17,"TECHNOLOGY":10.61,"VEHICLE PARTS & ACCESSORIES":10.04},
    "MLM": {"BEAUTY":10.60,"CONSTRUCTION & INDUSTRY":11.02,"CPG":8.71,"ENTERTAINMENT":17.22,"FASHION":13.83,"FURNISHING & HOUSEWARE":11.70,"HEALTH":10.56,"HOME ELECTRONICS":9.92,"OTHERS":13.34,"SPORTS":12.84,"T & B":18.62,"TECHNOLOGY":16.61,"VEHICLE PARTS & ACCESSORIES":13.42},
    "MLA": {"BEAUTY":12.40,"CONSTRUCTION & INDUSTRY":10.36,"CPG":12.50,"ENTERTAINMENT":13.37,"FASHION":15.02,"FURNISHING & HOUSEWARE":10.56,"HEALTH":6.92,"HOME ELECTRONICS":9.00,"OTHERS":18.44,"SPORTS":12.23,"T & B":16.51,"TECHNOLOGY":12.21,"VEHICLE PARTS & ACCESSORIES":12.67},
    "MLC": {"BEAUTY":10.44,"CONSTRUCTION & INDUSTRY":13.88,"CPG":7.72,"ENTERTAINMENT":19.97,"FASHION":20.33,"FURNISHING & HOUSEWARE":11.13,"HEALTH":13.56,"HOME ELECTRONICS":9.99,"OTHERS":12.65,"SPORTS":17.52,"T & B":20.51,"TECHNOLOGY":15.22,"VEHICLE PARTS & ACCESSORIES":16.34},
    "MCO": {"BEAUTY":15.39,"CONSTRUCTION & INDUSTRY":15.78,"CPG":16.06,"ENTERTAINMENT":25.85,"FASHION":23.45,"FURNISHING & HOUSEWARE":19.87,"HEALTH":19.39,"HOME ELECTRONICS":12.36,"OTHERS":24.11,"SPORTS":19.37,"T & B":22.31,"TECHNOLOGY":19.06,"VEHICLE PARTS & ACCESSORIES":17.63},
}


# ── Envio ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python scripts/test_chat_message.py <WEBHOOK_URL>")
        sys.exit(1)

    webhook_url = sys.argv[1]

    msg = build_message(
        week_id="W25",
        week_date=date(2026, 6, 20),
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
