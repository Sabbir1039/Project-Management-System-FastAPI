from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..schemas.user import UserCreateSchema, UserResponseSchema, UserUpdateSchema
from ..database import get_db
from ..crud.user import create_user, get_user, get_user_by_email, get_users
from ..utilities import get_hashed_password


router = APIRouter()

@router.post("/signup", response_model=UserResponseSchema)
def register_user(user: UserCreateSchema, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db=db, user=user)

@router.put("/update/{user_id}", response_model=UserResponseSchema)
def update_user(user_id: int, user: UserUpdateSchema, db: Session = Depends(get_db)):
    try:
        db_user = get_user(db, user_id)
        if db_user:
            if user.username:
                db_user.username = user.username
            if user.email:
                db_user.email = user.email
            if user.password:
                db_user.hashed_password = get_hashed_password(user.password)
            db.commit()
            db.refresh(db_user)
            return db_user
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{user_id}", response_model=UserResponseSchema)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/", response_model=List[UserResponseSchema])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    return users