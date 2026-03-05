#!/usr/bin/env python3
#! -*- coding : utf-8 -*-

import os
import joblib
import pandas as pd
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from src.schemas import EmployeeInput, PredictionOutput

app = FastAPI(title="API Prédiction Turnover")
model_status = "stop"

@app.get("/health")
def health_check():
    """Vérifie que l'API est opérationnelle."""
    return {"status": "healthy", "model_status": model_status}

@app.post("/predict", response_model=PredictionOutput)
def predict_turnover(data: EmployeeInput):
    """Prédit le risque de départ d'un employé."""
    try:
        # Conversion Pydantic -> DataFrame
        input_df = pd.DataFrame([data.dict()])

        # Prédiction
        prediction = model.predict(input_df)[0]
        proba = model.predict_proba(input_df)[0][1]

        # Interprétation
        message = "Risque de départ élevé" if prediction == 1 else "Risque de départ faible"

        return {
            "prediction": int(prediction),
            "probabilite_depart": float(proba),
            "message": message
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de prédiction: {str(e)}")


# Chargement du modèle au démarrage
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "model.pkl")

if os.path.exists(MODEL_PATH):
    try:
        model = joblib.load(MODEL_PATH)
        model_status = "loaded"
    except FileNotFoundError:
        model_status = "error"
        raise RuntimeError(f"Modèle non trouvé à {MODEL_PATH}. Lancez d'abord src/model.py")

else:
    from . import model
    model = model.train_and_save_model()
