from typing import Any, Dict
from pydantic import UUID4, BaseModel, Field

class InferInputModel(BaseModel):
    id: str = Field(..., alias='_id')
    user_id: UUID4
    messages: Dict[str, str]
    
    class Config:
        allow_population_by_field_name = True