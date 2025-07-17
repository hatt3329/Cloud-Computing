from fastapi import FastAPI, Header, Cookie, Response
from typing import Optional

app = FastAPI(title="Header/Cookie API")

# return user agent from header
@app.get("/user-agent")
def get_user_agent(user_agent: Optional[str] = Header(None)):
    return {"User-Agent": user_agent}

# set cookie
@app.get("/set-cookie")
def set_cookie(response: Response):
    response.set_cookie(key="visited", value="yes")
    return {"message": "Cookie 'visited' has been set"}

# read cookie
@app.get("/check-cookie")
def check_cookie(visited: Optional[str] = Cookie(None)):
    if visited:
        return {"message": "Welcome back!", "visited": visited}
    return {"message": "Welcome!"}

# require custom header
@app.get("/secure-header")
def secure_route(x_client_token: Optional[str] = Header(None)):
    if x_client_token == "secret123":
        return {"status": "access granted"}
    return {"status": "access denied, invalid token"}

# return the muliple headers along with cookie
@app.get("/multi-info")
def multi_info(
    accept_language: Optional[str] = Header(None),
    referer: Optional[str] = Header(None),
    session_id: Optional[str] = Cookie(None)
):
    return {
        "Accept-Language": accept_language,
        "Referer": referer,
        "Session ID": session_id
    }