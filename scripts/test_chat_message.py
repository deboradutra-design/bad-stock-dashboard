"""
Envio da mensagem W16 ao Google Chat com dados reais do BigQuery.
Execução: python scripts/test_chat_message.py <WEBHOOK_URL>
"""

import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from chat_notifier import build_message, send_to_chat


# ── W16 (19/04/2026) ─────────────────────────────────────────────────────────

curr_kpi = {
    "MLB": {
        "3P":        {"bs": 9.23,  "u": 61400090,  "bu": 5664465},
        "3P+CBT":    {"bs": 9.23,  "u": 61400090,  "bu": 5664465},
        "MELI PRO":  {"bs": 7.53,  "u": 15772999,  "bu": 1187082},
        "SELLER DEV":{"bs": 9.81,  "u": 45627091,  "bu": 4477383},
        "TOTAL":     {"bs": 10.0,  "u": 70498772,  "bu": 7052499},
    },
    "MLM": {
        "3P":        {"bs": 14.84, "u": 36251175,  "bu": 5378580},
        "CBT":       {"bs": 15.91, "u": 17787132,  "bu": 2830234},
        "3P+CBT":    {"bs": 15.19, "u": 54038307,  "bu": 8208814},
        "MELI PRO":  {"bs": 9.49,  "u": 9185247,   "bu": 871487},
        "SELLER DEV":{"bs": 16.65, "u": 27065928,  "bu": 4507093},
        "TOTAL":     {"bs": 15.38, "u": 58980075,  "bu": 9068881},
    },
    "MLA": {
        "3P":        {"bs": 11.14, "u": 5665326,   "bu": 631329},
        "3P+CBT":    {"bs": 11.14, "u": 5665326,   "bu": 631329},
        "MELI PRO":  {"bs": 8.80,  "u": 2015678,   "bu": 177446},
        "SELLER DEV":{"bs": 12.44, "u": 3649648,   "bu": 453883},
        "TOTAL":     {"bs": 12.79, "u": 6493051,   "bu": 830581},
    },
    "MLC": {
        "3P":        {"bs": 13.30, "u": 4301973,   "bu": 571980},
        "CBT":       {"bs": 22.07, "u": 304739,    "bu": 67262},
        "3P+CBT":    {"bs": 13.88, "u": 4606712,   "bu": 639242},
        "MELI PRO":  {"bs": 11.19, "u": 1244919,   "bu": 139273},
        "SELLER DEV":{"bs": 14.15, "u": 3057054,   "bu": 432707},
        "TOTAL":     {"bs": 14.22, "u": 5132170,   "bu": 730021},
    },
    "MCO": {
        "3P":        {"bs": 21.46, "u": 826000,    "bu": 177254},
        "3P+CBT":    {"bs": 21.46, "u": 826000,    "bu": 177254},
        "MELI PRO":  {"bs": 19.49, "u": 257129,    "bu": 50103},
        "SELLER DEV":{"bs": 22.35, "u": 568871,    "bu": 127151},
        "TOTAL":     {"bs": 21.77, "u": 893097,    "bu": 194390},
    },
}

