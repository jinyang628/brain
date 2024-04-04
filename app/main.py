import logging
from typing import Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from app.models.conversation import Conversation
from app.models.inference import InferenceInput
from app.models.task import Task
from app.scripts.practice import generate_practice
from app.scripts.summary import generate_summary

log = logging.getLogger(__name__)

app = FastAPI()

@app.post("/api/inference")
async def generate_notes(input: InferenceInput):
    try:
        tasks: list[str] = input.tasks
        validated_tasks: list[Task] = Task.validate(tasks)

        summary: Optional[dict[str, str]] = None
        practice: Optional[list[tuple[str, str, str]]] = None
        for task in validated_tasks:
            if task == Task.SUMMARISE:
                summary = await generate_summary(conversations=input.conversation)
            elif task == Task.PRACTICE:
                if not summary:
                    summary = await generate_summary(conversations=input.conversation)
                practice = []
                for key, value in summary.items():
                    language, question, answer = await generate_practice(topic=key, content=value)
                    practice.append((language, question, answer))        
                    
        return JSONResponse(
            status_code=200, 
            content={"summary": summary, "practice": practice}
        )
    except ValueError as e:
        log.error(f"Error in post-processing the LLM output: {str(e)}")
        raise HTTPException(
            status_code=400, detail=str(e)
        )
    except Exception as e:
        log.error(f"Error in generating notes: {str(e)}")
        raise HTTPException(
            status_code=500, detail=str(e)
        )
    
