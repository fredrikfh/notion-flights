
import re
from functions.console import log
from functions.create_flight_dict import create_flight_dict
from functions.parse_date import parse_date


def specific_flights(text):
    """To be used if tracking specific flights (carrier and date)"""

    text = remove_unwanted_elements(text)

    metadata = text[0].split(" ·")
    flights = text[1:]

    structured_metadata = transform_string(metadata[0])

    flights_arr = [transform(entry) for entry in flights]
    tracked_flight = flights_arr.pop(0)

    old_price = tracked_flight[-1]
    datearr = metadata[0].split(".")

    datearr = metadata[0].split(".")
    journey = datearr[0][0:-3]

    if len(datearr) >= 5:
        date = datearr[0][-3:] + "." + datearr[1] + \
            "." + datearr[2] + "." + datearr[3] + "." + \
            datearr[4].replace("Tur/retur", "")
    elif len(datearr) == 4:  # adjust as necessary
        date = datearr[0][-3:] + "." + datearr[1] + \
            "." + datearr[2] + "." + datearr[3]
    else:
        # Handle other cases or raise an error if unexpected
        raise ValueError(f"Unexpected date format: {metadata[0]}")

    date = structured_metadata[1]

    # ons. 2. apr.-ons. 2. sep.
    date = parse_date(date)

    flight_list_dict = []

    for flight in flights_arr:
        if len(flight) != 4:
            log("Unknown flight format", "danger")
            continue

        hours = flight[0]
        airlines = flight[1]
        stops = flight[2].split(" ")[0]
        price = flight[3]

        if stops == "Direkte":
            stops = 0
        stops = int(stops)

        flight_list_dict.append(create_flight_dict(
            journey=journey,
            start=date[0],
            end=date[1],
            cabin="Unknown",
            new_price=int(price),
            old_price=-1,
            duration=hours,
            airlines=airlines,
            connections=stops,
            route="TODO",
            type="Specific",
            value="Unknown"
        ))

    return flight_list_dict


def transform(entry):
    # Extracting time
    time = re.search(r'(\d{2}:\d{2} – \d{2}:\d{2})', entry).group(1)

    # Splitting data by "·"
    parts = entry.split('·')

    # Extracting airline
    airline = parts[0].replace(time, '').strip()

    # Extracting other details
    details = [part for part in parts[1:-1]]

    # Extracting prices
    prices = re.findall(r'kr(\d+)', entry)
    prices = [int(price) for price in prices]

    return [time, airline] + details + prices


def remove_unwanted_elements(array):
    unwanted_elements = ["Flyreisen du sporer",
                         "Alternative flyreiser", "Vis flere flyreiser"]

    for element in array:
        if element in unwanted_elements:
            array.remove(element)
    return array
    # return [[item for item in sublist if item not in unwanted_elements] for sublist in array]


def transform_string(s):

    # 'Oslo til Milanolør. 7. okt.–tor. 12. okt.Tur/retur'
    # transformed to:
    # ['Oslo til Milano', 'lør 7. okt.–tor. 12. okt.', 'Tur/retur']

    # 1. Extract the destination part (e.g., "Oslo til Milano")
    destination = re.match(r'\w+ til \w+', s).group()

    # 2. Extract the date range (e.g., "lør. 7. okt.–tor. 12. okt.")
    date_range_pattern = r'\w{3}\. \d{1,2}\. \w{3}\.–\w{3}\. \d{1,2}\. \w{3}\.'
    date_range = re.search(date_range_pattern, s)
    if date_range:
        date_range = date_range.group()
    else:
        # If the pattern is not found, handle the error or return the original string
        date_range = s

    # 3. The rest of the string (e.g., "Tur/retur")
    rest = s.replace(destination, '').replace(date_range, '').strip()

    return [destination, date_range, rest]
