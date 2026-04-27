from fastapi import FastAPI
from src.api.routes import router

app = FastAPI(
    title="Talent Vault API",
    version="0.1.0",
    description="API para consultar perfiles de personas procesados desde Kafka"
)

app.include_router(router)

@app.get("/health")
def health():
    return {"status": "ok"}