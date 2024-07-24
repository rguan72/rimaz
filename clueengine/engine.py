from database import crud, models, schemas
from sqlalchemy.orm import Session

def release_clue(db: Session, clue_id: int):
    db_clue = crud.get_clue(db, clue_id)
    return crud.update_clue(db, clue_id, schemas.ClueCreate(number=db_clue.number, released=True))
