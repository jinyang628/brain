from typing import Dict

from pydantic import UUID4, BaseModel, ConfigDict, Field


class InferenceInput(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    id: str = Field(..., alias="_id")
    user_id: UUID4
    messages: Dict[str, str]
