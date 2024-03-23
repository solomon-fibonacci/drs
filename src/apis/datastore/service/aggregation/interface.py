from abc import ABC, abstractmethod
from typing import Any, Dict, List, TypedDict
from ..utils import SortOrder
from ..service.interface import Query


class GroupAggregation(ABC):
    @abstractmethod
    def sum(self, field: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def avg(self, field: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def min(self, field: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def max(self, field: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def count(self, field: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def unique_count(self, field: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def first(self, field: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def last(self, field: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def mode(self, field: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def median(self, field: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def percentile(self, field: str, percentile: float) -> Dict[str, Any]:
        pass


class GroupBy(TypedDict):
    identifier: str
    aggregations: Dict[str, GroupAggregation]


class Sorter(TypedDict):
    field: str
    direction: SortOrder


class LookupDetails(TypedDict):
    from_collection: str
    local_field: str
    foreign_field: str
    as_field: str


class ProjectFields(TypedDict):
    include: List[str]
    exclude: List[str]
    rename: Dict[str, str]


class NewFieldSynth(ABC):
    @abstractmethod
    def copy(self, field: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def capitalize(self, field: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def multiply(self, fields: List[str], factor: float) -> Dict[str, Any]:
        pass

    @abstractmethod
    def substring(self, field: str, start: int, length: int) -> Dict[str, Any]:
        pass

    @abstractmethod
    def concatenate(self, fields: List[str], separator: str = "") -> Dict[str, Any]:
        pass

    @abstractmethod
    def to_upper(self, field: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def to_lower(self, field: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def date_to_string(self, field: str, format_string: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def string_to_date(self, field: str, format_string: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def date_to_epoch(self, field: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def epoch_to_date(self, field: str) -> Dict[str, Any]:
        pass


class AddFieldsFields(TypedDict):
    fields: Dict[str, NewFieldSynth]


class Aggregation(ABC):
    """
    Abstract base class representing an aggregation pipeline for database queries.
    This class should be subclassed for specific database implementations.
    Each method adds a stage to the aggregation pipeline, allowing for complex data processing and analysis queries.
    """

    @abstractmethod
    def match(self, query: Query) -> "Aggregation":
        """
        Adds a 'match' stage to the aggregation pipeline. This stage is used for filtering documents based on specified query.
        It functions similarly to a 'WHERE' clause in SQL. The conditions are specified as field-operator-value triples,
        allowing you to define criteria for including documents in the result set.

        The 'MatchCondition' type used for the condition parameter clearly specifies the field to filter on,
        the operator to use for comparison, and the value to compare against.

        Example usage:
            Suppose you have a collection of sales data with fields like 'year', 'amount', and 'category'.
            To filter out sales records for the year 2021, you would use the 'match' stage as follows:

            Data Sample Before Applying Match:
            [
                {"year": 2021, "amount": 500, "category": "Electronics"},
                {"year": 2020, "amount": 300, "category": "Books"},
                {"year": 2021, "amount": 700, "category": "Clothing"}
            ]

            Using Match Stage:
            pipeline = Aggregation.match({"year": 2021})

            Data Sample After Applying Match:
            [
                {"year": 2021, "amount": 500, "category": "Electronics"},
                {"year": 2021, "amount": 700, "category": "Clothing"}
            ]

        This method will filter documents in the pipeline to include only those that match the specified condition.
        The 'match' stage is often used as the initial stage in an aggregation pipeline to narrow down the data set for subsequent stages.

        :param condition: A MatchCondition specifying the conditions to match.
        :return: An instance of the subclass for method chaining.
        """

    @abstractmethod
    def group(self, group_by: GroupBy) -> "Aggregation":
        """
        Adds a 'group' stage to the aggregation pipeline. This stage groups documents based on a specified identifier
        and performs aggregate calculations for each group using the GroupAggregation class.

        The GroupBy type specifies the field to group by ('identifier') and a dictionary of aggregation operations
        to perform ('aggregations'). Each aggregation operation is expressed using an instance of a subclass of
        GroupAggregation, which provides methods like sum, avg, max, etc., for different databases.

        Example usage:
            To group sales records by 'product_id' and calculate total sales, total quantity, and average quantity:

            group_agg = MongoGroupAggregation()  # Or SQLGroupAggregation() depending on the database
            pipeline = Aggregation.group({
                "identifier": "product_id",  # Field name to group by
                "aggregations": {
                    "total_sales": group_agg.sum("amount"),  # Sum of 'amount' field
                    "total_quantity": group_agg.sum("quantity"),  # Sum of 'quantity' field
                    "avg_quantity": group_agg.avg("quantity")  # Average of 'quantity' field
                }
            })

        This method allows grouping of documents and computation of aggregate values, such as sums, averages,
        and counts, on the grouped data. It abstracts the specifics of the database implementation, providing a
        uniform interface for aggregation.

        Scenario:
        An e-commerce platform wants to analyze its sales performance by aggregating data for each product.
        The goal is to calculate the total sales revenue and the average quantity sold for each product.
        Data Before Aggregation:

        Imagine we have the following sales records, where each document represents a sale with product_id, amount (sales revenue), and quantity sold:

        json

        [
            {"product_id": "101", "amount": 120, "quantity": 2},
            {"product_id": "102", "amount": 200, "quantity": 3},
            {"product_id": "101", "amount": 180, "quantity": 3},
            {"product_id": "103", "amount": 150, "quantity": 2},
            {"product_id": "102", "amount": 250, "quantity": 4}
        ]

        Using Group Stage:

        The goal is to group these records by product_id and then calculate the total sales (total_sales) and average quantity (avg_quantity) sold for each product.

        The aggregation pipeline with the group stage would look something like this:

        group_agg = MongoGroupAggregation()  # Assuming a MongoDB implementation
        pipeline = Aggregation.group({
            "identifier": "product_id",
            "aggregations": {
                "total_sales": group_agg.sum("amount"),
                "avg_quantity": group_agg.avg("quantity")
            }
        })

        Data After Aggregation:

        After applying the group stage, the data would be aggregated as follows:

        [
            {"product_id": "101", "total_sales": 300, "avg_quantity": 2.5},
            {"product_id": "102", "total_sales": 450, "avg_quantity": 3.5},
            {"product_id": "103", "total_sales": 150, "avg_quantity": 2.0}
        ]

        In this aggregated data:

            For product_id 101, the total sales are $300 (120 + 180) and the average quantity sold is 2.5 ((2 + 3) / 2).
            For product_id 102, the total sales are $450 (200 + 250) and the average quantity sold is 3.5 ((3 + 4) / 2).
            For product_id 103, the total sales are $150 and the average quantity sold is 2.

        :param group_by: A GroupBy type specifying the grouping criteria and aggregate calculations.
        :return: An instance of the subclass for method chaining.
        """

    @abstractmethod
    def project(self, fields: ProjectFields) -> "Aggregation":
        """
        Adds a 'project' stage to the aggregation pipeline. This stage reshapes each document in the pipeline
        by including, excluding, or renaming fields. It allows you to specify exactly which fields should appear in the
        output documents, rename them, or add computed fields based on existing ones.

        The ProjectFields type includes 'include', 'exclude', and 'rename' attributes. 'include' specifies the fields
        to be retained or computed in the output, 'exclude' specifies the fields to be removed, and 'rename' allows
        for renaming included fields.

        Example usage:
            Suppose you have a collection of detailed sales data and need to create a summary report. You want to include
            only the 'product_id', 'amount', and 'quantity' fields in each document, rename 'amount' to 'total_amount',
            and exclude details like 'region' and 'date':

            Data Sample Before Applying Project:
            [
                {"product_id": "101", "amount": 120, "quantity": 2, "region": "North", "date": "2021-01-10"},
                {"product_id": "102", "amount": 200, "quantity": 3, "region": "South", "date": "2021-01-11"}
            ]

            Using Project Stage:
            pipeline = Aggregation.project({
                "include": ["product_id", "amount", "quantity"],
                "exclude": ["region", "date"],
                "rename": {"amount": "total_amount"}
            })

            Data Sample After Applying Project:
            [
                {"product_id": "101", "total_amount": 120, "quantity": 2},
                {"product_id": "102", "total_amount": 200, "quantity": 3}
            ]

        This method enhances the flexibility of the data shaping process in the aggregation pipeline, enabling precise
        control over the representation of data in the output.

        :param fields: A ProjectFields type specifying the fields to include, exclude, and rename.
        :return: An instance of the subclass for method chaining.
        """

    @abstractmethod
    def sort(self, sorter: Sorter) -> "Aggregation":
        """
        Adds a 'sort' stage to the aggregation pipeline. This stage sorts documents based on the specified field and direction.
        The Sorter type includes the field name and direction (1 for ascending, -1 for descending). These int values are
        defined in the SortOrder enum.

        Example:
            - To sort documents by the 'name' field in ascending order:
                .sort(Sorter(field="name", direction=SortOrder.ASCENDING))

        :param order: A Sorter type specifying the field and direction to sort by.
        :return: An instance of the subclass for method chaining.
        """

    @abstractmethod
    def limit(self, count: int) -> "Aggregation":
        """
        Adds a 'limit' stage to the aggregation pipeline. This stage restricts the number of documents passed to the next stage.

        Example:
            - To limit the result to 10 documents:
                .limit(10)

        :param count: The number of documents to limit to.
        :return: An instance of the subclass for method chaining.
        """

    @abstractmethod
    def skip(self, count: int) -> "Aggregation":
        """
        Adds a 'skip' stage to the aggregation pipeline. This stage skips over the specified number of documents.

        Example:
            - To skip the first 5 documents:
                .skip(5)

        :param count: The number of documents to skip.
        :return: An instance of the subclass for method chaining.
        """

    @abstractmethod
    def unwind(self, field: str) -> "Aggregation":
        """
        Adds an 'unwind' stage to the aggregation pipeline. This stage is used to deconstruct an array field from
        the input documents, outputting a document for each element in the array. It essentially flattens the array,
        turning each element into a separate document, while retaining the context of the original document.

        This method is particularly useful when working with documents that contain arrays and you need to perform
        operations on each element of the array separately.

        Example usage:
            Consider a collection of sales orders where each order has an array of 'items'. Each item in the array
            contains details like 'item_id' and 'quantity'. To analyze each item separately, you would use the 'unwind' stage:

            Data Sample Before Applying Unwind:
            [
                {"order_id": "001", "items": [{"item_id": "A", "quantity": 2}, {"item_id": "B", "quantity": 3}]},
                {"order_id": "002", "items": [{"item_id": "A", "quantity": 1}, {"item_id": "C", "quantity": 1}]}
            ]

            Using Unwind Stage:
            pipeline = Aggregation.unwind("items")

            Data Sample After Applying Unwind:
            [
                {"order_id": "001", "items": {"item_id": "A", "quantity": 2}},
                {"order_id": "001", "items": {"item_id": "B", "quantity": 3}},
                {"order_id": "002", "items": {"item_id": "A", "quantity": 1}},
                {"order_id": "002", "items": {"item_id": "C", "quantity": 1}}
            ]

        The 'unwind' method is a powerful tool for transforming array fields into a format that can be more easily
        manipulated and analyzed in subsequent stages of the aggregation pipeline.

        :param field: The field name of the array to unwind.
        :return: An instance of the subclass for method chaining.
        """

    @abstractmethod
    def lookup(self, details: LookupDetails) -> "Aggregation":
        """
        Adds a 'lookup' (join) stage to the aggregation pipeline. This stage is used to perform a join operation between
        two collections (or tables), enriching or augmenting documents from the primary collection with data from the
        secondary collection based on a join condition.

        The LookupDetails type includes necessary parameters for the join: 'from_collection' is the secondary collection
        to join with, 'local_field' is the field from the primary collection, 'foreign_field' is the field from the secondary
        collection, and 'as_field' is the field name under which the joined data will be added to the primary documents.

        Example usage:
            Consider an 'orders' collection where each document has a 'customer_id' field, and a 'customers' collection
            with customer details. To join each order with the corresponding customer details:

            Data Sample Before Applying Lookup:
            Orders collection:
            [
                {"order_id": "001", "customer_id": "123", "amount": 150},
                {"order_id": "002", "customer_id": "124", "amount": 200}
            ]

            Customers collection:
            [
                {"customer_id": "123", "name": "John Doe"},
                {"customer_id": "124", "name": "Jane Doe"}
            ]

            Using Lookup Stage:
            pipeline = Aggregation.lookup({
                "from_collection": "customers",
                "local_field": "customer_id",
                "foreign_field": "customer_id",
                "as_field": "customer_details"
            })

            Data Sample After Applying Lookup:
            [
                {"order_id": "001", "customer_id": "123", "amount": 150, "customer_details": [{"name": "John Doe"}]},
                {"order_id": "002", "customer_id": "124", "amount": 200, "customer_details": [{"name": "Jane Doe"}]}
            ]

        This method is particularly useful for enriching documents with related data from another collection or table,
        providing a more complete view of the data for subsequent analysis or reporting.

        :param details: A LookupDetails type specifying the join operation details.
        :return: An instance of the subclass for method chaining.
        """

    @abstractmethod
    def add_fields(self, fields: AddFieldsFields) -> "Aggregation":
        """
        Adds an 'add_fields' stage to the aggregation pipeline. This stage allows adding new fields to documents or
        modifying existing fields, using various synthesis operations defined in the NewFieldSynth class.

        The AddFieldsFields type specifies the new fields to be added, each associated with a synthesis operation from
        NewFieldSynth, such as copying an existing field, capitalizing a string field, multiplying numerical values, etc.

        Example usage:
            To add a new field 'total_price' calculated as the product of 'unit_price' and 'quantity', and
            'customer_name_uppercase' as the uppercase version of 'customer_name':

            pipeline = Aggregation.add_fields({
                "total_price": NewFieldSynth.multiply("unit_price", "$quantity"),
                "customer_name_uppercase": NewFieldSynth.to_upper("customer_name")
            })

        This method provides a flexible and powerful mechanism for enriching documents with new or modified fields,
        enhancing their utility for downstream analysis and reporting.

        :param fields: An AddFieldsFields type specifying the new fields to add with their corresponding synthesis operations.
        :return: An instance of the subclass for method chaining.
        """

    @abstractmethod
    def build(self) -> Any:
        """
        Constructs and returns the final aggregation pipeline object or query. This method compiles the added stages
        into a format suitable for the specific database implementation being used.

        :return: The final aggregation pipeline or query.
        """
