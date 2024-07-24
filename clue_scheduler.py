from database.database import SessionLocal
from clueengine import engine as clue_engine
import sys
import time

import time
from sqlalchemy.orm import Session

while True:
    try:
        print(".", end="")
        with SessionLocal() as db:
            clue_engine.release_clue_loop(db)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        time.sleep(60)
