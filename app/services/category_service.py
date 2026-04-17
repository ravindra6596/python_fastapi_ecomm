from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.constants.strings import ConstStrings
from app.model.categories_model import Category
from app.repository import category_repository
from app.schemas.category_schema import CategoryResponse, CategoryUpdate


# Create category service
def create_category_service(db, payload,token: dict):
    existing = db.query(Category).filter(
        Category.name.ilike(payload.name)
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail=ConstStrings.CATEGORY_EXISTS
        )
    return category_repository.create_category_repo(db, payload,token)

# list of category service

def get_category_service(db: Session,page: int,
    limit: int,
    search: str,
    sort_by: str,
    order: str,
    token: dict):
    result = category_repository.get_category_repo(
        db,
        page,
        limit,
        search,
        sort_by,
        order,
        token
    )

    result["items"] = [
        CategoryResponse.model_validate(cat).model_dump()
        for cat in result["items"]
    ]

    return result
# get category by id
def get_category_by_id_service(db, category_id: int,token: dict):

    category = category_repository.get_category_by_id_repo(db, category_id,token)

    if not category:
        raise HTTPException(
            status_code=404,
            detail=ConstStrings.NO_CATEGORY
        )
    return category

# bulk category service
def create_category_bulk_service(db, payload,token: dict):

    category_objects = []

    for item in payload:
        existing = db.query(Category).filter(
            Category.name.ilike(item.name)
        ).first()

        if existing:
            raise HTTPException(
                status_code=400,
                detail=f"{ConstStrings.CATEGORY_EXISTS}: {item.name}"
            )
        # Validate name
        if not item.name.strip():
            raise HTTPException(
                status_code=400,
                detail=ConstStrings.CATEGORY_NAME_EMPTY
            )

        category_objects.append(
            Category(name=item.name)
        )

    return category_repository.create_category_bulk_repo(
        db,
        category_objects,token
    )
# update category service


def update_category_service(db: Session, id: int, payload: CategoryUpdate,token: dict):

    #   Get existing record
    category = db.query(Category).filter(
        Category.id == id,
        Category.is_deleted == False
    ).first()

    if not category:
        raise HTTPException(
            status_code=404,
            detail=ConstStrings.NO_CATEGORY
        )

    #  Only incoming fields
    update_data = payload.model_dump(exclude_unset=True)

    #  If nothing sent
    if not update_data:
        raise HTTPException(
            status_code=400,
            detail=ConstStrings.NO_UPDATE
        )

    #  Check "no changes detected"
    no_change = True
    for key, value in update_data.items():
        if getattr(category, key) != value:
            no_change = False
            break

    if no_change:
        raise HTTPException(
            status_code=400,
            detail=ConstStrings.NO_CHANGE
        )

    #  Validate duplicate name
    if "name" in update_data:
        existing = db.query(Category).filter(
            Category.name.ilike(update_data["name"]),
            Category.id != id
        ).first()

        if existing:
            raise HTTPException(
                status_code=400,
                detail=ConstStrings.CATEGORY_EXISTS
            )

    #   Update repo
    return category_repository.update_category_repo(
        db,
        category,
        update_data,token
    )
# Soft delete category
def delete_category_service(db, category_id: int,token: dict):

    category = db.query(Category).filter(
        Category.id == category_id,
        Category.is_deleted == False
    ).first()

    if not category:
        raise HTTPException(
            status_code=404,
            detail=ConstStrings.NO_CATEGORY
        )

    return category_repository.delete_category_repo(db, category_id,token)