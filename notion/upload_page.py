from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import os

from functions.console import log
from notion.page_exists import page_exists
from notion_client import Client

# Load environment variable
NOTION_DB_TRAVEL = os.getenv("NOTION_DB_TRAVEL")


def upload_page(notion: Client, page: dict) -> None:
    """
    Create a new Notion database record.

    Args:
    notion: Notion client instance.
    page: Page data to be added to the Notion database.

    Returns:
    None
    """
    # check if page already exists in Notion
    if page_exists(notion, page):
        log("duplicate, skipping...", "warning")
        return

    try:
        log(f"Sending page to Notion...", "success")
        notion.pages.create(
            parent={"database_id": os.getenv("NOTION_DB_TRAVEL")}, properties=page)
    except Exception as e:
        log(f"Failed to create record: {e}", "danger")


if os.getenv("NOTION_PREMIUM") == "true":
    executor = ThreadPoolExecutor(max_workers=10)
else:
    executor = ThreadPoolExecutor(max_workers=1)


def upload_page_concurrently(notion: Client, page: dict):
    """
    Submit the function to be executed asynchronously in the background.

    Args:
    notion: Notion client instance.
    page: Page data to be added to the Notion database.

    Returns:
    concurrent.futures.Future: Future object that represents a computation 
    that hasn't necessarily completed yet.
    """
    future = executor.submit(upload_page, notion, page)
    return future
