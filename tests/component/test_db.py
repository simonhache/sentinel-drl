from datetime import datetime, timezone
from sentinel_rl.db.repositories.market_repository import (
    UpsertMarketData,
    DeleteMarketData,
)
from sentinel_rl.ingestion.market.models import OHLCV


def test_insert():
    sample = [
        OHLCV(
            timestamp=datetime.now(timezone.utc),
            symbol="BTC/USDT",
            open=50000,
            high=50500,
            low=49500,
            close=50200,
            volume=120.5,
        )
    ]

    UpsertMarketData.apply(sample)
    DeleteMarketData.apply(sample)
