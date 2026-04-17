from sqlalchemy.orm import Session

from app.constants.strings import ConstStrings
from app.model.categories_model import Category
from app.model.products_model import Product
from app.repository import products_repository
from app.schemas.product_schema import ProductCreate, ProductResponse


# Create product service
def create_product_service(db: Session, product: ProductCreate,token: dict):
    #  Validate category exists
    category = db.query(Category).filter(
        Category.id == product.category_id,
        Category.is_deleted == False
    ).first()
    # Validate name
    if not product.name.strip():
        raise HTTPException(
            status_code=400,
            detail=ConstStrings.PRODUCT_NAME_EMPTY
        )
    if not category:
        raise HTTPException(
            status_code=400,
            detail=ConstStrings.INVALID_CATEGORY
        )
    return products_repository.create_product_repo(db, product,token)


# List of products service

def get_products_service(
        db,
        page,
        limit,
        search,
        category_id,
        min_price,
        max_price,
        sort_by,
        order,
        token: dict
):
    result = products_repository.get_products_repo(
        db,
        page,
        limit,
        search,
        category_id,
        min_price,
        max_price,
        sort_by,
        order,
        token
    )

    result["items"] = [
        # ProductResponse.model_validate(item)
        ProductResponse(
            id=item.id,
            name=item.name,
            description=item.description,
            price=item.price,
            category_id=item.category_id,
            category_name=item.category.name if item.category else None,
            is_deleted=item.is_deleted,
            deleted_by=item.deleted_by,
            created_at=item.created_at,
            updated_at=item.updated_at
        )
        for item in result["items"]
    ]

    return result


# product by id
def get_product_by_id(db, id,token: dict):
    return products_repository.get_product_by_id_repo(db, id,token)

# update product by
def update_product_service(db, id: int, product, token: dict):

    # get only provided fields
    update_data = product.model_dump(exclude_unset=True)

    # validate category if provided
    if "category_id" in update_data:
        category = db.query(Category).filter(
            Category.id == update_data["category_id"]
        ).first()

        if not category:
            raise HTTPException(
                status_code=400,
                detail=ConstStrings.INVALID_CATEGORY
            )

    # validate price if provided
    if "price" in update_data:
        if update_data["price"] <= 0:
            raise HTTPException(
                status_code=400,
                detail=ConstStrings.PRICE_NOT_ZERO
            )

    return products_repository.update_product_repo(db, id, product,token)

from fastapi import HTTPException
# soft delete product
def soft_delete_product_service(db,  id: int,token: dict):

    product = db.query(Product).filter(
        Product.id == id,
        Product.is_deleted == False
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail=ConstStrings.NO_PRODUCT
        )

    return products_repository.soft_delete_product_repo(db, id, token)

def create_products_bulk_service(db, payload, token: dict):
    #   Fetch valid category IDs
    valid_category_ids = products_repository.get_valid_category_ids_repo(db)

    product_objects = []

    for item in payload:

        #   Invalid category check
        if item.category_id not in valid_category_ids:
            raise HTTPException(
                status_code=400,
                detail=f"{ConstStrings.INVALID_CATEGORY}: {item.category_id}"
            )

        product_objects.append(
            Product(
                name=item.name,
                description=item.description,
                price=item.price,
                category_id=item.category_id
            )
        )

    return products_repository.create_products_bulk_repo(db, product_objects,token)