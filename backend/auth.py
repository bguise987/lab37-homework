import uuid
from datetime import datetime, timezone

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import User

# In-memory session store: token -> user_id (resets on server restart)
sessions: dict[str, int] = {}


def create_session(user_id: int) -> str:
    token = str(uuid.uuid4())
    sessions[token] = user_id
    return token


def delete_session(token: str) -> None:
    sessions.pop(token, None)


def get_current_user(
    authorization: str = Header(...),
    db: Session = Depends(get_db),
) -> User:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authorization header")
    token = authorization.removeprefix("Bearer ")
    user_id = sessions.get(token)
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


def require_company_access(user: User, company_id: int) -> None:
    if company_id not in user.company_ids:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
