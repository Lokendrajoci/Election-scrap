from datetime import datetime, timedelta

from flask import Flask, jsonify, make_response, render_template

from processing import TOTAL_VOTES, process_party_votes, to_csv_bytes, to_excel_bytes
from scraper import fetch_raw_records

app = Flask(__name__)

CACHE_TTL_SECONDS = 600
_cache_df = None
_cache_expires_at = datetime.min


def get_votes_df(force_refresh: bool = False):
    """Small in-process cache to avoid hitting source on every request."""
    global _cache_df, _cache_expires_at

    now = datetime.utcnow()
    cache_valid = _cache_df is not None and now < _cache_expires_at

    if force_refresh or not cache_valid:
        records = fetch_raw_records()
        _cache_df = process_party_votes(records)
        _cache_expires_at = now + timedelta(seconds=CACHE_TTL_SECONDS)

    return _cache_df


@app.route("/")
def home():
    df = get_votes_df()
    top10 = df.head(10)

    return render_template(
        "index.html",
        updated_at=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
        ttl_minutes=CACHE_TTL_SECONDS // 60,
        total_votes=TOTAL_VOTES,
        rows=df.to_dict(orient="records"),
        chart_labels=top10["PoliticalPartyName"].tolist(),
        chart_values=top10["TotalVoteReceived"].tolist(),
    )


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/api/v1/votes")
def api_votes():
    df = get_votes_df()
    return jsonify(df.to_dict(orient="records"))


@app.route("/api/v1/votes/refresh")
def api_votes_refresh():
    df = get_votes_df(force_refresh=True)
    return jsonify(df.to_dict(orient="records"))


@app.route("/download/csv")
def download_csv():
    df = get_votes_df()
    payload = to_csv_bytes(df)

    response = make_response(payload)
    response.headers["Content-Type"] = "text/csv; charset=utf-8"
    response.headers["Content-Disposition"] = (
        "attachment; filename=pr_votes_party_votes.csv"
    )
    return response


@app.route("/download/excel")
def download_excel():
    df = get_votes_df()
    payload = to_excel_bytes(df)

    response = make_response(payload)
    response.headers["Content-Type"] = (
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response.headers["Content-Disposition"] = (
        "attachment; filename=pr_votes_party_votes.xlsx"
    )
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
