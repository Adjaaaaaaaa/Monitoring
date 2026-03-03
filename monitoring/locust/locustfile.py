from locust import HttpUser, task, between
import random
import json

class AccidentPredictionUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        """Called when a user starts"""
        self.client.get("/health")
    
    @task(3)
    def predict_accident(self):
        """Main prediction task - 70% of traffic"""
        # Generate realistic test data
        data = {
            "age_usager": random.uniform(18, 80),
            "vitesse_max_autorisee": random.choice([30, 50, 70, 90, 110, 130]),
            "nombre_de_voies": random.randint(1, 4),
            "ceinture_ou_casque_attache": random.choice([True, False]),
            "en_agglomeration": random.choice([True, False]),
            "collision_frontale": random.choice([True, False]),
            "sexe_masculin": random.choice([True, False]),
            "luminosite_pleine_nuit": random.choice([True, False]),
            "meteo_normale": random.choice([True, False])
        }
        
        with self.client.post("/predict", json=data, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Prediction failed: {response.status_code}")
    
    @task(1)
    def health_check(self):
        """Health check task - 30% of traffic"""
        with self.client.get("/health", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Health check failed: {response.status_code}")
    
    @task(1)
    def metrics_test(self):
        """Metrics test endpoint - 30% of traffic"""
        with self.client.get("/metrics-test", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Metrics test failed: {response.status_code}")

class ReadOnlyUser(HttpUser):
    wait_time = between(2, 4)
    
    @task(1)
    def health_check(self):
        """Read-only user only does health checks"""
        with self.client.get("/health", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Health check failed: {response.status_code}")

class StressTestUser(HttpUser):
    wait_time = between(0.1, 0.5)  # High frequency
    
    @task(10)
    def rapid_predictions(self):
        """High-frequency prediction requests"""
        data = {
            "age_usager": 35.0,
            "vitesse_max_autorisee": 50.0,
            "nombre_de_voies": 2,
            "ceinture_ou_casque_attache": True,
            "en_agglomeration": True,
            "collision_frontale": False,
            "sexe_masculin": True,
            "luminosite_pleine_nuit": False,
            "meteo_normale": True
        }
        
        with self.client.post("/predict", json=data, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Rapid prediction failed: {response.status_code}")
