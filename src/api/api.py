from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Testing": 1234}
