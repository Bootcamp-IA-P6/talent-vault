import time

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from src.api.routes import router
from src.monitoring.metrics import (
    api_request_duration_seconds,
    api_requests_total,
)

app = FastAPI(title="Talent Vault API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:8501",
    ],
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.middleware("http")
async def prometheus_middleware(request: Request, call_next):
    started = time.perf_counter()
    response = await call_next(request)
    elapsed = time.perf_counter() - started

    path = request.scope.get("route").path if request.scope.get("route") else request.url.path
    api_requests_total.labels(
        method=request.method,
        path=path,
        status=str(response.status_code),
    ).inc()
    api_request_duration_seconds.labels(method=request.method, path=path).observe(elapsed)
    return response


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/metrics")
def metrics() -> Response:
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


app.include_router(router)