curr_bd = {
    "MLB": {
        "3P":        {"str": 1.54, "sv": 1.06, "ag": 2.52, "exc": 4.11},
        "3P+CBT":    {"str": 1.54, "sv": 1.06, "ag": 2.52, "exc": 4.11},
        "MELI PRO":  {"str": 1.03, "sv": 0.76, "ag": 1.68, "exc": 4.05},
        "SELLER DEV":{"str": 1.71, "sv": 1.16, "ag": 2.81, "exc": 4.13},
    },
    "MLM": {
        "3P":        {"str": 1.05, "sv": 1.88, "ag": 4.84, "exc": 7.07},
        "CBT":       {"str": 1.08, "sv": 2.52, "ag": 4.01, "exc": 8.30},
        "3P+CBT":    {"str": 1.06, "sv": 2.09, "ag": 4.56, "exc": 7.48},
        "MELI PRO":  {"str": 0.62, "sv": 1.42, "ag": 2.95, "exc": 4.49},
        "SELLER DEV":{"str": 1.19, "sv": 2.03, "ag": 5.47, "exc": 7.95},
    },
    "MLA": {
        "3P":        {"str": 0.86, "sv": 1.27, "ag": 4.64, "exc": 4.35},
        "3P+CBT":    {"str": 0.86, "sv": 1.27, "ag": 4.64, "exc": 4.35},
        "MELI PRO":  {"str": 0.65, "sv": 1.00, "ag": 2.86, "exc": 4.28},
        "SELLER DEV":{"str": 0.98, "sv": 1.43, "ag": 5.62, "exc": 4.38},
    },
    "MLC": {
        "3P":        {"str": 0.73, "sv": 1.81, "ag": 4.92, "exc": 5.82},
        "CBT":       {"str": 0.91, "sv": 4.26, "ag": 2.99, "exc": 13.91},
        "3P+CBT":    {"str": 0.74, "sv": 1.97, "ag": 4.79, "exc": 6.36},
        "MELI PRO":  {"str": 0.74, "sv": 1.84, "ag": 3.16, "exc": 5.44},
        "SELLER DEV":{"str": 0.72, "sv": 1.80, "ag": 5.64, "exc": 5.98},
    },
    "MCO": {
        "3P":        {"str": 0.97, "sv": 2.97, "ag": 9.26, "exc": 8.20},
        "3P+CBT":    {"str": 0.97, "sv": 2.97, "ag": 9.26, "exc": 8.20},
        "MELI PRO":  {"str": 0.86, "sv": 3.63, "ag": 5.29, "exc": 9.69},
        "SELLER DEV":{"str": 1.02, "sv": 2.68, "ag": 11.06, "exc": 7.53},
    },
}

curr_vert = {
    "MLB": {"BEAUTY":8.0,"CONSTRUCTION & INDUSTRY":9.78,"CPG":7.15,"ENTERTAINMENT":11.75,"FASHION":10.07,"FURNISHING & HOUSEWARE":8.56,"HEALTH":6.69,"HOME ELECTRONICS":10.22,"OTHERS":11.18,"SPORTS":9.88,"T & B":13.83,"TECHNOLOGY":9.81,"VEHICLE PARTS & ACCESSORIES":9.54},
    "MLM": {"BEAUTY":11.71,"CONSTRUCTION & INDUSTRY":13.66,"CPG":8.67,"ENTERTAINMENT":18.78,"FASHION":15.67,"FURNISHING & HOUSEWARE":15.00,"HEALTH":11.99,"HOME ELECTRONICS":12.05,"OTHERS":14.47,"SPORTS":15.33,"T & B":22.52,"TECHNOLOGY":19.20,"VEHICLE PARTS & ACCESSORIES":16.00},
    "MLA": {"BEAUTY":10.45,"CONSTRUCTION & INDUSTRY":10.26,"CPG":10.38,"ENTERTAINMENT":11.67,"FASHION":14.58,"FURNISHING & HOUSEWARE":10.38,"HEALTH":6.73,"HOME ELECTRONICS":11.61,"OTHERS":31.76,"SPORTS":10.99,"T & B":20.43,"TECHNOLOGY":11.96,"VEHICLE PARTS & ACCESSORIES":12.52},
    "MLC": {"BEAUTY":10.94,"CONSTRUCTION & INDUSTRY":14.25,"CPG":9.27,"ENTERTAINMENT":23.63,"FASHION":18.70,"FURNISHING & HOUSEWARE":13.18,"HEALTH":12.87,"HOME ELECTRONICS":11.39,"OTHERS":15.02,"SPORTS":19.22,"T & B":25.55,"TECHNOLOGY":14.93,"VEHICLE PARTS & ACCESSORIES":16.67},
    "MCO": {"BEAUTY":18.92,"CONSTRUCTION & INDUSTRY":20.71,"CPG":24.18,"ENTERTAINMENT":26.69,"FASHION":24.34,"FURNISHING & HOUSEWARE":20.37,"HEALTH":20.58,"HOME ELECTRONICS":14.16,"OTHERS":23.61,"SPORTS":19.15,"T & B":40.30,"TECHNOLOGY":20.59,"VEHICLE PARTS & ACCESSORIES":20.83},
}


