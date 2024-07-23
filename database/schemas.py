from pydantic import BaseModel


class VoteBase(BaseModel):
    clue_id: int
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


class ClueCreate(ClueBase):
    pass


class Clue(ClueBase):
    id: int
    number: int
    released: bool

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

class DetectiveClueLinkBase(BaseModel):
    clue_id: int
    detective_id: int
    solved: bool
    voted: bool

class DetectiveClueLinkCreate(DetectiveClueLinkBase):
    pass

class DetectiveClueLink(DetectiveClueLinkBase):
    id: int

    class Config:
        orm_mode = True