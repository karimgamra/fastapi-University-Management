from fastapi import APIRouter ,Depends , HTTPException
from app.services.user import get_db
from app.schemas.user import User , Student , Teacher
from sqlalchemy.orm import Session
from app.models.user import UserLogin , UserCreate , UserUpdate , StudentCreate
from app.core.security import verify_password , get_current_user , hash_password
from app.api.v1.auth import create_token
from app.database import Base ,engine

# Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


router = APIRouter()

   
@router.post("/login")
async def login (user :UserLogin , db:Session = Depends(get_db)) :
    db_user = db.query(User).filter(User.email == user.email).first()
    
    if not db_user :
        raise HTTPException(status_code=404 , detail="User not found")
    if not verify_password(user.password , db_user.password) :
    
        raise HTTPException(status_code=404 , detail="password not correct try again")
    token = create_token({"email":db_user.email})
    return {"access_token": token, "token_type": "bearer"}

        
    
@router.get("/user")
def get_users(db : Session = Depends(get_db)):
    users = db.query(User).all()
    return users


@router.post("/user")
async def create_user (user:UserCreate , db:Session = Depends(get_db) , current_user :User = Depends(get_current_user)) :
    
    if current_user.role != "admin" :
        raise HTTPException (status_code=404 , detail="admin just can create user")
    
    new_user = User(
        name = user.name,
        password = hash_password(user.password),
        email = user.email,
        role = user.role
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


# @router.get("/user/{user_id}")
# async def get_user_by_id (user_id :int , db:Session = Depends(get_db)) :
#     user = db.query(User).filter(User.id == user_id).first()
#     if not user :
#         raise HTTPException(status_code=404 ,detail="user not found")
#     return user
    
    
@router.post("/student")
async def create_student(student_id : int , student:StudentCreate , db : Session = Depends(get_db) , current_user :User = Depends(get_current_user)) :
    if current_user.role != "admin" :
        raise HTTPException (status_code=403 , detail="admin just can create user")
    
    db_student = db.query(User).filter(User.id == student_id).first()
    if not db_student :
        raise HTTPException(status_code=404 , detail="User not found")
    if db_student.role != "student" :
        raise HTTPException(status_code=401 , detail="this is id is not for student check your id again please")
        
    new_student = Student(
        user_id = student_id ,
        enrollment_year =  student.enrollment_year ,
        major   = student.major ,
        level  = student.level
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student
    
@router.post("/teacher")
async def create_student(teacher_id : int , teacher:StudentCreate , db : Session = Depends(get_db) , current_user :User = Depends(get_current_user)) :
    if current_user.role != "admin" :
        raise HTTPException (status_code=403 , detail="admin just can create user")
    
    db_teacher = db.query(User).filter(User.id == teacher_id).first()
    if not db_teacher :
        raise HTTPException(status_code=404 , detail="User not found")
    if db_teacher.role != "student" :
        raise HTTPException(status_code=401 , detail="this is id is not for student check your id again please")
        
    new_teacher = Student(
        user_id = teacher_id ,
        enrollment_year =  teacher.enrollment_year ,
        major   = teacher.major ,
        level  = teacher.level
    )
    db.add(new_teacher)
    db.commit()
    db.refresh(new_teacher)
    return new_teacher
    
    
    
    
@router.put("/user/{user_id}")
async def update_user (user_id : int , user :UserUpdate , db:Session = Depends(get_db) , current_user :User = Depends(get_current_user)) :
    
    if current_user.role != "admin" :
        raise HTTPException (status_code=403 , detail="admin just can create user")
    
    user_db = db.query(User).filter(User.id == user_id).first()
    
    if not user_db :
        raise HTTPException (status_code=404 , detail="user not found")
    
    update_data = user.dict(exclude_unset=True)
    for key , value in update_data.items() :
        setattr(user_db, key, value)

    
    
    db.commit()
    db.refresh(user_db)
    return user_db


@router.delete("/user/{user_id}")
async def delete_user (user_id :int , db:Session = Depends(get_db) , current_user :User = Depends(get_current_user)) :
    
    if current_user.role != "admin" :
        raise HTTPException (status_code=403 , detail="admin just can create user")
    
    user_db = db.query(User).filter(User.id == user_id).first()
    
    if not user_db :
        raise HTTPException (status_code=404 , detail="user not found")
    db.delete(user_db)
    db.commit()
    
    return {"message": "user deleted"}




@router.get("/user/paginated")
async def pagination(
    skip: int = 0,
    limit: int = 2,
    role: str | None = None,
    search: str | None = None,
    db: Session = Depends(get_db)
):
    skip = skip * limit
    all_users = db.query(User).all()
    paginated_users = all_users [skip : skip+limit]
    
    if role != None :
        paginated_users = [user for user in paginated_users if user.role == role]
        
    if search is not None:
        search_lower = search.lower()
        paginated_users = [
            user for user in paginated_users
            if search_lower in user.name.lower() or search_lower in user.email.lower()
        ]

    
    return paginated_users
