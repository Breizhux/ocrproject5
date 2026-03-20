#!/usr/bin/env python3
#! -*- coding : utf-8 -*-

import pytest
import joblib
import os
from src.model import train_and_save_model

def test_model_file_created():
    """Vérifie que le modèle est sauvegardé."""
    model_path = "models/model.pkl"
    # Supprimer l'ancien modèle si existe
    if os.path.exists(model_path):
        os.remove(model_path)

    train_and_save_model()
    assert os.path.exists(model_path)

def test_model_loadable():
    """Vérifie que le modèle peut être chargé."""
    model_path = "models/model.pkl"
    if not os.path.exists(model_path):
        train_and_save_model()

    model = joblib.load(model_path)
    assert model is not None
