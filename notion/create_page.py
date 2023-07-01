from datetime import date
from typing import Optional


def create_page(journey: str, route: str, old_price: int, new_price: int, operator, start_date, end_date, duration: str, connections: int, destination, trend, cabin, type):

    new_page = {
        "Route": {"title": [{"text": {"content": journey}}]},
        "Price change": {"number": old_price - new_price},
        "New price": {"number": new_price},
        "Operator": {"relation": operator},
        "Date": {"date": {"start": start_date, "end": end_date}},
        "Duration": {"rich_text": [{"text": {"content": duration}}]},
        "Airports": {"rich_text": [{"text": {"content": route}}]},
        "Connections": {"number": connections},
        "Old price": {"number": old_price},
        "Destination": {"relation": destination},
        "Trend": {"relation": trend},
        "Cabin": {"select": {"name": cabin}},
        "Type": {"select": {"name": type}},
    }

    return new_page
