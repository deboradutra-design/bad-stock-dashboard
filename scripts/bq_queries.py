"""
BigQuery queries for the Bad Stock dashboard auto-update.
All KPI values come from DM_SHP_SALES_STOCK_MANAGEMENT_REPORT.
Using KPI_VERTICAL = 'TOTAL' to avoid double-counting across verticals.
"""

from datetime import date
from google.cloud import bigquery

TABLE = "meli-bi-data.WHOWNER.DM_SHP_SALES_STOCK_MANAGEMENT_REPORT"
SITES = ["MLB", "MLM", "MLA", "MLC", "MCO"]

# Maps KPI_CODE → field name used in dashboard constants
BREAKDOWN_CODES = {
    "MECE_SHARE_STRANDED_STOCK_SQ":      "str",
    "MECE_SHARE_NOT_SELLING_STOCK_SQ":   "sv",
    "MECE_SHARE_AGING_STOCK_SQ":          "ag",
    "MECE_SHARE_SURPLUS_AGING_STOCK_SQ": "exc",
}


def get_client() -> bigquery.Client:
    return bigquery.Client()


def _pct(val) -> float:
    """Convert BigQuery decimal (0–1) to percentage rounded to 2dp."""
    return round(float(val or 0) * 100, 2) if val is not None else None


def get_kpi_data(client: bigquery.Client, kpi_date: date) -> dict:
    """
    Returns bad stock % + units by site and initiative.
    Structure: {site: {initiative: {bs, u, bu}}}
    """
    query = f"""
    SELECT
      KPI_SITE                  AS site,
      KPI_INITIATIVE            AS initiative,
      KPI_VALUE                 AS bs_raw,
      KPI_DENOMINADOR_VAL       AS total_units,
      KPI_NUMERADOR_VAL         AS bad_units
    FROM `{TABLE}`
    WHERE KPI_CODE       = 'SHARE_BAD_STOCK_SQ'
      AND DIM_ESTRELLA   = 'TOTAL'
      AND KPI_VERTICAL   = 'TOTAL'
      AND KPI_DATE       = '{kpi_date}'
      AND KPI_SITE       IN ('MLB','MLM','MLA','MLC','MCO')
      AND KPI_INITIATIVE IN ('3P','3P+CBT','CBT','MELI PRO','SELLER DEV','1P/PL','TOTAL')
    ORDER BY KPI_SITE, KPI_INITIATIVE
    """
    result = {}
    for row in client.query(query).result():
        result.setdefault(row.site, {})[row.initiative] = {
            "bs": _pct(row.bs_raw),
            "u":  int(row.total_units or 0),
            "bu": int(row.bad_units  or 0),
        }
    return result


def get_breakdown_data(client: bigquery.Client, kpi_date: date) -> dict:
    """
    Returns Stranded / Sin Venta / Aging / Aging+Exc % by site and initiative.
    Structure: {site: {initiative: {str, sv, ag, exc}}}
    """
    codes = ", ".join(f"'{c}'" for c in BREAKDOWN_CODES)
    query = f"""
    SELECT
      KPI_SITE        AS site,
      KPI_INITIATIVE  AS initiative,
      KPI_CODE        AS kpi_code,
      KPI_VALUE       AS value
    FROM `{TABLE}`
    WHERE KPI_CODE       IN ({codes})
      AND DIM_ESTRELLA   = 'TOTAL'
      AND KPI_VERTICAL   = 'TOTAL'
      AND KPI_DATE       = '{kpi_date}'
      AND KPI_SITE       IN ('MLB','MLM','MLA','MLC','MCO')
      AND KPI_INITIATIVE IN ('3P','3P+CBT','CBT','MELI PRO','SELLER DEV','1P/PL','TOTAL')
    ORDER BY KPI_SITE, KPI_INITIATIVE, KPI_CODE
    """
    result = {}
    for row in client.query(query).result():
        field = BREAKDOWN_CODES.get(row.kpi_code)
        if field:
            result.setdefault(row.site, {}).setdefault(row.initiative, {})[field] = _pct(row.value)
    return result


def get_vertical_data(client: bigquery.Client, kpi_date: date) -> dict:
    """
    Returns bad stock % by vertical, per site (initiative = 3P+CBT).
    Structure: {site: {vertical: bs_pct}}
    Excludes the 'TOTAL' virtual vertical row.
    """
    query = f"""
    SELECT
      KPI_SITE       AS site,
      KPI_VERTICAL   AS vertical,
      KPI_VALUE      AS bs_raw
    FROM `{TABLE}`
    WHERE KPI_CODE      = 'SHARE_BAD_STOCK_SQ'
      AND DIM_ESTRELLA  = 'TOTAL'
      AND KPI_DATE      = '{kpi_date}'
      AND KPI_SITE      IN ('MLB','MLM','MLA','MLC','MCO')
      AND KPI_INITIATIVE = '3P+CBT'
      AND KPI_VERTICAL  IS NOT NULL
      AND KPI_VERTICAL  != 'TOTAL'
    ORDER BY KPI_SITE, KPI_VERTICAL
    """
    result = {}
    for row in client.query(query).result():
        result.setdefault(row.site, {})[row.vertical] = _pct(row.bs_raw)
    return result


def get_available_dates(client: bigquery.Client, from_date: date) -> list[date]:
    """Returns distinct KPI_DATE values on or after from_date (for week detection)."""
    query = f"""
    SELECT DISTINCT KPI_DATE
    FROM `{TABLE}`
    WHERE KPI_CODE = 'SHARE_BAD_STOCK_SQ'
      AND KPI_SITE = 'MLB'
      AND KPI_DATE >= '{from_date}'
    ORDER BY KPI_DATE
    """
    return [row.KPI_DATE for row in client.query(query).result()]
