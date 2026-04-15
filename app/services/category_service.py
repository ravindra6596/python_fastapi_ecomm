from sqlalchemy.orm import Session

from app.repository import category_repository
from app.schemas.category_schema import CategoryResponse


# Create category service
def create_category_service(db, payload):
    return category_repository.create_category_repo(db, payload)

# list of category service

def get_category_service(db: Session):
    categories = category_repository.get_category_repo(db)
    return [
        CategoryResponse.model_validate(cat).model_dump()
        for cat in categories
    ]