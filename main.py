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

load_dotenv()
models.Base.metadata.create_all(bind=engine)
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

@app.get("/clue/{clue_id}/vote_results/")
async def get_poll_results(clue_id: str):
    print(clue_id)
    return {"richard": 2, "maha": 4, "noah": 1}

@app.get("/clue_v2/{clue_id}/vote_results/")
async def get_poll_results(clue_id: str, db: Session = Depends(get_db)):
    votes = crud.get_votes_by_clue_id(db, clue_id)
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

@app.post("/detective/", response_model=schemas.Detective)
async def post_detective(detective: schemas.DetectiveCreate, db: Session = Depends(get_db)):
    created_detective = crud.create_detective(db, detective)
    return created_detective

class Vote(BaseModel):
    suspect: str
    detective_code: str

@app.post("/clue/{clue_id}/vote/")
async def post_vote(clue_id: str, vote: Vote, db: Session = Depends(get_db)):
    return vote

@app.post("/clue_v2/{clue_id}/vote/")
async def test_post_vote(clue_id: str, vote: Vote, db: Session = Depends(get_db)):
    detective = crud.get_detective_by_code(db, code=vote.detective_code)
    if vote.suspect not in suspects.all_suspects:
        raise HTTPException(status_code=400, detail="suspect not found")
    vote_create = schemas.VoteCreate(clue_id=clue_id, detective_id=detective.id, suspect=vote.suspect)
    voteOpt = crud.get_vote_by_clue_id_and_detective_id(db, clue_id=clue_id, detective_id=detective.id)
    if voteOpt is None:
        vote_result = crud.create_vote(db, vote_create)
    else:
        vote_result = crud.update_vote_by_clue_id_and_detective_id(db, clue_id=clue_id, detective_id=detective.id, vote=vote_create)
    return vote_result