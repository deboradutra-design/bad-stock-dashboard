"""
Envio da mensagem W29 ao Google Chat com dados reais do BigQuery.
Execução: python scripts/test_chat_message.py <WEBHOOK_URL>
"""

import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from chat_notifier import build_message, send_to_chat


# ── W29 (18/07/2026) ─────────────────────────────────────────────────────────

curr_kpi = {
    "MLB": {
        "3P":        {"bs": 10.33, "u": 66916319, "bu": 6914226},
        "3P+CBT":    {"bs": 10.33, "u": 66916319, "bu": 6914226},
        "MELI PRO":  {"bs": 7.46,  "u": 16815034, "bu": 1254930},
        "SELLER DEV":{"bs": 11.30, "u": 50101285, "bu": 5659296},
        "TOTAL":     {"bs": 10.59, "u": 78911530, "bu": 8355027},
    },
    "MLM": {
        "3P":        {"bs": 13.37, "u": 37253875, "bu": 4982009},
        "CBT":       {"bs": 13.92, "u": 19877245, "bu": 2766730},
        "3P+CBT":    {"bs": 13.56, "u": 57131120, "bu": 7748739},
        "MELI PRO":  {"bs": 10.57, "u": 9247058,  "bu": 977584},
        "SELLER DEV":{"bs": 14.30, "u": 28006817, "bu": 4004425},
        "TOTAL":     {"bs": 14.48, "u": 63740088, "bu": 9232243},
    },
    "MLA": {
        "3P":        {"bs": 13.12, "u": 6116770,  "bu": 802234},
        "3P+CBT":    {"bs": 13.12, "u": 6116770,  "bu": 802234},
        "MELI PRO":  {"bs": 11.49, "u": 2020544,  "bu": 232255},
        "SELLER DEV":{"bs": 13.91, "u": 4096226,  "bu": 569979},
        "TOTAL":     {"bs": 15.86, "u": 7085509,  "bu": 1124027},
    },
    "MLC": {
        "3P":        {"bs": 14.49, "u": 4866782,  "bu": 705034},
        "CBT":       {"bs": 21.29, "u": 308385,   "bu": 65658},
        "3P+CBT":    {"bs": 14.89, "u": 5175167,  "bu": 770692},
        "MELI PRO":  {"bs": 16.55, "u": 1367838,  "bu": 226376},
        "SELLER DEV":{"bs": 13.68, "u": 3498944,  "bu": 478658},
        "TOTAL":     {"bs": 16.18, "u": 5840409,  "bu": 945150},
    },
    "MCO": {
        "3P":        {"bs": 19.89, "u": 765635,   "bu": 152261},
        "3P+CBT":    {"bs": 19.89, "u": 765635,   "bu": 152261},
        "MELI PRO":  {"bs": 17.44, "u": 239268,   "bu": 41717},
        "SELLER DEV":{"bs": 21.00, "u": 526367,   "bu": 110544},
        "TOTAL":     {"bs": 20.25, "u": 839075,   "bu": 169939},
    },
}

