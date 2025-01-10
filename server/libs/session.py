from fastapi.responses import JSONResponse
from server.models.session import Session
from fastapi import status, HTTPException
from datetime import datetime

def validate(token : str | None):
    """
    Validates the session token and returns the token if it is valid.
    """
    s = Session()

    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={
            "status" : "error", 
            "message" : "Please provide a valid session header with a session id" ,
            "code" : "err_no_x_session_header"
        })
    
    if s.get_session_expiry(token) < datetime.now():
        s.delete_session(token)
        raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT, detail={
            "status" : "error", 
            "message" : "Session has expired" ,
            "code" : "err_session_expired"
        })

    if s.get_session(token) is None:
        s.delete_session(token)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
            "status" : "error", 
            "message" : "No user found with the given session id" ,
            "code" : "err_session_not_found"
        })
    
    return token