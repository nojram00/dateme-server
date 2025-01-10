from fastapi.responses import JSONResponse
from server.models.session import Session
from fastapi import status, HTTPException

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

    if s.get_session(token) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
            "status" : "error", 
            "message" : "No session found with the given session id" ,
            "code" : "err_session_not_found"
        })
    
    return token