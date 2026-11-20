from fastapi import FastAPI

app = FastAPI(title="Debate and Resolution Services")

@app.get("/health")
def health():
    return { "status": "ok" }

@app.get("/ready")
def ready():
    return { "status": "ready" }