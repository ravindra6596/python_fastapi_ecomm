from enum import Enum


class ProductSortField(str, Enum):
    price = "price"
    created_at = "created_at"
    id = "id"

class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"