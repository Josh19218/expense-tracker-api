from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database import engine, SessionLocal, Base
import models

Base.metadata.create_all(bind=engine)

app = FastAPI()

class ExpenseCreate(BaseModel):
  amount: float
  category: str
  description: str

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()
  
@app.get("/")
def read_root():
  return{"message": "Expense Tracker API is running"}

@app.post("/expenses")
def add_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
  db_expense = models.Expense(
    amount=expense.amount,
    category=expense.category,
    description=expense.description
  )
  db.add(db_expense)
  db.commit()
  db.refresh(db_expense)
  return db_expense

@app.get("/expenses")
def get_expenses(db: Session = Depends(get_db)):
  return db.query(models.Expense).all()