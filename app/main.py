import logging
from typing import Any, Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from app.models.inference import InferenceInput
from app.models.task import Task
from app.scripts.practice import generate_practice
from app.scripts.summary import generate_summary

log = logging.getLogger(__name__)

app = FastAPI()


@app.post("/api/inference")
async def generate_notes(input: InferenceInput) -> JSONResponse:
    """Entrance of the inference pipeline, which generates notes based on the input conversation.

    Args:
        input (InferenceInput): The input conversation and tasks to be performed.

    Returns:
       JSONResponse: The generated notes that will be propagated back to Stomach upon successful inference.
    """
    try:
        tasks: list[str] = input.tasks
        validated_tasks: list[Task] = Task.validate(tasks)

        summary: Optional[dict[str, str]] = None
        practice: Optional[list[dict[str, str]]] = None
        for task in validated_tasks:
            if task == Task.SUMMARISE:
                summary, token_sum = await generate_summary(
                    conversations=input.conversation
                )
            elif task == Task.PRACTICE:
                if not summary:
                    summary, token_sum = await generate_summary(
                        conversations=input.conversation
                    )
                practice: dict[str, Any] = await generate_practice(summary=summary)
                
        return JSONResponse(
            status_code=200,
            content={"summary": summary, "practice": practice, "token_sum": token_sum},
        )
    except ValueError as e:
        log.error(f"Error in fully post-processing the LLM output: {str(e)}")
        # Returns the parts that have been successfully processed. 
        if summary or practice:
            return JSONResponse(
                status_code=200,
                content={"summary": summary, "practice": practice, "token_sum": token_sum},
            )
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        log.error(f"Error in generating notes: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
