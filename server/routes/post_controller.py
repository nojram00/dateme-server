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

@router.get("/posts/user/{user_id}")
def get_posts_by_id(user_id: str):
    post = Post()
    result = post.get_posts_by_uid(user_id)

    return result