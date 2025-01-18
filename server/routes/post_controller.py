from server.models.posts import Post, PostSchema, CreateForm
from server.models.session import Session

from fastapi import APIRouter, Header
from fastapi.responses import JSONResponse

from server.libs.session import validate

router = APIRouter()

@router.post("/posts/create")
def create_post(body : CreateForm, x_session_header : str = Header(None)):

    token = validate(x_session_header)

    s = Session()
    post = Post()
    post_data = PostSchema(user_id=s.get_session(token).uid, content=body.content)

    result = post.create_post(post_data)

    return {
        "message" : "Post created successfully.",
        "post_id" : result
    }

@router.get("/posts")
def get_posts():
    post = Post()
    result = post.get_posts()

    return result

@router.get("/posts/user/{user_id}")
def get_posts_by_id(user_id: str):
    post = Post()
    result = post.get_posts_by_uid(user_id)

    return result

@router.get("/posts/find/{post_id}")
def get_post_by_id(post_id: str):
    post = Post()
    result = post.get_post_by_id(post_id)

    return result

@router.post("/posts/like/{post_id}")
def like_post(post_id : str, x_session_header : str = Header(None)):
    token = validate(x_session_header)

    s = Session()
    post = Post()
    liked = post.like_post(post_id, s.get_session(token).uid)

    if liked:
        return { "status" : "success", "message" : "Post liked successfully." }
    
    return { "status" : "success", "message" : "Post unliked successfully." }