from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from auth import hash_password, verify_password, create_access_token, decode_access_token

from database import engine, SessionLocal, Base
import models

Base.metadata.create_all(bind=engine)

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class ExpenseCreate(BaseModel):
  amount: float
  category: str
  description: str

class UserCreate(BaseModel):
  username: str
  password: str

class LoginRequest(BaseModel):
  username: str
  password: str

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
  username = decode_access_token(token)
  if username is None:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
  
  user = db.query(models.User).filter(models.User.username == username).first()
  if user is None:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
  
  return user
  
@app.get("/")
def read_root():
  return{"message": "Expense Tracker API is running"}

@app.post("/expenses")
def add_expense(expense: ExpenseCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_expense = models.Expense(
        amount=expense.amount,
        category=expense.category,
        description=expense.description,
        user_id=current_user.id
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

@app.get("/expenses")
def get_expenses(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.Expense).filter(models.Expense.user_id == current_user.id).all()

@app.put("/expenses/{expense_id}")
def update_expense(expense_id: int, updated: ExpenseCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    expense = db.query(models.Expense).filter(models.Expense.id == expense_id, models.Expense.user_id == current_user.id).first()

    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")

    expense.amount = updated.amount
    expense.category = updated.category
    expense.description = updated.description
    db.commit()
    db.refresh(expense)
    return expense

@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    expense = db.query(models.Expense).filter(models.Expense.id == expense_id, models.Expense.user_id == current_user.id).first()

    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")

    db.delete(expense)
    db.commit()
    return {"message": f"Expense {expense_id} deleted"}

@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
  existing_user = db.query(models.User).filter(models.User.username == user.username).first()
  if existing_user:
    return {"error": "Username already taken"}
  
  new_user = models.User(
    username=user.username,
    hashed_password=hash_password(user.password)
  )
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  return {"message": f"User {new_user.username} created successfully"}

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()

    if user is None or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}