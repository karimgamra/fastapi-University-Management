from datetime import datetime , timedelta
from jose import jwt 

SECRET_KEY = "5cdc5fce472765ad953323d4e7858bf25dff3de5d6bda8132ef54feb8b7e3aac"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_token(data:dict) -> str :
    to_encode = data.copy()
    expire =  datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode ,key=SECRET_KEY , algorithm=ALGORITHM)