from server.models.base import BaseMongoModel
from pydantic import BaseModel
from bson import ObjectId
from server.models.users import UserSchema

class PostSchema(BaseModel):
    user_id: str
    content : str

class PostData(BaseModel):
    post_id: str
    user_id: str
    content : str
    likes : int = 0
    user_likes : list[str] = []
    user_info : UserSchema = None

class CreateForm(BaseModel):
    content : str

class Post(BaseMongoModel):
    collection_name = 'posts'

    def create_post(self, data: PostSchema):
        d = data.model_dump()
        post = self.collection.insert_one(d)

        return str(post.inserted_id)
    
    def get_posts_by_uid(self, user_id: str) -> list[PostData]:
        # results = self.collection.find({ 'user_id' : user_id })
        results = self.collection.aggregate([
            {
                "$match" : { 'user_id' : user_id }
            },
            {
                "$project" : {
                    "post_id" : "$_id",
                    "user_id" : "$user_id",
                    "content" : "$content",
                    "like_count" : {
                        "$size" : "$likes"
                    },
                    "user_likes" : "$likes"
                }
            }
        ])
        posts = []
        for result in results:
            result['post_id'] = str(result['post_id'])
            posts.append(PostData(
                post_id=result['post_id'],
                user_id=result['user_id'],
                content=result['content'],
                likes=result['like_count'],
                user_likes=result['user_likes']
            ))
        return posts
    
    def get_post_by_id(self, post_id : str) -> PostData | None:
        # result = self.collection.find_one({ '_id' : ObjectId(post_id) })

        result = self.collection.aggregate([
            {
                "$match" : { '_id' : ObjectId(post_id) }
            },
            {
                "$addFields" : {
                    "user_id" : { "$toObjectId" : "$user_id" }
                }
            },
            {
                "$lookup" : {
                    "from" : "users",
                    "localField" : "user_id",
                    "foreignField" : "_id",
                    "as" : "user_info"
                }
            },
            {
                "$project" : {
                    "post_id" : "$_id",
                    "user_id" : "$user_id",
                    "content" : "$content",
                    "likes" : { "$size" : 
                            {
                                "$ifNull" : [ "$likes", [] ]
                            }
                    },
                    "user_likes" : {
                        "$ifNull" : [ "$likes", [] ]
                    }
                }
            },
            {
                "$limit" : 1
            }
        ]).to_list(1)[0]

        if result:
            return PostData(
                post_id=str(result['post_id']),
                user_id=str(result['user_id']),
                content=result['content'],
                likes=result['likes'],
                user_likes=result['user_likes'],
                user_info=UserSchema(
                    uid=str(result["user_info"][0]["_id"]), 
                    username=result["user_info"][0]["username"], 
                    email=result["user_info"][0]["email"],
                    first_name=result["user_info"][0]["first_name"],
                    last_name=result["user_info"][0]["last_name"],
                    )
            )
        return None
    
    def like_post(self, post_id : str, user_id : str):
        post = self.collection.find_one({ '_id' : ObjectId(post_id) })
        if post:
            likes = post.get('likes', [])
            if user_id not in likes:
                likes.append(user_id)
                self.collection.update_one({ '_id' : ObjectId(post_id) }, { '$set' : { 'likes' : likes } })
                return True
            else:
                likes.remove(user_id)
                self.collection.update_one({ '_id' : ObjectId(post_id) }, { '$set' : { 'likes' : likes } })
                return False
    
    def get_posts(self) -> list[PostData]:

        results = self.collection.aggregate([
            {
                "$addFields" : {
                    "user_id" : { "$toObjectId" : "$user_id" }
                }
            },
            {
                "$project" : {
                    "post_id" : "$_id",
                    "user_id" : "$user_id",
                    "content" : "$content",
                    "likes" : { "$size" : {
                        "$ifNull" : [ "$likes", [] ]
                    } 
                    },
                    "user_likes" : {
                        "$ifNull" : [ "$likes", [] ]
                    }
                }
            },
            {
                "$lookup" : {
                    "from" : "users",
                    "localField" : "user_id",
                    "foreignField" : "_id",
                    "as" : "user_info"
                }
            },
        ])

        posts = []
        for result in results:
            if result['user_info'] != None:
                result['_id'] = str(result['_id'])
                user_info = result["user_info"][0]
                if(len(result['user_likes']) == 0):
                    result['user_likes'] = []
                posts.append(PostData(
                    post_id=result['_id'],
                    user_id=str(result['user_id']),
                    content=result['content'],
                    likes=result['likes'],
                    user_likes=result['user_likes'],
                    user_info=UserSchema(
                        uid=str(user_info["_id"]), 
                        username=user_info["username"], 
                        email=user_info["email"],
                        first_name=user_info["first_name"],
                        last_name=user_info["last_name"],
                        gender=user_info['gender']
                    )
                ))
        print(posts)
        return posts
    
    def get_post_like_count(self, post_id : str) -> int:
        post = self.collection.aggregate([

        ])
    
    @staticmethod
    def instance():
        return Post()
    


if __name__ == '__main__':
    posts = Post()

    print(posts.get_posts())