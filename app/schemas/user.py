from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime, Text, UniqueConstraint, func
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"  

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)  
    role = Column(String, nullable=False)
    

    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

  
    student = relationship(
        "Student",
        back_populates="user",
        uselist=False,           
        cascade="all, delete",   
        passive_deletes=True     
    )

    
    teacher = relationship(
        "Teacher",
        back_populates="user",
        uselist=False,
        cascade="all, delete",
        passive_deletes=True
    )

    posts = relationship("Post" , back_populates="user" ,uselist=True)
    likes = relationship("Like", back_populates="user", cascade="all, delete", passive_deletes=True)

    

class Student(Base):
    __tablename__ = "students"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)

    enrollment_year = Column(String, nullable=False)
    major = Column(String, nullable=False)
    level = Column(String, nullable=False)

    
    user = relationship("User", back_populates="student")



class Teacher(Base):
    __tablename__ = "teachers"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)

    department = Column(String, nullable=False)
    hire_date = Column(Date, nullable=False)  

    
    user = relationship("User", back_populates="teacher")


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    user = relationship("User", back_populates="posts")
    likes = relationship("Like", back_populates="post", cascade="all, delete", passive_deletes=True)


    
class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"))
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="likes")
    post = relationship("Post", back_populates="likes")

    __table_args__ = (
        UniqueConstraint("user_id", "post_id", name="unique_user_post_like"),
    )


