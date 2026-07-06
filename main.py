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

@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
  expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()

  if expense is None:
    return {"error": "Expense not found"}
  
  db.delete(expense)
  db.commit()
  return {"message": f"Expense {expense_id} deleted"}

@app.put("/expenses/{expense_id}")
def update_expenses(expense_id: int, updated: ExpenseCreate, db: Session = Depends(get_db)):
  expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()

  if expense is None:
    return {"error": "Expense not found"}
  
  expense.amount = updated.amount
  expense.category = updated.category
  expense.description = updated.description

  db.commit()
  db.refresh(expense)
  return expense

@app.get("/expenses")
def get_expenses(db: Session = Depends(get_db)):
  return db.query(models.Expense).all()