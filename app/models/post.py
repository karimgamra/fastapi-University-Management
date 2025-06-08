from pydantic import BaseModel , Field
from typing import Literal , Optional
from datetime import date

class CreatePost (BaseModel) :
    title : str
    content : str
  
class UpdatePost(BaseModel) :
    title : str = Optional[None]
    content : str = Optional[None]