from pydantic import BaseModel , Field
from typing import Literal , Optional

class UserLogin (BaseModel) :
    email : str
    password : str
    
    
class UserCreate (BaseModel) :
    name :str
    role : Literal["student", "teacher", "admin"]
    email :str
    password : str
    
    
class UserUpdate (BaseModel) :
    name :str = Optional[None]
    role : str =Optional[None]
    email :str = Optional[None]
    password : str = Optional[None]
    

class StudentCreate (BaseModel) :
    enrollment_year : str
    major  :str
    level : str