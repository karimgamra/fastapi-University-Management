from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.services.user import get_db
from app.schemas.user import User 

my_CryptContext = CryptContext(schemes=["bcrypt"] , deprecated="auto")

def hash_password (password : str) -> str :
    return my_CryptContext.hash(password)
    
    
def verify_password (plain:str ,hashed: str ) -> bool :
    return my_CryptContext.verify(plain , hashed)



SECRET_KEY = "5cdc5fce472765ad953323d4e7858bf25dff3de5d6bda8132ef54feb8b7e3aac"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_current_user (token :str = Depends(oauth2_scheme) , db:Session = Depends(get_db)) :
    
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
    )
    try :
        payload = jwt.decode(token , key=SECRET_KEY , algorithms=ALGORITHM)
        email = payload.get("email")
        if not email :
            raise credentials_exception
        
        
    except JWTError :
        raise credentials_exception
    user = db.query(User).filter(User.email == email).first()
    if user is None :
        raise credentials_exception
    
    return user

    