curr_bd = {
    "MLB": {
        "3P":        {"str": 1.55, "sv": 1.13, "ag": 2.85, "exc": 4.80},
        "3P+CBT":    {"str": 1.55, "sv": 1.13, "ag": 2.85, "exc": 4.80},
        "MELI PRO":  {"str": 1.55, "sv": 1.13, "ag": 2.85, "exc": 4.80},
        "SELLER DEV":{"str": 1.55, "sv": 1.13, "ag": 2.85, "exc": 4.80},
    },
    "MLM": {
        "3P":        {"str": 1.27, "sv": 1.54, "ag": 3.76, "exc": 6.80},
        "CBT":       {"str": 1.59, "sv": 2.00, "ag": 2.71, "exc": 7.62},
        "3P+CBT":    {"str": 1.38, "sv": 1.70, "ag": 3.39, "exc": 7.08},
        "MELI PRO":  {"str": 1.38, "sv": 1.70, "ag": 3.39, "exc": 7.08},
        "SELLER DEV":{"str": 1.38, "sv": 1.70, "ag": 3.39, "exc": 7.08},
    },
    "MLA": {
        "3P":        {"str": 0.85, "sv": 1.24, "ag": 5.04, "exc": 5.97},
        "3P+CBT":    {"str": 0.85, "sv": 1.24, "ag": 5.04, "exc": 5.97},
        "MELI PRO":  {"str": 0.85, "sv": 1.24, "ag": 5.04, "exc": 5.97},
        "SELLER DEV":{"str": 0.85, "sv": 1.24, "ag": 5.04, "exc": 5.97},
    },
    "MLC": {
        "3P":        {"str": 0.64, "sv": 1.94, "ag": 5.37, "exc": 6.51},
        "CBT":       {"str": 0.75, "sv": 4.26, "ag": 2.97, "exc": 13.30},
        "3P+CBT":    {"str": 0.65, "sv": 2.08, "ag": 5.23, "exc": 6.92},
        "MELI PRO":  {"str": 0.65, "sv": 2.08, "ag": 5.23, "exc": 6.92},
        "SELLER DEV":{"str": 0.65, "sv": 2.08, "ag": 5.23, "exc": 6.92},
    },
    "MCO": {
        "3P":        {"str": 1.24, "sv": 2.43, "ag": 9.19, "exc": 7.00},
        "3P+CBT":    {"str": 1.24, "sv": 2.43, "ag": 9.19, "exc": 7.00},
        "MELI PRO":  {"str": 1.24, "sv": 2.43, "ag": 9.19, "exc": 7.00},
        "SELLER DEV":{"str": 1.24, "sv": 2.43, "ag": 9.19, "exc": 7.00},
    },
}

curr_vert = {
    "MLB": {"BEAUTY":9.11,"CONSTRUCTION & INDUSTRY":10.82,"CPG":9.13,"ENTERTAINMENT":11.72,"FASHION":9.29,"FURNISHING & HOUSEWARE":10.10,"HEALTH":8.21,"HOME ELECTRONICS":11.37,"OTHERS":12.06,"SPORTS":13.66,"T & B":14.97,"TECHNOLOGY":11.08,"VEHICLE PARTS & ACCESSORIES":11.13},
    "MLM": {"BEAUTY":11.77,"CONSTRUCTION & INDUSTRY":11.59,"CPG":10.75,"ENTERTAINMENT":19.60,"FASHION":13.45,"FURNISHING & HOUSEWARE":12.85,"HEALTH":11.99,"HOME ELECTRONICS":12.96,"OTHERS":13.62,"SPORTS":14.45,"T & B":19.34,"TECHNOLOGY":16.44,"VEHICLE PARTS & ACCESSORIES":14.71},
    "MLA": {"BEAUTY":11.90,"CONSTRUCTION & INDUSTRY":12.78,"CPG":12.47,"ENTERTAINMENT":17.08,"FASHION":14.64,"FURNISHING & HOUSEWARE":12.79,"HEALTH":9.32,"HOME ELECTRONICS":12.03,"OTHERS":22.90,"SPORTS":14.58,"T & B":15.94,"TECHNOLOGY":14.14,"VEHICLE PARTS & ACCESSORIES":17.12},
    "MLC": {"BEAUTY":15.17,"CONSTRUCTION & INDUSTRY":15.09,"CPG":9.63,"ENTERTAINMENT":20.27,"FASHION":23.54,"FURNISHING & HOUSEWARE":12.42,"HEALTH":15.58,"HOME ELECTRONICS":11.08,"OTHERS":13.73,"SPORTS":20.35,"T & B":20.96,"TECHNOLOGY":15.22,"VEHICLE PARTS & ACCESSORIES":16.06},
    "MCO": {"BEAUTY":17.53,"CONSTRUCTION & INDUSTRY":17.51,"CPG":18.90,"ENTERTAINMENT":19.81,"FASHION":22.30,"FURNISHING & HOUSEWARE":20.22,"HEALTH":23.61,"HOME ELECTRONICS":13.77,"OTHERS":16.70,"SPORTS":22.29,"T & B":29.93,"TECHNOLOGY":18.92,"VEHICLE PARTS & ACCESSORIES":21.44},
}


