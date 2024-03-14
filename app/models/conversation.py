from pydantic import BaseModel, ConfigDict, root_validator


class Conversation(BaseModel):
    model_config = ConfigDict(extra="allow")

    title: str

    @root_validator(pre=True)
    def validate_keys(cls, values):
        for key in values:
            if (
                key != "title"
                and not key.startswith("UserMessage")
                and not key.startswith("AssistantMessage")
            ):
                raise ValueError(f"Invalid key name: {key}")
        return values

    def stringify(self) -> str:
        return f"Title: {self.title}\n\n" + "\n".join(
            [
                f"{key}: {value}\n\n"
                for key, value in self.model_dump().items()
                if key != "title"
            ]
        )
