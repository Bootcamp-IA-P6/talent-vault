from fastapi import FastAPI
from fastapi.responses import Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
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

@app.get("/metrics")
def metrics():
    """Endpoint de métricas para Prometheus."""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)