from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime
from pydantic import ValidationError
from .database import get_db
from .crud.user import get_user_by_email
from .schemas.user import TokenPayload
from .utilities import ALGORITHM, JWT_SECRET_KEY
from .models.user import User

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scheme_name="JWT"
    )

def get_current_user_id(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> int:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
        
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        user = db.query(User).filter(User.email == token_data.sub).first()
        if user is None:
            raise credentials_exception
        
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user.id
