#!/usr/bin/env python3
#! -*- coding : utf-8 -*-

import pytest
from pydantic import ValidationError
from src.schemas import EmployeeInput

def test_valid_employee_input():
    """Teste des données d'entrée valides."""
    data = {
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
    }
    employee = EmployeeInput(**data)
    assert employee.age == 41

def test_invalid_age_too_young():
    """Teste qu'un âge < 18 lève une erreur."""
    data = {
        "age": 17,
        "revenu_mensuel": 3500.0,
        "departement": "Commercial",
        "genre": "M",
        "statut_marital": "Célibataire",
        "heure_supplementaires": "Non",
        "nombre_experiences_precedentes": 0,
        "annee_experience_totale": 1.0,
        "annees_dans_l_entreprise": 1.0,
        "annees_depuis_la_derniere_promotion": 0.0,
        "annes_sous_responsable_actuel": 0.0,
        "distance_domicile_travail": 10.0,
        "nombre_participation_pee": 0,
        "satisfaction_employee_environnement": 3.0,
        "satisfaction_employee_nature_travail": 3.0,
        "satisfaction_employee_equipe": 3.0,
        "satisfaction_employee_equilibre_pro_perso": 3.0,
        "note_evaluation_precedente": 3.0
    }
    with pytest.raises(ValidationError):
        EmployeeInput(**data)

def test_invalid_satisfaction_out_of_range():
    """Teste qu'une satisfaction > 5 lève une erreur."""
    data = {
        "age": 35,
        "revenu_mensuel": 3500.0,
        "departement": "Commercial",
        "genre": "M",
        "statut_marital": "Célibataire",
        "heure_supplementaires": "Non",
        "nombre_experiences_precedentes": 0,
        "annee_experience_totale": 1.0,
        "annees_dans_l_entreprise": 1.0,
        "annees_depuis_la_derniere_promotion": 0.0,
        "annes_sous_responsable_actuel": 0.0,
        "distance_domicile_travail": 10.0,
        "nombre_participation_pee": 0,
        "satisfaction_employee_environnement": 6.0,
        "satisfaction_employee_nature_travail": 3.0,
        "satisfaction_employee_equipe": 3.0,
        "satisfaction_employee_equilibre_pro_perso": 3.0,
        "note_evaluation_precedente": 3.0
    }
    with pytest.raises(ValidationError):
        EmployeeInput(**data)

def test_multiple_errors_accumulated():
    """Vérifie que plusieurs erreurs sont retournées en une fois."""
    data = {
        "age": 17,
        "revenu_mensuel": 3500.0,
        "departement": "Commercial",
        "genre": "Homme",
        "statut_marital": "Célibataire",
        "heure_supplementaires": 5,
        "nombre_experiences_precedentes": 0,
        "annee_experience_totale": 1.0,
        "annees_dans_l_entreprise": 1.0,
        "annees_depuis_la_derniere_promotion": 0.0,
        "annes_sous_responsable_actuel": 0.0,
        "distance_domicile_travail": 10.0,
        "nombre_participation_pee": 0,
        "satisfaction_employee_environnement": 6.0,
        "satisfaction_employee_nature_travail": 0.0,
        "satisfaction_employee_equipe": 3.0,
        "satisfaction_employee_equilibre_pro_perso": 3.0,
        "note_evaluation_precedente": 3.0
    }
    with pytest.raises(ValidationError) as exc_info:
        EmployeeInput(**data)
    # Vérifie qu'il y a au moins 2 erreurs (âge + satisfaction)
    assert len(exc_info.value.errors()) >= 2
