from fastapi import APIRouter, Header, HTTPException, status
from fastapi.responses import JSONResponse
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
def logout(x_session_header : str = Header(None)):
    s = session.Session()

    token = x_session_header

    if token is None:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={ 
                "status" : "error", 
                "message" : "Please provide a valid session header with a session id" ,
                "code" : "err_no_x_session_header"
            })
    
    if s.get_session(x_session_header) is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={ 
                "status" : "error", 
                "message" : "No session found with the given session id" ,
                "code" : "err_session_not_found"
            })

    s.delete_session(token)
    return { "status" : "success" }

@router.get("/users/get_session")
def get_session(x_session_header : str = Header(None)):
    s = session.Session()
    token = x_session_header
    if token is None:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={ 
                "status" : "error", 
                "message" : "Please provide a session header with a session id" ,
                "code" : "err_no_x_session_header"
            })
    
    if s.get_session(token) is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={ 
                "status" : "error", 
                "message" : "No session found with the given session id" ,
                "code" : "err_session_not_found"
            })

    return s.get_session(token)