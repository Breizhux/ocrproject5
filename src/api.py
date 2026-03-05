#!/usr/bin/env python3
#! -*- coding : utf-8 -*-

import os
import joblib
import pandas as pd
from threading import Thread
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from src.schemas import EmployeeInput, PredictionOutput

class TurnoverModel(Thread):
    """ Turnover model with parallel loading."""
    def __init__(self):
        super().__init__()
        self.model = None
        self.model_status = "stop"
        self.model_path = os.path.join(os.path.dirname(__file__), "..", "models", "model.pkl")

    def run(self):
        if os.path.exists(self.model_path):
            try:
                self.model = joblib.load(self.model_path)
                self.model_status = "loaded"
            except FileNotFoundError:
                self.model_status = "error : modèle non trouvé."
        else:
            from . import model
            self.model_status = "training..."
            self.model = model.train_and_save_model()
            self.model_status = "loaded"


app = FastAPI(title="API Prédiction Turnover")
model = TurnoverModel()
model.start()

@app.get("/health")
def health_check():
    """Vérifie que l'API est opérationnelle."""
    return {"status": "healthy", "model_status": model.model_status}

@app.post("/predict", response_model=PredictionOutput)
def predict_turnover(data: EmployeeInput):
    """Prédit le risque de départ d'un employé."""
    try:
        input_df = pd.DataFrame([data.dict()])

        # Prédiction
        prediction = model.model.predict(input_df)[0]
        proba = model.model.predict_proba(input_df)[0][1]

        # Interprétation
        message = "Risque de départ élevé" if prediction == 1 else "Risque de départ faible"

        return {
            "prediction": int(prediction),
            "probabilite_depart": float(proba),
            "message": message
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de prédiction: {str(e)}")

