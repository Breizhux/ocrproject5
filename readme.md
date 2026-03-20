# Projet 5 - Industrialisation Modèle ML (Turnover Employé)

## Description

Pipeline de Machine Learning pour prédire le départ des employés (`a_quitte_l_entreprise`).

Le projet inclut :
1. prétraitement des données
2. entraînement du modèle
3. une API de prédiction
4. une base de données PostgreSQL
5. un pipeline CI/CD.

## Installation

### Prérequis
- Python
- Git
- PostgreSQL

### Procédure

1. Cloner le dépôt :
   ```bash
   git clone https://github.com/breizhux/ocrproject5.git
   cd ocrproject5
   ```

2. Créer un environnement virtuel :
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Installer les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

4. Créer la base de données postgres (debian):
    ```bash
    apt install postgresql-contrib
    su postgres
    psql
    #change user et password
    CREATE USER postgres WITH PASSWORD 'postgres';
    CREATE DATABASE turnover_db OWNER postgres;
    \q
    ```

## Utilisation

### API

Lancer le serveur API :
```bash
uvicorn src.api:app --reload
```
*Le téléchargement, nettoyage, entraînement et ~~insertion des données dans la base de données~~ est automatique.*

#### Appel de l'API

Interface fastapi : [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

```bash
#avec curl:
curl -X POST "http://127.0.0.1:8000/predict" -H "Content-Type: application/json" -d '{
        "id_employee": 1,
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
    }'
```

### Entraînement du modèle
Pour lancer uniquement le pipeline d'entraînement et sauvegarder le modèle :
```bash
python src/model.py
```
Le modèle est sauvegardé dans `models/model.pkl`.

### Tests
Pour lancer la suite de tests unitaires et fonctionnels :
```bash
pytest tests/ --cov=src
```


## Structure du Projet

```text
ocrproject5/
├── src/
│   ├── __init__.py
│   ├── api.py           # Serveur d'api
│   ├── create_db.py     # Création de la base de donnée
│   ├── data.py          # Chargement et fusion des données
│   ├── preprocessing.py # Pipelines de transformation
│   ├── model.py         # Entraînement et sauvegarde du modèle
│   └── schemas.py       # Schéma des données entrantes (pydantic)
├── tests/               # Tests unitaires et fonctionnels
├── data/                # Données brutes (ignoré par .gitignore)
├── models/              # Modèles sérialisés (.pkl, ignoré par .gitignore)
├── .github/workflows/   # Pipeline CI/CD
├── .gitignore
├── requirements.txt
└── README.md
```

# Fonctionnement de l'API

L'API propose deux endpoints :

- `/predict` : prend en entrée un dictionnaire avec les données à prédire (cf Utilisation de l'API).
- `/health` : retourne le statut de l'API (si disponible, si le modèle est chargé, etc).
