"""
Envio da mensagem W26 ao Google Chat com dados reais do BigQuery.
Execução: python scripts/test_chat_message.py <WEBHOOK_URL>
"""

import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from chat_notifier import build_message, send_to_chat


# ── W26 (27/06/2026) ─────────────────────────────────────────────────────────

curr_kpi = {
    "MLB": {
        "3P":        {"bs": 9.44,  "u": 69753059, "bu": 6585573},
        "3P+CBT":    {"bs": 9.44,  "u": 69753059, "bu": 6585573},
        "MELI PRO":  {"bs": 7.04,  "u": 17913790, "bu": 1260333},
        "SELLER DEV":{"bs": 10.27, "u": 51839269, "bu": 5325240},
        "TOTAL":     {"bs": 9.65,  "u": 82345970, "bu": 7943008},
    },
    "MLM": {
        "3P":        {"bs": 12.53, "u": 37324724, "bu": 4675171},
        "CBT":       {"bs": 13.73, "u": 19187558, "bu": 2633851},
        "3P+CBT":    {"bs": 12.93, "u": 56512282, "bu": 7309022},
        "MELI PRO":  {"bs": 9.33,  "u": 9769727,  "bu": 911892},
        "SELLER DEV":{"bs": 13.66, "u": 27554997, "bu": 3763279},
        "TOTAL":     {"bs": 13.73, "u": 62732088, "bu": 8613718},
    },
    "MLA": {
        "3P":        {"bs": 12.35, "u": 6449352,  "bu": 796446},
        "3P+CBT":    {"bs": 12.35, "u": 6449352,  "bu": 796446},
        "MELI PRO":  {"bs": 11.48, "u": 2265000,  "bu": 259997},
        "SELLER DEV":{"bs": 12.82, "u": 4184352,  "bu": 536449},
        "TOTAL":     {"bs": 15.08, "u": 7403689,  "bu": 1116240},
    },
    "MLC": {
        "3P":        {"bs": 12.26, "u": 4995677,  "bu": 612654},
        "CBT":       {"bs": 21.10, "u": 321053,   "bu": 67757},
        "3P+CBT":    {"bs": 12.80, "u": 5316730,  "bu": 680411},
        "MELI PRO":  {"bs": 12.15, "u": 1452342,  "bu": 176478},
        "SELLER DEV":{"bs": 12.31, "u": 3543335,  "bu": 436176},
        "TOTAL":     {"bs": 13.69, "u": 5943640,  "bu": 813784},
    },
    "MCO": {
        "3P":        {"bs": 18.34, "u": 859994,   "bu": 157753},
        "3P+CBT":    {"bs": 18.34, "u": 859994,   "bu": 157753},
        "MELI PRO":  {"bs": 14.68, "u": 266289,   "bu": 39088},
        "SELLER DEV":{"bs": 19.99, "u": 593705,   "bu": 118665},
        "TOTAL":     {"bs": 19.03, "u": 934902,   "bu": 177950},
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
    "MLB": {"BEAUTY":8.27,"CONSTRUCTION & INDUSTRY":9.89,"CPG":7.82,"ENTERTAINMENT":11.49,"FASHION":8.85,"FURNISHING & HOUSEWARE":8.74,"HEALTH":7.28,"HOME ELECTRONICS":11.21,"OTHERS":10.50,"SPORTS":12.08,"T & B":13.99,"TECHNOLOGY":10.70,"VEHICLE PARTS & ACCESSORIES":10.33},
    "MLM": {"BEAUTY":11.16,"CONSTRUCTION & INDUSTRY":11.09,"CPG":9.17,"ENTERTAINMENT":16.72,"FASHION":13.39,"FURNISHING & HOUSEWARE":11.92,"HEALTH":11.07,"HOME ELECTRONICS":10.40,"OTHERS":12.65,"SPORTS":13.34,"T & B":19.37,"TECHNOLOGY":17.11,"VEHICLE PARTS & ACCESSORIES":13.49},
    "MLA": {"BEAUTY":12.76,"CONSTRUCTION & INDUSTRY":11.26,"CPG":13.32,"ENTERTAINMENT":14.61,"FASHION":14.88,"FURNISHING & HOUSEWARE":11.10,"HEALTH":7.68,"HOME ELECTRONICS":9.78,"OTHERS":20.46,"SPORTS":13.94,"T & B":16.88,"TECHNOLOGY":12.39,"VEHICLE PARTS & ACCESSORIES":14.67},
    "MLC": {"BEAUTY":11.27,"CONSTRUCTION & INDUSTRY":13.52,"CPG":7.33,"ENTERTAINMENT":14.85,"FASHION":21.93,"FURNISHING & HOUSEWARE":10.82,"HEALTH":12.95,"HOME ELECTRONICS":9.85,"OTHERS":13.03,"SPORTS":17.39,"T & B":19.06,"TECHNOLOGY":14.12,"VEHICLE PARTS & ACCESSORIES":16.02},
    "MCO": {"BEAUTY":15.32,"CONSTRUCTION & INDUSTRY":17.23,"CPG":15.68,"ENTERTAINMENT":23.04,"FASHION":24.25,"FURNISHING & HOUSEWARE":18.68,"HEALTH":18.58,"HOME ELECTRONICS":14.96,"OTHERS":23.84,"SPORTS":18.96,"T & B":23.16,"TECHNOLOGY":20.14,"VEHICLE PARTS & ACCESSORIES":19.19},
}


# ── W25 (20/06/2026) ─────────────────────────────────────────────────────────

prev_kpi = {
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
    "MLB": {"BEAUTY":8.42,"CONSTRUCTION & INDUSTRY":9.89,"CPG":7.52,"ENTERTAINMENT":11.33,"FASHION":9.00,"FURNISHING & HOUSEWARE":8.65,"HEALTH":7.15,"HOME ELECTRONICS":10.57,"OTHERS":10.38,"SPORTS":11.50,"T & B":14.29,"TECHNOLOGY":10.51,"VEHICLE PARTS & ACCESSORIES":9.95},
    "MLM": {"BEAUTY":11.13,"CONSTRUCTION & INDUSTRY":10.93,"CPG":9.15,"ENTERTAINMENT":16.95,"FASHION":13.36,"FURNISHING & HOUSEWARE":11.50,"HEALTH":10.60,"HOME ELECTRONICS":9.93,"OTHERS":12.39,"SPORTS":13.01,"T & B":19.82,"TECHNOLOGY":16.74,"VEHICLE PARTS & ACCESSORIES":13.61},
    "MLA": {"BEAUTY":12.96,"CONSTRUCTION & INDUSTRY":10.87,"CPG":12.37,"ENTERTAINMENT":14.97,"FASHION":15.26,"FURNISHING & HOUSEWARE":10.92,"HEALTH":7.82,"HOME ELECTRONICS":9.50,"OTHERS":17.77,"SPORTS":13.32,"T & B":17.39,"TECHNOLOGY":12.85,"VEHICLE PARTS & ACCESSORIES":14.06},
    "MLC": {"BEAUTY":10.80,"CONSTRUCTION & INDUSTRY":14.02,"CPG":7.39,"ENTERTAINMENT":19.33,"FASHION":21.54,"FURNISHING & HOUSEWARE":11.26,"HEALTH":12.84,"HOME ELECTRONICS":10.04,"OTHERS":12.22,"SPORTS":18.07,"T & B":20.69,"TECHNOLOGY":15.31,"VEHICLE PARTS & ACCESSORIES":15.72},
    "MCO": {"BEAUTY":16.09,"CONSTRUCTION & INDUSTRY":17.28,"CPG":15.62,"ENTERTAINMENT":26.32,"FASHION":23.96,"FURNISHING & HOUSEWARE":18.92,"HEALTH":17.96,"HOME ELECTRONICS":12.81,"OTHERS":23.86,"SPORTS":18.23,"T & B":23.35,"TECHNOLOGY":19.70,"VEHICLE PARTS & ACCESSORIES":17.96},
}


# ── Envio ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python scripts/test_chat_message.py <WEBHOOK_URL>")
        sys.exit(1)

    webhook_url = sys.argv[1]

    msg = build_message(
        week_id="W26",
        week_date=date(2026, 6, 27),
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
