from fastapi import Header, HTTPException, Depends
from config import get_settings

settings = get_settings()

async def verify_api_key(authorization: str = Header(...)):
    """
    Validates the API key provided in the Authorization header
    """
    if not authorization.startswith("ApiKey "):
        raise HTTPException(
            status_code=401, detail="Invalid Authorization header format"
        )
    
    api_key = authorization[len("ApiKey "):].strip()
    
    if api_key != settings.API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
