from pydantic import BaseModel

class LoginUserOutput(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"