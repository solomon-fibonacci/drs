from typing import Any, Dict, List, Optional
import logging
from pymongo.collection import ReturnDocument
from motor.motor_asyncio import AsyncIOMotorClient

from .query import MongoDBQuery
from apis.datastore.service.interface import (
    Datastore,
    PaginatedResult,
    DatastoreEntityName,
    GroupSumResult,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MongoDBDatastore(Datastore):

    def __init__(self, uri: str, dbname: str, cert_file: Optional[str] = None):
        kwargs: Dict = {}
        if cert_file:
            kwargs["tlsCAFile"] = cert_file

        self.client = AsyncIOMotorClient(uri, **kwargs)
        self.db = self.client[dbname]
        self.default_limit = 32

    async def add(self, collection: DatastoreEntityName,
                  document: Dict) -> str:
        result = await self.db[collection].insert_one(document)
        return str(result.inserted_id)

    async def get_one(self, collection: DatastoreEntityName,
                      query: MongoDBQuery) -> Optional[Dict]:
        query_pipeline = query.build()
        result = await self.db[collection].aggregate(query_pipeline).to_list(1)
        return result[0] if result else None

    async def get_many(self, collection: DatastoreEntityName,
                       query: MongoDBQuery) -> List[Dict]:
        query_pipeline = query.build()
        result = (await self.db[collection].aggregate(query_pipeline).to_list(
            query.limit or self.default_limit))
        return result

    async def get_paginated(self, collection: DatastoreEntityName,
                            query: MongoDBQuery) -> PaginatedResult:
        # Build the aggregation pipeline from the query object, including pagination
        query_pipeline = query.build()
        logger.info(f"Query pipeline for get_paginated: {query_pipeline}")
        # To get the total count, we need a count pipeline without the limit and skip stages
        count_pipeline = [
            stage for stage in query_pipeline
            if "$limit" not in stage and "$skip" not in stage
        ]
        count_pipeline.append({"$count": "total"})
        total_count = await self.db[collection].aggregate(count_pipeline
                                                          ).to_list(1)
        total = total_count[0]["total"] if total_count else 0

        # Execute the final query with pagination
        cursor = self.db[collection].aggregate(query_pipeline)
        limit = query.limit or self.default_limit
        items = await cursor.to_list(limit)
        # Calculate pagination details
        pages = (total + limit - 1) // limit if limit else 1
        current_page = (query.offset // limit + 1) if limit else 1

        return PaginatedResult(total=total,
                               items=items,
                               page=current_page,
                               pages=pages,
                               page_size=limit)

    async def count(self, collection: DatastoreEntityName,
                    query: MongoDBQuery) -> int:
        query_pipeline = query.build()
        count_pipeline = query_pipeline + [{"$count": "total"}]
        result = await self.db[collection].aggregate(count_pipeline).to_list(1)
        return result[0]["total"] if result else 0

    async def sum(
        self,
        collection: DatastoreEntityName,
        field: str,
        query: MongoDBQuery,
    ) -> float:
        query_pipeline = query.build()
        sum_pipeline = query_pipeline + [{
            "$group": {
                "_id": None,
                "total": {
                    "$sum": f"${field}"
                }
            }
        }]
        result = await self.db[collection].aggregate(sum_pipeline).to_list(1)
        return result[0]["total"] if result else 0

    async def group_sum(
        self,
        collection: DatastoreEntityName,
        group_field: str,
        value_field: str,
        query: MongoDBQuery,
    ) -> List[GroupSumResult]:
        query_pipeline = query.build()
        group_sum_pipeline = query_pipeline + [{
            "$group": {
                "_id": f"${group_field}",
                "total": {
                    "$sum": f"${value_field}"
                },
                "count": {
                    "$sum": 1
                },
            }
        }]
        result = await self.db[collection].aggregate(group_sum_pipeline
                                                     ).to_list(1000)
        return [
            GroupSumResult(
                group_field=entry["_id"],
                value_field=value_field,
                total=entry["total"],
                count=entry["count"],
            ) for entry in result
        ]

    async def aggregate(self, collection: DatastoreEntityName,
                        query: MongoDBQuery, pipeline: List) -> List:
        raise NotImplementedError(
            "Aggregations have not yet been implemented for MongoDB.")

    async def update_one(self, collection: DatastoreEntityName,
                         query: MongoDBQuery, update_values: Dict) -> Dict:
        match_clause = self._get_match_clause(query)
        result = await self.db[collection].find_one_and_update(
            match_clause,
            {"$set": update_values},
            return_document=ReturnDocument.AFTER,
        )
        return result

    async def update_many(self, collection: DatastoreEntityName,
                          query: MongoDBQuery,
                          update_values: Dict) -> List[Dict]:
        match_clause = self._get_match_clause(query)
        await self.db[collection].update_many(match_clause,
                                              {"$set": update_values})
        return await self.get_many(collection, MongoDBQuery())

    async def delete_many(self, collection: DatastoreEntityName,
                          query: MongoDBQuery) -> int:
        match_clause = self._get_match_clause(query)
        result = await self.db[collection].delete_many(match_clause)
        return result.deleted_count

    async def delete_one(self, collection: DatastoreEntityName,
                         query: MongoDBQuery) -> bool:
        match_clause = self._get_match_clause(query)
        result = await self.db[collection].delete_one(match_clause)
        return result.deleted_count > 0

    def get_query_builder(self) -> MongoDBQuery:
        return MongoDBQuery()

    def _get_match_clause(self, query: MongoDBQuery) -> Dict:
        query_pipeline = query.build()
        match_clause = query_pipeline.pop(0)["$match"]
        return match_clause
