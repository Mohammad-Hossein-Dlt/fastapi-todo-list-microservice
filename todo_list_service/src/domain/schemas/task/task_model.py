from src.infra.utils.custom_base_model import CustomBaseModel
from src.domain.enums import Status, Priority
from pydantic import ConfigDict, Field, model_validator
from datetime import datetime, timezone
from typing import Self

class TaskModel(CustomBaseModel):
    id: int | str | None = None
    user_id: int | str | None = None
    title: str | None = None
    description: str | None = None
    status: Status | None = None
    priority: Priority | None = None
    deadline: datetime | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    model_config = ConfigDict(
        extra='allow',
    )

    @model_validator(mode='after')
    def validate_values(
        self
    ) -> Self:
        
        if "updated_at" not in self.model_fields_set:
            self.updated_at = self.created_at
        
        return self