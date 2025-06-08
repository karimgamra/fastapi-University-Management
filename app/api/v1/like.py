from fastapi import APIRouter , Depends , HTTPException
from app.core.security import get_current_user
from app.schemas.user import Post , User , Like
from sqlalchemy.orm import Session
from app.services.user import get_db


# current_user:User = Depends(get_current_user)

router = APIRouter()


@router.post("/like/")
async def create_like (id_post : int , id_user :int ,db:Session = Depends(get_db) ) :
    
    post =  db.query(Post).filter(Post.id == id_post).first()
    user = db.query(User).filter(User.id == id_user).first()
    is_liked = db.query(Like).filter(Like.user_id == id_user).first()
    
    if not post :
            raise HTTPException(status_code=404 , detail="Post not exit")
    
    
    if not user :
            raise HTTPException(status_code=404 , detail="User not found")
    
        
    if is_liked :
            raise HTTPException(status_code=409 , detail="post already liked by this user")
        
    new_like = Like(
        user_id = id_user,
        post_id = id_post ,
        )
    
    db.add(new_like)
    db.commit()
    db.refresh(new_like)
    
    return new_like


@router.delete("/like/") 
async def delete_like (id_post : int , id_user :int ,db:Session = Depends(get_db)) :
    
    post =  db.query(Post).filter(Post.id == id_post).first()
    user = db.query(User).filter(User.id == id_user).first()
    is_liked = db.query(Like).filter(Like.user_id == id_user).first()
    
    
    if not post :
            raise HTTPException(status_code=404 , detail="Post not exit")
    
    
    if not user :
            raise HTTPException(status_code=404 , detail="User not found")
    
        
    if not is_liked :
            raise HTTPException(status_code=404 , detail="post do not like by this user")
        
    db.delete(is_liked)
    db.commit()
    return is_liked


@router.get("/posts/{post_id}/likes/count")
async def get_like_for_post(post_id : int , db:Session = Depends(get_db)) :
    
    post =  db.query(Post).filter(Post.id == post_id).first()
    if not post :
            raise HTTPException(status_code=404 , detail="Post not exit")

    all_like = db.query(Like).filter(Like.post_id == post_id).count()
    
    if len(all_like) == 0 :
        return {"message": "No one has liked this post yet."}

    
    return all_like


@router.get("/posts/{post_id}/likes/users")
async def get_user_isLiked (post_id : int , db:Session = Depends(get_db)) :
    
    post =  db.query(Post).filter(Post.id == post_id).first()
    if not post :
            raise HTTPException(status_code=404 , detail="Post not exit")
        
    db_users = db.query(Like).filter(Like.post_id == post_id).count()
    
    return db_users


@router.get("/users/{user_id}/likes/posts")
async def get_post_liked (user_id : int , db:Session = Depends(get_db)) :
    
    user = db.query(User).filter(User.id == user_id).first().all()
    if not user :
            raise HTTPException(status_code=404 , detail="User not found")
        
    post = db.query(Like).filter(Like.user_id == user_id)
    
    return post
    
    
    

