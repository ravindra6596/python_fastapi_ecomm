import math
from typing import Optional

from sqlalchemy import asc, desc, or_, cast, String, func
from sqlalchemy.orm import Session, joinedload

from app.constants.strings import ConstStrings
from app.model.categories_model import Category
from app.model.products_model import Product
from app.schemas.product_schema import ProductCreate, ProductResponse


# Create product repo

def create_product_repo(db: Session, product: ProductCreate,token: dict):
    product_repo = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        category_id=product.category_id,
    )

    db.add(product_repo)
    db.commit()
    db.refresh(product_repo)
    return product_repo


def get_products_repo(
    db: Session,
    page: int = 1,
    limit: int = 10,
    search: Optional[str] = None,
    category_id: Optional[int] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    sort_by=None,
    order=None,
    token: dict = None
):
    query = db.query(Product).options(
        joinedload(Product.category)
    ).filter(
        Product.is_deleted == False
    )

    # Search filter
    if search:
        search = search.strip()

        if search.lower() in [ConstStrings.TRUE, ConstStrings.FALSE]:
            query = query.filter(Product.is_deleted == (search.lower() == ConstStrings.TRUE))
        else:
            query = query.join(Category, Product.category_id == Category.id)
            query = query.filter(
                or_(
                    Product.name.ilike(f"%{search}%"),
                    Product.description.ilike(f"%{search}%"),
                    Category.name.ilike(f"%{search}%"),  # category search
                    cast(Product.created_at, String).ilike(f"%{search}%"),
                    cast(Product.updated_at, String).ilike(f"%{search}%"),
                )
            )
    #   FILTER BY CATEGORY
    if category_id is not None:
        query = query.filter(Product.category_id == category_id)

    #  PRICE RANGE FILTER
    if min_price is not None:
        query = query.filter(Product.price >= min_price)

    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    #  COUNT (remove ORDER BY issue)
    total = query.order_by(None).count()

    #   SORTING (Enum safe)
    # sort_column = getattr(Product, sort_by.value, Product.id)
    sort_column = getattr(Product, sort_by, None)
    try:
        column_type = sort_column.property.columns[0].type
        if isinstance(column_type, String):
            sort_column = func.lower(sort_column)
    except Exception:
        pass

    if order.value == ConstStrings.ASCENDING:
        query = query.order_by(asc(sort_column))
    else:
        query = query.order_by(desc(sort_column))

    #  PAGINATION
    total_pages = math.ceil(total / limit)
    offset = (page - 1) * limit

    items = query.offset(offset).limit(limit).all()

    # response
    return {
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": total_pages,
        "is_previous": page > 1,
        "is_next": page < total_pages,
        "items": items
    }

# get product by id
def get_product_by_id_repo(db, id, token):
    product = db.query(Product).options(
        joinedload(Product.category)
    ).filter(
        Product.id == id,
        Product.is_deleted == False
    ).first()

    if not product:
        return None

    return ProductResponse(
    id=product.id,
    name=product.name,
    description=product.description,
    price=product.price,
    category_id=product.category_id,
    category_name=product.category.name if product.category else None,
    is_deleted=product.is_deleted,
    deleted_by=product.deleted_by,
    created_at=product.created_at,
    updated_at=product.updated_at
)


# Update product
def update_product_repo(
    db,
    id: int,
    product_data,token: dict
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
def soft_delete_product_repo(db, id: int,token: dict):
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

def create_products_bulk_repo(db: Session, products: list[Product],token: dict):
    db.add_all(products)
    db.commit()

    for p in products:
        db.refresh(p)

    return products


def get_valid_category_ids_repo(db: Session):
    return {c.id for c in db.query(Category.id).all()}