from fastapi import APIRouter , Depends , HTTPException 
from sqlalchemy.orm import Session
from app.services.user import get_db
from app.models.post import CreatePost , UpdatePost
from app.schemas.user import Post , User
from datetime import datetime
from app.core.security import get_current_user


router = APIRouter()


@router.post("/posts")
async def create_post (author_id:int , post : CreatePost  ,db :Session = Depends(get_db)) :
    db_user = db.query(User).filter(User.id == author_id).first()
    if not db_user :
        raise HTTPException(status_code=404 , detail="User Not Found")
    
    new_post = Post(
        title = post.title , 
        content = post.content,
        created_at =datetime.utcnow() , 
        author_id = author_id , 
        
        )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
    
    
    
@router.get("/posts")
async def get_all_posts (
    skip :int = 0,
    limit :int =  2,
    search :str | None =None ,
    db : Session = Depends(get_db)
):
    all_posts = db.query(Post).all()
    paginated_post = all_posts[skip : limit+skip]
    if search != None :
        paginated_post = [post for post in all_posts if post.title.lower() == search.lower()]
    
    return paginated_post

@router.get("/post")
async def get_post_by_id(user_id :int , db : Session = Depends(get_db)) :
    post = db.query(Post).filter(Post.id == user_id).first()
    if not post :
        raise HTTPException(status_code=404 , detail="post not found")
    
    return post
    
    
@router.put("/post/{post_id}")
async def update_post(
    post_id: int,
    post: UpdatePost,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    
    if db_post.author_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to update this post")

    
    update_data = post.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_post, key, value)

    db.commit()
    db.refresh(db_post)

    return db_post

    
@router.delete("/post/{post_id}")
async def delete_post( 
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):
    
    db_post = db.query(Post).filter(Post.id == post_id).first()
    
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    
    if db_post.author_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to update this post")
    db.delete(db_post)
    db.commit()
    
    return db_post