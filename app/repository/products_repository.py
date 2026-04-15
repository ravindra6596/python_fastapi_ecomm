import math

from sqlalchemy import asc, desc
from sqlalchemy.orm import Session

from app.model.products_model import Product
from app.schemas.product_schema import ProductCreate
from app.utils.enums import ProductSortField, SortOrder


# Create product repo

def create_product_repo(db: Session, product: ProductCreate):
    product_repo = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        category_id=product.category_id
    )

    db.add(product_repo)
    db.commit()
    db.refresh(product_repo)
    return product_repo

# List of products repo
def get_products_repo(
    db: Session,
    page: int,
    limit: int,
    search: str,
    category_id: int,
    min_price: float,
    max_price: float,
    sort_by: ProductSortField,
    order: SortOrder
):
    query = db.query(Product).filter(
        Product.is_deleted == False
    )

    # search by name
    if search:
        query = query.filter(
            Product.name.ilike(f"%{search}%")
        )

    #  filter by category
    if category_id:
        query = query.filter(Product.category_id == category_id)

    # filter by price range
    if min_price is not None:
        query = query.filter(Product.price >= min_price)

    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    # sorting
    sort_column = getattr(Product, sort_by.value, Product.id)

    if order == "asc":
        query = query.order_by(asc(sort_column))
    else:
        query = query.order_by(desc(sort_column))

    # pagination
    total = query.count()
    offset = (page - 1) * limit

    items = query.offset(offset).limit(limit).all()

    # response
    return {
        "total": total,
        "page": page,
        "limit": limit,
        "items": items
    }

# get product by id
def get_product_by_id_repo(db: Session,  id: int):
    return db.query(Product).filter(
        Product.id ==  id,
        Product.is_deleted == False
    ).first()


# Update product
def update_product_repo(
    db,
    id: int,
    product_data,
):
    product = db.query(Product).filter(
        Product.id == id
    ).first()

    if not product:
        return None

    update_data = product_data.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)

    return product

# soft delete product
def soft_delete_product_repo(db, id: int):
    product = db.query(Product).filter(
        Product.id == id,
        Product.is_deleted == False
    ).first()

    if not product:
        return None

    product.is_deleted = True

    db.commit()
    db.refresh(product)

    return product