from fastapi import FastAPI

from routes import router

app = FastAPI(title="Transaction Service", version="1.0.0")

app.include_router(router)


@app.get("/")
def root():
    return {"message": "Transaction Service is running"}
