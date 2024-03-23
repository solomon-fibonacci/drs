template = """
from typing import List
from models import YourModel
from database import DatabaseSession

class YourService:
@staticmethod
async def create_item(item: YourModel) -> YourModel:
    # Implementation for creating an item
    pass

@staticmethod
async def get_items() -> List[YourModel]:
    # Implementation for getting all items
    pass

@staticmethod
async def get_item_by_id(item_id: str) -> YourModel:
    # Implementation for getting a specific item by ID
    pass

@staticmethod
async def update_item(item_id: str, item_update: YourModel) -> YourModel:
    # Implementation for updating an item
    pass

@staticmethod
async def delete_item(item_id: str) -> None:
    # Implementation for deleting an item
    pass
"""
