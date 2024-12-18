from sqlalchemy import Column, DateTime, Float, String

from db.db_setup import Base


class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(String, primary_key=True, unique=True, nullable=False)
    user_id = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String(3), nullable=False)
    timestamp = Column(DateTime, nullable=False)
