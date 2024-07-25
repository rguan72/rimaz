from lights import smart_plugs as smart_plugs
from sounds import speakers as speakers
from dotenv import load_dotenv
import time
import os
from fastapi import FastAPI
from dotenv import load_dotenv
from lights import smart_plugs as smart_plugs
from sounds import speakers as speakers
import time
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from common import suspects
from common import constants

from database import crud, models, schemas
from database.database import SessionLocal, engine
from clueengine import side_effects

load_dotenv()

side_effects.clue_1_side_effects()

# smart_plugs.set_lightbulb_effect(4, "colorloop")
# print(smart_plugs.get_lights())
# # smart_plugs.turn_all_lights_off()
# print(smart_plugs.get_lights())
# # smart_plugs.turn_all_lights_on()

# smart_plugs.turn_all_lights_on()
# time.sleep(1)
# smart_plugs.turn_all_lights_off()
# time.sleep(1)
# smart_plugs.turn_all_lights_on()
# time.sleep(1)
# smart_plugs.turn_all_lights_off()

# speakers.list_audio_devices()
# smart_plugs.turn_all_lights_off()
# smart_plugs.turn_all_lights_on()
# speakers.play_clue_solved_sound_effect()
# time.sleep(1)
# smart_plugs.turn_all_lights_off()

# smart_plugs.turn_all_lights_off()

# smart_plugs.light_effect()
