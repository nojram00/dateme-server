from .base import BaseMongoModel
from pydantic import BaseModel

class PostSchema(BaseModel):
    user_id: str
    content : str

class PostData(BaseModel):
    post_id: str
    user_id: str
    content : str

class CreateForm(BaseModel):
    content : str

class Post(BaseMongoModel):
    collection_name = 'posts'

    def create_post(self, data: PostSchema):
        d = data.model_dump()
        post = self.collection.insert_one(d)

        return str(post.inserted_id)
    
    def get_posts_by_id(self, user_id: str) -> list[PostData]:
        results = self.collection.find({ 'user_id' : user_id })
        posts = []
        for result in results:
            result['_id'] = str(result['_id'])
            posts.append(PostData(
                post_id=result['_id'],
                user_id=result['user_id'],
                content=result['content']
            ))
        return posts