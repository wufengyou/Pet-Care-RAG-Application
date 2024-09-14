import time
import psycopg2
import os

def wait_for_db():
    max_retries = 30
    retry_interval = 2

    for _ in range(max_retries):
        try:
            conn = psycopg2.connect(
                dbname=os.getenv('POSTGRES_DB'),
                user=os.getenv('POSTGRES_USER'),
                password=os.getenv('POSTGRES_PASSWORD'),
                host='postgres'
            )
            conn.close()
            print("Successfully connected to the database.")
            return
        except psycopg2.OperationalError:
            print("Database not ready. Waiting...")
            time.sleep(retry_interval)

    print("Failed to connect to the database after multiple attempts.")
    exit(1)

if __name__ == "__main__":
    wait_for_db()
