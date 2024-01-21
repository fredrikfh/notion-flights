import datetime
from babel.dates import get_month_names

# Create a dictionary to map Norwegian month names to numbers
months_no_wide = get_month_names('wide', locale='no')
months_no_abbr = get_month_names('abbreviated', locale='no')

month_to_num = {name.lower(): i for i, name in months_no_wide.items() if name}
month_to_num.update(
    {name.lower().replace('.', ''): i for i, name in months_no_abbr.items() if name})

month_to_num.update(
    {name.lower() + '.': i for i, name in months_no_abbr.items() if name})


def is_valid_date(year, month, day):
    """Check if a given date is valid."""
    try:
        datetime.date(year, month, day)
        return True
    except ValueError:
        return False


def extract_date(date_string, current_year):
    """Extract a date from a string."""
    day_month = date_string.split('.', 1)[1].strip().split(' ')
    if len(day_month) != 2:
        print(
            f"WARNING: Invalid date string format: '{date_string}'. Using None.")
        return None
    day, month = day_month
    day_int = int(day.replace(".", ""))
    month_key = month.lower().rstrip('.')
    if month_key in month_to_num and is_valid_date(current_year, month_to_num[month_key], day_int):
        return datetime.date(current_year, month_to_num[month_key], day_int).isoformat()
    else:
        print(
            f"WARNING: Invalid date: {day}.{month}.{current_year}. Using None.")
        return None


def parse_date(date_string: str):
    start_date_string, end_date_string = date_string.split('–')
    current_year = datetime.datetime.now().year
    start_date_iso = extract_date(start_date_string, current_year)
    end_date_iso = extract_date(end_date_string, current_year)
    return [start_date_iso, end_date_iso]
