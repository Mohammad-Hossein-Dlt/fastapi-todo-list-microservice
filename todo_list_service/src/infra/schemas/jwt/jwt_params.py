from pydantic import BaseModel, ConfigDict

class JWTParams(BaseModel):
    secret: str
    algorithm: str
    access_time: int
    refresh_time: int

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )
