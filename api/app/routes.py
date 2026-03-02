from fastapi import APIRouter, HTTPException

from .models import AccidentData, PredictionOutput
from .predictor import predictor

router = APIRouter()


@router.get("/health")
async def health_check():
    return {"status": "ok", "model_loaded": True}


@router.post("/predict", response_model=PredictionOutput)
async def get_prediction(data: AccidentData):
    try:
        # On appelle le prédicteur et on retourne son résultat
        result = predictor.predict(data.dict())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne : {str(e)}") from e
