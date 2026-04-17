from datetime import datetime, timezone
from sqlalchemy import Column, Integer, DateTime, Text

from app.constants.strings import ConstStrings
from app.database.connection import Base


class BlacklistedToken(Base):
    __tablename__ = ConstStrings.BLACKLIST_TOKEN_TABLE

    id = Column(Integer, primary_key=True)
    token = Column(Text, unique=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))