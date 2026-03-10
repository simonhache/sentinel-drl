from unittest.mock import MagicMock

from sentinel_rl.ingestion.market.market_fetcher import MarketDataFetcher


def test_fetch_batch_returns_normalized_rows():
    mock_exchange = MagicMock()

    mock_exchange.fetch_ohlcv.return_value = [[1672531201000, 1, 2, 0.5, 1.5, 100]]

    fetcher = MarketDataFetcher(
        exchange_client=mock_exchange, symbol="BTC/USDT", timeframe="15m"
    )

    rows = fetcher.fetch_batch(1672531200000)

    candle = rows[0]
    assert len(rows) == 1
    assert candle.symbol == "BTC/USDT"
    assert int(candle.timestamp.timestamp() * 1000) == 1672531200000

    mock_exchange.fetch_ohlcv.assert_called_once()
