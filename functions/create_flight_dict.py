
def create_flight_dict(journey, start, end, cabin, new_price, duration, airlines, connections, route, type, value, old_price=0):
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
