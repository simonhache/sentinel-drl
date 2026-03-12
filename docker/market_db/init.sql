CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;


ALTER SYSTEM SET max_connections = '100';
ALTER SYSTEM SET shared_buffers = '256MB';

-- Schema for OHLCV data

CREATE TABLE IF NOT EXISTS market_ohlcv(
    timestamp TIMESTAMPTZ NOT NULL,
    symbol TEXT NOT NULL,
    open DOUBLE PRECISION NOT NULL,
    high DOUBLE PRECISION NOT NULL,
    low DOUBLE PRECISION NOT NULL,
    close DOUBLE PRECISION NOT NULL,
    volume DOUBLE PRECISION NOT NULL,
    PRIMARY KEY (timestamp, symbol)
);

SELECT create_hypertable(
    'market_ohlcv',
    'timestamp',
    if_not_exists => TRUE
);


-- Schema for raw sentiment data 

CREATE TABLE IF NOT EXISTS raw_sentiments(
    id TEXT PRIMARY KEY,
    source TEXT NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL,
    text TEXT NOT NULL,
    sentiment_score DOUBLE PRECISION NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_raw_sentiment_timestamp
ON raw_sentiments(timestamp);


-- Schema for aggregated sentiments data 

CREATE TABLE IF NOT EXISTS agg_sentiments(
    timestamp TIMESTAMPTZ NOT NULL,
    symbol TEXT NOT NULL,
    mean_sentiment DOUBLE PRECISION,
    mode_sentiment DOUBLE PRECISION,
    message_count INT,
    PRIMARY KEY (timestamp, symbol)
);

SELECT create_hypertable(
    'agg_sentiments',
    'timestamp',
    if_not_exists => TRUE
);


-- Schema for ingestion state data 

CREATE TABLE IF NOT EXISTS ingestion_state(
    source TEXT PRIMARY KEY,
    last_timestamp TIMESTAMPTZ
    updated_at TIMESTAMPTZ DEFAULT NOW()
);


-- Schema for Feature Candle data

CREATE TABLE feature_candles (

    timestamp TIMESTAMPTZ NOT NULL,
    symbol TEXT NOT NULL,

    return_1 REAL,
    return_5 REAL,

    volatility_20 REAL,

    volume_zscore REAL,

    sentiment_mean REAL,

    PRIMARY KEY(symbol, timestamp)
);