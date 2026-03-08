import io
from typing import Any, Dict, List

import pandas as pd


def process_party_votes(records: List[Dict[str, Any]]) -> pd.DataFrame:
    """Select and clean party vote columns for downstream API/UI/export."""
    df = pd.DataFrame(records)
    selected = df[["PoliticalPartyName", "TotalVoteReceived"]].copy()
    selected["TotalVoteReceived"] = pd.to_numeric(
        selected["TotalVoteReceived"], errors="coerce"
    ).fillna(0)
    selected = selected.sort_values("TotalVoteReceived", ascending=False)
    return selected


def to_excel_bytes(df: pd.DataFrame) -> bytes:
    """Create in-memory Excel binary for downloads."""
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="PartyVotes")
    return buffer.getvalue()


def to_csv_bytes(df: pd.DataFrame) -> bytes:
    """Create CSV bytes for downloads."""
    return df.to_csv(index=False).encode("utf-8-sig")
