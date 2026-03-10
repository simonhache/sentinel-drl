import ccxt


class ExchangeClient:
    def __init__(self, exchange_name="binance"):
        exchange_class = getattr(ccxt, exchange_name)
        self.exchange = exchange_class({"enableRateLimit": True})

    def fetch_ohlcv(
        self, symbol: str, timeframe: str, since: int | None = None, limit=1000
    ):
        return self.exchange.fetch_ohlcv(
            symbol=symbol, timeframe=timeframe, since=since, limit=limit
        )
