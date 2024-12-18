from fastapi import FastAPI
from routes import router
from config import get_settings
from db.models import Base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

settings = get_settings()
app = FastAPI(title="Transaction Service", version="1.0.0")

engine = create_async_engine(settings.DATABASE_URL, echo=True, future=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

app.include_router(router)

@app.get("/")
def root():
    return {"message": "Transaction Service is running"}
