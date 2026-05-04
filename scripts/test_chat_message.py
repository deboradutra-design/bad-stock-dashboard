"""
Envio da mensagem W18 ao Google Chat com dados reais do BigQuery.
Execução: python scripts/test_chat_message.py <WEBHOOK_URL>
"""

import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from chat_notifier import build_message, send_to_chat


# ── W18 (02/05/2026) ─────────────────────────────────────────────────────────

curr_kpi = {
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

curr_bd = {
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

curr_vert = {
    "MLB": {"BEAUTY":8.57,"CONSTRUCTION & INDUSTRY":10.58,"CPG":7.12,"ENTERTAINMENT":10.84,"FASHION":9.99,"FURNISHING & HOUSEWARE":8.87,"HEALTH":6.61,"HOME ELECTRONICS":9.84,"OTHERS":10.53,"SPORTS":10.25,"T & B":14.23,"TECHNOLOGY":9.79,"VEHICLE PARTS & ACCESSORIES":10.03},
    "MLM": {"BEAUTY":11.61,"CONSTRUCTION & INDUSTRY":13.02,"CPG":8.69,"ENTERTAINMENT":19.69,"FASHION":16.50,"FURNISHING & HOUSEWARE":14.23,"HEALTH":11.77,"HOME ELECTRONICS":11.79,"OTHERS":13.29,"SPORTS":14.90,"T & B":20.98,"TECHNOLOGY":19.20,"VEHICLE PARTS & ACCESSORIES":15.39},
    "MLA": {"BEAUTY":9.99,"CONSTRUCTION & INDUSTRY":10.21,"CPG":10.44,"ENTERTAINMENT":14.85,"FASHION":14.16,"FURNISHING & HOUSEWARE":10.13,"HEALTH":6.36,"HOME ELECTRONICS":10.04,"OTHERS":31.73,"SPORTS":11.08,"T & B":17.98,"TECHNOLOGY":11.03,"VEHICLE PARTS & ACCESSORIES":12.27},
    "MLC": {"BEAUTY":12.19,"CONSTRUCTION & INDUSTRY":14.73,"CPG":10.26,"ENTERTAINMENT":26.38,"FASHION":19.62,"FURNISHING & HOUSEWARE":12.88,"HEALTH":16.34,"HOME ELECTRONICS":10.58,"OTHERS":16.42,"SPORTS":18.75,"T & B":24.43,"TECHNOLOGY":15.11,"VEHICLE PARTS & ACCESSORIES":16.80},
    "MCO": {"BEAUTY":17.31,"CONSTRUCTION & INDUSTRY":19.21,"CPG":22.53,"ENTERTAINMENT":30.67,"FASHION":26.71,"FURNISHING & HOUSEWARE":19.47,"HEALTH":19.61,"HOME ELECTRONICS":13.53,"OTHERS":19.13,"SPORTS":18.23,"T & B":29.56,"TECHNOLOGY":19.25,"VEHICLE PARTS & ACCESSORIES":19.13},
}


# ── W17 (25/04/2026) ─────────────────────────────────────────────────────────

prev_kpi = {
    "MLB": {
        "3P":        {"bs": 9.07,  "u": 62751200, "bu": 5689451},
        "3P+CBT":    {"bs": 9.07,  "u": 62751200, "bu": 5689451},
        "MELI PRO":  {"bs": 7.20,  "u": 16377012, "bu": 1179194},
        "SELLER DEV":{"bs": 9.73,  "u": 46374188, "bu": 4510257},
        "TOTAL":     {"bs": 9.96,  "u": 72207911, "bu": 7189011},
    },
    "MLM": {
        "3P":        {"bs": 14.36, "u": 36205275, "bu": 5198094},
        "CBT":       {"bs": 15.88, "u": 17733222, "bu": 2815334},
        "3P+CBT":    {"bs": 14.86, "u": 53938497, "bu": 8013428},
        "MELI PRO":  {"bs": 9.36,  "u": 9414106,  "bu": 881377},
        "SELLER DEV":{"bs": 16.11, "u": 26791169, "bu": 4316717},
        "TOTAL":     {"bs": 14.99, "u": 59380614, "bu": 8903740},
    },
    "MLA": {
        "3P":        {"bs": 10.17, "u": 6329147,  "bu": 643660},
        "3P+CBT":    {"bs": 10.17, "u": 6329147,  "bu": 643660},
        "MELI PRO":  {"bs": 7.93,  "u": 2328105,  "bu": 184661},
        "SELLER DEV":{"bs": 11.47, "u": 4001042,  "bu": 458999},
        "TOTAL":     {"bs": 11.47, "u": 7490464,  "bu": 859234},
    },
    "MLC": {
        "3P":        {"bs": 12.95, "u": 4482657,  "bu": 580503},
        "CBT":       {"bs": 22.61, "u": 296305,   "bu": 66981},
        "3P+CBT":    {"bs": 13.55, "u": 4778962,  "bu": 647484},
        "MELI PRO":  {"bs": 11.71, "u": 1297133,  "bu": 151927},
        "SELLER DEV":{"bs": 13.45, "u": 3185524,  "bu": 428576},
        "TOTAL":     {"bs": 13.95, "u": 5350939,  "bu": 746463},
    },
    "MCO": {
        "3P":        {"bs": 20.27, "u": 847373,   "bu": 171773},
        "3P+CBT":    {"bs": 20.27, "u": 847373,   "bu": 171773},
        "MELI PRO":  {"bs": 17.20, "u": 270898,   "bu": 46595},
        "SELLER DEV":{"bs": 21.71, "u": 576475,   "bu": 125178},
        "TOTAL":     {"bs": 20.55, "u": 916238,   "bu": 188276},
    },
}

prev_bd = {
    "MLB": {
        "3P":        {"str": 1.67, "sv": 1.03, "ag": 2.50, "exc": 3.86},
        "3P+CBT":    {"str": 1.67, "sv": 1.03, "ag": 2.50, "exc": 3.86},
        "MELI PRO":  {"str": 0.95, "sv": 0.76, "ag": 1.65, "exc": 3.83},
        "SELLER DEV":{"str": 1.93, "sv": 1.12, "ag": 2.79, "exc": 3.87},
    },
    "MLM": {
        "3P":        {"str": 0.95, "sv": 1.80, "ag": 4.84, "exc": 6.76},
        "CBT":       {"str": 1.04, "sv": 2.46, "ag": 4.11, "exc": 8.26},
        "3P+CBT":    {"str": 0.98, "sv": 2.02, "ag": 4.60, "exc": 7.25},
        "MELI PRO":  {"str": 0.64, "sv": 1.33, "ag": 3.01, "exc": 4.38},
        "SELLER DEV":{"str": 1.06, "sv": 1.97, "ag": 5.49, "exc": 7.59},
    },
    "MLA": {
        "3P":        {"str": 0.91, "sv": 1.11, "ag": 4.22, "exc": 3.92},
        "3P+CBT":    {"str": 0.91, "sv": 1.11, "ag": 4.22, "exc": 3.92},
        "MELI PRO":  {"str": 0.66, "sv": 0.87, "ag": 2.53, "exc": 3.86},
        "SELLER DEV":{"str": 1.05, "sv": 1.25, "ag": 5.20, "exc": 3.95},
    },
    "MLC": {
        "3P":        {"str": 0.57, "sv": 1.79, "ag": 4.86, "exc": 5.70},
        "CBT":       {"str": 0.77, "sv": 4.65, "ag": 3.18, "exc": 14.01},
        "3P+CBT":    {"str": 0.59, "sv": 1.97, "ag": 4.76, "exc": 6.22},
        "MELI PRO":  {"str": 0.56, "sv": 1.94, "ag": 3.52, "exc": 5.68},
        "SELLER DEV":{"str": 0.58, "sv": 1.73, "ag": 5.41, "exc": 5.72},
    },
    "MCO": {
        "3P":        {"str": 1.02, "sv": 2.58, "ag": 9.08, "exc": 7.55},
        "3P+CBT":    {"str": 1.02, "sv": 2.58, "ag": 9.08, "exc": 7.55},
        "MELI PRO":  {"str": 0.89, "sv": 2.87, "ag": 5.11, "exc": 8.32},
        "SELLER DEV":{"str": 1.07, "sv": 2.45, "ag": 10.95, "exc": 7.19},
    },
}

prev_vert = {
    "MLB": {"BEAUTY":7.98,"CONSTRUCTION & INDUSTRY":9.77,"CPG":6.74,"ENTERTAINMENT":10.42,"FASHION":10.14,"FURNISHING & HOUSEWARE":8.58,"HEALTH":6.73,"HOME ELECTRONICS":9.71,"OTHERS":10.93,"SPORTS":9.35,"T & B":13.66,"TECHNOLOGY":9.50,"VEHICLE PARTS & ACCESSORIES":9.33},
    "MLM": {"BEAUTY":10.98,"CONSTRUCTION & INDUSTRY":13.22,"CPG":8.42,"ENTERTAINMENT":18.92,"FASHION":15.95,"FURNISHING & HOUSEWARE":14.43,"HEALTH":11.67,"HOME ELECTRONICS":11.91,"OTHERS":13.88,"SPORTS":14.96,"T & B":21.63,"TECHNOLOGY":19.23,"VEHICLE PARTS & ACCESSORIES":15.64},
    "MLA": {"BEAUTY":9.72,"CONSTRUCTION & INDUSTRY":9.54,"CPG":9.05,"ENTERTAINMENT":10.25,"FASHION":13.64,"FURNISHING & HOUSEWARE":9.50,"HEALTH":5.78,"HOME ELECTRONICS":10.96,"OTHERS":31.57,"SPORTS":10.72,"T & B":18.38,"TECHNOLOGY":10.65,"VEHICLE PARTS & ACCESSORIES":12.78},
    "MLC": {"BEAUTY":11.48,"CONSTRUCTION & INDUSTRY":13.95,"CPG":9.28,"ENTERTAINMENT":23.06,"FASHION":18.75,"FURNISHING & HOUSEWARE":12.22,"HEALTH":12.76,"HOME ELECTRONICS":10.15,"OTHERS":16.30,"SPORTS":19.11,"T & B":23.66,"TECHNOLOGY":14.30,"VEHICLE PARTS & ACCESSORIES":16.34},
    "MCO": {"BEAUTY":17.14,"CONSTRUCTION & INDUSTRY":19.58,"CPG":23.25,"ENTERTAINMENT":28.36,"FASHION":24.57,"FURNISHING & HOUSEWARE":19.18,"HEALTH":19.60,"HOME ELECTRONICS":12.55,"OTHERS":18.30,"SPORTS":19.28,"T & B":34.41,"TECHNOLOGY":19.35,"VEHICLE PARTS & ACCESSORIES":21.18},
}


# ── Envio ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python scripts/test_chat_message.py <WEBHOOK_URL>")
        sys.exit(1)

    webhook_url = sys.argv[1]

    msg = build_message(
        week_id="W18",
        week_date=date(2026, 5, 2),
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
