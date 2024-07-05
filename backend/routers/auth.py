from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from ..database import get_db
from ..crud.user import authenticate_user
from ..schemas.user import TokenSchema
from ..models.user import User
from ..utilities import (
    verify_password,
    create_access_token,
    create_refresh_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_MINUTES
    )

router = APIRouter()


@router.post('/token', summary="Create access and refresh tokens for user", response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    user = authenticate_user(db, form_data.username, form_data.password)
   
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    hashed_pass = user.hashed_password
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
        
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    
    return {
        "access_token": create_access_token(user.email,  expires_delta=access_token_expires),
        "refresh_token": create_refresh_token(user.email,  expires_delta=refresh_token_expires),
        "token_type": "bearer"
    }
