#!/usr/bin/env python3
#! -*- coding : utf-8 -*-

from pydantic import BaseModel, Field
from typing import Optional, Literal

class EmployeeInput(BaseModel):
    """Schéma de validation des données d'entrée (Données brutes attendues par le pipeline)."""
    # Identifiant (optionnel, pour traçabilité BDD)
    id_employee: Optional[int] = None
    # Données démographiques
    age: int = Field(..., ge=18, le=100, description="Âge de l'employé")
    genre: Literal["M", "F"] = Field(..., description="Genre de l'employé")
    statut_marital: Literal["Célibataire", "Marié(e)", "Divorcé(e)"] = Field(..., description="Statut marital")
    # Données professionnelles
    revenu_mensuel: float = Field(..., gt=0, le=50000, description="Revenu mensuel en euros")
    departement: Literal['Commercial', 'Consulting', 'Ressources Humaines'] = Field(..., description="Département")
    heure_supplementaires: Literal["Oui", "Non"] = Field(..., description="Heures supplémentaires")
    # Expérience
    nombre_experiences_precedentes: int = Field(..., ge=0, le=50, description="Nombre d'expériences précédentes")
    annee_experience_totale: float = Field(..., ge=0, le=100, description="Années d'expérience totale")
    annees_dans_l_entreprise: float = Field(..., ge=0, le=50, description="Années dans l'entreprise")
    annees_depuis_la_derniere_promotion: float = Field(..., ge=0, le=40, description="Années depuis dernière promotion")
    annes_sous_responsable_actuel: float = Field(..., ge=0, le=40, description="Années sous responsable actuel")
    # Conditions de travail
    distance_domicile_travail: float = Field(..., ge=0, le=500, description="Distance domicile-travail en km")
    nombre_participation_pee: int = Field(..., ge=0, le=10, description="Nombre de participations PEE")
    # Satisfaction (échelles 1-5)
    satisfaction_employee_environnement: float = Field(..., ge=1, le=5, description="Satisfaction environnement (1-5)")
    satisfaction_employee_nature_travail: float = Field(..., ge=1, le=5, description="Satisfaction nature du travail (1-5)")
    satisfaction_employee_equipe: float = Field(..., ge=1, le=5, description="Satisfaction équipe (1-5)")
    satisfaction_employee_equilibre_pro_perso: float = Field(..., ge=1, le=5, description="Satisfaction équilibre pro/perso (1-5)")
    # Performance
    note_evaluation_precedente: float = Field(..., ge=1, le=5, description="Note évaluation précédente (1-5)")

class PredictionOutput(BaseModel):
    """Schéma de sortie de la prédiction."""
    prediction: int
    probabilite_depart: float
    message: str
