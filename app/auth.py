from datetime import datetime, timedelta
import jwt

SECRET_KEY = "entrix-secret"
ALGORITHM = "HS256"

def create_token(data: dict):
    payload = data.copy()
    payload.update({"exp": datetime.utcnow() + timedelta(hours=2)})
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
