import os
import sys

from dotenv import load_dotenv
from notion_client import Client
from functions.console import log

from functions.get_mails import get_mails
from notion.cache import fetch_databases_concurrently
from notion.upload_page import upload_page, upload_page_concurrently
from notion.create_page import create_page
from notion.find_relation import find_destination, find_operator

# Define mapping for trends and values
trend_mapping = {
    'Increase': lambda price_difference: price_difference > 0,
    'Decrease': lambda price_difference: price_difference < 0,
    'Neutral': lambda price_difference: price_difference == 0
}

value_mapping = {
    'Cheap': lambda value: value == 'Cheap',
    'Average': lambda value: value == 'Average',
    'Expensive': lambda value: value == 'Expensive',
    'Unknown': lambda value: value not in ['Cheap', 'Average', 'Expensive']
}

load_dotenv()  # Use context manager
notion = Client(auth=os.getenv('NOTION_KEY'))

flight_data = get_mails(int(sys.argv[1]) if len(sys.argv) > 1 else 10)

if not flight_data:
    log("No emails found", "warning")

fetch_databases_concurrently(notion, [os.getenv('NOTION_DB_TRAVEL'), os.getenv(
    'NOTION_DB_OPERATOR'), os.getenv('NOTION_DB_DESTINATION')])

for mail in flight_data:

    if not mail:
        log("No emails found", "danger")
        continue

    for trip in mail:
        operators = [{"id": operator} for airline in trip.get("Airlines", [])
                     for operator in find_operator(notion, airline) or []]

        destination_name = trip.get("Journey").split(" til ")[1]
        destinations = [{"id": dest}
                        for dest in find_destination(notion, destination_name) or []]

        # Get trend-arrow
        price_difference = trip.get("New Price", 0) - trip.get("Old Price", 0)
        trend = [next(({"id": find_operator(notion, trend_name)[0]}
                      for trend_name, condition in trend_mapping.items() if condition(price_difference)), None)]

        # Get value indicator
        value = [next(({"id": find_operator(notion, value_name)[0]}
                      for value_name, condition in value_mapping.items() if condition(trip.get("Value", ""))), None)]

        if trip.get("Old Price") == trip.get("New Price"):
            trend = value

        page = create_page(
            journey=trip.get("Journey"),
            route=trip.get("Route"),
            old_price=trip.get("Old Price"),
            new_price=trip.get("New Price"),
            duration=trip.get("Duration"),
            connections=trip.get("Connections"),
            start_date=trip.get("Start Date"),
            end_date=trip.get("End Date"),
            cabin=trip.get("Cabin"),
            type=trip.get("Type"),
            operator=operators,
            destination=destinations,
            trend=trend
        )

        upload_page_concurrently(notion, page)
