from ._base import Base
from src.infra.mixins.update_from_schema import UpdateFromSchemaMixin
from sqlalchemy import Column, DateTime, Integer, Text, Enum
from datetime import datetime, timezone
from src.domain.enums import Role

class UserDBModel(UpdateFromSchemaMixin, Base):
    __tablename__ = "User"
    
    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True, index=True)
    role = Column(Enum(Role), nullable=False)
    name = Column(Text, nullable=False)
    email = Column(Text, nullable=False)
    username = Column(Text, nullable=False)
    password = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))