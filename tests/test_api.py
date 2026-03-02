from fastapi.testclient import TestClient

from api.app.main import app

client = TestClient(app)


def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "model_loaded": True}


def test_predict_endpoint():
    """Test the prediction endpoint with valid data."""
    test_data = {
        "age_usager": 35.0,
        "vitesse_max_autorisee": 50.0,
        "nombre_de_voies": 2,
        "ceinture_ou_casque_attache": True,
        "en_agglomeration": True,
        "collision_frontale": False,
        "sexe_masculin": True,
        "luminosite_pleine_nuit": False,
        "meteo_normale": True,
    }

    response = client.post("/predict", json=test_data)
    assert response.status_code == 200

    result = response.json()
    assert "gravite_code" in result
    assert "label_francais" in result
    assert "probabilites" in result
    assert result["gravite_code"] in [1, 2, 3, 4]


def test_predict_endpoint_invalid_data():
    """Test the prediction endpoint with invalid data."""
    invalid_data = {
        "age_usager": -5.0,  # Invalid age
        "vitesse_max_autorisee": 50.0,
        "nombre_de_voies": 2,
        "ceinture_ou_casque_attache": True,
        "en_agglomeration": True,
        "collision_frontale": False,
        "sexe_masculin": True,
        "luminosite_pleine_nuit": False,
        "meteo_normale": True,
    }

    response = client.post("/predict", json=invalid_data)
    # Should handle the error gracefully
    assert response.status_code in [400, 422, 500]


def test_predict_endpoint_missing_data():
    """Test the prediction endpoint with missing required fields."""
    incomplete_data = {
        "age_usager": 35.0,
        "vitesse_max_autorisee": 50.0,
        # Missing other required fields
    }

    response = client.post("/predict", json=incomplete_data)
    assert response.status_code == 422  # Validation error
