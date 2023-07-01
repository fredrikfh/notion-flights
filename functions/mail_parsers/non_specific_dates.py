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

    journey = route

    metadata = text[0].split(" ·")
    cabin = metadata[-1]
    type = metadata[0].split(" ")[0]

    value = text[-1].split("kr")[1:]
    value = [int(i) for i in value]

    # remove first and last element
    text = text[1:-1]

    # loop through three elements at a time
    flight_list_dict = []
    for i in range(0, len(text), 3):
        date = parse_date(text[i])
        if "SPAR" in text[i+1]:
            text[i+1] = text[i+1][text[i+1].index("F"):]
        price = int(text[i+1][6:])
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
    if price < prices[0]:
        return "Cheap"
    elif price < prices[1]:
        return "Average"
    else:
        return "Expensive"
