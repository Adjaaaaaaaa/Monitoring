from fastapi import FastAPI
from .routes import router
from .metrics import setup_metrics, update_uptime
import uvicorn

app = FastAPI(title="Accident Gravity Prediction API")

# Setup Prometheus metrics
setup_metrics(app)

app.include_router(router)

@app.on_event("startup")
async def startup_event():
    """Initialize metrics on application startup."""
    update_uptime()

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on application shutdown."""
    pass
