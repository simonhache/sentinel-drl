from datetime import datetime, timezone
from dataclasses import dataclass

TIMEFRAME_SECONDS = {
    "1m": 60,
    "5m": 300,
    "15m": 900,
    "1h": 3600,
}


@dataclass
class OHLCV:
    timestamp: datetime
    symbol: str
    open: float
    high: float
    low: float
    close: float
    volume: float


def normalize_timestamp(ts_ms: int, timeframe: str) -> datetime:
    ts = ts_ms / 1000
    interval = TIMEFRAME_SECONDS[timeframe]

    aligned = int(ts // interval) * interval

    return datetime.fromtimestamp(aligned, tz=timezone.utc)


def normalize_ohlcv(symbol: str, raw_candle: list, timeframe: str) -> OHLCV:
    ts, o, h, l, c, v = raw_candle

    timestamp = normalize_timestamp(ts, timeframe)

    return OHLCV(
        timestamp=timestamp,
        symbol=symbol,
        open=float(o),
        high=float(h),
        low=float(l),
        close=float(c),
        volume=float(v),
    )
