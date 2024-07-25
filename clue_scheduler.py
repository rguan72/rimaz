from database.database import SessionLocal
from clueengine import engine as clue_engine
from sounds import speakers
import sys
import time

import time
from sqlalchemy.orm import Session

while True:
    try:
        speakers.play_inaudible_sound()
        with SessionLocal() as db:
            if clue_engine.release_clue_loop(db) == "end":
                sys.exit(0)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        time.sleep(60)
