from typing import Any

from pydantic import BaseModel


class InferenceInput(BaseModel):
    conversation: dict[str, Any]
    content: list[str]
