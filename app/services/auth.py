from fastapi import Header, HTTPException
from app.supabase import supabase

async def get_current_user(authorization:str = Header(...)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header is missing")

    token = authorization.replace("Bearer ", "")
    if not token:
        raise HTTPException(status_code=401, detail="Token is missing")

    data = supabase.auth.get_user(token)

    if not data:
        return None

    google_user = data.user

    return google_user