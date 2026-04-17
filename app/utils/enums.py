from enum import Enum

from app.constants.strings import ConstStrings


class ProductSortField(str, Enum):
    id = "id"
    name = "name"
    price = "price"
    created_at = "created_at"

class CategorySortField(str, Enum):
    id = "id"
    name = "name"
    created_at = "created_at"

class SortOrder(str, Enum):
    asc = ConstStrings.ASCENDING
    desc = ConstStrings.DESCENDING
