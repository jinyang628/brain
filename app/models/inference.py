from typing import Any, Dict

from pydantic import UUID4, BaseModel, ConfigDict, Field

from app.models.task import Task


class InferenceInput(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    # THIS SHOULD BE THE CORRECT FIELDS, not entry
    # id: str = Field(..., alias="_id")
    # user_id: UUID4
    # messages: Dict[str, str]
    
    # THIS entry parameter IS A QUICK FIX, should be replaced with above
    entry: dict[str, Any]
    tasks: list[Task]