from fastapi import FastAPI
from familymeet_common import ServiceSettings, install_common

settings = ServiceSettings(setting_name="debate")
app = FastAPI(title="Debate and Resolution Services")
install_common(app, settings)

@app.get("/health")
def health():
    return { "status": "ok" }

@app.get("/ready")
def ready():
    return { "status": "ready" }