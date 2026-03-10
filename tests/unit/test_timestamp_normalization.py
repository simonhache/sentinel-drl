from sentinel_rl.ingestion.market.models import normalize_timestamp
from pytest import mark
from datetime import datetime


@mark.parametrize(
    "ts, expected",
    [
        ("2023-01-01T00:14:59Z", "2023-01-01T00:00:00Z"),  # 00:14:59 → 00:00:00
        ("2023-01-01T00:15:00Z", "2023-01-01T00:15:00Z"),  # 00:15:00 → 00:15:00
        ("2023-01-01T00:29:59Z", "2023-01-01T00:15:00Z"),  # 00:29:59 → 00:15:00
        ("2023-01-01T00:45:01Z", "2023-01-01T00:45:00Z"),  # 00:45:01 → 00:45:00
    ],
)
def test_timestamp_alignment_15m(ts: str, expected: str):
    ts_ms = int(datetime.fromisoformat(ts).timestamp() * 1000)
    aligned = normalize_timestamp(ts_ms, "15m")

    assert aligned == datetime.fromisoformat(expected)
