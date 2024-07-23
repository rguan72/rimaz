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

def get_clue(db: Session, clue_id: int):
    return db.query(models.Clue).filter(models.Clue.id == clue_id).one()

def update_clue(db: Session, id: int, clue: schemas.ClueCreate):
    db.query(models.Clue).filter(models.Clue.id == id).update(clue.model_dump())
    db.commit()
    return get_clue(db, id)

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

def create_clue_detective_link(db: Session, link: schemas.DetectiveClueLinkCreate):
    db_link = models.DetectiveClueLink(detective_id=link.detective_id, clue_id=link.clue_id, solved=link.solved, voted=link.voted)
    db.add(db_link)
    db.commit()
    db.refresh(db_link)
    return db_link

def get_clue_detective_links_by_detective_id(db: Session, detective_id: int):
    return db.query(models.DetectiveClueLink).filter(models.DetectiveClueLink.detective_id == detective_id).all()

def get_clue_detective_links_by_clue_id(db: Session, clue_id: int):
    return db.query(models.DetectiveClueLink).filter(models.DetectiveClueLink.clue_id == clue_id).all()

def get_clue_detective_link_by_detective_id_and_clue_id(db: Session, detective_id: int, clue_id: int):
    return db.query(models.DetectiveClueLink).filter(models.DetectiveClueLink.detective_id == detective_id, models.DetectiveClueLink.clue_id == clue_id).one()

def maybe_get_clue_detective_link_by_detective_id_and_clue_id(db: Session, detective_id: int, clue_id: int):
    return db.query(models.DetectiveClueLink).filter(models.DetectiveClueLink.detective_id == detective_id, models.DetectiveClueLink.clue_id == clue_id).one_or_none()

def update_clue_detective_link(db: Session, id: int, link: schemas.DetectiveClueLinkCreate):
    db.query(models.DetectiveClueLink).filter(models.DetectiveClueLink.id == id).update(link.model_dump())
    db.commit()
    return get_clue_detective_link_by_detective_id_and_clue_id(db, link.detective_id, link.clue_id)