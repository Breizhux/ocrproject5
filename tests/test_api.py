#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from src.api import app, model

client = TestClient(app)

@pytest.fixture(autouse=True)
def mock_database():
    """Mock automatique de toutes les opérations BDD pour les tests."""
    with patch('src.create_db.SessionLocal') as mock_session:
        mock_db_instance = MagicMock()
        mock_session.return_value = mock_db_instance
        mock_db_instance.query.return_value.filter.return_value.first.return_value = None
        mock_db_instance.add.return_value = None
        mock_db_instance.commit.return_value = None
        mock_db_instance.refresh.return_value = None
        mock_db_instance.close.return_value = None
        yield mock_db_instance

def test_health_endpoint():
    """Teste la disponibilité de l'API et le chargement du modèle."""
    # Attendre que le thread de chargement du modèle démarre
    time.sleep(2)

    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "model_status" in data

def test_predict_endpoint(mock_database):
    """Teste la prédiction avec des données valides."""
    # Attendre que le modèle soit chargé
    time.sleep(2)
    if model.model is None:
        pytest.skip("Modèle non chargé, test ignoré")

    payload = {
        "id_employee": 1,
        "age": 41,
        "genre": "F",
        "revenu_mensuel": 5993.0,
        "statut_marital": "Célibataire",
        "departement": "Commercial",
        "poste": "Cadre Commercial",
        "domaine_etude": "Infra & Cloud",
        "frequence_deplacement": "Occasionnel",
        "niveau_education": 2,
        "nombre_experiences_precedentes": 8,
        "annee_experience_totale": 8.0,
        "annees_dans_le_poste_actuel": 4.0,
        "annees_dans_l_entreprise": 6.0,
        "annees_depuis_la_derniere_promotion": 0.0,
        "annes_sous_responsable_actuel": 5.0,
        "distance_domicile_travail": 1.0,
        "nb_formations_suivies": 0,
        "nombre_participation_pee": 0,
        "satisfaction_employee_environnement": 2.0,
        "satisfaction_employee_nature_travail": 4.0,
        "satisfaction_employee_equipe": 1.0,
        "satisfaction_employee_equilibre_pro_perso": 1.0,
        "note_evaluation_precedente": 3.0,
        "note_evaluation_actuelle": 3.0,
        "augementation_salaire_precedente": 11.0,
        "heure_supplementaires": "Oui"
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert "probabilite_depart" in data
    assert "message" in data
