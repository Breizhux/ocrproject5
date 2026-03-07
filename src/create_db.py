#!/usr/bin/env python3
#! -*- coding : utf-8 -*-

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, Float, String, Boolean, ForeignKey, DateTime, exc
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime
import pandas as pd

# Chargement des variables d'environnement
load_dotenv()

# Configuration de la connexion PostgreSQL
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "turnover_db")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
Base = declarative_base()



class EmployeeData(Base):
    """Table des données employées (inputs du modèle)."""
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_employee = Column(Integer, unique=True, index=True)

    # Données démographiques
    age = Column(Integer)
    genre = Column(String(10))
    statut_marital = Column(String(50))
#    ayant_enfants = Column(String(10))

    # Données professionnelles
    revenu_mensuel = Column(Float)
    departement = Column(String(100))
#    poste = Column(String(100))
#    niveau_hierarchique_poste = Column(Integer)
#    domaine_etude = Column(String(100))
#    niveau_education = Column(Integer)

    # Expérience
    nombre_experiences_precedentes = Column(Integer)
    annee_experience_totale = Column(Float)
    annees_dans_l_entreprise = Column(Float)
#    annees_dans_le_poste_actuel = Column(Float)
    annees_depuis_la_derniere_promotion = Column(Float)
    annes_sous_responsable_actuel = Column(Float)

    # Satisfaction & Performance
    satisfaction_employee_environnement = Column(Float)
    satisfaction_employee_nature_travail = Column(Float)
    satisfaction_employee_equipe = Column(Float)
    satisfaction_employee_equilibre_pro_perso = Column(Float)
    note_evaluation_precedente = Column(Float)
#    note_evaluation_actuelle = Column(Float)

    # Conditions de travail
    heure_supplementaires = Column(String(10))
#    nombre_heures_travailless = Column(Integer)
    distance_domicile_travail = Column(Float)
#    frequence_deplacement = Column(String(50))
#    nombre_employee_sous_responsabilite = Column(Integer)

    # Avantages & Formation
#    augementation_salaire_precedente = Column(Float)
    nombre_participation_pee = Column(Integer)
#    nb_formations_suivies = Column(Integer)

    # Cible (pour validation ultérieure)
    a_quitte_l_entreprise = Column(String(10))

    # Relation avec les prédictions
    predictions = relationship("Prediction", back_populates="employee", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Employee(id_employee={self.id_employee}, poste={self.poste})>"


class Prediction(Base):
    """Table des prédictions du modèle (outputs)."""
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)

    # Résultat de la prédiction
    prediction = Column(Integer)  # 0 = Reste, 1 = Part
    probabilite_depart = Column(Float)

    # Fiabilité de la prédiction
    human_validate = Column(Boolean, default=False)  # True = validé a posteriori, False = prédiction modèle
    commentaire = Column(String(255))

    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relation avec l'employé
    employee = relationship("EmployeeData", back_populates="predictions")

    def __repr__(self):
        return f"<Prediction(employee_id={self.employee_id}, prediction={self.prediction})>"



def clear_database():
    """Supprime toutes les données de la base de données."""
    session = SessionLocal()
    session.query(Prediction).delete()
    session.query(EmployeeData).delete()
    session.commit()
    session.close()
    print("Base de données vidée.")

def create_tables():
    """Crée les tables dans la base de données."""
    Base.metadata.create_all(bind=engine)


def load_dataset(csv_path=None):
    """Charge le dataset dans la table employees."""
    # Si aucun chemin fourni, charger depuis les URLs OpenClassrooms
    if csv_path is None:
        from .data import load_data
        df = load_data()
    else:
        df = pd.read_csv(csv_path)

    session = SessionLocal()

    count = 0
    for _, row in df.iterrows():
        employee = EmployeeData(
            id_employee=int(row['id_employee']),
            age=int(row['age']),
            genre=row['genre'],
            statut_marital=row['statut_marital'],
            nombre_experiences_precedentes=int(row['nombre_experiences_precedentes']),
            annee_experience_totale=float(row['annee_experience_totale']),
            satisfaction_employee_environnement=float(row['satisfaction_employee_environnement']),
            satisfaction_employee_nature_travail=float(row['satisfaction_employee_nature_travail']),
            satisfaction_employee_equipe=float(row['satisfaction_employee_equipe']),
            satisfaction_employee_equilibre_pro_perso=float(row['satisfaction_employee_equilibre_pro_perso']),
            note_evaluation_precedente=float(row['note_evaluation_precedente']),
            nombre_participation_pee=int(row['nombre_participation_pee']),
            annees_depuis_la_derniere_promotion=float(row['annees_depuis_la_derniere_promotion']),
            departement=row['departement'],
            heure_supplementaires=row['heure_supplementaires'],
            annees_dans_l_entreprise=float(row['annees_dans_l_entreprise']),
            annes_sous_responsable_actuel=float(row['annes_sous_responsable_actuel']),
            revenu_mensuel=float(row['revenu_mensuel']),
            distance_domicile_travail=float(row['distance_domicile_travail']),
#            ayant_enfants=row['ayant_enfants'],
#            poste=row['poste'],
#            niveau_hierarchique_poste=int(row['niveau_hierarchique_poste']),
#            domaine_etude=row['domaine_etude'],
#            niveau_education=int(row['niveau_education']),
#            annees_dans_le_poste_actuel=float(row['annees_dans_le_poste_actuel']),
#            note_evaluation_actuelle=float(row['note_evaluation_actuelle']),
#            nombre_heures_travailless=int(row['nombre_heures_travailless']),
#            frequence_deplacement=row['frequence_deplacement'],
#            nombre_employee_sous_responsabilite=int(row['nombre_employee_sous_responsabilite']),
#            augementation_salaire_precedente=float(row['augementation_salaire_precedente']),
#            nb_formations_suivies=int(row['nb_formations_suivies']),
#            a_quitte_l_entreprise=row['a_quitte_l_entreprise']
        )
        session.add(employee)
        count += 1

    session.commit()
    print(f"{count} employés insérés dans la base de données.")

    session.close()


def verify_data():
    session = SessionLocal()
    employee_count = session.query(EmployeeData).count()
    prediction_count = session.query(Prediction).count()
    print(f"→ Employés : {employee_count}")
    print(f"→ Prédictions : {prediction_count}")
    session.close()


# Création du moteur et de la session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


if __name__ == "__main__":
    # 1. Clean la base de données
    if True:
        clear_database()

    # 2. Créer les tables
    create_tables()

    # 3. Charger le dataset (optionnel)
    load_dataset()

    # 4. Vérifier les données
    verify_data()
