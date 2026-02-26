#!/usr/bin/env python3
#! -*- coding : utf-8 -*-

import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder, FunctionTransformer


class FeatureEngineer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()
        X['satisfaction_moyenne'] = self._compute_satisfaction_moyenne(X)
        X['time_in_current_role_ratio'] = self._time_in_current_role_ratio(X)
        X['family_conflict'] = self._create_family_conflict(X)
        X['training_rate_per_year'] = self._training_rate_per_year(X)
        X['recent_change_flag'] = self._create_recent_change_flag(X)
        X['relative_promo_delay'] = self._relative_promo_delay(X)
        return X

    def _compute_satisfaction_moyenne(self, X):
        cols = ['satisfaction_employee_environnement', 'satisfaction_employee_nature_travail',
                'satisfaction_employee_equipe', 'satisfaction_employee_equilibre_pro_perso']
        return X[cols].mean(axis=1)

    def _time_in_current_role_ratio(self, X):
        return X['annes_sous_responsable_actuel'] / X['annees_dans_l_entreprise'].clip(lower=1)

    def _training_rate_per_year(self, X):
        return X['nb_formations_suivies'] / X['annees_dans_l_entreprise'].clip(lower=1)

    def _relative_promo_delay(self, X):
        return X['annees_depuis_la_derniere_promotion'] / X['annees_dans_l_entreprise'].clip(lower=1)

    def _create_family_conflict(self, X):
        weights = (3, 2, 2, 2)
        salary_median = X['revenu_mensuel'].median()
        salary_score = (salary_median - X['revenu_mensuel']) / salary_median
        salary_score = salary_score.clip(lower=0) * weights[0]
        heures_sup_score = X['heure_supplementaires'].map({"Non": 0, "Oui": weights[1]})
        distance_max = X['distance_domicile_travail'].quantile(0.95)
        distance_score = (X['distance_domicile_travail'] / distance_max).clip(0, 1) * weights[2]
        marital_score = X['statut_marital'].map({'Célibataire': 0, 'Marié(e)': 0.5, 'Divorcé(e)': 1})
        conflict_score = salary_score + heures_sup_score + distance_score + marital_score
        return conflict_score.clip(0, 10)

    def _create_recent_change_flag(self, X):
        eval_change = X['note_evaluation_actuelle'] - X['note_evaluation_precedente']
        promotion_recente = (X['annees_depuis_la_derniere_promotion'] <= 1).astype(int)
        eval_degradee = (eval_change < 0).astype(int)
        return promotion_recente * eval_degradee

class SalaryRatioEncoder(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.poste_median = None
        self.department_median = None

    def fit(self, X, y=None):
        self.poste_median = X.groupby('poste')['revenu_mensuel'].median().to_dict()
        self.department_median = X.groupby('departement')['revenu_mensuel'].median().to_dict()
        return self

    def transform(self, X):
        X = X.copy()
        X['salary_to_poste_median'] = X['revenu_mensuel'] / X['poste'].map(self.poste_median)
        X['salary_to_dept_median'] = X['revenu_mensuel'] / X['departement'].map(self.department_median)
        return X

# --- Fonctions de Transformation ---
def label_encode_transform(X):
    X_encoded = X.copy()
    for col in X_encoded.columns:
        le = LabelEncoder()
        X_encoded[col] = le.fit_transform(X_encoded[col].astype(str))
    return X_encoded

def map_frequency(X):
    X_mapped = X.copy()
    X_mapped['frequence_deplacement'] = X_mapped['frequence_deplacement'].map({
        'Aucun': 0, 'Occasionnel': 1, 'Frequent': 2
    })
    return X_mapped

# --- Configuration des Colonnes ---
COLUMNS_TO_DROP = [
    'id_employee', 'ayant_enfants', 'nombre_heures_travailless',
    'nombre_employee_sous_responsabilite', 'salary_to_dept_median',
    'annees_dans_l_entreprise', 'niveau_hierarchique_poste'
]

NUMERIC_FEATURES = [
    'age', 'revenu_mensuel', 'nombre_experiences_precedentes',
    'annee_experience_totale', 'annees_dans_le_poste_actuel',
    'satisfaction_employee_environnement', 'note_evaluation_precedente',
    'satisfaction_employee_nature_travail', 'satisfaction_employee_equipe',
    'satisfaction_employee_equilibre_pro_perso', 'note_evaluation_actuelle',
    'augementation_salaire_precedente', 'nombre_participation_pee',
    'nb_formations_suivies', 'distance_domicile_travail',
    'niveau_education', 'annees_depuis_la_derniere_promotion',
    'annes_sous_responsable_actuel'
]

NUMERIC_BY_FEATURES_ENGINEERING = [
    'satisfaction_moyenne', 'time_in_current_role_ratio', 'family_conflict',
    'training_rate_per_year', 'recent_change_flag', 'relative_promo_delay'
]

CATEGORICAL_ONEHOT = ['genre', 'statut_marital', 'departement', 'heure_supplementaires']
CATEGORICAL_LABEL = ['poste', 'domaine_etude']

# --- Pipelines ---
numeric_pipeline = Pipeline([('scaler', StandardScaler())])
categorical_onehot_pipeline = Pipeline([('onehot', OneHotEncoder(drop='first', sparse_output=False))])
categorical_label_pipeline = Pipeline([('label_encoder', FunctionTransformer(label_encode_transform))])
categorical_map_pipeline = Pipeline([('mapper', FunctionTransformer(map_frequency))])

preprocessing_pipeline = Pipeline([
    ('feature_engineer', FeatureEngineer()),
    ('salary_ratio', SalaryRatioEncoder()),
    ('drop_columns', FunctionTransformer(
        lambda X: X.drop(columns=[c for c in COLUMNS_TO_DROP if c in X.columns], errors='ignore')
    )),
    ('map_frequency', categorical_map_pipeline),
    ('column_transformer', ColumnTransformer([
        ('num', numeric_pipeline, NUMERIC_FEATURES + NUMERIC_BY_FEATURES_ENGINEERING),
        ('cat_onehot', categorical_onehot_pipeline, CATEGORICAL_ONEHOT),
        ('cat_label', categorical_label_pipeline, CATEGORICAL_LABEL)
    ], remainder='drop'))
])
