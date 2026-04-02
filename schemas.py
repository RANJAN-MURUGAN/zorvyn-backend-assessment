from pydantic import BaseModel, Field
from typing import Literal, Dict, List, Optional
from datetime import datetime

class RecordBase(BaseModel):
    amount: float = Field(..., gt=0, description="Amount must be positive")
    type: Literal["Income", "Expense"] # Forces user to pick one of these two
    category: str
    description: Optional[str] = None

class RecordCreate(RecordBase):
    pass

class RecordResponse(RecordBase):
    id: int
    date: datetime

    class Config:
        from_attributes = True

# --- Dashboard Schemas ---
class DashboardOverview(BaseModel):
    total_income: float
    total_expense: float
    net_balance: float

class DashboardResponse(BaseModel):
    overview: DashboardOverview
    category_totals: Dict[str, float]
    recent_activity: List[RecordResponse]