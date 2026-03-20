#!/usr/bin/env python3
#! -*- coding : utf-8 -*-

import pytest
import pandas as pd
from src.data import load_data

def test_load_data_returns_dataframe():
    """Vérifie que load_data retourne un DataFrame."""
    df = load_data()
    assert isinstance(df, pd.DataFrame)

def test_load_data_has_expected_columns():
    """Vérifie les colonnes essentielles présentes."""
    df = load_data()
    required_cols = ['id_employee', 'age', 'revenu_mensuel', 'departement', 'a_quitte_l_entreprise']
    for col in required_cols:
        assert col in df.columns, f"Colonne manquante : {col}"

def test_load_data_no_null_target():
    """Vérifie qu'il n'y a pas de valeurs nulles dans la cible."""
    df = load_data()
    assert df['a_quitte_l_entreprise'].isnull().sum() == 0

