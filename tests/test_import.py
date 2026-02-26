#!/usr/bin/env python3
#! -*- coding : utf-8 -*-

def test_import_src():
    """Vérifie que les modules s'importent sans erreur."""
    try:
        from src import data, preprocessing, model
        assert True
    except ImportError:
        assert False, "Importation des modules échouée"
