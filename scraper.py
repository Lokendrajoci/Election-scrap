import json
from typing import Any, Dict, List

import requests

SOURCE_URL = "https://result.election.gov.np/PRVoteChartResult2082.aspx"
DATA_PATH = "JSONFiles/Election2082/Common/PRHoRPartyTop5.txt"
DATA_URL = f"https://result.election.gov.np/Handlers/SecureJson.ashx?file={DATA_PATH}"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/121.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": SOURCE_URL,
    "X-Requested-With": "XMLHttpRequest",
}


def fetch_raw_records(timeout: int = 30) -> List[Dict[str, Any]]:
    """Fetch raw election records from target website handler endpoint."""
    session = requests.Session()
    session.headers.update(HEADERS)

    # First request initializes cookies including CsrfToken.
    home = session.get(SOURCE_URL, timeout=timeout)
    home.raise_for_status()

    csrf_token = session.cookies.get("CsrfToken")
    if csrf_token:
        session.headers.update({"X-CSRF-Token": csrf_token})

    response = session.get(DATA_URL, timeout=timeout)
    response.raise_for_status()

    return json.loads(response.text)


def fetch_total_votes(records: List[Dict[str, Any]] = None, timeout: int = 30) -> int:
    """Calculate total votes from the election records (sum of all parties)."""
    if records is None:
        records = fetch_raw_records(timeout=timeout)
    
    total = 0
    for record in records:
        votes = record.get("TotalVoteReceived", 0)
        if votes:
            total += int(float(votes))
    
    return total
