from ._base import Base
from src.domain.schemas.user.user_model import UserModel
from src.infra.mixins.update_from_schema import UpdateFromSchemaMixin
from sqlalchemy import Column, DateTime, Integer, Text
from datetime import datetime, timezone

class UserDBModel(UpdateFromSchemaMixin, Base):
    __tablename__ = "users"
    
    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True, index=True)
    name = Column(Text, nullable=False)
    email = Column(Text, nullable=False)
    username = Column(Text, nullable=False)
    password = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))