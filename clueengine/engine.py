from database import crud, models, schemas

def is_answer_correct(clue: schemas.Clue, answer: str):
    return answer == "rimaz"