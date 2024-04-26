import logging
from typing import Any, Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from app.exceptions.exception import InferenceFailure, LogicError
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
    except LogicError as e:
        log.error(f"Logic error while trying to generate notes: {str(e)}")
    except InferenceFailure as e:
        log.error(f"Inference failure while trying to generate notes: {str(e)}")
    except Exception as e:
        log.error(f"Error in generating notes: {str(e)}")
        # Raise exception only when an unexpected error occurs. If not, try to return good results as much as possible.
        raise HTTPException(status_code=500, detail=str(e))
    
    # Returns the parts that have been successfully processed. 
    if summary or practice:
        return JSONResponse(
            status_code=200,
            content={"summary": summary, "practice": practice, "token_sum": token_sum},
        )
    raise HTTPException(status_code=400, detail="Failed to generate notes completely.")
