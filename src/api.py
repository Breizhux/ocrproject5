#!/usr/bin/env python3
#! -*- coding : utf-8 -*-

import os
import joblib
import pandas as pd
from threading import Thread
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException

from . import create_db
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
            except:
                self.model_status = "erreur"
        else:
            from . import model
            self.model_status = "training..."
            self.model = model.train_and_save_model()
            self.model_status = "loaded"


def save_prediction(employee_data, prediction, probabilite, human_validate=False, commentaire="Prédiction automatique de l'API"):
    session = create_db.SessionLocal()

    # 1. Vérifier si l'employé existe déjà
    employee = None
    if employee_data.get('id_employee') is not None:
        employee = session.query(create_db.EmployeeData).filter(
            create_db.EmployeeData.id_employee == employee_data['id_employee']
        ).first()

    # 2. Si n'existe pas, créer un nouvel employé
    if employee is None:
        employee = create_db.EmployeeData(
            id_employee=employee_data.get('id_employee'),
            age=employee_data.get('age'),
            genre=employee_data.get('genre'),
            statut_marital=employee_data.get('statut_marital'),
            revenu_mensuel=employee_data.get('revenu_mensuel'),
            departement=employee_data.get('departement'),
            nombre_experiences_precedentes=employee_data.get('nombre_experiences_precedentes'),
            annee_experience_totale=employee_data.get('annee_experience_totale'),
            annees_dans_l_entreprise=employee_data.get('annees_dans_l_entreprise'),
            annees_depuis_la_derniere_promotion=employee_data.get('annees_depuis_la_derniere_promotion'),
            annes_sous_responsable_actuel=employee_data.get('annes_sous_responsable_actuel'),
            satisfaction_employee_environnement=employee_data.get('satisfaction_employee_environnement'),
            satisfaction_employee_nature_travail=employee_data.get('satisfaction_employee_nature_travail'),
            satisfaction_employee_equipe=employee_data.get('satisfaction_employee_equipe'),
            satisfaction_employee_equilibre_pro_perso=employee_data.get('satisfaction_employee_equilibre_pro_perso'),
            note_evaluation_precedente=employee_data.get('note_evaluation_precedente'),
            heure_supplementaires=employee_data.get('heure_supplementaires'),
            distance_domicile_travail=employee_data.get('distance_domicile_travail'),
            nombre_participation_pee=employee_data.get('nombre_participation_pee')
        )
        session.add(employee)
        session.commit()
        session.refresh(employee)

    # 3. Créer la prédiction liée à l'employé
    new_prediction = create_db.Prediction(
        employee_id=employee.id,
        prediction=prediction,
        probabilite_depart=probabilite,
        human_validate=human_validate,
        commentaire=commentaire
    )
    session.add(new_prediction)
    session.commit()
    print("1 entrée insérée dans la base de données.")

    return {
        "employee_id": employee.id,
        "prediction_id": new_prediction.id
    }

    session.close()




# create database
#create_db.clear_database()
#create_db.create_tables()
#create_db.load_dataset()

# create api (and model if needed)
app = FastAPI(title="API Prédiction Turnover")
model = TurnoverModel()
model.start()

@app.get("/health")
def health_check():
    """Vérifie que l'API est opérationnelle."""
    return {"status": "ok", "model_status": model.model_status}

@app.post("/predict", response_model=PredictionOutput)
def predict_turnover(data: EmployeeInput):
    """Prédit le risque de départ d'un employé."""
    try:
        input_df = pd.DataFrame([data.model_dump()])

        # Prédiction
        prediction = int(model.model.predict(input_df)[0])
        proba = float(model.model.predict_proba(input_df)[0][1])

        # Enregistrement de la donnée dans la BDD
        db_result = save_prediction(
            employee_data=data.model_dump(),
            prediction=prediction,
            probabilite=proba,
        )

        return {
            "prediction": prediction,
            "probabilite_depart": proba,
            "message": f"Risque de départ {'élevé' if prediction else 'faible'}"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de prédiction: {str(e)}")

