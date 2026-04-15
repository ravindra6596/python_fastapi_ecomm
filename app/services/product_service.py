from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.model.categories_model import Category
from app.model.products_model import Product
from app.schemas.product_schema import ProductCreate, ProductResponse
from app.repository import products_repository


# Create product service
def create_product_service(db: Session, product: ProductCreate):
    #  Validate category exists
    category = db.query(Category).filter(
        Category.id == product.category_id
    ).first()

    if not category:
        raise HTTPException(
            status_code=400,
            detail="Invalid category id"
        )
    return products_repository.create_product_repo(db, product)


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
        order
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
        order
    )

    result["items"] = [
        ProductResponse.model_validate(item)
        for item in result["items"]
    ]

    return result


# product by id
def get_product_by_id(db, id):
    return products_repository.get_product_by_id_repo(db, id)

# update product by
def update_product_service(db, id: int, product):

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
                detail="Invalid category id"
            )

    # validate price if provided
    if "price" in update_data:
        if update_data["price"] <= 0:
            raise HTTPException(
                status_code=400,
                detail="Price must be greater than 0"
            )

    return products_repository.update_product_repo(db, id, product)

from fastapi import HTTPException
# soft delete product
def soft_delete_product_service(db,  id: int):

    product = db.query(Product).filter(
        Product.id == id,
        Product.is_deleted == False
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return products_repository.soft_delete_product_repo(db, id)