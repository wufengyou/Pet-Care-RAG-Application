import os
from dotenv import load_dotenv
import psycopg2
import time

load_dotenv()

def init_db():
    max_retries = 5
    retry_delay = 5

    for attempt in range(max_retries):
        try:
            conn = psycopg2.connect(
                host=os.getenv("POSTGRES_HOST", "postgres"),
                database=os.getenv("POSTGRES_DB", "pet_care"),
                user=os.getenv("POSTGRES_USER", "wufy1234"),
                password=os.getenv("POSTGRES_PASSWORD", "wufy1234"),
                port=os.getenv("POSTGRES_PORT", 5432)
            )
            
            with conn.cursor() as cur:
                # Create conversations table
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS conversations (
                        id TEXT PRIMARY KEY,
                        question TEXT NOT NULL,
                        answer TEXT NOT NULL,
                        model_used TEXT NOT NULL,
                        response_time FLOAT NOT NULL,
                        relevance TEXT NOT NULL,
                        relevance_explanation TEXT NOT NULL,
                        prompt_tokens INTEGER NOT NULL,
                        completion_tokens INTEGER NOT NULL,
                        total_tokens INTEGER NOT NULL,
                        eval_prompt_tokens INTEGER NOT NULL,
                        eval_completion_tokens INTEGER NOT NULL,
                        eval_total_tokens INTEGER NOT NULL,
                        openai_cost FLOAT NOT NULL,
                        timestamp TIMESTAMP WITH TIME ZONE NOT NULL
                    )
                """)
                
                # Create feedback table
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS feedback (
                        id SERIAL PRIMARY KEY,
                        conversation_id TEXT REFERENCES conversations(id),
                        feedback INTEGER NOT NULL,
                        timestamp TIMESTAMP WITH TIME ZONE NOT NULL
                    )
                """)
            
            conn.commit()
            print("Database initialized successfully.")
            return
        except psycopg2.OperationalError as e:
            print(f"Attempt {attempt + 1} failed. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
    
    print("Failed to initialize database after multiple attempts.")
    exit(1)

if __name__ == "__main__":
    init_db()
