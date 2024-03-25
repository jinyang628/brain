from typing import Optional
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from app.models.conversation import Conversation
from app.models.inference import InferenceInput
from app.models.task import Task
from app.scripts.generate import generate_summary
import logging

log = logging.getLogger(__name__)

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/api/inference")
async def generate_notes(input: InferenceInput):
    try:
        conversation: Conversation = Conversation(**input.conversation)
        tasks: list[str] = input.tasks
        validated_tasks: list[Task] = Task.validate(tasks) 
                
        summary: Optional[str] = None
        practice: Optional[str] = None
        for task in validated_tasks:
            if task == Task.SUMMARISE:
                summary = await generate_summary(conversation=conversation)
            elif task == Task.PRACTICE:
                if not summary:
                    summary = await generate_summary(conversation=conversation)
                # TODO: implement practice
                # practice: str = await generate_practice(summary=summary)
                practice = "practice"
        return JSONResponse(status_code=200, content={"summary": summary, "practice": practice})
    except Exception as e:
        log.error(f"Error in generating notes: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
