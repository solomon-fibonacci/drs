from typing import List
from models import EventModel
from database import DatabaseSession

class EventService:
    @staticmethod
    async def create_item(item: EventModel) -> EventModel:
        new_item = EventModel(**item.dict())
        await DatabaseSession.async_save(new_item)
        return new_item

    @staticmethod
    async def get_items() -> List[EventModel]:
        return await DatabaseSession.async_get_all(EventModel)

    @staticmethod
    async def get_item_by_id(item_id: str) -> EventModel:
        return await DatabaseSession.async_get(EventModel, item_id)

    @staticmethod
    async def update_item(item_id: str, item_update: EventModel) -> EventModel:
        item = await EventService.get_item_by_id(item_id)
        updated_item = item.copy(update=item_update.dict(exclude_unset=True))
        await DatabaseSession.async_save(updated_item)
        return updated_item

    @staticmethod
    async def delete_item(item_id: str) -> None:
        item = await EventService.get_item_by_id(item_id)
        await DatabaseSession.async_delete(item)