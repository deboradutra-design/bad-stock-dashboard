"""
Weekly Bad Stock dashboard auto-update.
Runs every Monday at 09:00 BRT (12:00 UTC via GitHub Actions).

Workflow:
  1. Parse current state from index.html to determine the last week.
  2. Compute the expected BQ date for the new week (last_date + 7 days, ±1 day).
  3. Query BigQuery for current + previous week data.
  4. Update index.html via html_updater.
  5. Commit and push to GitHub (triggers Pages deployment).
  6. Send Google Chat notification.
"""

import os
import re
import sys
import subprocess
from datetime import date, timedelta
from pathlib import Path

# Allow running directly from scripts/ or from repo root
sys.path.insert(0, str(Path(__file__).parent))

from bq_queries import (
    get_client,
    get_kpi_data,
    get_breakdown_data,
    get_vertical_data,
    get_available_dates,
)
from html_updater import update_html
from chat_notifier import build_message, send_to_chat


# ── Paths & config ─────────────────────────────────────────────────────────────

REPO_ROOT   = Path(__file__).resolve().parent.parent
HTML_PATH   = REPO_ROOT / "index.html"
WEBHOOK_URL = os.environ.get("GOOGLE_CHAT_WEBHOOK", "")


# ── Helpers ────────────────────────────────────────────────────────────────────

def _parse_last_week(html: str) -> tuple[str, date, int]:
    """
    Extracts the last week entry from the WEEKS JS array.
    Returns (week_id, week_date, month).

    Parses lines like:
      { id:'W15', date:'12/04/2026', month:4, label:'W15 (12/04)★', current:true },
    """
    matches = re.findall(
        r"\{\s*id:'(W\d+)',\s*date:'(\d{2}/\d{2}/\d{4})',\s*month:(\d+)",
        html,
    )
    if not matches:
        raise RuntimeError("WEEKS array não encontrado ou vazio em index.html")
    wid, date_str, month = matches[-1]
    d, m, y = int(date_str[:2]), int(date_str[3:5]), int(date_str[6:])
    return wid, date(y, m, d), int(month)


def _next_week_id(last_id: str) -> str:
    return f"W{int(last_id[1:]) + 1}"


def _find_bq_date(client, last_date: date) -> date | None:
    """
    Looks for a BQ date 7 days after last_date (±1 day for Sunday offset).
    Returns the matching date or None if data is not yet available.
    """
    candidate = last_date + timedelta(days=7)
    # Search from one day before the candidate to handle ±1 day offset
    available = get_available_dates(client, from_date=candidate - timedelta(days=1))
    for d in available:
        if abs((d - candidate).days) <= 1:
            return d
    return None


def _week_date_from_bq(bq_date: date) -> date:
    """
    Dashboard reference date from a BQ date.
    Jan–Feb 2026: BQ uses Sunday → dashboard Saturday = BQ - 1 day.
    Mar onwards:  BQ uses Saturday directly.
    """
    # weekday() == 6 → Sunday
    if bq_date.weekday() == 6:
        return bq_date - timedelta(days=1)
    return bq_date


def _git_commit_push(week_id: str) -> None:
    """Stages index.html, commits, and pushes to GitHub."""
    repo = str(REPO_ROOT)
    subprocess.run(["git", "-C", repo, "add", "index.html"], check=True)
    subprocess.run(
        ["git", "-C", repo, "commit", "-m", f"auto: atualiza dashboard {week_id}"],
        check=True,
    )
    subprocess.run(["git", "-C", repo, "push"], check=True)
    print(f"✅ Push realizado — {week_id}")


# ── Main ───────────────────────────────────────────────────────────────────────

def main() -> None:
    # 1. Parse current state from HTML
    html = HTML_PATH.read_text(encoding="utf-8")
    last_id, last_date, _ = _parse_last_week(html)
    next_id = _next_week_id(last_id)

    print(f"🔍 Último week no HTML: {last_id} ({last_date.strftime('%d/%m/%Y')})")
    print(f"🔍 Buscando dados para: {next_id}…")

    # 2. Check BigQuery for new week data
    client = get_client()
    bq_date = _find_bq_date(client, last_date)

    if bq_date is None:
        print(
            f"⏳ Dados para {next_id} ainda não disponíveis no BigQuery — abortando."
        )
        sys.exit(0)

    print(f"📅 Data BigQuery encontrada: {bq_date}")

    week_date   = _week_date_from_bq(bq_date)
    month       = week_date.month
    prev_bq_date = bq_date - timedelta(days=7)

    # 3. Query BigQuery — current and previous week
    print("📊 Consultando BigQuery…")
    curr_kpi  = get_kpi_data(client, bq_date)
    prev_kpi  = get_kpi_data(client, prev_bq_date)
    curr_bd   = get_breakdown_data(client, bq_date)
    prev_bd   = get_breakdown_data(client, prev_bq_date)
    curr_vert = get_vertical_data(client, bq_date)
    prev_vert = get_vertical_data(client, prev_bq_date)

    if not curr_kpi:
        print(f"❌ Nenhum dado KPI retornado para {bq_date} — abortando.")
        sys.exit(1)

    # 4. Update index.html
    html = update_html(html, next_id, week_date, month, curr_kpi, curr_bd)
    HTML_PATH.write_text(html, encoding="utf-8")

    # 5. Commit and push to GitHub
    _git_commit_push(next_id)

    # 6. Send Google Chat notification
    if WEBHOOK_URL:
        msg = build_message(
            week_id=next_id,
            week_date=week_date,
            curr_kpi=curr_kpi,
            prev_kpi=prev_kpi,
            curr_bd=curr_bd,
            prev_bd=prev_bd,
            curr_vert=curr_vert,
            prev_vert=prev_vert,
            month=month,
        )
        send_to_chat(WEBHOOK_URL, msg)
    else:
        print("⚠️  GOOGLE_CHAT_WEBHOOK não configurado — notificação não enviada.")

    print(f"🎉 Dashboard atualizado com {next_id}!")


if __name__ == "__main__":
    main()