# ── W15 (11/04/2026) ─────────────────────────────────────────────────────────

prev_kpi = {
    "MLB": {
        "3P":        {"bs": 9.24,  "u": 122429040, "bu": 11293545},
        "3P+CBT":    {"bs": 9.24,  "u": 122429040, "bu": 11293545},
        "MELI PRO":  {"bs": 7.63,  "u": 31324727,  "bu": 2394652},
        "SELLER DEV":{"bs": 9.79,  "u": 91104313,  "bu": 8898893},
        "TOTAL":     {"bs": 9.95,  "u": 70538661,  "bu": 7015572},
    },
    "MLM": {
        "3P":        {"bs": 14.98, "u": 72763802,  "bu": 10883305},
        "CBT":       {"bs": 15.91, "u": 35391665,  "bu": 5625926},
        "3P+CBT":    {"bs": 15.28, "u": 108155467, "bu": 16509231},
        "MELI PRO":  {"bs": 9.42,  "u": 18230989,  "bu": 1712692},
        "SELLER DEV":{"bs": 16.84, "u": 54532813,  "bu": 9170613},
        "TOTAL":     {"bs": 15.62, "u": 58719128,  "bu": 9169529},
    },
    "MLA": {
        "3P":        {"bs": 11.48, "u": 11016678,  "bu": 1263955},
        "3P+CBT":    {"bs": 11.48, "u": 11016678,  "bu": 1263955},
        "MELI PRO":  {"bs": 8.89,  "u": 3847576,   "bu": 341356},
        "SELLER DEV":{"bs": 12.87, "u": 7169102,   "bu": 922599},
        "TOTAL":     {"bs": 13.23, "u": 6359624,   "bu": 841606},
    },
    "MLC": {
        "3P":        {"bs": 13.06, "u": 8526749,   "bu": 1111879},
        "CBT":       {"bs": 22.96, "u": 616812,    "bu": 141010},
        "3P+CBT":    {"bs": 13.73, "u": 9143561,   "bu": 1252889},
        "MELI PRO":  {"bs": 10.41, "u": 2427572,   "bu": 251966},
        "SELLER DEV":{"bs": 14.11, "u": 6099177,   "bu": 859913},
        "TOTAL":     {"bs": 14.09, "u": 5056388,   "bu": 712208},
    },
    "MCO": {
        "3P":        {"bs": 22.20, "u": 1627621,   "bu": 360785},
        "3P+CBT":    {"bs": 22.20, "u": 1627621,   "bu": 360785},
        "MELI PRO":  {"bs": 20.91, "u": 502155,    "bu": 104829},
        "SELLER DEV":{"bs": 22.77, "u": 1125466,   "bu": 255956},
        "TOTAL":     {"bs": 22.21, "u": 884183,    "bu": 196414},
    },
}

