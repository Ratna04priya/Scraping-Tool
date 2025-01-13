from fastapi import HTTPException, Header

def authenticate(token: str = Header(...)):
    if token != settings["API_TOKEN"]:
        raise HTTPException(status_code=401, detail="Invalid token")
