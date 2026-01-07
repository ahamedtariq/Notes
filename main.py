from fastapi import FastAPI
from app.apis.notes import router as notes_router
from app.models import notes
from database import engine,Base


app = FastAPI()

Base.metadata.create_all(engine)

app.include_router(notes_router)


with open("error_logs.txt","w") as file:
    pass

@app.get("/test")
def test():
    return {"message":"test"}