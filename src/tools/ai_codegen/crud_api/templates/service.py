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

# Make sure to replace "Implementation for ..." with the actual code for each method.
See some examples below:

    async def add_datasource(self, new_datasource: NewDataSourceRequest) -> str:
        datasource = DataSource(
            id=str(uuid.uuid4()),
            name=new_datasource.name,
            source_type=new_datasource.source_type,
            subscriptions=[],
            created_at=datetime.utcnow(),
        )
        existing_name = await self.datastore.get_one(
            self.db_collection,
            self.datastore.get_query_builder().filter("name", datasource.name),
        )
        if existing_name:
            raise ConflictError(f"Datasource {datasource.name} already exists")

        await self.datastore.add(self.db_collection, to_savable(datasource))
        return datasource.id

    async def get_datasources(
        self, page: int = 1, page_size: int = 0
    ) -> PaginatedResult[DataSource]:
        page_size = page_size or self.default_limit
        query = self.datastore.get_query_builder()
        query.sort_by("created_at", SortOrder.DESCENDING)
        query.set_limit(page_size)
        query.set_offset((page - 1) * page_size)
        result_data = await self.datastore.get_paginated(self.db_collection, query)
        result = PaginatedResult[DataSource](
            total=result_data.total,
            items=[],
            page=result_data.page,
            pages=result_data.pages,
            page_size=result_data.page_size,
        )
        result.items = [DataSource(**datasource) for datasource in result_data.items]
        logger.info(f"Found {len(result.items)} datasources")
        return result
"""
