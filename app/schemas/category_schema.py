from pydantic import BaseModel, Field, field_validator


class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=1)

    @field_validator("name")
    @classmethod
    def name_must_be_alpha(cls, v):
        if v.strip().isdigit():
            raise ValueError("Category name cannot be numeric only")
        return v

class CategoryResponse(BaseModel):
    id: int
    name: str
    model_config = {
        "from_attributes": True
    }