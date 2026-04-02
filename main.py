import os
import sys
from typing import Optional, List
from enum import Enum

# --- VERCEL PATH FIX ---
# This ensures Python can see models.py and database.py in the same folder
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

# Relative imports to handle Vercel's folder structure
try:
    from . import models, schemas
    from .database import engine, get_db
except ImportError:
    import models, schemas
    from database import engine, get_db

# Create the database tables in RAM
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Zorvyn Finance API", version="1.0.0")

# --- MOCK ACCESS CONTROL ---
class UserRole(str, Enum):
    Admin = "Admin"
    Analyst = "Analyst"
    Viewer = "Viewer"

def role_checker(allowed_roles: List[str]):
    def check_role(x_user_role: UserRole = Header(default=UserRole.Viewer)):
        if x_user_role.value not in allowed_roles:
            raise HTTPException(status_code=403, detail="Access Denied: Insufficient Permissions")
        return x_user_role.value
    return check_role

# ==========================================
#              RECORDS APIs
# ==========================================

@app.post("/records/", response_model=schemas.RecordResponse)
def create_record(
    record: schemas.RecordCreate, 
    db: Session = Depends(get_db),
    role: str = Depends(role_checker(["Admin", "Analyst"]))
):
    db_record = models.Record(**record.model_dump())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

@app.get("/records/", response_model=List[schemas.RecordResponse])
def get_records(
    category: Optional[str] = None,
    type: Optional[str] = None,
    role: str = Depends(role_checker(["Admin", "Analyst", "Viewer"])),
    db: Session = Depends(get_db)
):
    query = db.query(models.Record)
    if category:
        query = query.filter(models.Record.category == category)
    if type:
        query = query.filter(models.Record.type == type)
    return query.all()

@app.put("/records/{record_id}", response_model=schemas.RecordResponse)
def update_record(
    record_id: int, 
    updated_data: schemas.RecordCreate,
    db: Session = Depends(get_db),
    role: str = Depends(role_checker(["Admin"]))
):
    record = db.query(models.Record).filter(models.Record.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    
    for key, value in updated_data.model_dump().items():
        setattr(record, key, value)
        
    db.commit()
    db.refresh(record)
    return record

@app.delete("/records/{record_id}")
def delete_record(
    record_id: int, 
    db: Session = Depends(get_db),
    role: str = Depends(role_checker(["Admin"]))
):
    record = db.query(models.Record).filter(models.Record.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    
    db.delete(record)
    db.commit()
    return {"message": "Record deleted successfully"}

# ==========================================
#            DASHBOARD APIs
# ==========================================

@app.get("/dashboard/summary", response_model=schemas.DashboardResponse)
def get_dashboard_summary(
    db: Session = Depends(get_db),
    role: str = Depends(role_checker(["Admin", "Analyst", "Viewer"]))
):
    income = db.query(func.sum(models.Record.amount)).filter(models.Record.type == "Income").scalar() or 0.0
    expense = db.query(func.sum(models.Record.amount)).filter(models.Record.type == "Expense").scalar() or 0.0
    
    category_query = db.query(models.Record.category, func.sum(models.Record.amount)).group_by(models.Record.category).all()
    category_totals = {cat: amt for cat, amt in category_query}
    
    recent_activity = db.query(models.Record).order_by(desc(models.Record.id)).limit(5).all()
    
    return schemas.DashboardResponse(
        overview=schemas.DashboardOverview(
            total_income=income,
            total_expense=expense,
            net_balance=income - expense
        ),
        category_totals=category_totals,
        recent_activity=recent_activity
    )