from .base import BaseMongoModel
from pydantic import BaseModel

class PostSchema(BaseModel):
    user_id: str
    content : str

class Post(BaseMongoModel):
    collection_name = 'posts'

    def create_post(self, data: PostSchema):
        d = data.model_dump()
        post = self.collection.insert_one(d)

        return str(post.inserted_id)