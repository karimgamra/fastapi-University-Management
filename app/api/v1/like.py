import datetime
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
async def get_user_isLiked (post_id : int  , db:Session = Depends(get_db)) :
    
    post =  db.query(Post).filter(Post.id == post_id).first()
    if not post :
            raise HTTPException(status_code=404 , detail="Post not exit")
        
    db_users = (
            db.query(User)
            .join(Like , Like.user_id == User.id)
            .filter(Like.post_id == post_id)
            .all()
    )
    
    return db_users


@router.get("/users/{user_id}/likes/posts")
async def get_post_liked (user_id : int , db:Session = Depends(get_db)) :
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user :
            raise HTTPException(status_code=404 , detail="User not found")
        
    posts = (
            db.query(Post)
            .join(Like ,Post.id == Like.post_id)
            .filter(Like.user_id == user_id)
            .all()
    )
    
    return posts
    
    
    

@router.post("/like/toggle")
async def toggle_like(id_post: int, id_user: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == id_post).first()
    user = db.query(User).filter(User.id == id_user).first()

    if not user:
        raise HTTPException(status_code=404, detail="User Not Found")
    if not post:
        raise HTTPException(status_code=404, detail="Post Not Found")

    is_liked = db.query(Like).filter(Like.user_id == id_user, Like.post_id == id_post).first()

    if not is_liked:
        new_like = Like(user_id=id_user, post_id=id_post )
        db.add(new_like)
        db.commit()
        db.refresh(new_like)
        return {"message": "Post liked", "like": new_like}

    if is_liked:
        db.delete(is_liked)
        db.commit()
        return {"message": "Post unLiked"}

                
        
        
@router.get("/posts/{post_id}/likes/summary")
async def get_post_likes (post_id : int ,  db:Session = Depends(get_db)) :
        
        post = db.query(Post).filter(Post.id == post_id).first()
        if not post :
                raise HTTPException(status_code=403 , detail="Post Not Found")
        
        likes = (
        db.query(Like)
        .filter(Like.post_id == post_id)
        .all()
                 )

        user_infos = (
        db.query(User.id, User.name)
        .join(Like, Like.user_id == User.id)
        .filter(Like.post_id == post_id)
        .all()
                )
        
        
        return {
                "post_id" : post_id ,
                "total_liked" : len(likes) ,
                "liked by users" :[{'user_id' : uid , "name" :name } for uid , name in user_infos]        
        }
        

        
