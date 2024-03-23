from datetime import datetime
import os
import json
from typing import Dict, List, Optional
import uuid
from apis.datastore.service.interface import (
    Datastore,
    GroupSumResult,
    PaginatedResult,
    DatastoreEntityName,
)
from .query import OnDiskQuery
from .helpers import check_query_matches, CustomJSONEncoder


class OnDiskDatastore(Datastore):

    def __init__(self):
        self.collections = {}
        self.default_limit = 32
        self.data_dir = "ondiskdb_data"
        os.makedirs(self.data_dir, exist_ok=True)
        self._load_collections()

    async def add(self, collection: DatastoreEntityName,
                  document: Dict) -> str:
        if collection not in self.collections:
            self.collections[collection] = {}
        doc_id = str(uuid.uuid4())
        self.collections[collection][doc_id] = document
        self._save_collection(collection)
        return doc_id

    async def get_one(self, collection: DatastoreEntityName,
                      query: OnDiskQuery) -> Optional[Dict]:
        documents = self.collections.get(collection, {}).values()
        for doc in documents:
            if self._matches_query(doc, query):
                return doc
        return None

    async def get_many(self, collection: DatastoreEntityName,
                       query: OnDiskQuery) -> List[Dict]:
        documents = self.collections.get(collection, {}).values()
        return [doc for doc in documents if self._matches_query(doc, query)]

    async def get_paginated(self, collection: DatastoreEntityName,
                            query: OnDiskQuery) -> PaginatedResult:
        all_docs = await self.get_many(collection, query)
        limit = query.limit or self.default_limit
        offset = query.offset or 0
        page = offset // limit + 1
        total = len(all_docs)
        paginated_docs = all_docs[offset:offset + limit]
        return PaginatedResult(
            total=total,
            items=paginated_docs,
            page=page,
            pages=(total + limit - 1) // limit,
            page_size=limit,
        )

    async def count(self, collection: DatastoreEntityName,
                    query: OnDiskQuery) -> int:
        documents = self.collections.get(collection, {}).values()
        return sum(1 for doc in documents if self._matches_query(doc, query))

    async def sum(self, collection: DatastoreEntityName, field: str,
                  query: OnDiskQuery) -> float:
        documents = self.collections.get(collection, {}).values()
        return sum(doc[field] for doc in documents
                   if self._matches_query(doc, query))

    async def group_sum(
        self,
        collection: DatastoreEntityName,
        group_field: str,
        value_field: str,
        query: OnDiskQuery,
    ) -> List[GroupSumResult]:
        documents = self.collections.get(collection, {}).values()
        groups = {}
        for doc in documents:
            if self._matches_query(doc, query):
                group = doc[group_field]
                value = doc[value_field]
                if group not in groups:
                    groups[group] = {"total": 0, "count": 0}
                groups[group]["total"] += value
                groups[group]["count"] += 1
        return [
            GroupSumResult(
                group_field=group,
                value_field=value_field,
                total=groups[group]["total"],
                count=groups[group]["count"],
            ) for group in groups
        ]

    async def aggregate(self, collection: DatastoreEntityName,
                        query: OnDiskQuery, pipeline: List) -> List:
        raise NotImplementedError()

    async def update_one(self, collection: DatastoreEntityName,
                         query: OnDiskQuery,
                         update_values: Dict) -> Optional[Dict]:
        documents = self.collections.get(collection, {})
        for doc_id, doc in documents.items():
            if self._matches_query(doc, query):
                documents[doc_id].update(update_values)
                self._save_collection(collection)
                return documents[doc_id]
        return None

    async def update_many(self, collection: DatastoreEntityName,
                          query: OnDiskQuery,
                          update_values: Dict) -> List[Dict]:
        documents = self.collections.get(collection, {})
        updated = []
        for doc_id, doc in documents.items():
            if self._matches_query(doc, query):
                documents[doc_id].update(update_values)
                updated.append(documents[doc_id])
        self._save_collection(collection)
        return updated

    async def delete_many(self, collection: DatastoreEntityName,
                          query: OnDiskQuery) -> int:
        documents = self.collections.get(collection, {})
        initial_count = len(documents)
        self.collections[collection] = {
            doc_id: doc
            for doc_id, doc in documents.items()
            if not self._matches_query(doc, query)
        }
        self._save_collection(collection)
        return initial_count - len(self.collections[collection])

    async def delete_one(self, collection: DatastoreEntityName,
                         query: OnDiskQuery) -> bool:
        documents = self.collections.get(collection, {})
        for doc_id, doc in documents.items():
            if self._matches_query(doc, query):
                del documents[doc_id]
                self._save_collection(collection)
                return True
        return False

    def get_query_builder(self) -> OnDiskQuery:
        return OnDiskQuery()

    def _matches_query(self, doc: Dict, query: OnDiskQuery) -> bool:
        query_data = query.build()
        return check_query_matches(doc, query_data)

    def _load_collections(self):
        for collection_file in os.listdir(self.data_dir):
            if collection_file.endswith(".json"):
                collection_name = collection_file[:
                                                  -5]  # Remove '.json' extension
                file_path = os.path.join(self.data_dir, collection_file)

                # Check if the file is empty
                if os.path.getsize(file_path) == 0:
                    self.collections[collection_name] = {}
                    continue

                with open(file_path, "r") as f:
                    try:
                        self.collections[collection_name] = json.load(f)
                    except json.JSONDecodeError:
                        # Handle the case where the JSON is not properly formatted
                        print(
                            f"""Warning: Could not decode JSON from {collection_file}. 
                            Initializing as empty collection.
                            """)
                        self.collections[collection_name] = {}

    def _save_collection(self, collection: str):
        collection_path = os.path.join(self.data_dir, collection + ".json")
        with open(collection_path, "w") as f:
            json.dump(self.collections[collection], f, cls=CustomJSONEncoder)

    def reset_db(self):
        for collection in self.collections:
            self.collections[collection] = {}
            self._save_collection(collection)
        self.collections = {}
        self._load_collections()
        return True
