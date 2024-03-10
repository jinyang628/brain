from app.llm.base import LLMBaseModel, LLMConfig


class GoogleAI(LLMBaseModel):
    """This class handles the interaction with Google AI API."""

    def __init__(self, model_name: str, model_config: LLMConfig):
        super().__init__(model_name=model_name, model_config=model_config)

    async def send_message(
        self,
        message: str,
    ) -> str:
        """Sends a message to Google AI and returns the response."""
        # TODO: Implement the GoogleAI API call here.
