import logging

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from app.llm.base import LLMBaseModel, LLMConfig

load_dotenv()

log = logging.getLogger(__name__)


class GoogleAI(LLMBaseModel):
    """This class handles the interaction with Google AI API."""

    model: ChatGoogleGenerativeAI

    def __init__(self, model_name: str, model_config: LLMConfig):
        super().__init__(model_name=model_name, model_config=model_config)
        try:
            self.model = ChatGoogleGenerativeAI(
                model=model_name, temperature=model_config.temperature
            )
        except Exception as e:
            log.error(f"Error initializing Google AI: {e}")
            raise e

    async def send_message(self, system_message: str, user_message: str) -> str:
        """Sends a message to Google AI and returns the response."""
        # As of now, gemini pro doesn't support system message, and the messages must follow Human/AI/Human/AI pattern. We will be using Human/AI conversation to mimic system message.
        messages = []
        if system_message:
            messages.append(HumanMessage(content=system_message))
            messages.append(
                AIMessage(content="Sure, I will strictly follow the instructions.")
            )
        messages.append(HumanMessage(content=user_message))

        log.info(f"Sending messages to Google AI")
        response = (await self.model.ainvoke(messages)).content
        return response
