from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from .database import Base


class Vote(Base):
    __tablename__ = "vote"

    id = Column(Integer, primary_key=True)
    detective_id = Column(Integer, ForeignKey("detective.id"), unique=True)
    suspect = Column(String)

    detective = relationship("Detective", back_populates="vote")

class Detective(Base):
    __tablename__ = "detective"

    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True)
    name = Column(String, unique=True)

    vote = relationship("Vote", back_populates="detective")

class Clue(Base):
    __tablename__ = "clue"

    id = Column(Integer, primary_key=True)
    number = Column(Integer, unique=True)
    released = Column(Boolean, default=False)
