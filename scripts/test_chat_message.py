"""
Envio da mensagem W20 ao Google Chat com dados reais do BigQuery.
Execução: python scripts/test_chat_message.py <WEBHOOK_URL>
"""

import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from chat_notifier import build_message, send_to_chat


# ── W20 (16/05/2026) ─────────────────────────────────────────────────────────

curr_kpi = {
    "MLB": {
        "3P":        {"bs": 9.48,  "u": 63819868, "bu": 6048072},
        "3P+CBT":    {"bs": 9.48,  "u": 63819868, "bu": 6048072},
        "MELI PRO":  {"bs": 7.73,  "u": 16323017, "bu": 1262439},
        "SELLER DEV":{"bs": 10.08, "u": 47496851, "bu": 4785633},
        "TOTAL":     {"bs": 9.95,  "u": 73437012, "bu": 7306506},
    },
    "MLM": {
        "3P":        {"bs": 13.23, "u": 38808889, "bu": 5134426},
        "CBT":       {"bs": 14.36, "u": 18264580, "bu": 2623111},
        "3P+CBT":    {"bs": 13.59, "u": 57073469, "bu": 7757537},
        "MELI PRO":  {"bs": 9.58,  "u": 10595734, "bu": 1014562},
        "SELLER DEV":{"bs": 14.60, "u": 28213155, "bu": 4119864},
        "TOTAL":     {"bs": 13.53, "u": 65502435, "bu": 8865494},
    },
    "MLA": {
        "3P":        {"bs": 11.19, "u": 6546931,  "bu": 732325},
        "3P+CBT":    {"bs": 11.19, "u": 6546931,  "bu": 732325},
        "MELI PRO":  {"bs": 8.92,  "u": 2450050,  "bu": 218452},
        "SELLER DEV":{"bs": 12.54, "u": 4096881,  "bu": 513873},
        "TOTAL":     {"bs": 11.90, "u": 7733150,  "bu": 919869},
    },
    "MLC": {
        "3P":        {"bs": 13.99, "u": 4660946,  "bu": 652130},
        "CBT":       {"bs": 22.94, "u": 274221,   "bu": 62910},
        "3P+CBT":    {"bs": 14.49, "u": 4935167,  "bu": 715040},
        "MELI PRO":  {"bs": 12.75, "u": 1477418,  "bu": 188304},
        "SELLER DEV":{"bs": 14.57, "u": 3183528,  "bu": 463826},
        "TOTAL":     {"bs": 14.81, "u": 5607369,  "bu": 830480},
    },
    "MCO": {
        "3P":        {"bs": 19.47, "u": 845541,   "bu": 164639},
        "3P+CBT":    {"bs": 19.47, "u": 845541,   "bu": 164639},
        "MELI PRO":  {"bs": 16.39, "u": 271779,   "bu": 44534},
        "SELLER DEV":{"bs": 20.93, "u": 573762,   "bu": 120105},
        "TOTAL":     {"bs": 19.80, "u": 924696,   "bu": 183068},
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
        "3P":        {"str": 1.11, "sv": 1.67, "ag": 4.33, "exc": 6.10},
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
        "3P":        {"str": 0.67, "sv": 1.93, "ag": 5.26, "exc": 6.11},
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
    "MLB": {"BEAUTY":8.54,"CONSTRUCTION & INDUSTRY":10.53,"CPG":7.78,"ENTERTAINMENT":10.41,"FASHION":10.26,"FURNISHING & HOUSEWARE":8.75,"HEALTH":6.43,"HOME ELECTRONICS":9.96,"OTHERS":9.44,"SPORTS":10.48,"T & B":14.11,"TECHNOLOGY":9.95,"VEHICLE PARTS & ACCESSORIES":9.51},
    "MLM": {"BEAUTY":10.49,"CONSTRUCTION & INDUSTRY":11.96,"CPG":7.92,"ENTERTAINMENT":18.25,"FASHION":15.98,"FURNISHING & HOUSEWARE":12.80,"HEALTH":10.14,"HOME ELECTRONICS":10.16,"OTHERS":12.43,"SPORTS":13.40,"T & B":18.53,"TECHNOLOGY":17.51,"VEHICLE PARTS & ACCESSORIES":14.14},
    "MLA": {"BEAUTY":10.27,"CONSTRUCTION & INDUSTRY":10.83,"CPG":10.80,"ENTERTAINMENT":23.09,"FASHION":14.16,"FURNISHING & HOUSEWARE":10.49,"HEALTH":6.66,"HOME ELECTRONICS":10.32,"OTHERS":30.68,"SPORTS":12.21,"T & B":17.26,"TECHNOLOGY":10.89,"VEHICLE PARTS & ACCESSORIES":11.06},
    "MLC": {"BEAUTY":11.57,"CONSTRUCTION & INDUSTRY":15.43,"CPG":10.33,"ENTERTAINMENT":23.18,"FASHION":18.95,"FURNISHING & HOUSEWARE":12.73,"HEALTH":15.91,"HOME ELECTRONICS":10.45,"OTHERS":12.79,"SPORTS":19.15,"T & B":23.10,"TECHNOLOGY":15.72,"VEHICLE PARTS & ACCESSORIES":16.90},
    "MCO": {"BEAUTY":15.58,"CONSTRUCTION & INDUSTRY":18.77,"CPG":19.85,"ENTERTAINMENT":32.77,"FASHION":26.26,"FURNISHING & HOUSEWARE":19.51,"HEALTH":18.72,"HOME ELECTRONICS":13.86,"OTHERS":24.95,"SPORTS":18.55,"T & B":28.02,"TECHNOLOGY":19.95,"VEHICLE PARTS & ACCESSORIES":18.17},
}


# ── W19 (09/05/2026) ─────────────────────────────────────────────────────────

prev_kpi = {
    "MLB": {
        "3P":        {"bs": 9.43,  "u": 62263407, "bu": 5873556},
        "3P+CBT":    {"bs": 9.43,  "u": 62263407, "bu": 5873556},
        "MELI PRO":  {"bs": 7.06,  "u": 16045239, "bu": 1133189},
        "SELLER DEV":{"bs": 10.26, "u": 46218168, "bu": 4740367},
        "TOTAL":     {"bs": 10.33, "u": 71696672, "bu": 7407129},
    },
    "MLM": {
        "3P":        {"bs": 14.24, "u": 36854115, "bu": 5248527},
        "CBT":       {"bs": 15.48, "u": 17621224, "bu": 2728181},
        "3P+CBT":    {"bs": 14.64, "u": 54475339, "bu": 7976708},
        "MELI PRO":  {"bs": 9.99,  "u": 9863558,  "bu": 985793},
        "SELLER DEV":{"bs": 15.79, "u": 26990557, "bu": 4262734},
        "TOTAL":     {"bs": 14.41, "u": 62381898, "bu": 8986333},
    },
    "MLA": {
        "3P":        {"bs": 10.55, "u": 7082854,  "bu": 747248},
        "3P+CBT":    {"bs": 10.55, "u": 7082854,  "bu": 747248},
        "MELI PRO":  {"bs": 8.39,  "u": 2833787,  "bu": 237651},
        "SELLER DEV":{"bs": 11.99, "u": 4249067,  "bu": 509597},
        "TOTAL":     {"bs": 11.68, "u": 8634483,  "bu": 1008728},
    },
    "MLC": {
        "3P":        {"bs": 14.45, "u": 4226302,  "bu": 610646},
        "CBT":       {"bs": 23.13, "u": 276306,   "bu": 63918},
        "3P+CBT":    {"bs": 14.98, "u": 4502608,  "bu": 674564},
        "MELI PRO":  {"bs": 12.76, "u": 1307294,  "bu": 166855},
        "SELLER DEV":{"bs": 15.20, "u": 2919008,  "bu": 443791},
        "TOTAL":     {"bs": 15.24, "u": 5108131,  "bu": 778695},
    },
    "MCO": {
        "3P":        {"bs": 20.12, "u": 819980,   "bu": 164987},
        "3P+CBT":    {"bs": 20.12, "u": 819980,   "bu": 164987},
        "MELI PRO":  {"bs": 16.76, "u": 266062,   "bu": 44597},
        "SELLER DEV":{"bs": 21.73, "u": 553918,   "bu": 120390},
        "TOTAL":     {"bs": 20.37, "u": 893470,   "bu": 182036},
    },
}

prev_bd = {
    "MLB": {
        "3P":        {"str": 1.80, "sv": 1.01, "ag": 2.54, "exc": 4.08},
        "3P+CBT":    {"str": 1.80, "sv": 1.01, "ag": 2.54, "exc": 4.08},
        "MELI PRO":  {"str": 0.90, "sv": 0.71, "ag": 1.58, "exc": 3.87},
        "SELLER DEV":{"str": 2.10, "sv": 1.12, "ag": 2.87, "exc": 4.15},
    },
    "MLM": {
        "3P":        {"str": 1.08, "sv": 1.74, "ag": 4.71, "exc": 6.70},
        "CBT":       {"str": 1.02, "sv": 2.38, "ag": 4.09, "exc": 7.99},
        "3P+CBT":    {"str": 1.06, "sv": 1.95, "ag": 4.51, "exc": 7.11},
        "MELI PRO":  {"str": 0.94, "sv": 1.32, "ag": 3.00, "exc": 4.73},
        "SELLER DEV":{"str": 1.14, "sv": 1.90, "ag": 5.34, "exc": 7.41},
    },
    "MLA": {
        "3P":        {"str": 0.84, "sv": 1.09, "ag": 4.21, "exc": 4.40},
        "3P+CBT":    {"str": 0.84, "sv": 1.09, "ag": 4.21, "exc": 4.40},
        "MELI PRO":  {"str": 0.57, "sv": 0.82, "ag": 2.37, "exc": 4.63},
        "SELLER DEV":{"str": 1.01, "sv": 1.27, "ag": 5.43, "exc": 4.25},
    },
    "MLC": {
        "3P":        {"str": 0.65, "sv": 2.03, "ag": 5.42, "exc": 6.32},
        "CBT":       {"str": 0.66, "sv": 4.69, "ag": 3.14, "exc": 14.64},
        "3P+CBT":    {"str": 0.65, "sv": 2.20, "ag": 5.28, "exc": 6.83},
        "MELI PRO":  {"str": 0.64, "sv": 2.29, "ag": 3.90, "exc": 5.93},
        "SELLER DEV":{"str": 0.66, "sv": 1.92, "ag": 6.10, "exc": 6.50},
    },
    "MCO": {
        "3P":        {"str": 1.17, "sv": 2.31, "ag": 8.96, "exc": 7.63},
        "3P+CBT":    {"str": 1.17, "sv": 2.31, "ag": 8.96, "exc": 7.63},
        "MELI PRO":  {"str": 1.19, "sv": 2.33, "ag": 5.13, "exc": 8.08},
        "SELLER DEV":{"str": 1.16, "sv": 2.30, "ag": 10.80, "exc": 7.41},
    },
}

prev_vert = {
    "MLB": {"BEAUTY":8.80,"CONSTRUCTION & INDUSTRY":10.38,"CPG":7.60,"ENTERTAINMENT":10.28,"FASHION":9.92,"FURNISHING & HOUSEWARE":8.70,"HEALTH":6.57,"HOME ELECTRONICS":9.72,"OTHERS":10.35,"SPORTS":10.22,"T & B":13.88,"TECHNOLOGY":10.37,"VEHICLE PARTS & ACCESSORIES":9.87},
    "MLM": {"BEAUTY":11.24,"CONSTRUCTION & INDUSTRY":12.85,"CPG":9.17,"ENTERTAINMENT":19.36,"FASHION":16.85,"FURNISHING & HOUSEWARE":13.88,"HEALTH":11.20,"HOME ELECTRONICS":11.14,"OTHERS":13.04,"SPORTS":14.56,"T & B":19.85,"TECHNOLOGY":19.00,"VEHICLE PARTS & ACCESSORIES":14.94},
    "MLA": {"BEAUTY":9.08,"CONSTRUCTION & INDUSTRY":10.22,"CPG":11.18,"ENTERTAINMENT":12.44,"FASHION":13.46,"FURNISHING & HOUSEWARE":9.52,"HEALTH":6.96,"HOME ELECTRONICS":9.41,"OTHERS":30.84,"SPORTS":10.86,"T & B":17.14,"TECHNOLOGY":10.04,"VEHICLE PARTS & ACCESSORIES":11.09},
    "MLC": {"BEAUTY":11.95,"CONSTRUCTION & INDUSTRY":15.42,"CPG":10.47,"ENTERTAINMENT":24.57,"FASHION":20.75,"FURNISHING & HOUSEWARE":13.15,"HEALTH":16.30,"HOME ELECTRONICS":10.14,"OTHERS":15.21,"SPORTS":19.06,"T & B":24.60,"TECHNOLOGY":16.20,"VEHICLE PARTS & ACCESSORIES":17.86},
    "MCO": {"BEAUTY":17.61,"CONSTRUCTION & INDUSTRY":19.38,"CPG":19.76,"ENTERTAINMENT":29.87,"FASHION":27.60,"FURNISHING & HOUSEWARE":19.37,"HEALTH":19.84,"HOME ELECTRONICS":12.94,"OTHERS":24.58,"SPORTS":18.48,"T & B":32.43,"TECHNOLOGY":19.82,"VEHICLE PARTS & ACCESSORIES":20.08},
}


# ── Envio ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python scripts/test_chat_message.py <WEBHOOK_URL>")
        sys.exit(1)

    webhook_url = sys.argv[1]

    msg = build_message(
        week_id="W20",
        week_date=date(2026, 5, 16),
        curr_kpi=curr_kpi,
        prev_kpi=prev_kpi,
        curr_bd=curr_bd,
        prev_bd=prev_bd,
        curr_vert=curr_vert,
        prev_vert=prev_vert,
        month=5,
    )

    import io, sys as _sys
    _sys.stdout = io.TextIOWrapper(_sys.stdout.buffer, encoding="utf-8", errors="replace")
    print("--- Previa da mensagem ---")
    print(msg)
    print("-" * 57)
    print()

    send_to_chat(webhook_url, msg)
