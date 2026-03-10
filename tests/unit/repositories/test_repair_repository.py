from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta

from sentinel_rl.ingestion.repair.repair_service import MarketDataRepairService
from sentinel_rl.ingestion.market.models import OHLCV
from sentinel_rl.ingestion.repair.repair_service import build_repair_windows


@patch("sentinel_rl.ingestion.repair.repair_service.RepairRepository")
@patch("sentinel_rl.ingestion.repair.repair_service.UpsertMarketData.apply")
@patch("sentinel_rl.ingestion.repair.repair_service.SessionLocal")
def test_repair_service_processes_missing_windows(mock_session, mock_upsert, mock_repo):
    # Mock missing candles returned from repo
    mock_repo_instance = MagicMock()

    base = datetime(2023, 1, 1)

    mock_repo_instance.find_missing_candles.return_value = [
        base,
        base + timedelta(minutes=15),
        base + timedelta(minutes=30),
    ]

    mock_repo.return_value = mock_repo_instance

    # Mock exchange fetcher
    mock_fetcher = MagicMock()

    mock_fetcher.fetch_batch.return_value = [
        OHLCV(
            timestamp=base,
            symbol="BTC/USDT",
            open=1,
            high=1,
            low=1,
            close=1,
            volume=1,
        )
    ]

    service = MarketDataRepairService(
        fetcher=mock_fetcher, symbol="BTC/USDT", timeframe_seconds=900
    )

    service.repair(base, base + timedelta(hours=1))

    assert mock_fetcher.fetch_batch.called
    assert mock_upsert.called


def test_window_builder():
    base = datetime(2023, 1, 1)

    missing = [
        base,
        base + timedelta(minutes=15),
        base + timedelta(minutes=60),
    ]

    windows = build_repair_windows(missing, 900)

    assert len(windows) == 2
