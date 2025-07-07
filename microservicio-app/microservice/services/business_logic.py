from typing import Dict, List, Optional

from microservice.services import database


def create_note(name: str, description: Optional[str] = None) -> Dict[str, Optional[int or str]]:
    item_id = database.add_note(name, description)

    item = {
        "id": item_id,
        "name": name,
        "description": description,
    }

    return item


def get_all_notes() -> List[Dict[str, Optional[int or str]]]:
    try:
        notes = database.list_notes()
        return notes
    except Exception as exc:
        return []
