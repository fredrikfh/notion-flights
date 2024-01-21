import quopri
import re
from functions.create_flight_dict import create_flight_dict
from functions.console import log
from itertools import groupby
from functions.get_html import get_data_from_html

from functions.parse_date import parse_date

from bs4 import BeautifulSoup


def non_specific_dates(text: str, route: str):

    # print dates with enumeration
    # for i in range(len(text)):
    #     print(i, text[i])

    # print(text)

    journey = route

    metadata = text[0].split(" ·")
    cabin = metadata[-1]
    type = metadata[0].split(" ")[0]

    print("val1: ", text[-1])
    value = extract_prices(text[-1])
    print("val2: ", value)

    # remove first element
    text = text[1:]

    # get the price range
    price_range = text[-1]
    numbers = re.findall(r'\d+', price_range)
    price_range = [int(num) for num in numbers]

    # remove last element
    text = text[:-1]

    # loop through three elements at a time
    flight_list_dict = []
    for i in range(0, len(text), 3):
        date = parse_date(text[i])

        if "SPAR" in text[i+1]:
            text[i+1] = text[i+1][text[i+1].index("F"):]

        price = int(get_numbers_from_string(text[i+1])[0])
        info = text[i+2].split(' ·')
        airlines = info[0].split(',')
        connections = info[1].split(" ")[0]
        if connections == "Direkte":
            connections = 0
        connections = int(connections)
        route = info[2]
        duration = info[3]

        flight_list_dict.append(create_flight_dict(
            journey=journey,
            start=date[0],
            end=date[1],
            cabin=cabin,
            new_price=price,
            old_price=price,
            duration=info[3],
            airlines=info[0].split(','),
            connections=connections,
            route=info[2],
            type=type,
            value=get_value(price, value)
        ))

    return flight_list_dict


def get_value(price: int, prices: list):
    if len(prices) < 2:
        return "Unknown"
    if price < prices[0]:
        return "Cheap"
    if price < prices[1]:
        return "Average"
    return "Expensive"


def get_numbers_from_string(string: str):
    return re.findall(r'\d+', string)


def extract_prices(text):
    # Find all occurrences of numbers in the string
    prices = re.findall(r'\d+', text)
    # Convert the found strings to integers
    return [int(price) for price in prices]
