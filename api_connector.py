import requests
import json
import uuid
import os
from dotenv import load_dotenv

load_dotenv()
from parser import parse_low_data, parse_price_history
from db_loader import insert_price_history, insert_game_summary

API_KEY = os.getenv("ITAD_API_KEY")
BASE_URL = "https://api.isthereanydeal.com"
COUNTRY_CODE = "US"

def get_game_id(game_title):
    endpoint = f"{BASE_URL}/games/lookup/v1"
    headers = {
        "User-Agent": "SteamSalesPredictor/1.0 (mahirasifchowdhury@gmail.com)",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(endpoint, params={"key": API_KEY, "title": game_title}, headers=headers)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, dict) and data.get("found"):
            return data['game']['id']
        else:
            print(f"Could not find game with title {game_title}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching game ID: {e}")
        return None

def get_historical_low(game_id):
    endpoint = f"{BASE_URL}/games/historylow/v1"
    headers = {"User-Agent": "SteamSalesPredictor/1.0 (mahirasifchowdhury@gmail.com)",
               "Content-Type": "application/json"}
    payload = [game_id]

    try:
        response = requests.post(endpoint, params={"key": API_KEY, "country": COUNTRY_CODE}, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching historical data: {e}")
        return None

def get_price_history(game_id):
    endpoint = f'{BASE_URL}/games/history/v2'
    headers = {
        "User-Agent": "SteamSalesPredictor/1.0 (mahirasifchowdhury@gmail.com)",
        "Content-Type": "application/json"
    }
    params = {
        "key": API_KEY,
        "country": COUNTRY_CODE,
        "id": game_id
    }

    try:
        response = requests.get(endpoint, params=params, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print("Error fetching historical pricing data")
        return None

def main():
    target_game = "Persona 4 Golden"
    print(f"Searching game ID for: {target_game}...")

    game_id = get_game_id(target_game)

    if game_id:
        print(f"Successfully found game ID: {game_id}")

        print(f"Fetching full time-series price history...")

        low_data = get_historical_low(game_id)
        history_data = get_price_history(game_id)
        if history_data:
            print("\n--- raw time series json ---")
            if isinstance(history_data, list):
                print(json.dumps(history_data[:3], indent=4))
            else:
                print(json.dumps(history_data, indent=4))
            print("\n--- Parsed Output (Ready for database) ---")

            parsed_history = parse_price_history(history_data, game_id)
            insert_price_history(parsed_history)
            for record in parsed_history[:3]:
                print(record)
        if low_data:
            parsed_summary = parse_low_data(low_data)
            insert_game_summary(parsed_summary[0])

            print(f"\nExtracted {len(parsed_history)} records from {target_game}.")
        else:
            print(f"Failed to fetch time-series data for ID: {game_id}")
    else:
        print(f"Could not find game ID for {target_game}")
if __name__ == "__main__":
    main()