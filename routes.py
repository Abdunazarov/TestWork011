from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from db.schemas import TransactionIn
from db.db_setup import get_session
from services import (
    get_transaction_by_id,
    add_transaction,
    get_total_transactions,
    get_average_transaction_amount,
    get_top_transactions,
    delete_all_transactions,
    send_statistics_update_task
)
from auth import verify_api_key


router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"],
    dependencies=[Depends(verify_api_key)],
)

@router.post("")
async def create_transaction(data: TransactionIn, db: AsyncSession = Depends(get_session)):
    """
    Adds a new transaction to the database and enqueues a task to update statistics
    """
    transaction = await get_transaction_by_id(data.transaction_id, db)
    if transaction:
        raise HTTPException(status_code=400, detail="Transaction ID already exists")
    
    await add_transaction(data.model_dump(), db)
    await send_statistics_update_task(data.model_dump())
    
    return {"message": "Transaction received", "task_id": data.transaction_id}

    return {"message": "Transaction received", "task_id": task_id}

@router.get("/statistics")
async def fetch_statistics(db: AsyncSession = Depends(get_session)):
    """
    Fetches and combines statistics on total transactions, average amount, and top transactions
    """
    total_transactions = await get_total_transactions(db)
    average_transaction_amount = await get_average_transaction_amount(db)
    top_transactions = await get_top_transactions(db)

    top_transactions_list = [
        {"transaction_id": t.transaction_id, "amount": t.amount} for t in top_transactions
    ]

    return {
        "total_transactions": total_transactions,
        "average_transaction_amount": average_transaction_amount,
        "top_transactions": top_transactions_list,
    }

@router.delete("")
async def delete_transactions(db: AsyncSession = Depends(get_session)):
    """
    Deletes all transactions from the database
    """
    await delete_all_transactions(db)
    return {"message": "All transactions have been deleted successfully"}
