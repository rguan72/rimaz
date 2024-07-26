from database.database import SessionLocal
from clueengine import engine as clue_engine
from clueengine import side_effects
import sys

db = SessionLocal()
if int(sys.argv[1]) < 5:
    clue_engine.release_clue(db, sys.argv[1])
elif int(sys.argv[1]) == 5:
    side_effects.final_side_effects()
