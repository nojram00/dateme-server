from server.models.posts import Post, PostSchema

from fastapi import APIRouter

router = APIRouter()

@router.post("/posts/create")
def create_post(body : PostSchema):
    post = Post()
    result = post.create_post(body)

    return {
        "message" : "Post created successfully.",
        "post_id" : result
    }