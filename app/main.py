import os
import time
import logging
from fastapi import FastAPI, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = FastAPI(title="EKS SRE Demo App")

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

REQUEST_COUNT = Counter(
    "sre_demo_requests_total",
    "Total HTTP requests",
    ["endpoint"]
)

REQUEST_LATENCY = Histogram(
    "sre_demo_request_latency_seconds",
    "Request latency in seconds",
    ["endpoint"]
)


@app.get("/")
def root():
    REQUEST_COUNT.labels(endpoint="/").inc()
    return {
        "service": "eks-sre-platform",
        "message": "SRE demo application running on Kubernetes",
        "version": os.getenv("APP_VERSION", "local")
    }


@app.get("/healthz")
def healthz():
    REQUEST_COUNT.labels(endpoint="/healthz").inc()
    return {"status": "healthy"}


@app.get("/readyz")
def readyz():
    REQUEST_COUNT.labels(endpoint="/readyz").inc()
    return {"status": "ready"}


@app.get("/version")
def version():
    REQUEST_COUNT.labels(endpoint="/version").inc()
    return {
        "version": os.getenv("APP_VERSION", "local"),
        "commit_sha": os.getenv("GIT_SHA", "unknown")
    }


@app.get("/slow")
def slow():
    REQUEST_COUNT.labels(endpoint="/slow").inc()
    with REQUEST_LATENCY.labels(endpoint="/slow").time():
        # CPU-intensive computation to trigger HPA scaling
        result = sum(i * i for i in range(500000))
    return {"message": "slow response generated", "result": result}


@app.get("/error")
def error():
    REQUEST_COUNT.labels(endpoint="/error").inc()
    logging.error("Simulated application error triggered")
    return Response(
        content='{"error":"simulated failure"}',
        media_type="application/json",
        status_code=500
    )


@app.get("/log")
def log():
    REQUEST_COUNT.labels(endpoint="/log").inc()
    logging.info("Structured log test event generated")
    return {"message": "log event generated"}


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)