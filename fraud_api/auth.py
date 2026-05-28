# services/fraud_api/auth.py

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from jose import jwt

security = HTTPBearer()
SECRET = "SUPER_SECRET_KEY"

def get_current_tenant(credentials=Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET, algorithms=["HS256"])
        return payload["tenant_id"]
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")