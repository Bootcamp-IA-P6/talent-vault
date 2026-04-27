from fastapi import FastAPI

from src.api.routes import router

app = FastAPI(title="Talent Vault API", version="0.1.0")


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(router)
