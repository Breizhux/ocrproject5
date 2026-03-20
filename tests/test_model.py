#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
import joblib
import os
import sys

# Ajouter la racine du projet au path pour les imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.model import train_and_save_model

@pytest.fixture(scope="module")
def model_path():
    """Retourne le chemin absolu du modèle."""
    return os.path.join(os.path.dirname(__file__), '..', 'models', 'model.pkl')

@pytest.fixture(scope="module")
def ensure_model(model_path):
    """Génère le modèle avant les tests s'il n'existe pas."""
    # Créer le dossier models s'il n'existe pas
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    # Entraîner le modèle s'il n'existe pas
    if not os.path.exists(model_path):
        train_and_save_model()
    return model_path

def test_model_file_created(ensure_model):
    """Vérifie que le modèle est sauvegardé."""
    assert os.path.exists(ensure_model), "Le fichier model.pkl n'existe pas"

def test_model_loadable(ensure_model):
    """Vérifie que le modèle peut être chargé."""
    model = joblib.load(ensure_model)
    assert model is not None, "Le modèle chargé est None"

def test_model_has_predict_method(ensure_model):
    """Vérifie que le modèle a une méthode predict."""
    model = joblib.load(ensure_model)
    assert hasattr(model, 'predict'), "Le modèle n'a pas de méthode predict"

def test_model_has_predict_proba_method(ensure_model):
    """Vérifie que le modèle a une méthode predict_proba."""
    model = joblib.load(ensure_model)
    assert hasattr(model, 'predict_proba'), "Le modèle n'a pas de méthode predict_proba"
