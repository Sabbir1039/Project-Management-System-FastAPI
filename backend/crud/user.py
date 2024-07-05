from sqlalchemy.orm import Session
from ..models.user import User
from ..schemas.user import UserCreateSchema
from ..utilities import get_hashed_password, verify_password

def create_user(db: Session, user: UserCreateSchema):
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=get_hashed_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(User).offset(skip).limit(limit).all()



