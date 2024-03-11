from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/api/infer")
def generate_notes():
    response = {
        "data": {
            "summary": "ABC",
            "code": "DEF"
        }
    }
    return response
