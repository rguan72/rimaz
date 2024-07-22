from sqlalchemy.orm import Session

from . import models, schemas


def get_votes_by_clue_id(db: Session, clue_id: str):
    return db.query(models.Vote).filter(models.Vote.clue_id == clue_id).all()

def get_vote_by_clue_id_and_detective_id(db: Session, clue_id: str, detective_id: int):
    return db.query(models.Vote).filter(models.Vote.clue_id == clue_id, models.Vote.detective_id == detective_id).one_or_none()

def update_vote_by_clue_id_and_detective_id(db: Session, clue_id: str, detective_id: int, vote: schemas.VoteCreate):
    db.query(models.Vote).filter(models.Vote.clue_id == clue_id, models.Vote.detective_id == detective_id).update(vote.model_dump())
    db.commit()
    return get_vote_by_clue_id_and_detective_id(db, clue_id, detective_id)

def create_vote(db: Session, vote: schemas.VoteCreate):
    db_vote = models.Vote(clue_id=vote.clue_id, detective_id=vote.detective_id, suspect=vote.suspect)
    db.add(db_vote)
    db.commit()
    db.refresh(db_vote)
    return db_vote

def get_clues(db: Session):
    return db.query(models.Clue).all()

def create_clue(db: Session, clue: schemas.ClueCreate):
    db_clue = models.Clue(number=clue.number)
    db.add(db_clue)
    db.commit()
    db.refresh(db_clue)
    return db_clue

def get_detectives(db: Session):
    return db.query(models.Detective).all()

def get_detective_by_code(db: Session, code: str):
    return db.query(models.Detective).filter(models.Detective.code == code).one()

def create_detective(db: Session, detective: schemas.DetectiveCreate):
    db_detective = models.Detective(code=detective.code, name=detective.name)
    db.add(db_detective)
    db.commit()
    db.refresh(db_detective)
    return db_detective