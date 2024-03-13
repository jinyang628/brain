from app.llm.base import LLMBaseModel, LLMConfig


class OpenAI(LLMBaseModel):
    """This class handles the interaction with OpenAI API."""

    def __init__(self, model_name: str, model_config: LLMConfig):
        super().__init__(model_name=model_name, model_config=model_config)

    async def send_message(self, system_message: str, user_message: str) -> str:
        """Sends a message to OpenAI and returns the response."""
        # TODO: Implement the OpenAI API call here.
