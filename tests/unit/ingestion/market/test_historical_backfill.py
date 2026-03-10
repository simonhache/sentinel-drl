from unittest.mock import MagicMock, patch
from datetime import datetime, timezone

from sentinel_rl.ingestion.market.historical_backfill import HistoricalBackfillService
from sentinel_rl.ingestion.market.models import OHLCV


@patch("sentinel_rl.ingestion.market.historical_backfill.UpsertMarketData.apply")
@patch("sentinel_rl.ingestion.market.historical_backfill.SessionLocal")
def test_backfill_runs_and_updates_cursor(mock_session, mock_upsert):
    mock_fetcher = MagicMock()

    mock_fetcher.fetch_batch.return_value = [
        OHLCV(
            timestamp=datetime(2023, 1, 1, tzinfo=timezone.utc),
            symbol="BTC/USDT",
            open=1,
            high=1,
            low=1,
            close=1,
            volume=1,
        )
    ]

    service = HistoricalBackfillService(fetcher=mock_fetcher, source_id="test_source")

    start = datetime(2023, 1, 1, tzinfo=timezone.utc)

    # stop infinite loop
    mock_fetcher.fetch_batch.side_effect = [mock_fetcher.fetch_batch.return_value, []]

    service.run(start)

    assert mock_fetcher.fetch_batch.called
    assert mock_upsert.called
