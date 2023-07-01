import os
from notion.cache import get_database_data

from functions.console import log


def page_exists(notion, page) -> bool:

    existing_record = False
    data = get_database_data(notion, os.getenv("NOTION_DB_TRAVEL"))

    for page_record in data["results"]:

        page_record_route = page_record["properties"]["Route"]["title"][0]["text"]["content"]
        page_record_old_price = page_record["properties"]["Old price"]["number"]
        page_record_new_price = page_record["properties"]["New price"]["number"]

        page_route = page["Route"]["title"][0]["text"]["content"]
        page_old_price = page["Old price"]["number"]
        page_new_price = page["New price"]["number"]

        identical_route = page_record_route == page_route
        identical_new_price = page_old_price == page_record_old_price
        identical_old_price = page_new_price == page_record_new_price

        if identical_route and identical_new_price and identical_old_price:
            existing_record = True
            break

    return existing_record
