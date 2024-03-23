import re
from typing import Any, Callable, Dict, Optional
from apis.datastore.service.interface import LogicalOperator, Query, JoinType

from typing import List, Dict, Any, Optional
from apis.datastore.service.interface import (
    Query,
    LogicalOperator,
    Operator,
    SortOrder,
    JoinType,
    DatastoreEntityName,
)
from .helpers import check_query_matches


class DiskDbOperator(Operator):

    def equals(self, operand: Any) -> Callable[[Any, Any], bool]:
        return lambda field, doc: field in doc and doc[field] == operand

    def not_equal(self, operand: Any) -> Callable[[Any, Any], bool]:
        return lambda field, doc: field not in doc or doc[field] != operand

    def greater_than(self, operand: Any) -> Callable[[Any, Any], bool]:
        return lambda field, doc: field in doc and doc[field] > operand

    def less_than(self, operand: Any) -> Callable[[Any, Any], bool]:
        return lambda field, doc: field in doc and doc[field] < operand

    def greater_than_or_equal(self,
                              operand: Any) -> Callable[[Any, Any], bool]:
        return lambda field, doc: field in doc and doc[field] >= operand

    def less_than_or_equal(self, operand: Any) -> Callable[[Any, Any], bool]:
        return lambda field, doc: field in doc and doc[field] <= operand

    def is_in(self, operand: Any) -> Callable[[Any, Any], bool]:
        return lambda field, doc: field in doc and doc[field] in operand

    def not_in(self, operand: Any) -> Callable[[Any, Any], bool]:
        return lambda field, doc: doc[field] not in operand

    def like(self, operand: Any) -> Callable[[Any, Any], bool]:
        return lambda field, doc: field in doc and re.match(
            operand, doc[field])

    def starts_with(self, operand: Any) -> Callable[[Any, Any], bool]:
        return lambda field, doc: field in doc and doc[field].startswith(
            operand)

    def ends_with(self, operand: Any) -> Callable[[Any, Any], bool]:
        return lambda field, doc: field in doc and doc[field].endswith(operand)

    def regex_match(self, operand: Any) -> Callable[[Any, Any], bool]:
        return lambda field, doc: field in doc and re.match(
            operand, doc[field])

    def value_in_range(self, operand: Any) -> Callable[[Any, Any], bool]:
        # single value field is in range
        return (lambda field, doc: field in doc and operand[0] <= doc[field] <=
                operand[1])

    def range_contains(self, operand: Any) -> Callable[[Any, Any], bool]:
        # array field has at least one value in range
        return lambda field, doc: field in doc and any(
            operand[0] <= value <= operand[1] for value in doc[field])

    def contains(self, operand: Any) -> Callable[[Any, Any], bool]:
        return lambda field, doc: field in doc and operand in doc[field]

    def contains_doc(self, sub_query: Query) -> Callable[[Any, Any], bool]:
        sub_doc_query = sub_query.build()
        return lambda field, doc: field in doc and any(
            check_query_matches(sub_doc, sub_doc_query)
            for sub_doc in doc[field])

    def excludes(self, operand: Any) -> Callable[[Any, Any], bool]:
        return lambda field, doc: field in doc and operand not in doc[field]

    def has_substring(self, operand: Any) -> Callable[[Any, Any], bool]:
        return lambda field, doc: field in doc and operand in doc[field]


class OnDiskQuery(Query):

    def __init__(self):
        self.conditions = {}
        self.joins = []
        self.sort_fields = []
        self.limit = None
        self.offset = None

    def ops(self) -> DiskDbOperator:
        return DiskDbOperator()

    def filter(
        self,
        field: str,
        statement: Callable[[Any, Any], bool],
        logical_op: LogicalOperator = LogicalOperator.AND,
    ) -> "Query":
        if logical_op == LogicalOperator.AND:
            self.conditions.setdefault("$$", []).append({field: statement})
        elif logical_op == LogicalOperator.OR:
            self.conditions.setdefault("||", []).append({field: statement})
        return self

    def join(
        self,
        collection: DatastoreEntityName,
        local_field: str,
        foreign_field: str,
        alias: Optional[str] = None,
        join_type: JoinType = JoinType.INNER,
    ) -> "Query":
        self.joins.append({
            "collection": collection,
            "local_field": local_field,
            "foreign_field": foreign_field,
            "alias": alias,
            "join_type": join_type,
        })
        return self

    def sort_by(self,
                field: str,
                direction: SortOrder = SortOrder.ASCENDING) -> "Query":
        self.sort_fields.append({"field": field, "direction": direction})
        return self

    def set_limit(self, limit: int) -> "Query":
        self.limit = limit
        return self

    def set_offset(self, offset: int) -> "Query":
        self.offset = offset
        return self

    def build(self) -> Dict:
        query_data = {}
        if self.conditions:
            query_data["conditions"] = self.conditions
        if self.joins:
            query_data["joins"] = self.joins
        if self.sort_fields:
            query_data["sort"] = self.sort_fields
        if self.limit is not None:
            query_data["limit"] = self.limit
        if self.offset is not None:
            query_data["offset"] = self.offset
        return query_data
