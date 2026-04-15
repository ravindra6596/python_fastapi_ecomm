from sqlalchemy.orm import Session

from app.model.categories_model import Category

# Create Category
def create_category_repo(db: Session, payload):
    category = Category(name=payload.name)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

# get all category
def get_category_repo(db: Session):
    return db.query(Category).all()