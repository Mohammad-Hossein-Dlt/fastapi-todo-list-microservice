from pydantic import BaseModel

class UserRegisterInput(BaseModel):
    name: str
    email: str
    username: str
    password: str
