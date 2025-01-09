from fastapi import APIRouter
from server.models import users, session

router = APIRouter()

@router.get("/users")
def get_users():
    user = users.User()
    return user.get_users()

@router.post("/users/create")
def create_users(body : users.UserForm):
    user = users.User()
    return user.create_user(body)

@router.post("/users/login")
def login(body : session.LoginForm):
    s = session.Session()
    return { "session_id" : s.create_session(body) }

@router.post("/users/logout")
def logout(body : session.SessionSchema):
    s = session.Session()
    s.delete_session(body.session_id)
    return { "status" : "success" }