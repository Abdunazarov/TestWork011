from sqlalchemy.ext.asyncio import AsyncSession
import heapq
from sqlalchemy.future import select
from sqlalchemy.sql import func, insert, delete
from db.models import Transaction
from config import get_settings
import json


from datetime import datetime
from redis import Redis

settings = get_settings()
redis_client = Redis.from_url(settings.REDIS_URL)

async def send_statistics_update_task(transaction_data: dict):
    """
    Sends the transaction task to Redis for processing.
    """
    if "timestamp" in transaction_data and isinstance(transaction_data["timestamp"], datetime):
        transaction_data["timestamp"] = transaction_data["timestamp"].isoformat()

    redis_client.rpush("transaction_tasks", json.dumps(transaction_data))


async def get_transaction_by_id(transaction_id: str, db: AsyncSession):
    """Fetch a transaction by its ID"""
    query = select(Transaction).where(Transaction.transaction_id == transaction_id)
    result = await db.execute(query)
    return result.scalar()

async def add_transaction(transaction_data: dict, db: AsyncSession):
    """Adds a new transaction to the database"""
    
    if isinstance(transaction_data.get("timestamp"), str):
        transaction_data["timestamp"] = datetime.fromisoformat(transaction_data["timestamp"])

    query = insert(Transaction).values(**transaction_data)
    await db.execute(query)

async def get_total_transactions(db: AsyncSession):
    """Fetches the total number of transactions"""
    query = select(func.count(Transaction.transaction_id))
    result = await db.execute(query)
    return result.scalar()

async def get_average_transaction_amount(db: AsyncSession):
    """Fetches the average transaction amount"""
    query = select(func.avg(Transaction.amount))
    result = await db.execute(query)
    return result.scalar()

async def get_top_transactions(db: AsyncSession):
    """Fetches the top 3 transactions using a min-heap for better performance with large data sets"""
    query = select(Transaction).order_by(Transaction.amount.desc())
    result = await db.execute(query)
    top_transactions = []
    
    async for transaction in result.scalars():
        if len(top_transactions) < 3:
            heapq.heappush(top_transactions, transaction)
        else:
            heapq.heappushpop(top_transactions, transaction)
    
    return top_transactions

async def delete_all_transactions(db: AsyncSession):
    """Deletes all transactions from the database"""
    query = delete(Transaction)
    await db.execute(query)
