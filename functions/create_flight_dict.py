
from functions.console import log


def create_flight_dict(journey, start, end, cabin, new_price, duration, airlines: list, connections, route, type, value, old_price=0):

    if not isinstance(airlines, list):
        log("airlines is not a list", "danger")
        airlines = [airlines]

    print("airlines: ", airlines)
    for airline in airlines:
        print("testing", airline)
        if len(airline) < 3:
            log("airline is not a string", "danger")
            airlines.remove(airline)

    flight_dict = {
        "Journey": journey,         # "Oslo til London"
        "Start Date": start,        # "2021-10-01"
        "End Date": end,            # "2021-10-01"
        "Cabin": cabin,             # "Economy"
        "New Price": new_price,     # 1234
        "Old Price": old_price,     # 1234
        "Duration": duration,       # "22t"
        "Airlines": airlines,       # ["SAS", "Norwegian"]
        "Connections": connections,  # 1
        "Route": route,             # "OSL-LHR"
        "Type": type,               # "Specific" or "Non-Specific"
        "Value": value,             # "Cheap" "Average" "Expensive"
    }
    return flight_dict
