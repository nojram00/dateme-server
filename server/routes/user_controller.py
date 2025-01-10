from fastapi import APIRouter, Header, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from server.models import users, session
from server.libs.session import validate

router = APIRouter()

@router.get("/users")
def get_users():
    user = users.User()
    return user.get_users()

@router.post("/users/register")
def create_users(body : users.UserForm):
    user = users.User()
    s = session.Session()
    created_user = user.create_user(body)
    session_id = s.create_session(session.LoginForm(
        username=created_user.username,
        password=body.password
    ))
    return { "session_id" : session_id }

@router.post("/users/login")
def login(body : session.LoginForm):
    s = session.Session()
    return { "session_id" : s.create_session(body) }

@router.post("/users/logout")
def logout(x_session_header : str = Header(None)):
    token = validate(x_session_header)

    s = session.Session()
    s.delete_session(token)
    return { "status" : "success" }

@router.get("/users/get_session")
def get_session(x_session_header : str = Header(None)):
    """
    Get the session data of the user based on a session Id Provided.
    """
    token = validate(x_session_header)

    s = session.Session()
    return s.get_session(token)

@router.get("/users/gender/{gender}")
def get_users_by_gender(gender : users.Gender, x_session_header :str=Header(None)):
    validate(x_session_header)

    u = users.User()
    results = u.get_users_by_gender(gender)

    return results
