import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DATABASE_URL")

def insert_price_history(parsed_records):
    if not parsed_records:
        print("No records found.")
        return

    sql_command = """
    INSERT INTO price_history
    (game_id, shop_id, shop_name, price_amount, regular_amount, currency, discount, timestamp)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (game_id, shop_id, timestamp)
    DO NOTHING;
    """
    print(f"Preparing to insert {len(parsed_records)} records.")

    try:
        connection = psycopg2.connect(DB_URL)
        cursor = connection.cursor()

        for record in parsed_records:
            cursor.execute(sql_command, (
                record['game_id'],
                record['shop_id'],
                record['shop_name'],
                record['price_amount'],
                record['regular_amount'],
                record['currency'],
                record['discount'],
                record['timestamp']
            ))

        connection.commit()
        print(f"Successfully inserted all records.")

    except psycopg2.Error as e:
        print(f"Error during insertion: {e}")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

def insert_game_summary(record):
    if not record:
        print("No records found.")
        return

    sql_command = """
    INSERT INTO games_summary
    (game_id, shop_id, shop_name, price_amount, regular_amount, currency, discount, timestamp)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (game_id)
    DO UPDATE SET
        shop_id = EXCLUDED.shop_id,
        shop_name = EXCLUDED.shop_name,
        price_amount = EXCLUDED.price_amount,
        regular_amount = EXCLUDED.regular_amount,
        currency = EXCLUDED.currency,
        discount = EXCLUDED.discount,
        timestamp = EXCLUDED.timestamp;
    """

    try:
        connection = psycopg2.connect(DB_URL)
        cursor = connection.cursor()
        cursor.execute(sql_command, (
            record['game_id'],
            record['shop_id'],
            record['shop_name'],
            record['price_amount'],
            record['regular_amount'],
            record['currency'],
            record['discount'],
            record['timestamp']
        ))
        connection.commit()
        print("Successfully upserted game summary")
    except psycopg2.Error as e:
        print(f"Error during upsert: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()