from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator

from app.constants.strings import ConstStrings


class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=1)

    @field_validator("name")
    @classmethod
    def name_must_be_alpha(cls, v):
        v = v.strip()

        if not v:
            raise ValueError(ConstStrings.CATEGORY_NAME_EMPTY)

        if v.isdigit():
            raise ValueError(ConstStrings.CATEGORY_NAME_STRINGS)

        return v

# Update category
class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        if v is None:
            return v

        v = v.strip()

        if not v:
            raise ValueError(ConstStrings.CATEGORY_NAME_EMPTY)

        if v.isdigit():
            raise ValueError(ConstStrings.CATEGORY_NAME_STRINGS)

        return v

class CategoryResponse(BaseModel):
    id: int
    name: str
    is_deleted: bool
    deleted_by: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    model_config = {
        "from_attributes": True
    }