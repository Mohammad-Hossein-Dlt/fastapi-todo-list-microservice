from pydantic import BaseModel
from typing import Literal
from datetime import datetime

class JWTPayload(BaseModel):
    user_id: str
    type: Literal["access", "refresh"]
    exp: datetime | None = None