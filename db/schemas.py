from pydantic import BaseModel, Field
from datetime import datetime

class TransactionIn(BaseModel):
    transaction_id: str = Field(..., pattern="^[a-zA-Z0-9_-]+$", max_length=50)
    user_id: str
    amount: float
    currency: str = Field(..., max_length=3)
    timestamp: datetime

class TransactionOut(BaseModel):
    transaction_id: str
    user_id: str
    amount: float
    currency: str
    timestamp: datetime

class Statistics(BaseModel):
    total_transactions: int
    average_transaction_amount: float
    top_transactions: list
