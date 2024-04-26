import logging 
import requests
import os 

from app.llm.base import LLMBaseModel, LLMConfig

log = logging.getLogger(__name__)

HUGGINGFACE_TOKEN = os.environ.get("HUGGINGFACE_TOKEN")

API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
headers = {"Authorization": f"Bearer {HUGGINGFACE_TOKEN}"}

class Llama3(LLMBaseModel):
    """This class handles the interaction with Llama3 API."""
    
    def query(self, payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()

    def __init__(self, model_name: str, model_config: LLMConfig):
        super().__init__(model_name=model_name, model_config=model_config)
        self._model = None
    
    async def send_message(self, system_message: str, user_message: str) -> str:
        """Sends a message to Llama3 and returns the response."""
        log.info(f"Sending messages to Llama3")
        response = self.query({
            "inputs": system_message + "\n\n" + user_message,
        })
        print(response[0].get("generated_text"))
        return response[0].get("generated_text")