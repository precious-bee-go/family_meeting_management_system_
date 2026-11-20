from fastapi import FastAPI

app = FastAPI(title="bff resolutions")

@app.get("/health")
def health():
    return { "status": "ok" }

@app.get("/ready")
def ready():
    return { "status": "ok" }