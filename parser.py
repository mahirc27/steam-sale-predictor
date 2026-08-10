from datetime import datetime
from typing import Any, Dict, List, Optional

def parse_low_data(raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    parsed_data = []

    for item in raw_data:
        game_id = item.get("id")
        low_data = item.get("low", {})

        if not low_data:
            continue

        shop_info = low_data.get("shop", {})
        price_info = low_data.get("price", {})
        regular_info = low_data.get("regular", {})

        raw_time = low_data.get("timestamp")

        parsed_time = datetime.fromisoformat(raw_time.split('T')[0]) if raw_time else None

        record = {
            'game_id': game_id,
            'shop_id': shop_info.get("id"),
            'shop_name': shop_info.get("name"),
            'price_amount': price_info.get('amount'),
            'regular_amount': regular_info.get('amount'),
            'currency': price_info.get('currency'),
            'discount': low_data.get('cut'),
            'timestamp': parsed_time,
        }

        parsed_data.append(record)

    return parsed_data

def parse_price_history(raw_data: List[Dict[str, Any]], game_id: str) -> List[Dict[str, Any]]:
    parsed_data = []

    for item in raw_data:
        shop_info = item.get("shop", {})
        deal_info = item.get("deal", {})

        if not deal_info:
            continue

        price_info = deal_info.get("price", {})
        regular_info = deal_info.get("regular", {})

        raw_time = item.get("timestamp")
        parsed_time = datetime.fromisoformat(raw_time) if raw_time else None

        record = {
            'game_id': game_id,
            'shop_id': shop_info.get("id"),
            'shop_name': shop_info.get("name"),
            'price_amount': price_info.get("amount"),
            'regular_amount': regular_info.get("amount"),
            'currency': price_info.get("currency"),
            'discount': deal_info.get("cut"),
            'timestamp': parsed_time,
        }

        parsed_data.append(record)

    return parsed_data
