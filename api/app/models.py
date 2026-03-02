from pydantic import BaseModel


class AccidentData(BaseModel):
    # Noms complets pour l'utilisateur (Exposés dans l'API)
    age_usager: float
    vitesse_max_autorisee: float
    nombre_de_voies: int
    ceinture_ou_casque_attache: bool
    en_agglomeration: bool
    collision_frontale: bool
    sexe_masculin: bool = True
    luminosite_pleine_nuit: bool = False
    meteo_normale: bool = True


class PredictionOutput(BaseModel):
    gravite_code: int
    label_francais: str
    probabilites: dict[str, float]
