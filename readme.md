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

4. Créer la base de données postgres:
    ```
    psql -U postgres -h localhost -d turnover_db
    ```

## Utilisation

### API

Lancer le serveur API :
```bash
uvicorn src.api:app --reload
```
*Le téléchargement, nettoyage, entraînement et ~~insertion des données dans la base de données~~ est automatique.*

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
├── docs/                # Documentation technique
├── .github/workflows/   # Pipeline CI/CD
├── .gitignore
├── requirements.txt
└── README.md
```
