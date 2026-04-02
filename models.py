from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from database import Base

class Record(Base):
    __tablename__ = "records"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    type = Column(String, index=True) # "Income" or "Expense"
    category = Column(String, index=True)
    description = Column(String, nullable=True)
    date = Column(DateTime, default=datetime.utcnow) # Added date tracking