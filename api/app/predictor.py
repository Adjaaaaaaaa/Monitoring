import os

import joblib
import pandas as pd


class AccidentPredictor:
    def __init__(self):
        # Chemin vers le modèle multi-classe
        model_path = os.path.join(
            os.path.dirname(__file__), "..", "data_models", "model_multi_xgb.joblib"
        )
        self.pipeline = joblib.load(model_path)
        self.labels = {1: "Indemne", 2: "Tué", 3: "Grave", 4: "Léger"}

    def predict(self, user_data: dict):
        # 1. Calcul des variables internes attendues par le modèle
        internal_data = {
            "age": user_data["age_usager"],
            "vma": user_data["vitesse_max_autorisee"],
            "nbv": user_data["nombre_de_voies"],
            # Recalcul des features importantes identifiées lors du Feature Engineering
            "vitesse_x_collision": user_data["vitesse_max_autorisee"]
            if user_data["collision_frontale"]
            else 0,
            "age_x_securite": user_data["age_usager"]
            if user_data["ceinture_ou_casque_attache"]
            else 0,
            "agglo_x_vitesse": user_data["vitesse_max_autorisee"]
            if user_data["en_agglomeration"]
            else 0,
            # Mapping des Dummies
            "sexe_2": 0 if user_data["sexe_masculin"] else 1,
            "agg_2": 1 if user_data["en_agglomeration"] else 0,
            "lum_3": 1 if user_data["luminosite_pleine_nuit"] else 0,
        }

        # 2. Création du DataFrame et alignement des colonnes
        df = pd.DataFrame([internal_data])
        expected_columns = self.pipeline.feature_names_in_
        for col in expected_columns:
            if col not in df.columns:
                df[col] = 0
        df = df[expected_columns]

        # 3. Prédiction et conversion de l'index (0-3 -> 1-4)
        prediction_idx = self.pipeline.predict(df)[0]
        real_gravity = int(prediction_idx + 1)

        # 4. Calcul des probabilités par modalité
        probs = self.pipeline.predict_proba(df).tolist()[0]

        return {
            "gravite_code": real_gravity,
            "label_francais": self.labels.get(real_gravity, "Inconnu"),
            "probabilites": {
                self.labels[i + 1]: round(probs[i], 4) for i in range(len(probs))
            },
        }


predictor = AccidentPredictor()