# ── W28 (11/07/2026) ─────────────────────────────────────────────────────────

prev_kpi = {
    "MLB": {
        "3P":        {"bs": 10.44, "u": 66719353, "bu": 6965263},
        "3P+CBT":    {"bs": 10.44, "u": 66719353, "bu": 6965263},
        "MELI PRO":  {"bs": 7.04,  "u": 17165000, "bu": 1196000},
        "SELLER DEV":{"bs": 10.27, "u": 49554000, "bu": 5769000},
        "TOTAL":     {"bs": 10.53, "u": 78999747, "bu": 8316639},
    },
    "MLM": {
        "3P":        {"bs": 13.49, "u": 37910603, "bu": 5112000},
        "CBT":       {"bs": 14.37, "u": 19560906, "bu": 2640821},
        "3P+CBT":    {"bs": 13.49, "u": 57471509, "bu": 7752821},
        "MELI PRO":  {"bs": 9.33,  "u": 10027000, "bu": 929000},
        "SELLER DEV":{"bs": 13.66, "u": 27884000, "bu": 4183000},
        "TOTAL":     {"bs": 14.37, "u": 64315815, "bu": 9239429},
    },
    "MLA": {
        "3P":        {"bs": 14.06, "u": 5921230,  "bu": 832584},
        "3P+CBT":    {"bs": 14.06, "u": 5921230,  "bu": 832584},
        "MELI PRO":  {"bs": 11.48, "u": 2079000,  "bu": 277000},
        "SELLER DEV":{"bs": 12.82, "u": 3842000,  "bu": 556000},
        "TOTAL":     {"bs": 16.98, "u": 6863382,  "bu": 1165556},
    },
    "MLC": {
        "3P":        {"bs": 13.99, "u": 4432696,  "bu": 620000},
        "CBT":       {"bs": 22.49, "u": 631842,   "bu": 88296},
        "3P+CBT":    {"bs": 13.99, "u": 5064538,  "bu": 708296},
        "MELI PRO":  {"bs": 12.15, "u": 1299000,  "bu": 160000},
        "SELLER DEV":{"bs": 12.31, "u": 3133000,  "bu": 460000},
        "TOTAL":     {"bs": 14.93, "u": 5730604,  "bu": 855836},
    },
    "MCO": {
        "3P":        {"bs": 18.62, "u": 790817,   "bu": 147281},
        "3P+CBT":    {"bs": 18.62, "u": 790817,   "bu": 147281},
        "MELI PRO":  {"bs": 14.68, "u": 247000,   "bu": 36000},
        "SELLER DEV":{"bs": 19.99, "u": 544000,   "bu": 111000},
        "TOTAL":     {"bs": 19.23, "u": 868605,   "bu": 167055},
    },
}

prev_bd = {
    "MLB": {
        "3P":        {"str": 1.95, "sv": 1.01, "ag": 2.55, "exc": 3.96},
        "3P+CBT":    {"str": 1.95, "sv": 1.01, "ag": 2.55, "exc": 3.96},
        "MELI PRO":  {"str": 1.95, "sv": 1.01, "ag": 2.55, "exc": 3.96},
        "SELLER DEV":{"str": 1.95, "sv": 1.01, "ag": 2.55, "exc": 3.96},
    },
    "MLM": {
        "3P":        {"str": 1.08, "sv": 1.85, "ag": 4.16, "exc": 6.49},
        "CBT":       {"str": 1.00, "sv": 2.24, "ag": 3.80, "exc": 7.32},
        "3P+CBT":    {"str": 1.08, "sv": 1.85, "ag": 4.16, "exc": 6.49},
        "MELI PRO":  {"str": 1.08, "sv": 1.85, "ag": 4.16, "exc": 6.49},
        "SELLER DEV":{"str": 1.08, "sv": 1.85, "ag": 4.16, "exc": 6.49},
    },
    "MLA": {
        "3P":        {"str": 1.04, "sv": 1.07, "ag": 4.41, "exc": 4.64},
        "3P+CBT":    {"str": 1.04, "sv": 1.07, "ag": 4.41, "exc": 4.64},
        "MELI PRO":  {"str": 1.04, "sv": 1.07, "ag": 4.41, "exc": 4.64},
        "SELLER DEV":{"str": 1.04, "sv": 1.07, "ag": 4.41, "exc": 4.64},
    },
    "MLC": {
        "3P":        {"str": 0.69, "sv": 2.08, "ag": 5.14, "exc": 6.56},
        "CBT":       {"str": 1.00, "sv": 2.24, "ag": 3.80, "exc": 7.32},
        "3P+CBT":    {"str": 0.69, "sv": 2.08, "ag": 5.14, "exc": 6.56},
        "MELI PRO":  {"str": 0.69, "sv": 2.08, "ag": 5.14, "exc": 6.56},
        "SELLER DEV":{"str": 0.69, "sv": 2.08, "ag": 5.14, "exc": 6.56},
    },
    "MCO": {
        "3P":        {"str": 0.98, "sv": 2.22, "ag": 8.87, "exc": 7.34},
        "3P+CBT":    {"str": 0.98, "sv": 2.22, "ag": 8.87, "exc": 7.34},
        "MELI PRO":  {"str": 0.98, "sv": 2.22, "ag": 8.87, "exc": 7.34},
        "SELLER DEV":{"str": 0.98, "sv": 2.22, "ag": 8.87, "exc": 7.34},
    },
}

