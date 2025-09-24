from pydantic import BaseModel

class LoginUserInput(BaseModel):
    username: str
    password: str
