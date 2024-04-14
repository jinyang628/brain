import logging
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

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
                practice = []
                for topic, summary_chunk in summary.items():
                    language, question, answer = await generate_practice(
                        topic=topic, summary_chunk=summary_chunk
                    )
                    practice.append(
                        {"language": language, "question": question, "answer": answer}
                    )
        return JSONResponse(
            status_code=200,
            content={"summary": summary, "practice": practice, "token_sum": token_sum},
        )
    except ValueError as e:
        log.error(f"Error in post-processing the LLM output: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        log.error(f"Error in generating notes: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
