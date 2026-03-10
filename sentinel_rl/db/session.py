from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sentinel_rl.db.config import Settings

engine = create_engine(
    Settings().database_url,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    echo=False,  # set True for SQL debugging
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
