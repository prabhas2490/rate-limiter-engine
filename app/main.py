from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import router

app = FastAPI(title="Rate Limiter Engine")

app.include_router(router)

@app.get("/health")
def health():
    return {"status": "ok"}

app.mount("/", StaticFiles(directory="app/static", html=True), name="static")