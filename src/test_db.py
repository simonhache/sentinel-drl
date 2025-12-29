import os
import psycopg
from dotenv import load_dotenv

# Load credentials from your .env file
load_dotenv()

try:
    with psycopg.connect(
        host="localhost",
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    ) as conn:
        with conn.cursor() as cur:
            # Check if TimescaleDB extension is active
            cur.execute(
                "SELECT extname FROM pg_extension WHERE extname = 'timescaledb';"
            )
            extension = cur.fetchone()

            if extension:
                print(
                    f"✅ Success! Connected to {os.getenv('DB_NAME')} with TimescaleDB active."
                )

except Exception as e:
    print(f"❌ Connection failed: {e}")
