#!/usr/bin/env python3
#! -*- coding : utf-8 -*-

from pydantic import BaseModel, Field
from typing import Optional

from pydantic import BaseModel, Field
from typing import Optional, List

class EmployeeInput(BaseModel):
    """Schéma de validation des données d'entrée (Données brutes attendues par le pipeline)."""
    id_employee: int = None
    age: int = Field(..., ge=18, le=100)
    revenu_mensuel: float = Field(..., gt=0)
#    poste: str
    departement: str
    genre: str
    statut_marital: str
    heure_supplementaires: str
#    domaine_etude: str
#    frequence_deplacement: str
#    niveau_education: int
    nombre_experiences_precedentes: int
    annee_experience_totale: float
#    annees_dans_le_poste_actuel: float
    annees_dans_l_entreprise: float
    annees_depuis_la_derniere_promotion: float
    annes_sous_responsable_actuel: float
    distance_domicile_travail: float
#    nb_formations_suivies: int
    nombre_participation_pee: int
    satisfaction_employee_environnement: float
    satisfaction_employee_nature_travail: float
    satisfaction_employee_equipe: float
    satisfaction_employee_equilibre_pro_perso: float
    note_evaluation_precedente: float
#    note_evaluation_actuelle: float
#    augementation_salaire_precedente: float

class PredictionOutput(BaseModel):
    """Schéma de sortie de la prédiction."""
    prediction: int
    probabilite_depart: float
    message: str
