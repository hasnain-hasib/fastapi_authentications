from fastapi import HTTPException
from app.config.security import hash_password
from app.models.user import User
from sqlalchemy.orm import Session

def create_user_account(data, session: Session):
    user_exist = session.query(User).filter(User.email == data.email).first()
    
    if user_exist:
        raise HTTPException(status_code=400, detail="Email already exists.")
    
    user = User()
    user.name = data.name
    user.email = data.email
    user.password = hash_password(data.password)
    user.is_active = False
    
    session.add(user)
    session.commit()
    session.refresh(user)
    
    return user
