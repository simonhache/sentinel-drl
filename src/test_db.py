import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError


def test_connection():
    # 1. Load environment variables from .env
    load_dotenv()

    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME")

    # 2. Construct the Connection URL
    # Format: postgresql+psycopg2://user:password@host:port/dbname
    url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}"

    print(f"--- Attempting to connect to: {host}:{port}/{db_name} ---")

    # 3. Create the Engine
    engine = create_engine(url)

    try:
        # 4. Use a context manager to connect and execute a test query
        with engine.connect() as connection:
            # Test 1: Simple Version Query
            res = connection.execute(text("SELECT version();"))
            version = res.fetchone()[0]
            print(f"✅ Success! Connected to PostgreSQL.")
            print(f"🔹 Version: {version[:50]}...")

            # Test 2: TimescaleDB Specific Check
            # This ensures the extension we wanted in Docker is actually running
            res = connection.execute(
                text(
                    "SELECT extname, installed_version FROM pg_extension WHERE extname = 'timescaledb';"
                )
            )
            extension = res.fetchone()
            if extension:
                print(f"✅ TimescaleDB Detected: Version {extension[1]}")
            else:
                print(
                    "⚠️ Warning: Connected to Postgres, but TimescaleDB extension is NOT found."
                )

    except OperationalError as e:
        print(f"❌ Connection Failed!")
        print(f"Error details: {e}")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")


if __name__ == "__main__":
    test_connection()
