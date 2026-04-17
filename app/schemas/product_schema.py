from datetime import datetime

from pydantic import BaseModel, Field, field_validator
from typing import Optional

from app.constants.strings import ConstStrings
from app.schemas.category_schema import CategoryResponse


class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    category_id: int
    @field_validator("name")
    @classmethod
    def name_must_be_alpha(cls, v):
        if v.strip().isdigit():
            raise ValueError(ConstStrings.PRODUCT_NAME_EMPTY)
        return v

class ProductUpdate(BaseModel):
    name: Optional[str]= None
    description: Optional[str]= None
    price: Optional[float]= None
    category_id: Optional[int]= None
    @field_validator("name")
    @classmethod
    def name_must_be_alpha(cls, v):
        if v.strip().isdigit():
            raise ValueError(ConstStrings.PRODUCT_NAME_STRINGS)
        return v

class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    category_id: int
    category_name: Optional[str] = None
    is_deleted: bool
    deleted_by: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    model_config = {
        "from_attributes": True
    }