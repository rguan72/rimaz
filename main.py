from fastapi import FastAPI
from dotenv import load_dotenv
from lights import smart_plugs as smart_plugs

from common import constants

load_dotenv()

app = FastAPI()


# LED light control + also project in projector

@app.get("/")
async def root():
    return {"message": "Hello World"}