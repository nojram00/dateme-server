from server.models.posts import Post, PostSchema, CreateForm
from server.models.session import Session

from fastapi import APIRouter, Header
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/posts/create")
def create_post(body : CreateForm, x_session_header : str = Header(None)):

    token = x_session_header
    if token is None:
        return JSONResponse(status_code=401, content={
            "message" : "Please provide a valid session header with a session id",
            "code" : "err_no_x_session_header"
        })
    
    s = Session()
    if s.get_session(token) is None:
        return JSONResponse(status_code=404, content={
            "message" : "No session found with the given session id",
            "code" : "err_session_not_found"
        })

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
    result = post.get_posts_by_id(user_id)

    return result