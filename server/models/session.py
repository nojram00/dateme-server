from .base import BaseMongoModel
from pydantic import BaseModel
from .users import User, UserSchema
from bson import ObjectId
from uuid import uuid4

class LoginForm(BaseModel):
    username : str
    password : str

class SessionSchema(BaseModel):
    session_id : str

class Session(BaseMongoModel):
    collection_name = 'sessions'

    def create_session(self, credentials : LoginForm) -> str | None:
        creds = credentials.model_dump()
        userModel = User()
        user = userModel.get_user_by_username(creds['username'], creds['password'])

        if user:
            while True:
                session_id = str(uuid4())
                if not self.collection.find_one({ 'session_id' : session_id }):
                    break

            result = self.collection.insert_one({
                'user_id' : user.uid,
                'session_id' : session_id
            })

            session = self.collection.find_one({ '_id' : ObjectId(result.inserted_id) })

            return str(session['session_id'])
        
        print('User not found.')
        return None
    

    def get_session(self, session_id : str) -> UserSchema | None:
        session = self.collection.find_one({ "session_id" : session_id })
        if session:
            userModel = User()
            user = userModel.get_user_by_id(session['user_id'])
            return user
        return None

    def delete_session(self, session_id : str):
        self.collection.delete_one({ "session_id" : session_id })