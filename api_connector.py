import requests
import json
import uuid

API_KEY = "API_KEY_HERE"
BASE_URL = "https://api.isthereanydeal.com"
COUNTRY_CODE = "US"

def get_game_id(game_title):
    endpoint = f"{BASE_URL}/games/lookup/v1"
    headers = {
        "User-Agent": "SteamSalesPredictor/1.0 (mahirasifchowdhury@gmail.com)",
        "Content-Type": "application/json"
    }
    payload = [game_title]

    try:
        response = requests.post(endpoint, params={"key": API_KEY}, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, list) and len(data) > 0 and data.get('found'):
            return data[0]['game']['id']
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