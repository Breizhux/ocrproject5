#!/usr/bin/env python3
#! -*- coding : utf-8 -*-

import time
import pytest
from fastapi.testclient import TestClient
from src.api import app, model

client = TestClient(app)

def test_health_endpoint():
    """Teste la disponibilité de l'API et le chargement du modèle."""
    # Attendre que le thread de chargement du modèle démarre
    time.sleep(2)

    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "model_status" in data

def test_predict_endpoint():
    """Teste la prédiction avec des données valides."""
    # Attendre que le modèle soit chargé
    time.sleep(2)
    if model.model is None:
        pytest.skip("Modèle non chargé, test ignoré")

    payload = {
        "id_employee": 1,
        "age": 41,
        "genre": "F",
        "revenu_mensuel": 5993,
        "statut_marital": "Célibataire",
        "departement": "Commercial",
        "poste": "Cadre Commercial",
        "nombre_experiences_precedentes": 8,
        "nombre_heures_travailless": 80,
        "annee_experience_totale": 8,
        "annees_dans_l_entreprise": 6,
        "annees_dans_le_poste_actuel": 4,
        "satisfaction_employee_environnement": 2,
        "note_evaluation_precedente": 3,
        "niveau_hierarchique_poste": 2,
        "satisfaction_employee_nature_travail": 4,
        "satisfaction_employee_equipe": 1,
        "satisfaction_employee_equilibre_pro_perso": 1,
        "note_evaluation_actuelle": 3,
        "heure_supplementaires": "Oui",
        "augementation_salaire_precedente": 11.0,
        "a_quitte_l_entreprise": "Oui",
        "nombre_participation_pee": 0,
        "nb_formations_suivies": 0,
        "nombre_employee_sous_responsabilite": 1,
        "distance_domicile_travail": 1,
        "niveau_education": 2,
        "domaine_etude": "Infra & Cloud",
        "ayant_enfants": "Y",
        "frequence_deplacement": "Occasionnel",
        "annees_depuis_la_derniere_promotion": 0,
        "annes_sous_responsable_actuel": 5
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert "probabilite_depart" in data
    assert "message" in data
