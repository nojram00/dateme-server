from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from server.routes import user_controller, post_controller

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_controller.router)
app.include_router(post_controller.router)

@app.get("/")
def test():
    return "testing"


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)