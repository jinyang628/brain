from fastapi import FastAPI, HTTPException, Request

from app.models.conversation import Conversation
from app.models.inference import InferenceInput
from app.scripts.generate import generate_summary

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/api/inference")
async def generate_notes(input: InferenceInput, request: Request):
    
    # Update the shape of InferenceInput to be the correct shape without the entry wrapper
    body = await request.json()
    
    # print(body["entry"])
    # print(input)
    
    try:
        
        # conversation: Conversation = Conversation(**input.messages)
        
        # QUICK FIX
        print(body["entry"].get("_id"))
        print(body["entry"].get("user_id"))
        print(body["entry"].get("messages")) 
        conversation: Conversation = Conversation(body["entry"].get("_id"), body["entry"].get("user_id"), body["entry"].get("messages"))
        
        print(conversation)
        
        # Even though we don't use the result, we await the response to ensure there's no error (e.g. link is invalid)
        await generate_summary(conversation=conversation)
        # Do not return inference result here. That will be a separate api call. Simply return a success/failure message
        return {"message": "Successfully completed summary inference"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
