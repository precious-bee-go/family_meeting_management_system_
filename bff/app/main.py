from fastapi import FastAPI
from familymeet_common import ServiceSettings, install_common

settings = ServiceSettings(service_name="bff")
app = FastAPI(title="GraphQL BFF")
install_common(app, settings)

@app.get("/health")
def health():
    return { "status": "ok" }

@app.get("/ready")
def ready():
    return { "status": "ok" }