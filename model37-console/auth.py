import os
from fastapi import Header, HTTPException

API_TOKEN = os.getenv("API_TOKEN", "change_me")

def check_token(authorization: str = Header(default="")):
    parts = authorization.split()
    if len(parts) == 2 and parts[0].lower() == "bearer" and parts[1] == API_TOKEN:
        return True
    raise HTTPException(status_code=401, detail="Unauthorized")
