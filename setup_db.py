import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
DB_URL = os.getenv("DATABASE_URL")

def create_tables():
    sql_commands = """
    CREATE TABLE IF NOT EXISTS games_summary (
        game_id VARCHAR(255) PRIMARY KEY,
        shop_id INTEGER,
        shop_name VARCHAR(255),
        price_amount NUMERIC(10, 2),
        regular_amount NUMERIC(10, 2),
        currency VARCHAR(10),
        discount INTEGER,
        timestamp TIMESTAMP WITH TIME ZONE
    );
    
    CREATE TABLE IF NOT EXISTS price_history (
        id SERIAL PRIMARY KEY,
        game_id VARCHAR(255),
        shop_id INTEGER,
        shop_name VARCHAR(255),
        price_amount NUMERIC(10, 2),
        regular_amount NUMERIC(10, 2),
        currency VARCHAR(10),
        discount INTEGER,
        timestamp TIMESTAMP WITH TIME ZONE
    );
    """
    print("Connecting to Neon PostgreSQL...")

    try:
        connection = psycopg2.connect(DB_URL)

        cursor = connection.cursor()

        cursor.execute(sql_commands)

        connection.commit()

        cursor.close()
        connection.close()

        print("Successfully created database tables.")

    except psycopg2.Error as e:
        print(f"Database error: {e}")

if __name__ == "__main__":
    create_tables()