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
from clueengine import engine as clue_engine

load_dotenv()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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

@app.get("/vote_summary/")
async def get_poll_results(db: Session = Depends(get_db)):
    votes = crud.get_votes(db)
    num_votes_richard = len([vote for vote in votes if vote.suspect == suspects.richard])
    num_votes_noah = len([vote for vote in votes if vote.suspect == suspects.noah])
    num_votes_maha = len([vote for vote in votes if vote.suspect == suspects.maha])
    return {"richard": num_votes_richard, "maha": num_votes_maha, "noah": num_votes_noah}

@app.get("/clues/", response_model=list[schemas.Clue])
async def get_clues(db: Session = Depends(get_db)):
    return crud.get_clues(db)

@app.post("/clue/", response_model=schemas.Clue)
async def post_clue(clue: schemas.ClueCreate, db: Session = Depends(get_db)):
    created_clue = crud.create_clue(db, clue)
    return created_clue

@app.get("/detectives/", response_model=list[schemas.Detective])
async def get_detectives(db: Session = Depends(get_db)):
    return crud.get_detectives(db)

@app.get("/detective/{detective_code}", response_model=schemas.Detective)
async def get_detective(detective_code: str, db: Session = Depends(get_db)):
    return crud.get_detective_by_code(db, code=detective_code)

@app.post("/detective/", response_model=schemas.Detective)
async def post_detective(detective: schemas.DetectiveCreate, db: Session = Depends(get_db)):
    maybe_detective = crud.maybe_get_detective_by_name(db, detective.name)
    if maybe_detective == None:
        return crud.create_detective(db, detective)
    else:
        return maybe_detective

@app.post("/vote/", response_model=schemas.Vote)
async def post_vote(vote: schemas.VoteCreate, db: Session = Depends(get_db)):
    if vote.model_dump()['suspect'] not in suspects.all_suspects:
        raise HTTPException(status_code=400, detail="suspect must be one of: " + ", ".join(suspects.all_suspects))
    if crud.maybe_get_vote_by_detective_id(db, vote.detective_id) == None:
        vote = crud.create_vote(db, vote)
    else:
        vote = crud.update_vote_detective_id(db, vote.detective_id, vote)
    return vote
