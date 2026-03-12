from datetime import timedelta

from sentinel_rl.db.session import SessionLocal
from sentinel_rl.db.repositories.repair_repository import RepairRepository
from sentinel_rl.ingestion.market.market_fetcher import MarketDataFetcher
from sentinel_rl.db.repositories.market_repository import UpsertMarketData


from datetime import datetime


def build_repair_windows(missing_ts, timeframe_seconds):
    windows = []

    if not missing_ts:
        return windows

    start = missing_ts[0]
    prev = start

    for ts in missing_ts[1:]:
        if (ts - prev).total_seconds() > timeframe_seconds:
            windows.append((start, prev))
            start = ts

        prev = ts

    windows.append((start, prev))

    return windows


class MarketDataRepairService:
    def __init__(
        self,
        fetcher: MarketDataFetcher,
        repository: RepairRepository,
        symbol: str,
        timeframe_seconds: int,
    ):
        self.fetcher = fetcher
        self.repo = repository
        self.symbol = symbol
        self.tf_seconds = timeframe_seconds

    def repair(self, start: datetime, end: datetime):
        missing = self.repo.find_missing_candles(self.symbol, start, end)

        if not missing:
            print("No gaps detected")
            return

        print(f"Gaps detected: {len(missing)}")

        windows = build_repair_windows(missing, self.tf_seconds)

        for w_start, w_end in windows:
            since = int(w_start.timestamp() * 1000)

            rows = self.fetcher.fetch_batch(since)

            UpsertMarketData.apply(rows, SessionLocal)

            print(f"Repaired window {w_start} → {w_end}")
