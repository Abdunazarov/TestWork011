import redis
import json
import asyncio
from db.db_setup import get_session
from config import get_settings
from services import add_transaction, get_total_transactions, get_average_transaction_amount, get_top_transactions

settings = get_settings()
redis_client = redis.Redis.from_url(settings.REDIS_URL)

async def process_transaction_task(transaction: dict):
    """
    Process a single transaction by saving it and calculating statistics.
    """
    session_generator = get_session()
    db = await anext(session_generator)
    try:
        await add_transaction(transaction, db)
        print(f"Transaction saved: {transaction}")

        total = await get_total_transactions(db)
        average = await get_average_transaction_amount(db)
        top = await get_top_transactions(db)

        print({
            "total_transactions": total,
            "average_transaction_amount": average,
            "top_transactions": [
                {"transaction_id": t.transaction_id, "amount": t.amount} for t in top
            ]
        })
    finally:
        await db.close() 

async def process_transaction_tasks():
    """
    Continuously process transaction tasks from the Redis queue.
    """
    while True:
        task_data = redis_client.lpop("transaction_tasks")
        if task_data:
            transaction = json.loads(task_data)
            print(f"Processing transaction: {transaction}")
            await process_transaction_task(transaction)
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(process_transaction_tasks())
