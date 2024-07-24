from database.database import SessionLocal
from clueengine import engine as clue_engine
import sys

db = SessionLocal()
clue_engine.release_clue(db, sys.argv[1])
