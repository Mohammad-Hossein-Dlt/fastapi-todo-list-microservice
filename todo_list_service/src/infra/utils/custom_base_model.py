from pydantic import BaseModel, ConfigDict, model_validator, field_validator, field_serializer
from bson.objectid import ObjectId
from typing import TypeAlias, Literal, ClassVar, Any

db_stack_types: TypeAlias = Literal["no-sql", "sql"]

class CustomBaseModel(BaseModel):
    
    aliases: ClassVar[dict[str, str]] = {
        "id": "_id"
    }
        
    model_config = ConfigDict(
        use_enum_values=True,
    )
    
    def __setattr__(self, name, value):
        
        if isinstance(value, str):
            value = value.strip()
        
        return super().__setattr__(name, value)
    
    @model_validator(mode="before")
    def alias_validator_before(cls, values) -> dict:
                
        if isinstance(values, dict):
            
            for k, v in cls.aliases.items():      
                if v in values:
                    values[k] = values.pop(v)
                    
        return values
    
    @model_validator(mode="before")
    def str_validator_before(cls, values) -> dict:
                
        if isinstance(values, dict):
            
            for k, v in values.items():
                if isinstance(v, str):
                    values[k] = v.strip()
                    
                    if ObjectId.is_valid(v):
                        values[k] = ObjectId(v)
        
        return values
    
    @field_validator("*")
    def object_id_validator(cls, var):
        if ObjectId.is_valid(var):
            return ObjectId(var)
        return var
    
    @field_serializer("*", when_used="json")
    def object_id_serializer(self, var):
        if ObjectId.is_valid(var):
            return str(var)
        return var

    def model_dump_for_db(
        self,
        exclude_unset: bool = False,
        exclude_none: bool = False,
        exclude: set = None,
    ) -> dict[str, Any]:
        
        if exclude:
            exclude = exclude.union({"id", "_id"})
        else:
            exclude = {"id", "_id"}
            
        dumped = self.model_dump(
            exclude_unset=exclude_unset,
            exclude_none=exclude_none,
            exclude=exclude,
            mode="python",
        )
                
        return dumped