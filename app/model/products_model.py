from sqlalchemy import Column, String, Integer, Float, ForeignKey, Boolean, DateTime, func
from sqlalchemy.orm import relationship

from app.constants.strings import ConstStrings
from app.database.connection import Base


class Product(Base):
    __tablename__ = ConstStrings.PRODUCTS_TABLE

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category") # for category name
    is_deleted = Column(Boolean, default=False)
    deleted_by = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )