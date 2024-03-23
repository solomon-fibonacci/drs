from typing import Any, Dict, List, Optional
from pymongo import ASCENDING, DESCENDING
from apis.datastore.utils import SortOrder
from apis.datastore.service.interface import (
    Operator,
    LogicalOperator,
    Query,
    JoinType,
    DatastoreEntityName,
)


class MongoOperator(Operator):

    def equals(self, operand: Any) -> Dict:
        return {"$eq": operand}

    def not_equal(self, operand: Any) -> Dict:
        return {"$ne": operand}

    def greater_than(self, operand: Any) -> Dict:
        return {"$gt": operand}

    def less_than(self, operand: Any) -> Dict:
        return {"$lt": operand}

    def greater_than_or_equal(self, operand: Any) -> Dict:
        return {"$gte": operand}

    def less_than_or_equal(self, operand: Any) -> Dict:
        return {"$lte": operand}

    def is_in(self, operand: Any) -> Dict:
        return {"$in": operand}

    def not_in(self, operand: Any) -> Dict:
        return {"$nin": operand}

    def like(self, operand: Any) -> Dict:
        return {"$regex": operand}

    def starts_with(self, operand: Any) -> Dict:
        return {"$regex": f"^{operand}"}

    def ends_with(self, operand: Any) -> Dict:
        return {"$regex": f"{operand}$"}

    def regex_match(self, operand: Any) -> Dict:
        return {"$regex": operand}

    def value_in_range(self, operand: Any) -> Dict:
        # single value field is in range
        return {"$gte": operand[0], "$lte": operand[1]}

    def range_contains(self, operand: Any) -> Dict:
        # array field has at least one value in range
        return {"$elemMatch": {"$gte": operand[0], "$lte": operand[1]}}

    def contains(self, operand: Any) -> Dict:
        return {"$elemMatch": {"$eq": operand}}

    def contains_doc(self, sub_query: Query) -> Dict:
        operand = sub_query.build()
        sub_doc_match_clause = operand[0]["$match"]
        return {"$elemMatch": sub_doc_match_clause}

    def excludes(self, operand: Any) -> Dict:
        return {"$not": {"$elemMatch": {"$eq": operand}}}

    def has_substring(self, operand: Any) -> Dict:
        return {"$regex": operand}


class MongoDBQuery(Query):

    def __init__(self):
        self.filters = {"$and": [], "$or": []}
        self.sorts = []
        self.limit = None
        self.offset = 0
        self.joins = []
        self.operator = self.ops()

    def ops(self) -> Operator:
        return MongoOperator()

    def filter(
        self,
        field: str,
        statement: Dict,
        logical_op: LogicalOperator = LogicalOperator.AND,
    ) -> Query:
        if logical_op == LogicalOperator.AND:
            self.filters["$and"].append({field: statement})
        elif logical_op == LogicalOperator.OR:
            self.filters["$or"].append({field: statement})
        return self

    def join(
        self,
        collection: DatastoreEntityName,
        local_field: str,
        foreign_field: str,
        alias: Optional[str] = None,
        join_type: JoinType = JoinType.INNER,
    ) -> Query:
        if join_type != JoinType.INNER:
            raise NotImplementedError(
                "MongoDB only supports inner joins using $lookup.")
        join = {
            "from": collection,
            "localField": local_field,
            "foreignField": foreign_field,
            "as": alias or collection,
        }
        self.joins.append({"$lookup": join})
        return self

    def sort_by(self,
                field: str,
                direction: SortOrder = SortOrder.ASCENDING) -> Query:
        dir = ASCENDING if direction == SortOrder.ASCENDING else DESCENDING
        self.sorts.append((field, dir))
        return self

    def set_limit(self, limit: int) -> Query:
        self.limit = limit
        return self

    def set_offset(self, offset: int) -> Query:
        self.offset = offset
        return self

    def build(self) -> List[Dict[str, Any]]:
        query = []

        # Handle filter conditions
        if self.filters["$and"] or self.filters["$or"]:
            match_conditions = {
                key: value
                for key, value in self.filters.items() if value
            }
            query.append({"$match": match_conditions})
        else:
            query.append({"$match": {}})

        # Handle joins (lookup)
        for join in self.joins:
            query.append(join)

        # Handle sorting
        if self.sorts:
            sort_stage = {"$sort": dict(self.sorts)}
            query.append(sort_stage)

        # Handle offset (skip)
        if self.offset is not None:
            skip_stage = {"$skip": self.offset}
            query.append(skip_stage)

        # Handle limit
        if self.limit is not None:
            limit_stage = {"$limit": self.limit}
            query.append(limit_stage)

        return query
