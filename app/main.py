from fastapi import FastAPI
from app.api.v1 import user , post , like

app = FastAPI(title="My FastAPI Project")

# Include routers
app.include_router(user.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(post.router , prefix="/api/v1/posts" , tags=["posts"])
app.include_router(like.router , prefix="/api/v1/like" , tags=["likes"])
