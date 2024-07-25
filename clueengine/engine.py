from database import crud, models, schemas
from sqlalchemy.orm import Session
from datetime import datetime
from clueengine import side_effects

clue_1_release_time = 2000
clue_2_release_time = 2005
clue_3_release_time = 2010
clue_4_release_time = 2015

def release_clue_loop(db: Session):
    current_local_time = datetime.now()
    clue_to_try_release = get_clue_to_release(current_local_time)
    if clue_to_try_release:
        release_clue(db, clue_to_try_release)
    
def get_clue_to_release(localtime: datetime):
    hhmm = localtime.hour * 100 + localtime.minute
    if hhmm >= clue_1_release_time and hhmm < clue_2_release_time:
        return 1
    elif hhmm >= clue_2_release_time and hhmm < clue_3_release_time:
        return 2
    elif hhmm >= clue_3_release_time and hhmm < clue_4_release_time:
        return 3
    elif hhmm >= clue_4_release_time:
        return 4
    return None

def release_clue(db: Session, clue_id: int):
    db_clue = crud.get_clue(db, clue_id)
    if db_clue.released:
        return
    result = crud.update_clue(db, clue_id, schemas.ClueCreate(number=db_clue.number, released=True))
    if int(clue_id) == 1:
        side_effects.clue_1_side_effects()
    elif int(clue_id) == 2:
        side_effects.clue_2_side_effects()
    elif int(clue_id) == 3:
        side_effects.clue_3_side_effects()
    elif int(clue_id) == 4:
        side_effects.clue_4_side_effects()
    return result
