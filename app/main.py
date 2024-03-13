from fastapi import FastAPI, HTTPException
from app.models.conversation import Conversation
from app.models.inference import InferenceInput
from app.scripts.generate import generate

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/api/inference")
async def generate_notes(input: InferenceInput):
    try:
        conversation: Conversation = Conversation(**input.messages)
        await generate(conversation)
        # Do not return inference result here. That will be a separate api call. Simply return a success/failure message
        return {"message": "Successfully completed inference"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
