from fastapi import FastAPI
from routes.cooking import router as cooking_router

app = FastAPI(
    title="AI Cooking Assistant",
    version="1.0.0"
)

app.include_router(cooking_router)


@app.get("/")
def home():
    return {
        "message": "AI Cooking Assistant Running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }