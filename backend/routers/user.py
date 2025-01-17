from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..schemas.user import UserCreateSchema, UserResponseSchema, UserUpdateSchema
from ..database import get_db
from ..crud.user import create_user, get_user, get_user_by_email, get_users
from ..utilities import get_hashed_password
from ..models.user import User
from ..dependencies import get_current_user


router = APIRouter()

@router.post("/signup", response_model=UserResponseSchema)
def register_user(user: UserCreateSchema, db: Session = Depends(get_db)):
    try:
        db_user = get_user_by_email(db, email=user.email)
        if db_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
        return create_user(db=db, user=user)
    except Exception as e:
         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while fetching user by email")

@router.put("/update/{user_id}", response_model=UserResponseSchema)
def update_user(
    user_id: int,
    user: UserUpdateSchema,
    db: Session = Depends(get_db),
    curr_user: User = Depends(get_current_user)):
    
    if not curr_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    
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
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    curr_user: User = Depends(get_current_user)):
    
    if not curr_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    
    try:
        db_user = get_user(db, user_id=user_id)
        
        if db_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return db_user
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.get("/", response_model=List[UserResponseSchema])
def read_users(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    curr_user: User = Depends(get_current_user)):
    
    if not curr_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    
    try:
        users = get_users(db, skip=skip, limit=limit)
        
        if not users:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return users
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))