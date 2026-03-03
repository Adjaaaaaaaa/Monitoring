from fastapi import APIRouter, HTTPException
import time

from .models import AccidentData, PredictionOutput
from .predictor import predictor
from .metrics import (
    track_prediction, track_http_error, track_age, track_speed, 
    track_confidence, health_checks_total, time_metric, model_prediction_duration_seconds
)

router = APIRouter()


@router.get("/health")
async def health_check():
    """Health check endpoint with metrics tracking."""
    health_checks_total.inc()
    return {"status": "ok", "model_loaded": True}


@router.post("/predict", response_model=PredictionOutput)
@time_metric(model_prediction_duration_seconds)
async def get_prediction(data: AccidentData):
    """Prediction endpoint with comprehensive metrics tracking."""
    try:
        # Track business metrics before prediction
        track_age(data.age_usager)
        track_speed(data.vitesse_max_autorisee)
        
        # Make prediction
        result = predictor.predict(data.dict())
        
        # Track success and confidence
        track_prediction(success=True)
        
        # Extract confidence from probabilities (max probability as confidence)
        if hasattr(result, 'probabilites') and result.probabilites:
            max_confidence = max(result.probabilites.values())
            track_confidence(max_confidence)
        
        return result
        
    except ValueError as e:
        # Track validation errors
        track_prediction(success=False)
        track_http_error("validation_error", 400)
        raise HTTPException(status_code=400, detail=f"Erreur de validation : {str(e)}") from e
        
    except KeyError as e:
        # Track missing data errors
        track_prediction(success=False)
        track_http_error("missing_data", 400)
        raise HTTPException(status_code=400, detail=f"Données manquantes : {str(e)}") from e
        
    except Exception as e:
        # Track server errors
        track_prediction(success=False)
        track_http_error("server_error", 500)
        raise HTTPException(status_code=500, detail=f"Erreur interne : {str(e)}") from e


# Additional endpoints for testing metrics
@router.get("/metrics-test")
async def metrics_test():
    """Test endpoint for generating various metrics."""
    # Generate some test data for metrics
    track_age(35.0)
    track_speed(50.0)
    track_confidence(0.85)
    track_prediction(success=True)
    
    return {"message": "Test metrics generated", "timestamp": time.time()}


@router.get("/error-test")
async def error_test(error_type: str = "validation"):
    """Test endpoint for generating error metrics."""
    if error_type == "validation":
        track_http_error("validation_error", 400)
        raise HTTPException(status_code=400, detail="Test validation error")
    elif error_type == "server":
        track_http_error("server_error", 500)
        raise HTTPException(status_code=500, detail="Test server error")
    else:
        track_http_error("unknown_error", 400)
        raise HTTPException(status_code=400, detail="Test unknown error")
