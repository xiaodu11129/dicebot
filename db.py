from sqlalchemy import (
    create_engine, Column, Integer, String, Float, Boolean, DateTime, ForeignKey
)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime
from config import DB_PATH

Base = declarative_base()
engine = create_engine(DB_PATH, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    tg_id = Column(Integer, unique=True)
    name = Column(String(64))
    password = Column(String(128), default="")
    is_admin = Column(Boolean, default=False)
    balance = Column(Float, default=0)
    profit = Column(Float, default=0)
    banned = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)

    bets = relationship("Bet", back_populates="user")
    requests = relationship("Request", back_populates="user")

class Bet(Base):
    __tablename__ = "bets"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    bet_type = Column(String(16))
    amount = Column(Float)
    period = Column(Integer)
    win_amount = Column(Float, default=0)
    status = Column(String(16), default="pending")  # pending, won, lost
    created_at = Column(DateTime, default=datetime.now)
    user = relationship("User", back_populates="bets")

class Lottery(Base):
    __tablename__ = "lotteries"
    id = Column(Integer, primary_key=True)
    period = Column(Integer, unique=True)
    dice1 = Column(Integer)
    dice2 = Column(Integer)
    dice3 = Column(Integer)
    sum = Column(Integer)
    result_text = Column(String(128))
    created_at = Column(DateTime, default=datetime.now)

class Request(Base):
    __tablename__ = "requests"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    req_type = Column(String(8))  # recharge, withdraw
    amount = Column(Float)
    status = Column(String(16), default="pending")  # pending, approved, rejected
    created_at = Column(DateTime, default=datetime.now)
    reviewed_by = Column(String(64))
    reviewed_at = Column(DateTime)
    user = relationship("User", back_populates="requests")

def create_db():
    Base.metadata.create_all(engine)
