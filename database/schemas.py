from pydantic import BaseModel


class VoteBase(BaseModel):
    detective_id: int
    suspect: str


class VoteCreate(VoteBase):
    pass


class Vote(VoteBase):
    id: int

    class Config:
        orm_mode = True


class ClueBase(BaseModel):
    number: int
    released: bool


class ClueCreate(ClueBase):
    pass


class Clue(ClueBase):
    id: int

    class Config:
        orm_mode = True

class DetectiveBase(BaseModel):
    name: str
    code: str


class DetectiveCreate(DetectiveBase):
    pass


class Detective(DetectiveBase):
    id: int

    class Config:
        orm_mode = True
