from pydantic import BaseModel, ConfigDict

class OperationOutput(BaseModel):
    id: str
    request: str
    status: bool
    
    model_config = ConfigDict(
        from_attributes=True,
        extra='allow',
    )