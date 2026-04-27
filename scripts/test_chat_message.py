"""
Envio da mensagem W17 ao Google Chat com dados reais do BigQuery.
Execução: python scripts/test_chat_message.py <WEBHOOK_URL>
"""

import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from chat_notifier import build_message, send_to_chat


# ── W17 (25/04/2026) ─────────────────────────────────────────────────────────

curr_kpi = {
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

curr_bd = {
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

curr_vert = {
    "MLB": {"BEAUTY":7.98,"CONSTRUCTION & INDUSTRY":9.77,"CPG":6.74,"ENTERTAINMENT":10.42,"FASHION":10.14,"FURNISHING & HOUSEWARE":8.58,"HEALTH":6.73,"HOME ELECTRONICS":9.71,"OTHERS":10.93,"SPORTS":9.35,"T & B":13.66,"TECHNOLOGY":9.50,"VEHICLE PARTS & ACCESSORIES":9.33},
    "MLM": {"BEAUTY":10.98,"CONSTRUCTION & INDUSTRY":13.22,"CPG":8.42,"ENTERTAINMENT":18.92,"FASHION":15.95,"FURNISHING & HOUSEWARE":14.43,"HEALTH":11.67,"HOME ELECTRONICS":11.91,"OTHERS":13.88,"SPORTS":14.96,"T & B":21.63,"TECHNOLOGY":19.23,"VEHICLE PARTS & ACCESSORIES":15.64},
    "MLA": {"BEAUTY":9.72,"CONSTRUCTION & INDUSTRY":9.54,"CPG":9.05,"ENTERTAINMENT":10.25,"FASHION":13.64,"FURNISHING & HOUSEWARE":9.50,"HEALTH":5.78,"HOME ELECTRONICS":10.96,"OTHERS":31.57,"SPORTS":10.72,"T & B":18.38,"TECHNOLOGY":10.65,"VEHICLE PARTS & ACCESSORIES":12.78},
    "MLC": {"BEAUTY":11.48,"CONSTRUCTION & INDUSTRY":13.95,"CPG":9.28,"ENTERTAINMENT":23.06,"FASHION":18.75,"FURNISHING & HOUSEWARE":12.22,"HEALTH":12.76,"HOME ELECTRONICS":10.15,"OTHERS":16.30,"SPORTS":19.11,"T & B":23.66,"TECHNOLOGY":14.30,"VEHICLE PARTS & ACCESSORIES":16.34},
    "MCO": {"BEAUTY":17.14,"CONSTRUCTION & INDUSTRY":19.58,"CPG":23.25,"ENTERTAINMENT":28.36,"FASHION":24.57,"FURNISHING & HOUSEWARE":19.18,"HEALTH":19.60,"HOME ELECTRONICS":12.55,"OTHERS":18.30,"SPORTS":19.28,"T & B":34.41,"TECHNOLOGY":19.35,"VEHICLE PARTS & ACCESSORIES":21.18},
}


# ── W16 (18/04/2026) ─────────────────────────────────────────────────────────

prev_kpi = {
    "MLB": {
        "3P":        {"bs": 9.00,  "u": 62641019, "bu": 5638213},
        "3P+CBT":    {"bs": 9.00,  "u": 62641019, "bu": 5638213},
        "MELI PRO":  {"bs": 7.30,  "u": 16055636, "bu": 1172381},
        "SELLER DEV":{"bs": 9.59,  "u": 46585383, "bu": 4465832},
        "TOTAL":     {"bs": 9.81,  "u": 71896177, "bu": 7053034},
    },
    "MLM": {
        "3P":        {"bs": 14.71, "u": 36430079, "bu": 5359613},
        "CBT":       {"bs": 15.96, "u": 17761065, "bu": 2834900},
        "3P+CBT":    {"bs": 15.12, "u": 54191144, "bu": 8194513},
        "MELI PRO":  {"bs": 9.29,  "u": 9243005,  "bu": 858720},
        "SELLER DEV":{"bs": 16.56, "u": 27187074, "bu": 4500893},
        "TOTAL":     {"bs": 15.32, "u": 59100983, "bu": 9054468},
    },
    "MLA": {
        "3P":        {"bs": 10.86, "u": 5824017,  "bu": 632774},
        "3P+CBT":    {"bs": 10.86, "u": 5824017,  "bu": 632774},
        "MELI PRO":  {"bs": 8.51,  "u": 2066759,  "bu": 175895},
        "SELLER DEV":{"bs": 12.16, "u": 3757258,  "bu": 456879},
        "TOTAL":     {"bs": 12.48, "u": 6666097,  "bu": 832253},
    },
    "MLC": {
        "3P":        {"bs": 13.11, "u": 4325743,  "bu": 567255},
        "CBT":       {"bs": 22.98, "u": 300192,   "bu": 68986},
        "3P+CBT":    {"bs": 13.75, "u": 4625935,  "bu": 636241},
        "MELI PRO":  {"bs": 11.03, "u": 1250439,  "bu": 137887},
        "SELLER DEV":{"bs": 13.96, "u": 3075304,  "bu": 429368},
        "TOTAL":     {"bs": 14.10, "u": 5154944,  "bu": 726774},
    },
    "MCO": {
        "3P":        {"bs": 21.64, "u": 814453,   "bu": 176250},
        "3P+CBT":    {"bs": 21.64, "u": 814453,   "bu": 176250},
        "MELI PRO":  {"bs": 19.52, "u": 256711,   "bu": 50105},
        "SELLER DEV":{"bs": 22.62, "u": 557742,   "bu": 126145},
        "TOTAL":     {"bs": 21.91, "u": 882671,   "bu": 193421},
    },
}

prev_bd = {
    "MLB": {
        "3P":        {"str": 1.53, "sv": 1.03, "ag": 2.46, "exc": 3.98},
        "3P+CBT":    {"str": 1.53, "sv": 1.03, "ag": 2.46, "exc": 3.98},
        "MELI PRO":  {"str": 0.99, "sv": 0.74, "ag": 1.64, "exc": 3.92},
        "SELLER DEV":{"str": 1.71, "sv": 1.12, "ag": 2.74, "exc": 4.00},
    },
    "MLM": {
        "3P":        {"str": 0.97, "sv": 1.86, "ag": 4.72, "exc": 7.15},
        "CBT":       {"str": 1.12, "sv": 2.47, "ag": 3.87, "exc": 8.50},
        "3P+CBT":    {"str": 1.02, "sv": 2.06, "ag": 4.44, "exc": 7.59},
        "MELI PRO":  {"str": 0.58, "sv": 1.40, "ag": 2.88, "exc": 4.42},
        "SELLER DEV":{"str": 1.11, "sv": 2.02, "ag": 5.34, "exc": 8.08},
    },
    "MLA": {
        "3P":        {"str": 0.91, "sv": 1.24, "ag": 4.45, "exc": 4.26},
        "3P+CBT":    {"str": 0.91, "sv": 1.24, "ag": 4.45, "exc": 4.26},
        "MELI PRO":  {"str": 0.58, "sv": 0.98, "ag": 2.73, "exc": 4.21},
        "SELLER DEV":{"str": 0.68, "sv": 1.38, "ag": 5.39, "exc": 4.29},
    },
    "MLC": {
        "3P":        {"str": 0.68, "sv": 1.77, "ag": 4.85, "exc": 5.80},
        "CBT":       {"str": 1.09, "sv": 4.70, "ag": 2.89, "exc": 14.29},
        "3P+CBT":    {"str": 0.71, "sv": 1.96, "ag": 4.72, "exc": 6.35},
        "MELI PRO":  {"str": 0.69, "sv": 1.81, "ag": 3.18, "exc": 5.35},
        "SELLER DEV":{"str": 0.68, "sv": 1.76, "ag": 5.53, "exc": 5.98},
    },
    "MCO": {
        "3P":        {"str": 1.07, "sv": 2.97, "ag": 9.40, "exc": 8.16},
        "3P+CBT":    {"str": 1.07, "sv": 2.97, "ag": 9.40, "exc": 8.16},
        "MELI PRO":  {"str": 1.02, "sv": 3.59, "ag": 5.40, "exc": 9.48},
        "SELLER DEV":{"str": 1.09, "sv": 2.68, "ag": 11.24, "exc": 7.55},
    },
}

prev_vert = {
    "MLB": {"BEAUTY":8.0,"CONSTRUCTION & INDUSTRY":9.78,"CPG":7.15,"ENTERTAINMENT":11.75,"FASHION":10.07,"FURNISHING & HOUSEWARE":8.56,"HEALTH":6.69,"HOME ELECTRONICS":10.22,"OTHERS":11.18,"SPORTS":9.88,"T & B":13.83,"TECHNOLOGY":9.81,"VEHICLE PARTS & ACCESSORIES":9.54},
    "MLM": {"BEAUTY":11.71,"CONSTRUCTION & INDUSTRY":13.66,"CPG":8.67,"ENTERTAINMENT":18.78,"FASHION":15.67,"FURNISHING & HOUSEWARE":15.00,"HEALTH":11.99,"HOME ELECTRONICS":12.05,"OTHERS":14.47,"SPORTS":15.33,"T & B":22.52,"TECHNOLOGY":19.20,"VEHICLE PARTS & ACCESSORIES":16.00},
    "MLA": {"BEAUTY":10.45,"CONSTRUCTION & INDUSTRY":10.26,"CPG":10.38,"ENTERTAINMENT":11.67,"FASHION":14.58,"FURNISHING & HOUSEWARE":10.38,"HEALTH":6.73,"HOME ELECTRONICS":11.61,"OTHERS":31.76,"SPORTS":10.99,"T & B":20.43,"TECHNOLOGY":11.96,"VEHICLE PARTS & ACCESSORIES":12.52},
    "MLC": {"BEAUTY":10.94,"CONSTRUCTION & INDUSTRY":14.25,"CPG":9.27,"ENTERTAINMENT":23.63,"FASHION":18.70,"FURNISHING & HOUSEWARE":13.18,"HEALTH":12.87,"HOME ELECTRONICS":11.39,"OTHERS":15.02,"SPORTS":19.22,"T & B":25.55,"TECHNOLOGY":14.93,"VEHICLE PARTS & ACCESSORIES":16.67},
    "MCO": {"BEAUTY":18.92,"CONSTRUCTION & INDUSTRY":20.71,"CPG":24.18,"ENTERTAINMENT":26.69,"FASHION":24.34,"FURNISHING & HOUSEWARE":20.37,"HEALTH":20.58,"HOME ELECTRONICS":14.16,"OTHERS":23.61,"SPORTS":19.15,"T & B":40.30,"TECHNOLOGY":20.59,"VEHICLE PARTS & ACCESSORIES":20.83},
}


# ── Envio ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python scripts/test_chat_message.py <WEBHOOK_URL>")
        sys.exit(1)

    webhook_url = sys.argv[1]

    msg = build_message(
        week_id="W17",
        week_date=date(2026, 4, 25),
        curr_kpi=curr_kpi,
        prev_kpi=prev_kpi,
        curr_bd=curr_bd,
        prev_bd=prev_bd,
        curr_vert=curr_vert,
        prev_vert=prev_vert,
        month=4,
    )

    print("─── Prévia da mensagem ───────────────────────────────────")
    print(msg)
    print("─────────────────────────────────────────────────────────")
    print()

    send_to_chat(webhook_url, msg)
