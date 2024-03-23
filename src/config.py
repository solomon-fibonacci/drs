from enum import Enum


class DatastoreEntityName(str, Enum):
    """
    Enum for the different entities in the datastore.
    """

    PRODUCT = "products"
    ORDER = "orders"
    DESIGN_SPEC = "design_specs"


storefront_url = "http://localhost:3000"