prev_vert = {
    "MLB": {"BEAUTY":9.11,"CONSTRUCTION & INDUSTRY":10.82,"CPG":9.13,"ENTERTAINMENT":11.84,"FASHION":7.22,"FURNISHING & HOUSEWARE":10.19,"HEALTH":7.37,"HOME ELECTRONICS":11.84,"OTHERS":11.42,"SPORTS":14.04,"T & B":15.26,"TECHNOLOGY":11.18,"VEHICLE PARTS & ACCESSORIES":11.35},
    "MLM": {"BEAUTY":11.38,"CONSTRUCTION & INDUSTRY":11.22,"CPG":10.49,"ENTERTAINMENT":17.69,"FASHION":11.82,"FURNISHING & HOUSEWARE":12.93,"HEALTH":8.84,"HOME ELECTRONICS":11.88,"OTHERS":12.66,"SPORTS":14.35,"T & B":19.32,"TECHNOLOGY":16.53,"VEHICLE PARTS & ACCESSORIES":13.84},
    "MLA": {"BEAUTY":13.04,"CONSTRUCTION & INDUSTRY":13.19,"CPG":17.92,"ENTERTAINMENT":18.19,"FASHION":13.68,"FURNISHING & HOUSEWARE":13.06,"HEALTH":9.49,"HOME ELECTRONICS":11.52,"OTHERS":20.75,"SPORTS":14.83,"T & B":18.57,"TECHNOLOGY":15.10,"VEHICLE PARTS & ACCESSORIES":17.23},
    "MLC": {"BEAUTY":13.48,"CONSTRUCTION & INDUSTRY":14.01,"CPG":8.37,"ENTERTAINMENT":20.65,"FASHION":18.69,"FURNISHING & HOUSEWARE":12.24,"HEALTH":14.68,"HOME ELECTRONICS":10.15,"OTHERS":11.90,"SPORTS":19.11,"T & B":21.56,"TECHNOLOGY":14.11,"VEHICLE PARTS & ACCESSORIES":15.49},
    "MCO": {"BEAUTY":15.55,"CONSTRUCTION & INDUSTRY":17.79,"CPG":15.77,"ENTERTAINMENT":19.89,"FASHION":23.29,"FURNISHING & HOUSEWARE":19.53,"HEALTH":19.59,"HOME ELECTRONICS":12.14,"OTHERS":17.51,"SPORTS":19.49,"T & B":27.50,"TECHNOLOGY":17.58,"VEHICLE PARTS & ACCESSORIES":19.71},
}


# ── Envio ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python scripts/test_chat_message.py <WEBHOOK_URL>")
        sys.exit(1)

    webhook_url = sys.argv[1]

    msg = build_message(
        week_id="W29",
        week_date=date(2026, 7, 18),
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
