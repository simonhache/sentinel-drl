from sqlalchemy import Column, String, Float, Integer, Text, TIMESTAMP
from sqlalchemy.orm import declarative_base
from sqlalchemy.schema import PrimaryKeyConstraint

Base = declarative_base()


class MarketOHLCV(Base):
    __tablename__ = "market_ohlcv"

    timestamp = Column(TIMESTAMP(timezone=True), nullable=False)
    symbol = Column(String, nullable=False)
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)

    __table_args__ = (PrimaryKeyConstraint("timestamp", "symbol"),)


class RawSentiment(Base):
    __tablename__ = "raw_sentiment"

    id = Column(String, primary_key=True)
    source = Column(String, nullable=False)
    timestamp = Column(TIMESTAMP(timezone=True), nullable=False)
    text = Column(Text, nullable=False)
    sentiment_score = Column(Float)


class SentimentAgg(Base):
    __tablename__ = "sentiment_agg"

    timestamp = Column(TIMESTAMP(timezone=True), nullable=False)
    symbol = Column(String, nullable=False)
    mean_sentiment = Column(Float)
    message_count = Column(Integer)

    __table_args__ = (PrimaryKeyConstraint("timestamp", "symbol"),)


class IngestionState(Base):
    __tablename__ = "ingestion_state"

    source = Column(String, primary_key=True)
    last_timestamp = Column(TIMESTAMP(timezone=True))
    updated_at = Column(TIMESTAMP(timezone=True), default="now()")
