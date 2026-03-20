#!/usr/bin/env python3
#! -*- coding : utf-8 -*-

import pytest
import pandas as pd
from src.preprocessing import FeatureEngineer, SalaryRatioEncoder, preprocessing_pipeline

@pytest.fixture
def sample_data():
    """Données d'exemple pour les tests."""
    return pd.DataFrame([{
        "age": 41,
        "genre": "F",
        "revenu_mensuel": 5993,
        "statut_marital": "Célibataire",
        "departement": "Commercial",
        "nombre_experiences_precedentes": 8,
        "annee_experience_totale": 8,
        "annees_dans_l_entreprise": 6,
        "satisfaction_employee_environnement": 2,
        "note_evaluation_precedente": 3,
        "satisfaction_employee_nature_travail": 4,
        "satisfaction_employee_equipe": 1,
        "satisfaction_employee_equilibre_pro_perso": 1,
        "heure_supplementaires": "Oui",
        "a_quitte_l_entreprise": "Oui",
        "nombre_participation_pee": 0,
        "distance_domicile_travail": 1,
        "annees_depuis_la_derniere_promotion": 0,
        "annes_sous_responsable_actuel": 5
    }])

def test_feature_engineer_creates_features(sample_data):
    """Vérifie que FeatureEngineer crée les nouvelles features."""
    engineer = FeatureEngineer()
    transformed = engineer.transform(sample_data)
    assert 'satisfaction_moyenne' in transformed.columns
    assert 'family_conflict' in transformed.columns

