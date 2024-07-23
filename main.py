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

@app.get("/clue_v2/{clue_id}/vote_results/")
async def get_poll_results(clue_id: str, db: Session = Depends(get_db)):
    votes = crud.get_votes_by_clue_id(db, clue_id)
    num_votes_richard = len([vote for vote in votes if vote.suspect == suspects.richard])
    num_votes_noah = len([vote for vote in votes if vote.suspect == suspects.noah])
    num_votes_maha = len([vote for vote in votes if vote.suspect == suspects.maha])
    links = crud.get_clue_detective_links_by_clue_id(db, clue_id)
    finished_detective_ids = [link.detective_id for link in links if link.solved]
    return {"richard": num_votes_richard, "maha": num_votes_maha, "noah": num_votes_noah, "finished_detetive_ids": finished_detective_ids}

@app.get("/clues/", response_model=list[schemas.Clue])
async def get_clues(db: Session = Depends(get_db)):
    return crud.get_clues(db)

@app.post("/clue/", response_model=schemas.Clue)
async def post_clue(clue: schemas.ClueCreate, db: Session = Depends(get_db)):
    created_clue = crud.create_clue(db, clue)
    return created_clue

class DetectiveClueStatus(BaseModel):
    clue_id: int
    solved: bool
    voted: bool

class Detective(schemas.Detective):
    clue_statuses: list[DetectiveClueStatus]

def enrich_detective(db: Session, detective: schemas.Detective):
    clues = crud.get_clues(db)
    clue_detective_links = crud.get_clue_detective_links_by_detective_id(db, detective.id)
    clue_statuses = []
    for clue in clues:
        if clue.id in [link.clue_id for link in clue_detective_links]:
            relationship = [clue_detective_link for clue_detective_link in clue_detective_links if clue_detective_link.clue_id == clue.id][0]
            clue_statuses.append(DetectiveClueStatus(clue_id=clue.id, solved=relationship.solved, voted=relationship.voted))
        else:
            clue_statuses.append(DetectiveClueStatus(clue_id=clue.id, solved=False, voted=False))
    return Detective(id=detective.id, name=detective.name, code=detective.code, clue_statuses=clue_statuses)

@app.get("/detectives/", response_model=list[Detective])
async def get_detectives(db: Session = Depends(get_db)):
    detectives = crud.get_detectives(db)
    enriched_detectives = []
    for detective in detectives:
        enriched_detectives.append(enrich_detective(db, detective))
    return enriched_detectives

@app.get("/detective/{detective_code}", response_model=Detective)
async def get_detective(detective_code: str, db: Session = Depends(get_db)):
    detective = crud.get_detective_by_code(db, code=detective_code)
    return enrich_detective(db, detective)

@app.post("/detective/", response_model=schemas.Detective)
async def post_detective(detective: schemas.DetectiveCreate, db: Session = Depends(get_db)):
    created_detective = crud.create_detective(db, detective)
    return created_detective

class Vote(BaseModel):
    suspect: str
    detective_code: str

@app.post("/clue_v2/{clue_id}/vote/")
async def post_vote(clue_id: str, vote: Vote, db: Session = Depends(get_db)):
    detective = crud.get_detective_by_code(db, code=vote.detective_code)
    if vote.suspect not in suspects.all_suspects:
        raise HTTPException(status_code=400, detail="suspect not found")
    vote_create = schemas.VoteCreate(clue_id=clue_id, detective_id=detective.id, suspect=vote.suspect)
    voteOpt = crud.get_vote_by_clue_id_and_detective_id(db, clue_id=clue_id, detective_id=detective.id)
    if voteOpt is None:
        vote_result = crud.create_vote(db, vote_create)
    else:
        vote_result = crud.update_vote_by_clue_id_and_detective_id(db, clue_id=clue_id, detective_id=detective.id, vote=vote_create)
    link = crud.get_clue_detective_link_by_detective_id_and_clue_id(db, detective_id=detective.id, clue_id=clue_id)
    if link.solved:
        crud.update_clue_detective_link(db, id=link.id, link=schemas.DetectiveClueLinkCreate(clue_id=clue_id, detective_id=detective.id, solved=True, voted=True))
    else:
        raise HTTPException(status_code=400, detail="clue must be solved before voting")
    return vote_result

class ClueAttemptSolve(BaseModel):
    detective_code: str
    answer: str

@app.post("/clue_v2/{clue_id}/attempt_solve/")
async def post_attempt_solve(clue_id: str, clue_attempt_solve: ClueAttemptSolve, db: Session = Depends(get_db)):
    clue = crud.get_clue(db, clue_id=clue_id)
    detective = crud.get_detective_by_code(db, code=clue_attempt_solve.detective_code)
    if clue_engine.is_answer_correct(clue=clue, answer=clue_attempt_solve.answer):
        if crud.maybe_get_clue_detective_link_by_detective_id_and_clue_id(db, detective_id=detective.id, clue_id=clue_id):
            pass
        else:
            crud.create_clue_detective_link(db, schemas.DetectiveClueLinkCreate(detective_id=detective.id, clue_id=clue_id, solved=True, voted=False))
        return {"success": True}
    else:
        return {"success": False}