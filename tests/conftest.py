import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sentinel_rl.db.models import Base


@pytest.fixture(scope="function", name="local_db_session_factory")
def test_db():
    engine = create_engine("sqlite:///:memory:")

    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Create schema
    Base.metadata.create_all(bind=engine)

    yield TestingSessionLocal

    # Teardown
    Base.metadata.drop_all(bind=engine)
