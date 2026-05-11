"""
Envio da mensagem W19 ao Google Chat com dados reais do BigQuery.
Execução: python scripts/test_chat_message.py <WEBHOOK_URL>
"""

import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from chat_notifier import build_message, send_to_chat


# ── W19 (09/05/2026) ─────────────────────────────────────────────────────────

curr_kpi = {
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

curr_bd = {
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

curr_vert = {
    "MLB": {"BEAUTY":8.80,"CONSTRUCTION & INDUSTRY":10.38,"CPG":7.60,"ENTERTAINMENT":10.28,"FASHION":9.92,"FURNISHING & HOUSEWARE":8.70,"HEALTH":6.57,"HOME ELECTRONICS":9.72,"OTHERS":10.35,"SPORTS":10.22,"T & B":13.88,"TECHNOLOGY":10.37,"VEHICLE PARTS & ACCESSORIES":9.87},
    "MLM": {"BEAUTY":11.24,"CONSTRUCTION & INDUSTRY":12.85,"CPG":9.17,"ENTERTAINMENT":19.36,"FASHION":16.85,"FURNISHING & HOUSEWARE":13.88,"HEALTH":11.20,"HOME ELECTRONICS":11.14,"OTHERS":13.04,"SPORTS":14.56,"T & B":19.85,"TECHNOLOGY":19.00,"VEHICLE PARTS & ACCESSORIES":14.94},
    "MLA": {"BEAUTY":9.08,"CONSTRUCTION & INDUSTRY":10.22,"CPG":11.18,"ENTERTAINMENT":12.44,"FASHION":13.46,"FURNISHING & HOUSEWARE":9.52,"HEALTH":6.96,"HOME ELECTRONICS":9.41,"OTHERS":30.84,"SPORTS":10.86,"T & B":17.14,"TECHNOLOGY":10.04,"VEHICLE PARTS & ACCESSORIES":11.09},
    "MLC": {"BEAUTY":11.95,"CONSTRUCTION & INDUSTRY":15.42,"CPG":10.47,"ENTERTAINMENT":24.57,"FASHION":20.75,"FURNISHING & HOUSEWARE":13.15,"HEALTH":16.30,"HOME ELECTRONICS":10.14,"OTHERS":15.21,"SPORTS":19.06,"T & B":24.60,"TECHNOLOGY":16.20,"VEHICLE PARTS & ACCESSORIES":17.86},
    "MCO": {"BEAUTY":17.61,"CONSTRUCTION & INDUSTRY":19.38,"CPG":19.76,"ENTERTAINMENT":29.87,"FASHION":27.60,"FURNISHING & HOUSEWARE":19.37,"HEALTH":19.84,"HOME ELECTRONICS":12.94,"OTHERS":24.58,"SPORTS":18.48,"T & B":32.43,"TECHNOLOGY":19.82,"VEHICLE PARTS & ACCESSORIES":20.08},
}


# ── W18 (02/05/2026) ─────────────────────────────────────────────────────────

prev_kpi = {
    "MLB": {
        "3P":        {"bs": 9.42,  "u": 62668807, "bu": 5900697},
        "3P+CBT":    {"bs": 9.42,  "u": 62668807, "bu": 5900697},
        "MELI PRO":  {"bs": 6.92,  "u": 16461890, "bu": 1138901},
        "SELLER DEV":{"bs": 10.31, "u": 46206917, "bu": 4761796},
        "TOTAL":     {"bs": 10.36, "u": 72380824, "bu": 7496359},
    },
    "MLM": {
        "3P":        {"bs": 14.41, "u": 36198390, "bu": 5217463},
        "CBT":       {"bs": 15.83, "u": 17586081, "bu": 2783436},
        "3P+CBT":    {"bs": 14.88, "u": 53784471, "bu": 8000899},
        "MELI PRO":  {"bs": 9.66,  "u": 8966887,  "bu": 865878},
        "SELLER DEV":{"bs": 15.98, "u": 27231503, "bu": 4351585},
        "TOTAL":     {"bs": 14.57, "u": 61070118, "bu": 8896410},
    },
    "MLA": {
        "3P":        {"bs": 10.81, "u": 6457891,  "bu": 698160},
        "3P+CBT":    {"bs": 10.81, "u": 6457891,  "bu": 698160},
        "MELI PRO":  {"bs": 9.18,  "u": 2273694,  "bu": 208677},
        "SELLER DEV":{"bs": 11.70, "u": 4184197,  "bu": 489483},
        "TOTAL":     {"bs": 11.86, "u": 7919036,  "bu": 938979},
    },
    "MLC": {
        "3P":        {"bs": 14.05, "u": 4244226,  "bu": 596388},
        "CBT":       {"bs": 22.43, "u": 297624,   "bu": 66743},
        "3P+CBT":    {"bs": 14.60, "u": 4541850,  "bu": 663131},
        "MELI PRO":  {"bs": 13.05, "u": 1178544,  "bu": 153767},
        "SELLER DEV":{"bs": 14.44, "u": 3065682,  "bu": 442621},
        "TOTAL":     {"bs": 15.08, "u": 5104045,  "bu": 769934},
    },
    "MCO": {
        "3P":        {"bs": 20.08, "u": 862062,   "bu": 173130},
        "3P+CBT":    {"bs": 20.08, "u": 862062,   "bu": 173130},
        "MELI PRO":  {"bs": 17.09, "u": 279927,   "bu": 47851},
        "SELLER DEV":{"bs": 21.52, "u": 582135,   "bu": 125279},
        "TOTAL":     {"bs": 20.35, "u": 937604,   "bu": 190757},
    },
}

prev_bd = {
    "MLB": {
        "3P":        {"str": 1.74, "sv": 1.03, "ag": 2.59, "exc": 4.05},
        "3P+CBT":    {"str": 1.74, "sv": 1.03, "ag": 2.59, "exc": 4.05},
        "MELI PRO":  {"str": 0.81, "sv": 0.76, "ag": 1.64, "exc": 3.71},
        "SELLER DEV":{"str": 2.07, "sv": 1.13, "ag": 2.93, "exc": 4.17},
    },
    "MLM": {
        "3P":        {"str": 1.04, "sv": 1.81, "ag": 4.87, "exc": 6.69},
        "CBT":       {"str": 1.10, "sv": 2.42, "ag": 4.25, "exc": 8.05},
        "3P+CBT":    {"str": 1.06, "sv": 2.01, "ag": 4.66, "exc": 7.13},
        "MELI PRO":  {"str": 0.61, "sv": 1.38, "ag": 3.21, "exc": 4.45},
        "SELLER DEV":{"str": 1.18, "sv": 1.96, "ag": 5.41, "exc": 7.42},
    },
    "MLA": {
        "3P":        {"str": 0.79, "sv": 1.24, "ag": 4.44, "exc": 4.33},
        "3P+CBT":    {"str": 0.79, "sv": 1.24, "ag": 4.44, "exc": 4.33},
        "MELI PRO":  {"str": 0.61, "sv": 1.00, "ag": 2.81, "exc": 4.75},
        "SELLER DEV":{"str": 0.89, "sv": 1.37, "ag": 5.33, "exc": 4.10},
    },
    "MLC": {
        "3P":        {"str": 0.67, "sv": 2.03, "ag": 5.20, "exc": 6.13},
        "CBT":       {"str": 1.39, "sv": 4.46, "ag": 3.38, "exc": 13.20},
        "3P+CBT":    {"str": 0.72, "sv": 2.19, "ag": 5.08, "exc": 6.59},
        "MELI PRO":  {"str": 0.68, "sv": 2.32, "ag": 3.78, "exc": 6.25},
        "SELLER DEV":{"str": 0.67, "sv": 1.92, "ag": 5.74, "exc": 6.08},
    },
    "MCO": {
        "3P":        {"str": 0.99, "sv": 2.55, "ag": 8.92, "exc": 7.58},
        "3P+CBT":    {"str": 0.99, "sv": 2.55, "ag": 8.92, "exc": 7.58},
        "MELI PRO":  {"str": 0.86, "sv": 2.77, "ag": 4.97, "exc": 8.48},
        "SELLER DEV":{"str": 1.05, "sv": 2.44, "ag": 10.82, "exc": 7.15},
    },
}

prev_vert = {
    "MLB": {"BEAUTY":8.57,"CONSTRUCTION & INDUSTRY":10.58,"CPG":7.12,"ENTERTAINMENT":10.84,"FASHION":9.99,"FURNISHING & HOUSEWARE":8.87,"HEALTH":6.61,"HOME ELECTRONICS":9.84,"OTHERS":10.53,"SPORTS":10.25,"T & B":14.23,"TECHNOLOGY":9.79,"VEHICLE PARTS & ACCESSORIES":10.03},
    "MLM": {"BEAUTY":11.61,"CONSTRUCTION & INDUSTRY":13.02,"CPG":8.69,"ENTERTAINMENT":19.69,"FASHION":16.50,"FURNISHING & HOUSEWARE":14.23,"HEALTH":11.77,"HOME ELECTRONICS":11.79,"OTHERS":13.29,"SPORTS":14.90,"T & B":20.98,"TECHNOLOGY":19.20,"VEHICLE PARTS & ACCESSORIES":15.39},
    "MLA": {"BEAUTY":9.99,"CONSTRUCTION & INDUSTRY":10.21,"CPG":10.44,"ENTERTAINMENT":14.85,"FASHION":14.16,"FURNISHING & HOUSEWARE":10.13,"HEALTH":6.36,"HOME ELECTRONICS":10.04,"OTHERS":31.73,"SPORTS":11.08,"T & B":17.98,"TECHNOLOGY":11.03,"VEHICLE PARTS & ACCESSORIES":12.27},
    "MLC": {"BEAUTY":12.19,"CONSTRUCTION & INDUSTRY":14.73,"CPG":10.26,"ENTERTAINMENT":26.38,"FASHION":19.62,"FURNISHING & HOUSEWARE":12.88,"HEALTH":16.34,"HOME ELECTRONICS":10.58,"OTHERS":16.42,"SPORTS":18.75,"T & B":24.43,"TECHNOLOGY":15.11,"VEHICLE PARTS & ACCESSORIES":16.80},
    "MCO": {"BEAUTY":17.31,"CONSTRUCTION & INDUSTRY":19.21,"CPG":22.53,"ENTERTAINMENT":30.67,"FASHION":26.71,"FURNISHING & HOUSEWARE":19.47,"HEALTH":19.61,"HOME ELECTRONICS":13.53,"OTHERS":19.13,"SPORTS":18.23,"T & B":29.56,"TECHNOLOGY":19.25,"VEHICLE PARTS & ACCESSORIES":19.13},
}


# ── Envio ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python scripts/test_chat_message.py <WEBHOOK_URL>")
        sys.exit(1)

    webhook_url = sys.argv[1]

    msg = build_message(
        week_id="W19",
        week_date=date(2026, 5, 9),
        curr_kpi=curr_kpi,
        prev_kpi=prev_kpi,
        curr_bd=curr_bd,
        prev_bd=prev_bd,
        curr_vert=curr_vert,
        prev_vert=prev_vert,
        month=5,
    )

    print("─── Prévia da mensagem ───────────────────────────────────")
    print(msg)
    print("─────────────────────────────────────────────────────────")
    print()

    send_to_chat(webhook_url, msg)
