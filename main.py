from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()

class Expense(BaseModel):
  amount: float
  category: str
  description: str

expenses = []

@app.post("/expenses")
def add_expense(expense: Expense):
  expenses.append(expense)
  return expense

@app.get("/expenses")
def get_expenses():
  return expenses

@app.get("/")
def read_root():
  return{"message": "Expense Tracker API is running"}