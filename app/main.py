from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.models.infer import InferInputModel

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/api/infer")
def generate_notes(input: InferInputModel):
    try:
        # TODO: Pass input to inference
        print(input)
        # Do not return inference result here. That will be a separate api call. Simply return a success/failure message
        return {"message": "Successfully completed inference"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
