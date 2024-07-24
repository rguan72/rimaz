from database import crud, models, schemas
from sqlalchemy.orm import Session
from datetime import datetime

clue_1_release_time = 2200
clue_2_release_time = 2230
clue_3_release_time = 2300
clue_4_release_time = 2330

def release_clue_loop(db: Session):
    current_local_time = datetime.now()
    clue_to_try_release = get_clue_to_release(current_local_time)
    print("releasing clue: " + str(clue_to_try_release))
    # await clue_engine.release_clue(db, clue_to_try_release)

def get_clue_to_release(localtime: datetime):
    hhmm = localtime.hour * 100 + localtime.minute
    if hhmm >= clue_1_release_time and hhmm < clue_2_release_time:
        return 1
    elif hhmm >= clue_2_release_time and hhmm < clue_3_release_time:
        return 2
    elif hhmm >= clue_3_release_time and hhmm < clue_4_release_time:
        return 3
    else:
        return 4

async def release_clue(db: Session, clue_id: int):
    db_clue = crud.get_clue(db, clue_id)
    if db_clue.released:
        return
    return crud.update_clue(db, clue_id, schemas.ClueCreate(number=db_clue.number, released=True))
