from sqlalchemy import Column, Integer, Float, String
from database import Base

class Expense(Base):
  __tablename__ = "expenses"

  id = Column(Integer, primary_key=True, index=True)
  amount = Column(Float)
  category = Column(String)
  description = Column(String)

class User(Base):
  __tablename__ = "users"

  id = Column(Integer, primary_key=True, index=True)
  username = Column(String, unique=True, index=True)
  hashed_password = Column(String)