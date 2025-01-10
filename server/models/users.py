from .base import BaseMongoModel
from pydantic import BaseModel
from bson import ObjectId
from enum import Enum

class Gender(str, Enum):
    male = "male"
    female = "female"
    other = "other"

class UserForm(BaseModel):
    username : str
    email : str
    password : str
    first_name : str
    last_name : str
    gender : Gender

class UserSchema(BaseModel):
    """
    A basic data response model for user.

    Attributes:
        uid (str): The user id.
        username (str): The username.
        email (str): The email.
        first_name (str): The first name.
        last_name (str): The last name.
    """
    uid : str
    username : str
    email : str
    first_name : str
    last_name : str
    gender : Gender

class User(BaseMongoModel):
    collection_name = 'users'

    def get_users(self) -> list[UserSchema]:
        """
        Returns a list of users from the database.
        """
        results = self.collection.find()
        users = []
        for result in results:
            user = UserSchema(
                uid=str(result['_id']),
                username=result['username'], 
                email=result['email'], 
                first_name=result['first_name'], 
                last_name=result['last_name'],
                gender=result['gender']
                )
            users.append(user)
        return users
    
    def create_user(self, user : UserForm) -> UserSchema | None:
        """
        Creates a new user and insert to database.
        """
        try:
            if self.collection.find_one({"username": user.username}):
                raise ValueError('Username already exists.')

            user_dict = user.model_dump()
            result = self.collection.insert_one(user_dict)
            return UserSchema(
                uid=str(result.inserted_id),
                username=user_dict['username'], 
                email=user_dict['email'], 
                first_name=user_dict['first_name'], 
                last_name=user_dict['last_name'],
                gender=user_dict['gender']
            )
        except Exception as e:
            print(e)
            return None
        
    def get_user_by_username(self, username : str, password : str) -> UserSchema | None:
        """
        Returns a user by username.
        """
        result = self.collection.find_one({
            "username": username,
            "password": password
        })

        if result:
            return UserSchema(
                uid=str(result['_id']),
                username=result['username'], 
                email=result['email'], 
                first_name=result['first_name'], 
                last_name=result['last_name'],
                gender=result['gender']
            )
        
        return None
    
    def get_user_by_id(self, uid : str) -> UserSchema | None:
        """
        Returns a user by user id.
        """
        result = self.collection.find_one({
            "_id": ObjectId(uid)
        })

        if result:
            return UserSchema(
                uid=str(result['_id']),
                username=result['username'], 
                email=result['email'], 
                first_name=result['first_name'], 
                last_name=result['last_name'],
                gender=result['gender']
            )
        
        return None
    
    def get_users_by_gender(self, gender : Gender) -> list[UserSchema]:
        """
        Returns a list of users based on gender
        """
        results = self.collection.find({ "gender" : gender })

        users = []
        if results:
            for result in results:
                users.append(UserSchema(
                    uid=str(result['_id']),
                    username=result['username'], 
                    email=result['email'], 
                    first_name=result['first_name'], 
                    last_name=result['last_name'],
                    gender=result['gender']
                ))
        
        return users