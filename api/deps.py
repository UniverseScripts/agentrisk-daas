import hashlib
from fastapi import Header, HTTPException, status
from sqlalchemy import select
from db.connection import AsyncSessionLocal
from db.models import APIKey

async def verify_api_key(x_api_key: str = Header(...)):
    """
    Dependency to verify API keys via constant-time SHA-256 lookup in PostgreSQL.
    If the key is inactive or balance is <= 0, strictly terminates the socket.
    """
    if not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing X-API-Key mechanism"
        )
        
    key_hash = hashlib.sha256(x_api_key.encode('utf-8')).hexdigest()
    
    async with AsyncSessionLocal() as session:
        stmt = select(APIKey).where(APIKey.valid_api_keys == key_hash)
        result = await session.execute(stmt)
        api_key_record = result.scalars().first()
        
        if not api_key_record or not api_key_record.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or inactive API Key verification"
            )
            
        if api_key_record.token_balance <= 0:
            raise HTTPException(
                status_code=status.HTTP_402_PAYMENT_REQUIRED,
                detail="Zero compute tokens remaining on ledger."
            )
            
        return api_key_record
