from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import func, insert, delete
from db.models import Transaction

async def get_transaction_by_id(transaction_id: str, db: AsyncSession):
    """Fetch a transaction by its ID"""
    query = select(Transaction).where(Transaction.transaction_id == transaction_id)
    result = await db.execute(query)
    return result.scalar()

async def add_transaction(transaction_data: dict, db: AsyncSession):
    """Adds a new transaction to the database"""
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
    """Fetches the top 3 transactions by amount"""
    query = select(Transaction).order_by(Transaction.amount.desc()).limit(3)
    result = await db.execute(query)
    return result.scalars().all()


async def delete_all_transactions(db: AsyncSession):
    """Deletes all transactions from the database"""
    query = delete(Transaction)
    await db.execute(query)
