from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta

from app.database import get_db
from app import services, schemas, models

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/signup")
def signup(payload: schemas.user.UserCreate, db: Session = Depends(get_db)):
    existing = services.auth.get_user_by_email(db, payload.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = services.auth.create_user(db, payload.name, payload.email, payload.password, payload.role)
    return {"user": schemas.user.UserOut.from_orm(user)}


@router.post("/login")
def login(payload: schemas.user.UserLogin, db: Session = Depends(get_db)):
    user = services.auth.authenticate_user(db, payload.email, payload.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect credentials")
    token = services.auth.create_access_token({"sub": str(user.id), "role": user.role})
    return {"access_token": token, "token_type": "bearer", "user": schemas.user.UserOut.from_orm(user)}


from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
import os

security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, services.auth.SECRET_KEY, algorithms=[services.auth.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate token")
    user = db.query(models.User).filter(models.User.id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


@router.get("/me")
def me(user: object = Depends(get_current_user)):
    # return user info
    return {"user": schemas.user.UserOut.from_orm(user)}