prev_bd = {
    "MLB": {
        "3P":        {"str": 1.53, "sv": 1.03, "ag": 2.53, "exc": 4.14},
        "3P+CBT":    {"str": 1.53, "sv": 1.03, "ag": 2.53, "exc": 4.14},
        "MELI PRO":  {"str": 0.90, "sv": 0.77, "ag": 1.75, "exc": 4.20},
        "SELLER DEV":{"str": 1.75, "sv": 1.12, "ag": 2.80, "exc": 4.12},
    },
    "MLM": {
        "3P":        {"str": 0.93, "sv": 1.90, "ag": 4.67, "exc": 7.47},
        "CBT":       {"str": 1.13, "sv": 2.49, "ag": 3.75, "exc": 8.55},
        "3P+CBT":    {"str": 1.00, "sv": 2.09, "ag": 4.37, "exc": 7.82},
        "MELI PRO":  {"str": 0.56, "sv": 1.45, "ag": 2.88, "exc": 4.53},
        "SELLER DEV":{"str": 1.06, "sv": 2.05, "ag": 5.27, "exc": 8.45},
    },
    "MLA": {
        "3P":        {"str": 0.81, "sv": 1.26, "ag": 4.80, "exc": 4.61},
        "3P+CBT":    {"str": 0.81, "sv": 1.26, "ag": 4.80, "exc": 4.61},
        "MELI PRO":  {"str": 0.60, "sv": 0.87, "ag": 3.01, "exc": 4.41},
        "SELLER DEV":{"str": 0.92, "sv": 1.46, "ag": 5.76, "exc": 4.71},
    },
    "MLC": {
        "3P":        {"str": 0.65, "sv": 1.77, "ag": 4.73, "exc": 5.90},
        "CBT":       {"str": 1.21, "sv": 4.72, "ag": 2.98, "exc": 14.04},
        "3P+CBT":    {"str": 0.69, "sv": 1.97, "ag": 4.61, "exc": 6.45},
        "MELI PRO":  {"str": 0.76, "sv": 1.61, "ag": 2.92, "exc": 5.11},
        "SELLER DEV":{"str": 0.61, "sv": 1.83, "ag": 5.45, "exc": 6.21},
    },
    "MCO": {
        "3P":        {"str": 1.37, "sv": 2.96, "ag": 9.43, "exc": 8.39},
        "3P+CBT":    {"str": 1.37, "sv": 2.96, "ag": 9.43, "exc": 8.39},
        "MELI PRO":  {"str": 1.79, "sv": 3.44, "ag": 5.21, "exc": 10.44},
        "SELLER DEV":{"str": 1.19, "sv": 2.75, "ag": 11.29, "exc": 7.48},
    },
}

prev_vert = {
    "MLB": {"BEAUTY":8.03,"CONSTRUCTION & INDUSTRY":9.75,"CPG":7.66,"ENTERTAINMENT":12.09,"FASHION":10.19,"FURNISHING & HOUSEWARE":8.54,"HEALTH":6.57,"HOME ELECTRONICS":9.86,"OTHERS":10.94,"SPORTS":9.72,"T & B":13.95,"TECHNOLOGY":9.45,"VEHICLE PARTS & ACCESSORIES":9.83},
    "MLM": {"BEAUTY":11.60,"CONSTRUCTION & INDUSTRY":13.98,"CPG":8.85,"ENTERTAINMENT":19.07,"FASHION":15.59,"FURNISHING & HOUSEWARE":15.17,"HEALTH":12.10,"HOME ELECTRONICS":12.24,"OTHERS":14.61,"SPORTS":15.70,"T & B":23.14,"TECHNOLOGY":19.20,"VEHICLE PARTS & ACCESSORIES":16.30},
    "MLA": {"BEAUTY":10.59,"CONSTRUCTION & INDUSTRY":10.29,"CPG":10.39,"ENTERTAINMENT":11.88,"FASHION":14.69,"FURNISHING & HOUSEWARE":10.73,"HEALTH":6.94,"HOME ELECTRONICS":11.53,"OTHERS":32.74,"SPORTS":11.75,"T & B":21.60,"TECHNOLOGY":12.06,"VEHICLE PARTS & ACCESSORIES":13.80},
    "MLC": {"BEAUTY":11.20,"CONSTRUCTION & INDUSTRY":14.11,"CPG":9.16,"ENTERTAINMENT":21.62,"FASHION":18.02,"FURNISHING & HOUSEWARE":13.73,"HEALTH":13.05,"HOME ELECTRONICS":11.73,"OTHERS":15.22,"SPORTS":19.14,"T & B":25.69,"TECHNOLOGY":15.31,"VEHICLE PARTS & ACCESSORIES":16.62},
    "MCO": {"BEAUTY":18.70,"CONSTRUCTION & INDUSTRY":20.25,"CPG":25.83,"ENTERTAINMENT":28.19,"FASHION":24.58,"FURNISHING & HOUSEWARE":21.14,"HEALTH":21.97,"HOME ELECTRONICS":14.75,"OTHERS":22.11,"SPORTS":19.67,"T & B":39.97,"TECHNOLOGY":21.10,"VEHICLE PARTS & ACCESSORIES":21.45},
}


# ── Envio ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python scripts/test_chat_message.py <WEBHOOK_URL>")
        sys.exit(1)

    webhook_url = sys.argv[1]

    msg = build_message(
        week_id="W16",
        week_date=date(2026, 4, 19),
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
