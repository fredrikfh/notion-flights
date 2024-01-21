import quopri
import re
from functions.console import log
from functions.create_flight_dict import create_flight_dict

from functions.parse_date import parse_date


def specific_dates(text):

    # for i in range(len(text)):
    #     print("TOT"+str(i)+": ", text[i])

    flight_list_dict = []
    for i in range(0, len(text), 4):
        # print(i, text)

        metadata = text[i].split(" ·")

        old_price = get_prices_from_string(metadata[-1])[0]
        # new_price = get_prices_from_string(metadata[-1])[1]

        datearr = metadata[0].split(".")
        journey = datearr[0][0:-3]
        date = datearr[0][-3:] + "." + datearr[1] + \
            "." + datearr[2] + "." + datearr[3] + "." + \
            datearr[4].replace("Tur/retur", "")

        if len(date) < len("ons. 2. apr.-ons. 2. sep."):
            date = datearr[0][-3:] + "." + datearr[1] + \
                "." + datearr[2] + "." + datearr[3] + "." + \
                datearr[4] + "." + datearr[5] + "."

        # ons. 2. apr.-ons. 2. sep.
        date = parse_date(date)

        # loop three times
        for j in range(3):
            flight = text[i+j+1]
            # print("FLIGHT-"+str(j)+": ", flight)

            hours = None
            if flight[13:15] == "+1":
                hours = flight[0:15]
                flight = flight[15:]

            else:
                hours = flight[0:13]
                flight = flight[13:]

            flight = flight.split(" ·")
            # print("FLIGHT-"+str(j)+": ", flight)

            airlines = flight[0].split(", ")
            stops = flight[1].split(" ")[0]
            if stops == "Direkte":
                stops = 0
            stops = int(stops)
            if len(flight) == 3:
                route_and_price = extract_flight_info(flight[2])
                # print("ROUTE AND PRICE: ", route_and_price)
                route = route_and_price[0]
                price = route_and_price[1]

            else:
                log("Unknown flight format", "danger")
                continue

            flight_list_dict.append(create_flight_dict(
                journey=journey,
                start=date[0],
                end=date[1],
                cabin="Unknown",
                new_price=int(price),
                old_price=old_price,
                duration=hours,
                airlines=airlines,
                connections=stops,
                route=route,
                type="Specific",
                value="Unknown"
            ))

    return flight_list_dict


def get_prices_from_string(string: str):
    # transforms 1 voksen4654kr4377kr into [4654, 4377]
    prices = re.findall(r'\d+(?=kr)', string)
    # Converting the found strings to integers
    prices = [int(price) for price in prices]

    return prices


def extract_flight_info(flight_string):
    # Extracts OSL–PDL4654kr into [OSL–PDL, 4654]
    # Extracting the airport codes
    airport_codes = re.search(r'[A-Z]{3}–[A-Z]{3}', flight_string)
    if airport_codes:
        airport_codes = airport_codes.group()
    else:
        airport_codes = None

    # Extracting the price
    price = re.search(r'\d+', flight_string)
    if price:
        price = int(price.group())
    else:
        price = 0

    return [airport_codes, price]
