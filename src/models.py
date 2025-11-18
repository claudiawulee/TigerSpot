# -----------------------------------------------------------------------
# models.py
# SQLAlchemy ORM models for TigerSpot database tables
# -----------------------------------------------------------------------

from sqlalchemy import Column, Integer, String, Boolean, Date, ARRAY, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# -----------------------------------------------------------------------


class User(Base):
    """Model for users table - stores overall user points"""

    __tablename__ = "users"

    username = Column(String(255), primary_key=True)
    points = Column(Integer, default=0)
    admin = Column(Boolean, default=False)

    def __repr__(self):
        return f"<User(username={self.username}, points={self.points})>"


# -----------------------------------------------------------------------


class UserDaily(Base):
    """Model for usersDaily table - stores daily user game stats"""

    __tablename__ = "usersdaily"

    username = Column(String(255), primary_key=True)
    points = Column(Integer, default=0)
    distance = Column(Integer, default=0)
    played = Column(Boolean, default=False)
    last_played = Column(Date, nullable=True)
    last_versus = Column(Date, nullable=True)
    current_streak = Column(Integer, default=0)

    def __repr__(self):
        return f"<UserDaily(username={self.username}, points={self.points}, streak={self.current_streak})>"


# -----------------------------------------------------------------------


class Picture(Base):
    """Model for pictures table - stores campus location images"""

    __tablename__ = "pictures"

    pictureid = Column(Integer, primary_key=True, autoincrement=False)
    coordinates = Column(ARRAY(Float, dimensions=1), nullable=False)
    link = Column(String(255), nullable=False)
    place = Column(String(255), nullable=False)

    def __repr__(self):
        return f"<Picture(id={self.pictureid}, place={self.place})>"


# -----------------------------------------------------------------------


class Challenge(Base):
    """Model for challenges table - stores versus mode challenges"""

    __tablename__ = "challenges"

    id = Column(Integer, primary_key=True, autoincrement=True)
    challenger_id = Column(String(255), nullable=False)
    challengee_id = Column(String(255), nullable=False)
    status = Column(String(255), nullable=False)
    challenger_finished = Column(Boolean, default=False)
    challengee_finished = Column(Boolean, default=False)
    challenger_points = Column(Integer, default=0)
    challengee_points = Column(Integer, default=0)
    versuslist = Column(ARRAY(Integer, dimensions=1), default=[0, 0, 0, 0, 0])
    challenger_bool = Column(
        ARRAY(Boolean, dimensions=1), default=[False, False, False, False, False]
    )
    challengee_bool = Column(
        ARRAY(Boolean, dimensions=1), default=[False, False, False, False, False]
    )
    challenger_pic_points = Column(
        ARRAY(Integer, dimensions=1), default=[0, 0, 0, 0, 0]
    )
    challengee_pic_points = Column(
        ARRAY(Integer, dimensions=1), default=[0, 0, 0, 0, 0]
    )
    playger_button_status = Column(Boolean, default=False)
    playgee_button_status = Column(Boolean, default=False)

    def __repr__(self):
        return f"<Challenge(id={self.id}, challenger={self.challenger_id}, challengee={self.challengee_id}, status={self.status})>"


# -----------------------------------------------------------------------


class Match(Base):
    """Model for matches table - stores completed versus mode match results"""

    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, autoincrement=True)
    challenge_id = Column(Integer, nullable=False)
    winner_id = Column(String(255), nullable=True)
    challenger_score = Column(Integer, nullable=False)
    challengee_score = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<Match(id={self.id}, challenge_id={self.challenge_id}, winner={self.winner_id})>"
