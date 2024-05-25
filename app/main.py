import logging

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from app.exceptions.exception import InferenceFailure, LogicError
from app.models.inference import InferenceInput
from app.models.content import Content
from app.scripts.generate import generate

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
        content: list[str] = input.content
        validated_content_lst: list[Content] = Content.validate(content_str_lst=content)
        result, token_sum = await generate(
            conversation=input.conversation,
            content_lst=validated_content_lst
        )
        return JSONResponse(
            status_code=200,
            content={"result": result, "token_sum": token_sum},
        )
    except LogicError as e:
        log.error(f"Logic error while trying to generate notes: {str(e)}")
    except InferenceFailure as e:
        log.error(f"Inference failure while trying to generate notes: {str(e)}")
    except Exception as e:
        log.error(f"Error in generating notes: {str(e)}")
        # Raise exception only when an unexpected error occurs. If not, try to return good results as much as possible.
        raise HTTPException(status_code=500, detail=str(e))

    raise HTTPException(status_code=400, detail="Failed to generate notes completely.")
