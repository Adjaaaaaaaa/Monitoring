from app.routes import router
from fastapi import FastAPI

app = FastAPI(title="Accident Gravity Prediction API")

app.include_router(router)
