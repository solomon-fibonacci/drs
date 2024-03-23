from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Callable, List, Dict, Any, Optional, Union, Tuple, TypeVar, Generic
from pydantic import BaseModel
from config import DatastoreEntityName
from apis.datastore.utils import SortOrder


QueryExpression = Union[str, Dict, Callable]


@dataclass
class GroupSumResult:
    """
    A dataclass representing the result of a group sum query.
    """

    group_field: str
    value_field: str
    total: float
    count: int


class Operator(ABC):
    @abstractmethod
    def equals(self, operand: Any) -> QueryExpression:
        pass

    @abstractmethod
    def not_equal(self, operand: Any) -> QueryExpression:
        pass

    @abstractmethod
    def greater_than(self, operand: Any) -> QueryExpression:
        pass

    @abstractmethod
    def less_than(self, operand: Any) -> QueryExpression:
        pass

    @abstractmethod
    def greater_than_or_equal(self, operand: Any) -> QueryExpression:
        pass

    @abstractmethod
    def less_than_or_equal(self, operand: Any) -> QueryExpression:
        pass

    @abstractmethod
    def is_in(self, operand: List[Any]) -> QueryExpression:
        """
        Checks if the field is in the operand.
        """
        pass

    @abstractmethod
    def not_in(self, operand: Any) -> QueryExpression:
        pass

    @abstractmethod
    def like(self, operand: Any) -> QueryExpression:
        pass

    @abstractmethod
    def starts_with(self, operand: Any) -> QueryExpression:
        pass

    @abstractmethod
    def ends_with(self, operand: Any) -> QueryExpression:
        pass

    @abstractmethod
    def regex_match(self, operand: Any) -> QueryExpression:
        pass

    @abstractmethod
    def value_in_range(self, operand: Tuple[Any, Any]) -> QueryExpression:
        pass

    @abstractmethod
    def range_contains(self, operand: Tuple[Any, Any]) -> QueryExpression:
        pass

    @abstractmethod
    def contains(self, operand: Any) -> QueryExpression:
        """
        Checks if the operand is contained in the field.
        """
        pass
    @abstractmethod
    def contains_doc(self, sub_query: "Query") -> QueryExpression:
        """
        Checks if the sub_query matches any document in the field.
        """

    @abstractmethod
    def excludes(self, operand: Any) -> QueryExpression:
        pass

    @abstractmethod
    def has_substring(self, operand: Any) -> QueryExpression:
        pass


class LogicalOperator(Enum):
    AND = "and"
    OR = "or"


class JoinType(Enum):
    INNER = "inner"
    LEFT = "left"
    RIGHT = "right"
    FULL = "full"


T = TypeVar("T")


@dataclass
class PaginatedResult(Generic[T]):
    """
    A dataclass representing a paginated result.
    """

    total: int
    items: List[T]
    page: int
    pages: int
    page_size: int


class Query(ABC):
    @abstractmethod
    def ops(self) -> Operator:
        """
        Returns the operator mapping for the query language.
        """

    @abstractmethod
    def filter(
        self,
        field: str,
        statement: QueryExpression,
        logical_op: LogicalOperator = LogicalOperator.AND,
    ) -> "Query":
        """
        Adds a filter to the query.
        """

    @abstractmethod
    def join(
        self,
        collection: DatastoreEntityName,
        local_field: str,
        foreign_field: str,
        alias: Optional[str] = None,
        join_type: JoinType = JoinType.INNER,
    ) -> "Query":
        """
        Adds a join to the query.
        """

    @abstractmethod
    def sort_by(
        self, field: str, direction: SortOrder = SortOrder.ASCENDING
    ) -> "Query":
        """
        Adds a sort field and direction to the query.
        """

    @abstractmethod
    def set_limit(self, limit: int) -> "Query":
        """
        Sets the limit of the query.
        """

    @abstractmethod
    def set_offset(self, offset: int) -> "Query":
        """
        Sets the offset of the query.
        """

    @abstractmethod
    def build(self) -> Any:
        """
        Constructs and returns the final query object or string, depending on the database type.
        """


class Datastore(ABC):
    @abstractmethod
    async def add(self, collection: DatastoreEntityName, document: Dict) -> str:
        pass

    @abstractmethod
    async def get_one(self, collection: DatastoreEntityName, query: Query) -> Dict:
        pass

    @abstractmethod
    async def get_many(
        self, collection: DatastoreEntityName, query: Query
    ) -> List[Dict]:
        pass

    @abstractmethod
    async def get_paginated(
        self, collection: DatastoreEntityName, query: Query
    ) -> PaginatedResult:
        pass

    @abstractmethod
    async def count(self, collection: DatastoreEntityName, query: Query) -> int:
        pass

    @abstractmethod
    async def sum(
        self, collection: DatastoreEntityName, field: str, query: Query
    ) -> float:
        pass

    @abstractmethod
    async def group_sum(
        self,
        collection: DatastoreEntityName,
        group_field: str,
        value_field: str,
        query: Query,
    ) -> List[GroupSumResult]:
        """
        Returns the sum of the value_field for each group_field.
        """
        pass

    @abstractmethod
    async def aggregate(
        self, collection: DatastoreEntityName, query: Query, pipeline: List
    ) -> List:
        pass

    @abstractmethod
    async def update_one(
        self, collection: DatastoreEntityName, query: Query, update_values: Dict
    ) -> Dict:
        pass

    @abstractmethod
    async def update_many(
        self, collection: DatastoreEntityName, query: Query, update_values: Dict
    ) -> List[Dict]:
        pass

    @abstractmethod
    async def delete_many(self, collection: DatastoreEntityName, query: Query) -> int:
        pass

    @abstractmethod
    async def delete_one(self, collection: DatastoreEntityName, query: Query) -> bool:
        pass

    @abstractmethod
    def get_query_builder(self) -> Query:
        pass
