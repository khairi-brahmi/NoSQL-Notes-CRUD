from fastapi import FastAPI

from server.routes.note import router as noteRouter

app = FastAPI()

app.include_router(noteRouter, tags=["note"], prefix="/note")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}
