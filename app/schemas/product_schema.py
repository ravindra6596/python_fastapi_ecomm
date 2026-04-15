from datetime import datetime

from pydantic import BaseModel, Field, field_validator
from typing import Optional

class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    category_id: int
    @field_validator("name")
    @classmethod
    def name_must_be_alpha(cls, v):
        if v.strip().isdigit():
            raise ValueError("Product name cannot be numeric")
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
            raise ValueError("Product name cannot be numeric")
        return v

class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    category_id: int
    is_deleted: bool
    created_at: datetime
    model_config = {
        "from_attributes": True
    }