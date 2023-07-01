import concurrent.futures
import sys
import threading
import time

import cachetools
from notion_client import Client

from functions.console import log

# Global variables
cache = cachetools.TTLCache(maxsize=200, ttl=600)
fetch_lock = threading.Lock()


def fetch_data(notion: Client, database_id: str, filter_params=None):
    """Fetch data from Notion API."""
    all_data = []
    has_more = True
    start_cursor = None

    while has_more:
        database_data = notion.databases.query(
            database_id, filter=filter_params, start_cursor=start_cursor, page_size=100)

        all_data.extend(database_data["results"])

        if "next_cursor" in database_data and database_data["next_cursor"]:
            log("fetching...", "info")
            start_cursor = database_data["next_cursor"]
        else:
            has_more = False

    return {"results": all_data}


def get_database_data(notion: Client, database_id: str, filter_params=None) -> dict:
    """
    Get data from the cache. If not available, fetch it from Notion API.

    Args:
    notion: notion_client.Client instance.
    database_id: Notion database id.
    filter_params: Filter parameters for the notion query (default is None).

    Returns:
    A dictionary containing the fetched data.
    """
    cache_key = f"{database_id}"
    while True:
        try:
            # If the data is in the cache, return it
            return cache[cache_key]
        except KeyError:
            # Try to acquire the lock to fetch data from Notion API
            # with fetch_lock:
            # Check the cache again after acquiring the lock
            if cache_key in cache:
                return cache[cache_key]

            # If the data is not in the cache, fetch it and store it in the cache
            log("Fetching data from Notion API...", "info")
            try:
                data = fetch_data(
                    notion, database_id, filter_params)
                cache[cache_key] = data
            except Exception:
                log("Unable to access database (make sure to add connections in notion)", "danger")
                sys.exit(1)

            return cache[cache_key]
            # wait 1-5 seconds and try again
            # time.sleep(int(time.time()) % 5 + 1)


def destroy_cache(key: str):
    """
    Destroy the cache for a specific key.

    Args:
    key: The key to be destroyed.

    Returns:
    None
    """
    try:
        del cache[key]
        log(f"Cache destroyed: {key}", "warning")
    except KeyError:
        pass


def fetch_databases_concurrently(notion, database_ids, filter_params=None):
    """
    Fetch data from three databases concurrently.

    Args:
    notion: notion_client.Client instance.
    database_ids: A list of Notion database ids.
    filter_params: Filter parameters for the notion query (default is None).

    Returns:
    A list of dictionaries, each containing the fetched data for a database.
    """
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_database = {executor.submit(
            get_database_data, notion, db_id, filter_params): db_id for db_id in database_ids}

        for future in concurrent.futures.as_completed(future_to_database):
            db_id = future_to_database[future]
            try:
                data = future.result()
                log(f"Fetched data for database: {db_id}", "info")
            except Exception as exc:
                log(
                    f'An exception occurred while fetching database: {db_id} - {exc}', "danger")

    return [future.result() for future in concurrent.futures.as_completed(future_to_database)]
