from fastapi import FastAPI
from dotenv import load_dotenv
from lights import smart_plugs as smart_plugs
from sounds import speakers as speakers
import time

from common import constants

load_dotenv()

app = FastAPI()


# LED light control + also project in projector

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/trigger_effects")
async def trigger():
    smart_plugs.turn_all_lights_off()
    smart_plugs.turn_all_lights_on()
    speakers.play_clue_solved_sound_effect()
    time.sleep(1)
    smart_plugs.turn_all_lights_off()