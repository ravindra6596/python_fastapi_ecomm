from sqlalchemy import Column, Integer, String, DateTime, func, Boolean

from app.constants.strings import ConstStrings
from app.database.connection import Base


class User(Base):
    __tablename__ = ConstStrings.USER_TABLE

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    email = Column(String(150), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False, index=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
