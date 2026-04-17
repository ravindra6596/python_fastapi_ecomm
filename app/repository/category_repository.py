import math

from sqlalchemy import asc, desc, or_, cast, String, func
from sqlalchemy.orm import Session

from app.constants.strings import ConstStrings
from app.model.categories_model import Category
from app.model.products_model import Product


# Create Category
def create_category_repo(db: Session, payload, token):
    category = Category(name=payload.name)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


# get all category
def get_category_repo(
        db: Session,
        page: int,
        limit: int,
        search: str,
        sort_by: str,
        order: str,
        token
):
    query = db.query(Category).filter(
        Category.is_deleted == False
    )

    #  Search
    if search:
        query = query.filter(
            or_(
                Category.name.ilike(f"%{search}%"),
                cast(Category.created_at, String).ilike(f"%{search}%"),
                cast(Category.updated_at, String).ilike(f"%{search}%")
            )
        )

    #   Sorting
    # sort_column = getattr(Category, sort_by, Category.id)
    sort_column = getattr(Category, sort_by, None)
    try:
        column_type = sort_column.property.columns[0].type
        if isinstance(column_type, String):
            sort_column = func.lower(sort_column)
    except Exception:
        pass

    if order == ConstStrings.ASCENDING:
        query = query.order_by(asc(sort_column))
    else:
        query = query.order_by(desc(sort_column))

    # Pagination
    total = query.count()
    total_pages = math.ceil(total / limit)
    offset = (page - 1) * limit

    categories = query.offset(offset).limit(limit).all()
    return {
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": total_pages,
        "is_previous": page > 1,
        "is_next": page < total_pages,
        "items": categories
    }


# get category by id
def get_category_by_id_repo(db, category_id: int, token):
    return db.query(Category).filter(
        Category.id == category_id,
        Category.is_deleted == False
    ).first()


# Insert bulk category records
def create_category_bulk_repo(db, categories, token):
    db.add_all(categories)
    db.commit()

    for category in categories:
        db.refresh(category)

    return categories


# Update category
def update_category_repo(db: Session, category: Category, update_data: dict, token):
    for key, value in update_data.items():
        setattr(category, key, value)

    db.commit()
    db.refresh(category)

    return category


# soft delete
def delete_category_repo(db, category_id: int, token: dict):
    category = db.query(Category).filter(
        Category.id == category_id,
        Category.is_deleted == False
    ).first()

    if not category:
        return None

    # extract user_id from token
    user_id = token.get(ConstStrings.USER_ID_FIELD)

    category.is_deleted = True
    category.deleted_by = user_id
    #  soft delete all linked products (IMPORTANT)
    db.query(Product).filter(
        Product.category_id == category_id,
        Product.is_deleted == False
    ).update(
        {
            Product.is_deleted: True,
            Product.deleted_by: user_id
        },
        synchronize_session=False
    )

    db.commit()
    db.refresh(category)

    return category
