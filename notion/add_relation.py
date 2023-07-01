from typing import Any, Dict
from notion_client import Client
from notion.find_relation import find_operator
from functions.console import log


def add_relation(notion: Client,
                 page: Dict[str,
                            Any],
                 page_property: str,
                 relation_name: str) -> Dict[str,
                                             Any]:
    """
    Adds a relation (another record) on the record's property.

    Args:
    notion: notion_client.Client instance.
    page: The notion page/record to modify.
    page_property: The column-name 
    relation: The name of the relative page.

    Returns:
    record: Updated record with the new relation added.
    """
    operator = find_operator(notion, relation_name)
    if operator:
        page[page_property] = {"relation": [{"id": operator[0]}]}
    else:
        # Consider logging or raising an exception here.
        log(f"Unable to find relation '{relation_name}'.", "warning")

    return page
