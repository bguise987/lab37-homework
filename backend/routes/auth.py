from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from auth import create_session, delete_session, get_current_user
from database import get_db
from models import User
from schemas import LoginRequest, LoginResponse

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
def login(body: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == body.username).first()
    if user is None or user.password != body.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    user.last_login_at = datetime.now(timezone.utc)
    db.commit()
    token = create_session(user.id)
    return LoginResponse(token=token, user_id=user.id)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(authorization: str = Header(...), _: User = Depends(get_current_user)):
    token = authorization.removeprefix("Bearer ")
    delete_session(token)
