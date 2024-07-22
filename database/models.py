from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from .database import Base


class Vote(Base):
    __tablename__ = "vote"

    id = Column(Integer, primary_key=True)
    detective_id = Column(Integer, ForeignKey("detective.id"))
    clue_id = Column(Integer, ForeignKey("clue.id"))
    suspect = Column(String)

    detective = relationship("Detective", back_populates="vote")
    clue = relationship("Clue", back_populates="vote")
    __table_args__ = (UniqueConstraint("clue_id", "detective_id", name="__clue_id_detective_id_uc"),)


class Detective(Base):
    __tablename__ = "detective"

    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True)
    name = Column(String)

    vote = relationship("Vote", back_populates="detective")

class Clue(Base):
    __tablename__ = "clue"

    id = Column(Integer, primary_key=True)
    number = Column(Integer, unique=True)

    vote = relationship("Vote", back_populates="clue")
