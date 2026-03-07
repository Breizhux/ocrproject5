#!/usr/bin/env python3
#! -*- coding : utf-8 -*-

import joblib
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import SelectFromModel
from sklearn.metrics import classification_report
from sklearn.pipeline import Pipeline

from .data import load_data
from .preprocessing import preprocessing_pipeline

def train_and_save_model():
    print("Chargement et préparation des données...")
    df = load_data()

    X = df.drop(columns=['a_quitte_l_entreprise'])
    y = df['a_quitte_l_entreprise'].map({'Non': 0, 'Oui': 1})

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print("Entraînement du modèle...")

    # Paramètres optimisés (penalty retiré car défaut='l2' et déprécié)
    best_lr_params = {
        'C': 0.1,
        'class_weight': 'balanced',
        'max_iter': 100,
        'penalty': 'l2',
        'solver': 'saga',
        'random_state': 42
    }

    sfm_pipeline = Pipeline([
        ('preprocessing', preprocessing_pipeline),
        ('feature_selection', SelectFromModel(
            LogisticRegression(**best_lr_params),
            threshold='0.85*mean'
        )),
        ('classifier', LogisticRegression(max_iter=1000, random_state=42, class_weight='balanced'))
    ])

    sfm_pipeline.fit(X_train, y_train)

    print("Entraînement terminé. Évaluation sur le jeu de test...")
    y_pred = sfm_pipeline.predict(X_test)
    print(classification_report(y_test, y_pred, target_names=['Reste', 'Part']))

    print("Sauvegarde du modèle dans models/model.pkl...", end="\r")
    joblib.dump(sfm_pipeline, 'models/model.pkl')
    print("Sauvegarde du modèle dans models/model.pkl : fait.")

    return sfm_pipeline


if __name__ == "__main__":
    train_and_save_model()
