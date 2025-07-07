from typing import Dict, List, Optional

from microservice.services import database


def create_item(name: str, description: Optional[str] = None) -> Dict[str, Optional[int or str]]:
    item_id = database.add_item(name, description)

    item = {
        "id": item_id,
        "name": name,
        "description": description,
    }

    return item


def get_all_items() -> List[Dict[str, Optional[int or str]]]:
    try:
        items = database.list_items()
        return items
    except Exception as exc:
        return []
