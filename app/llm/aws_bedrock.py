from app.llm.base import LLMBaseModel, LLMConfig


class AWSBedrock(LLMBaseModel):
    """This class handles the interaction with AWS Bedrock API."""

    def __init__(self, model_name: str, model_config: LLMConfig):
        super().__init__(model_name=model_name, model_config=model_config)

    async def send_message(self, system_message: str, user_message: str) -> str:
        """Sends a message to AWS Bedrock and returns the response."""
        # TODO: Implement the AWS Bedrock API call here.
